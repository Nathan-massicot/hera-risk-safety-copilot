"""Thin wrapper over the persisted ChromaDB collection.

Used by `src.rag.copilot.RAGCopilot` and any future RAG-aware tooling.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CHROMA_DIR = REPO_ROOT / "models/chroma_hera"
COLLECTION_NAME = "hera_regulations"
DEFAULT_EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

log = logging.getLogger("rag.retriever")


@dataclass
class Passage:
    chunk_id: str
    text: str
    doc_id: str
    title: str
    publisher: str
    jurisdiction: str | None
    url: str | None
    page: int | None
    score: float

    def cite(self) -> str:
        bits = [self.doc_id]
        if self.page is not None:
            bits.append(f"p.{self.page}")
        return f"[{' · '.join(bits)}]"


class Retriever:
    def __init__(
        self,
        chroma_dir: Path = CHROMA_DIR,
        collection_name: str = COLLECTION_NAME,
        embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    ) -> None:
        import chromadb
        from chromadb.utils import embedding_functions

        if not chroma_dir.exists():
            raise FileNotFoundError(
                f"Chroma directory not found: {chroma_dir}. "
                "Run `uv run --extra rag python -m src.rag.ingest` first."
            )

        self._client = chromadb.PersistentClient(path=str(chroma_dir))
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_model)
        self._coll = self._client.get_collection(name=collection_name, embedding_function=ef)

    def __len__(self) -> int:
        return self._coll.count()

    def search(
        self,
        query: str,
        top_k: int = 5,
        jurisdictions: list[str] | None = None,
    ) -> list[Passage]:
        where: dict | None = None
        if jurisdictions:
            where = {"jurisdiction": {"$in": jurisdictions}}

        result = self._coll.query(
            query_texts=[query],
            n_results=top_k,
            where=where,
            include=["documents", "metadatas", "distances"],
        )
        ids = result["ids"][0]
        docs = result["documents"][0]
        metas = result["metadatas"][0]
        dists = result["distances"][0]

        passages: list[Passage] = []
        for cid, text, m, d in zip(ids, docs, metas, dists, strict=True):
            passages.append(
                Passage(
                    chunk_id=cid,
                    text=text,
                    doc_id=m.get("doc_id", "?"),
                    title=m.get("title", "?"),
                    publisher=m.get("publisher", "?"),
                    jurisdiction=m.get("jurisdiction"),
                    url=m.get("url"),
                    page=m.get("page"),
                    score=1.0 - float(d),  # cosine distance → similarity
                )
            )
        return passages
