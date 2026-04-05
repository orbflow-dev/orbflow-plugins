"""Random Data Generator — generate random numbers, categories, and timestamps."""

import random
import string
from datetime import datetime, timedelta, timezone

from orbflow_sdk import Field, action, plugin, run


@plugin(
    name="unsloth-random-data",
    version="0.2.0",
    author="Unsloth",
    category="utility",
    icon="dice",
    description="Generate random numbers, categories, booleans, timestamps, and strings.",
)
class RandomDataPlugin:

    @action(
        ref="plugin:random-data",
        name="Random Data Generator",
        description="Generate random values in various modes.",
        outputs=[
            Field.object("value").label("Value").description("Single generated value"),
            Field.array("values").label("Values").description("Array of values when count > 1"),
            Field.number("count").label("Count").description("Number generated"),
        ],
        parameters=[
            Field.string("mode").label("Mode").default("uniform"),
            Field.number("count").label("Count").default(1),
            Field.number("min").label("Min").default(0),
            Field.number("max").label("Max").default(100),
            Field.number("mean").label("Mean").default(0),
            Field.number("std_dev").label("Std Dev").default(1),
            Field.string("categories").label("Categories").default("A,B,C"),
            Field.number("string_length").label("String Length").default(8),
        ],
    )
    async def generate(self, ctx):
        mode = ctx.parameters.get("mode", "uniform")
        count = min(max(int(ctx.parameters.get("count", 1)), 1), 10000)

        generators = {
            "uniform": self._gen_uniform,
            "gaussian": self._gen_gaussian,
            "category": self._gen_category,
            "boolean": self._gen_boolean,
            "datetime": self._gen_datetime,
            "string": self._gen_string,
        }

        gen = generators.get(mode)
        if gen is None:
            from orbflow_sdk.types import ActionResult
            return ActionResult(error=f"Unknown mode: {mode}")

        values = [gen(ctx.parameters) for _ in range(count)]
        return {"value": values[0], "values": values, "count": len(values)}

    @staticmethod
    def _gen_uniform(params: dict):
        lo = float(params.get("min", 0))
        hi = float(params.get("max", 100))
        return round(random.uniform(lo, hi), 4)

    @staticmethod
    def _gen_gaussian(params: dict):
        mean = float(params.get("mean", 0))
        std = float(params.get("std_dev", 1))
        return round(random.gauss(mean, std), 4)

    @staticmethod
    def _gen_category(params: dict):
        cats = [c.strip() for c in params.get("categories", "A,B,C").split(",")]
        return random.choice(cats) if cats else "A"

    @staticmethod
    def _gen_boolean(_params: dict):
        return random.choice([True, False])

    @staticmethod
    def _gen_datetime(_params: dict):
        now = datetime.now(tz=timezone.utc)
        offset = timedelta(seconds=random.randint(-86400 * 365, 86400 * 365))
        return (now + offset).isoformat()

    @staticmethod
    def _gen_string(params: dict):
        length = min(max(int(params.get("string_length", 8)), 1), 256)
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))


if __name__ == "__main__":
    run(RandomDataPlugin)
