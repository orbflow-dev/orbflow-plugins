"""UUID Generator — generate unique identifiers."""

import uuid

from orbflow_sdk import Field, action, plugin, run


@plugin(
    name="orbflow-uuid-gen",
    version="0.2.0",
    author="Orbflow",
    category="utility",
    icon="hash",
    description="Generate UUID v4 identifiers in multiple formats.",
)
class UuidGenPlugin:

    FORMATTERS = {
        "hyphenated": str,
        "simple": lambda u: u.hex,
        "urn": lambda u: u.urn,
        "upper": lambda u: str(u).upper(),
    }

    @action(
        ref="plugin:uuid-gen",
        name="UUID Generator",
        outputs=[
            Field.string("uuid").label("UUID").description("Single generated UUID"),
            Field.array("uuids").label("UUIDs").description("Array of UUIDs when count > 1"),
            Field.number("count").label("Count").description("Number generated"),
        ],
        parameters=[
            Field.number("count").default(1).description("Number of UUIDs (1-1000)"),
            Field.string("format").default("hyphenated").enum("hyphenated", "simple", "urn", "upper"),
        ],
    )
    async def generate(self, ctx):
        count = min(max(int(ctx.parameters.get("count", 1)), 1), 1000)
        fmt = ctx.parameters.get("format", "hyphenated")
        formatter = self.FORMATTERS.get(fmt, str)

        generated = [formatter(uuid.uuid4()) for _ in range(count)]

        return {
            "uuid": generated[0],
            "uuids": generated,
            "count": len(generated),
        }


if __name__ == "__main__":
    run(UuidGenPlugin)
