"""Document Parser — split text into chunks for RAG pipelines."""

import re

from orbflow_sdk import Field, action, plugin, run


@plugin(
    name="unsloth-doc-parser",
    version="0.2.0",
    author="Unsloth",
    category="data-source",
    icon="file-text",
    description="Split text into overlapping chunks for RAG, embeddings, and search.",
)
class DocParserPlugin:

    @action(
        ref="plugin:doc-parser",
        name="Document Parser",
        description="Split text into chunks with configurable size, overlap, and strategy.",
        inputs=[
            Field.string("content", required=True).label("Content"),
        ],
        outputs=[
            Field.array("chunks").label("Chunks"),
            Field.number("chunk_count").label("Chunk Count"),
            Field.number("total_chars").label("Total Characters"),
        ],
        parameters=[
            Field.number("chunk_size").label("Chunk Size").default(1000),
            Field.number("chunk_overlap").label("Overlap").default(200),
            Field.string("strategy").label("Strategy").default("sentences"),
        ],
    )
    async def parse(self, ctx):
        content = ctx.input.get("content", "")
        chunk_size = min(max(int(ctx.parameters.get("chunk_size", 1000)), 100), 10000)
        overlap = min(max(int(ctx.parameters.get("chunk_overlap", 200)), 0), chunk_size // 2)
        strategy = ctx.parameters.get("strategy", "sentences")

        if not content.strip():
            return {"chunks": [], "chunk_count": 0, "total_chars": 0}

        splitters = {
            "sentences": self._split_sentences,
            "paragraphs": self._split_paragraphs,
            "fixed": self._split_fixed,
            "recursive": self._split_recursive,
        }

        split_fn = splitters.get(strategy, self._split_sentences)
        segments = split_fn(content)
        chunks = self._merge_into_chunks(segments, chunk_size, overlap)

        result_chunks = []
        for i, chunk in enumerate(chunks):
            char_start = content.find(chunk[:50]) if len(chunk) >= 50 else content.find(chunk)
            result_chunks.append({
                "text": chunk,
                "index": i,
                "char_start": max(char_start, 0),
                "char_end": max(char_start, 0) + len(chunk),
                "char_count": len(chunk),
            })

        return {
            "chunks": result_chunks,
            "chunk_count": len(result_chunks),
            "total_chars": len(content),
        }

    @staticmethod
    def _split_sentences(text: str) -> list[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def _split_paragraphs(text: str) -> list[str]:
        paragraphs = re.split(r"\n\s*\n", text)
        return [p.strip() for p in paragraphs if p.strip()]

    @staticmethod
    def _split_fixed(text: str) -> list[str]:
        return list(text)  # character-level, merged later

    @staticmethod
    def _split_recursive(text: str) -> list[str]:
        for sep in ["\n\n", "\n", ". ", " "]:
            parts = text.split(sep)
            if len(parts) > 1:
                return [p.strip() for p in parts if p.strip()]
        return [text]

    @staticmethod
    def _merge_into_chunks(segments: list[str], target_size: int, overlap: int) -> list[str]:
        chunks = []
        current = ""
        for segment in segments:
            if len(current) + len(segment) + 1 > target_size and current:
                chunks.append(current.strip())
                # Keep overlap from the end of the current chunk
                if overlap > 0:
                    current = current[-overlap:] + " " + segment
                else:
                    current = segment
            else:
                current = (current + " " + segment).strip() if current else segment

        if current.strip():
            chunks.append(current.strip())

        return chunks


if __name__ == "__main__":
    run(DocParserPlugin)
