"""HuggingFace Dataset — load rows from HuggingFace Hub datasets."""

from __future__ import annotations

import json
import urllib.request

from orbflow_sdk import Field, action, plugin, run


@plugin(
    name="unsloth-hf-dataset",
    version="0.2.0",
    author="Unsloth",
    category="data-source",
    icon="database",
    description="Load rows from HuggingFace Hub datasets via the API (no dependencies).",
)
class HfDatasetPlugin:

    @action(
        ref="plugin:hf-dataset",
        name="HuggingFace Dataset",
        description="Fetch rows from a HuggingFace dataset using the datasets API.",
        inputs=[
            Field.string("dataset", required=True).label("Dataset"),
        ],
        outputs=[
            Field.array("rows").label("Rows").description("Array of dataset rows"),
            Field.array("columns").label("Columns").description("Column names"),
            Field.number("total_rows").label("Total Rows"),
            Field.string("dataset_id").label("Dataset ID"),
        ],
        parameters=[
            Field.string("subset").label("Subset"),
            Field.string("split").label("Split").default("train"),
            Field.number("offset").label("Offset").default(0),
            Field.number("limit").label("Limit").default(100),
        ],
    )
    async def load(self, ctx):
        dataset_id = ctx.input.get("dataset", "")
        if not dataset_id:
            from orbflow_sdk.types import ActionResult
            return ActionResult(error="Dataset ID is required")

        subset = ctx.parameters.get("subset", "")
        split = ctx.parameters.get("split", "train")
        offset = max(int(ctx.parameters.get("offset", 0)), 0)
        limit = min(max(int(ctx.parameters.get("limit", 100)), 1), 1000)

        # Use the HuggingFace datasets API (no library needed).
        url = f"https://datasets-server.huggingface.co/rows?dataset={dataset_id}"
        if subset:
            url += f"&config={subset}"
        url += f"&split={split}&offset={offset}&length={limit}"

        hf_token = None
        try:
            import os
            hf_token = os.environ.get("HF_TOKEN", "")
        except Exception:
            pass

        headers = {"Accept": "application/json"}
        if hf_token:
            headers["Authorization"] = f"Bearer {hf_token}"

        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            from orbflow_sdk.types import ActionResult
            return ActionResult(error=f"HuggingFace API error {e.code}: {error_body[:500]}")

        # Extract rows from the response.
        raw_rows = data.get("rows", [])
        rows = [row.get("row", row) for row in raw_rows]
        columns = []
        if data.get("features"):
            columns = [f.get("name", f"col_{i}") for i, f in enumerate(data["features"])]
        elif rows:
            columns = list(rows[0].keys())

        num_rows = data.get("num_rows_total", len(rows))

        return {
            "rows": rows,
            "columns": columns,
            "total_rows": num_rows,
            "dataset_id": dataset_id,
        }


if __name__ == "__main__":
    run(HfDatasetPlugin)
