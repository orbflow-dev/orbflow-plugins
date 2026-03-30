"""Schema Transform — reshape data rows to a target schema."""

import json
import re

from orbflow_sdk import Field, action, plugin, run


@plugin(
    name="orbflow-schema-transform",
    version="0.2.0",
    author="Orbflow",
    category="data-processing",
    icon="filter",
    description="Reshape data rows using field mapping, templates, and filtering.",
)
class SchemaTransformPlugin:

    @action(
        ref="plugin:schema-transform",
        name="Schema Transform",
        description="Map, rename, and reshape fields across rows.",
        inputs=[
            Field.array("rows", required=True).label("Rows"),
            Field.object("mapping").label("Field Mapping"),
        ],
        outputs=[
            Field.array("rows").label("Rows").description("Transformed rows"),
            Field.number("row_count").label("Row Count"),
            Field.array("columns").label("Columns").description("Output column names"),
        ],
        parameters=[
            Field.boolean("drop_unmapped").label("Drop Unmapped").default(True),
            Field.string("template").label("Template"),
            Field.string("template_field").label("Template Field").default("computed"),
        ],
    )
    async def transform(self, ctx):
        rows = ctx.input.get("rows", [])
        mapping = ctx.input.get("mapping", {})
        drop_unmapped = ctx.parameters.get("drop_unmapped", True)
        template = ctx.parameters.get("template", "")
        template_field = ctx.parameters.get("template_field", "computed")

        result = []
        for row in rows:
            if not isinstance(row, dict):
                continue

            if mapping:
                new_row = {}
                for new_key, source_key in mapping.items():
                    if source_key in row:
                        new_row[new_key] = row[source_key]
                    elif not drop_unmapped:
                        new_row[new_key] = None
                if not drop_unmapped:
                    for k, v in row.items():
                        if k not in mapping.values():
                            new_row.setdefault(k, v)
            else:
                new_row = dict(row)

            if template:
                new_row[template_field] = self._render_template(template, row)

            result.append(new_row)

        columns = list(result[0].keys()) if result else []
        return {"rows": result, "row_count": len(result), "columns": columns}

    @staticmethod
    def _render_template(template: str, row: dict) -> str:
        """Simple {{field}} template rendering."""
        def replacer(match):
            key = match.group(1).strip()
            return str(row.get(key, ""))
        return re.sub(r"\{\{(.+?)\}\}", replacer, template)


if __name__ == "__main__":
    run(SchemaTransformPlugin)
