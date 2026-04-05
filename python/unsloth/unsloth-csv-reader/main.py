"""CSV/JSON Reader — parse structured data from text."""

import csv
import io
import json

from orbflow_sdk import Field, action, plugin, run


@plugin(
    name="unsloth-csv-reader",
    version="0.2.0",
    author="Unsloth",
    category="data-source",
    icon="file-text",
    description="Parse CSV, JSON, and JSONL data into structured rows.",
)
class CsvReaderPlugin:

    @action(
        ref="plugin:csv-reader",
        name="CSV/JSON Reader",
        description="Parse CSV, JSON array, or JSONL text into rows.",
        inputs=[
            Field.string("content", required=True).label("Content"),
        ],
        outputs=[
            Field.array("rows").label("Rows").description("Parsed array of row objects"),
            Field.array("columns").label("Columns").description("Column/field names"),
            Field.number("row_count").label("Row Count"),
        ],
        parameters=[
            Field.string("format").label("Format").default("auto"),
            Field.boolean("has_header").label("Has Header").default(True),
            Field.string("delimiter").label("Delimiter").default(","),
            Field.number("max_rows").label("Max Rows").default(10000),
        ],
    )
    async def read(self, ctx):
        content = ctx.input.get("content", "")
        fmt = ctx.parameters.get("format", "auto")
        has_header = ctx.parameters.get("has_header", True)
        delimiter = ctx.parameters.get("delimiter", ",")
        max_rows = min(max(int(ctx.parameters.get("max_rows", 10000)), 1), 100000)

        if fmt == "auto":
            fmt = self._detect_format(content)

        parsers = {
            "json": self._parse_json,
            "jsonl": self._parse_jsonl,
            "csv": lambda c: self._parse_csv(c, has_header, delimiter),
        }

        parser = parsers.get(fmt)
        if parser is None:
            from orbflow_sdk.types import ActionResult
            return ActionResult(error=f"Unknown format: {fmt}")

        rows = parser(content)
        rows = rows[:max_rows]
        columns = list(rows[0].keys()) if rows else []

        return {"rows": rows, "columns": columns, "row_count": len(rows)}

    @staticmethod
    def _detect_format(content: str) -> str:
        stripped = content.strip()
        if stripped.startswith("["):
            return "json"
        if stripped.startswith("{"):
            return "jsonl"
        return "csv"

    @staticmethod
    def _parse_json(content: str) -> list[dict]:
        data = json.loads(content)
        if isinstance(data, list):
            return [row if isinstance(row, dict) else {"value": row} for row in data]
        if isinstance(data, dict):
            return [data]
        return [{"value": data}]

    @staticmethod
    def _parse_jsonl(content: str) -> list[dict]:
        rows = []
        for line in content.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            rows.append(obj if isinstance(obj, dict) else {"value": obj})
        return rows

    @staticmethod
    def _parse_csv(content: str, has_header: bool, delimiter: str) -> list[dict]:
        reader = csv.reader(io.StringIO(content), delimiter=delimiter)
        rows_raw = list(reader)
        if not rows_raw:
            return []

        if has_header:
            headers = [h.strip() for h in rows_raw[0]]
            data_rows = rows_raw[1:]
        else:
            max_cols = max(len(r) for r in rows_raw)
            headers = [f"col_{i}" for i in range(max_cols)]
            data_rows = rows_raw

        result = []
        for row in data_rows:
            obj = {}
            for i, header in enumerate(headers):
                obj[header] = row[i].strip() if i < len(row) else ""
            result.append(obj)
        return result


if __name__ == "__main__":
    run(CsvReaderPlugin)
