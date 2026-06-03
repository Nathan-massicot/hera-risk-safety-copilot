"""Ingest regulatory PDFs into a local ChromaDB collection.

Reads:
- data/regulatory_docs/manifest.json  (which PDFs to ingest + metadata)
- data/regulatory_docs/<filename>.pdf  (one per doc, downloaded by Task #6)

Writes:
- models/chroma_hera/                  persistent Chroma store (gitignored)

Usage:
    uv run --extra rag python -m src.rag.ingest
    uv run --extra rag python -m src.rag.ingest --reset   # wipe + re-ingest all
    uv run --extra rag python -m src.rag.ingest --only eu_ai_act
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.utils.logging_config import configure_logging, new_run_dir  # noqa: E402

log = logging.getLogger("rag.ingest")

DOCS_DIR = REPO_ROOT / "data/regulatory_docs"
MANIFEST_PATH = DOCS_DIR / "manifest.json"
CHROMA_DIR = REPO_ROOT / "models/chroma_hera"
COLLECTION_NAME = "hera_regulations"
CARDS_DIR = REPO_ROOT / "data/regulations/cards_rich"

# Embedding model — local, no API call. Multilingual would be MiniLM-L12-v2;
# bge-small-en-v1.5 is faster and very strong on English regulatory text.
DEFAULT_EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


# ---------------------------------------------------------------------------
# PDF → chunks
# ---------------------------------------------------------------------------


def extract_pages(pdf_path: Path) -> list[tuple[int, str]]:
    """Return list of (page_num_1based, text)."""
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    pages: list[tuple[int, str]] = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            txt = page.extract_text() or ""
        except Exception as exc:
            log.warning("Page %d extraction failed in %s: %s", i, pdf_path.name, exc)
            txt = ""
        pages.append((i, txt))
    return pages


def chunk_text(text: str, target_words: int = 220, overlap_words: int = 30) -> list[str]:
    """Sliding-window word-based chunking with overlap.

    220 words ≈ 300 tokens, which fits BGE's 512-token limit comfortably.
    Overlap preserves context across boundaries (relevant for legal articles).
    """
    words = text.split()
    if not words:
        return []
    if len(words) <= target_words:
        return [" ".join(words)]

    chunks: list[str] = []
    step = target_words - overlap_words
    for start in range(0, len(words), step):
        chunk = words[start : start + target_words]
        if not chunk:
            break
        chunks.append(" ".join(chunk))
        if start + target_words >= len(words):
            break
    return chunks


# ---------------------------------------------------------------------------
# Chroma collection
# ---------------------------------------------------------------------------


def get_collection(reset: bool, embedding_model: str):
    import chromadb
    from chromadb.utils import embedding_functions

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_model)
    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
            log.info("Deleted existing collection '%s'", COLLECTION_NAME)
        except Exception:
            pass
    coll = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )
    return client, coll


def already_indexed_docs(coll) -> set[str]:
    """Read existing chunk ids to know which docs were already ingested."""
    try:
        n = coll.count()
        if n == 0:
            return set()
        # ids look like "<doc_id>::p<page>::c<chunk>"
        all_ids = coll.get(include=[])["ids"]
        return {i.split("::", 1)[0] for i in all_ids}
    except Exception:
        return set()


# ---------------------------------------------------------------------------
# Main ingest loop
# ---------------------------------------------------------------------------


def ingest_doc(coll, doc: dict, pdf_path: Path) -> int:
    pages = extract_pages(pdf_path)
    log.info("  %d pages extracted", len(pages))

    ids: list[str] = []
    docs: list[str] = []
    metas: list[dict] = []

    for page_num, page_text in pages:
        if not page_text.strip():
            continue
        chunks = chunk_text(page_text)
        for c_idx, chunk in enumerate(chunks):
            cid = f"{doc['id']}::p{page_num:04d}::c{c_idx:02d}"
            ids.append(cid)
            docs.append(chunk)
            metas.append(
                {
                    "doc_id": doc["id"],
                    "title": doc["title"],
                    "publisher": doc["publisher"],
                    "year": doc.get("year"),
                    "jurisdiction": doc.get("jurisdiction"),
                    "url": doc.get("url"),
                    "page": page_num,
                }
            )

    if not ids:
        log.warning("  No chunks extracted from %s", pdf_path.name)
        return 0

    # Chroma batch limit ~5k; we batch defensively at 200
    BATCH = 200
    for i in range(0, len(ids), BATCH):
        coll.add(
            ids=ids[i : i + BATCH],
            documents=docs[i : i + BATCH],
            metadatas=metas[i : i + BATCH],
        )
    log.info("  %d chunks added to Chroma", len(ids))
    return len(ids)


def parse_frontmatter(md: str) -> tuple[dict, str]:
    """Split a card's YAML-ish frontmatter from its markdown body."""
    import re

    m = re.match(r"^---\n(.*?)\n---\n(.*)$", md, re.S)
    if not m:
        return {}, md
    fm: dict = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("-"):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm, m.group(2)


def ingest_cards(coll) -> int:
    """Ingest the curated regulatory cards (data/regulations/cards_rich/*.md)."""
    files = sorted(CARDS_DIR.glob("*.md"))
    total = 0
    for path in files:
        fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        cid = fm.get("id", path.stem)
        meta = {
            "doc_id": f"card_{cid}",
            "title": fm.get("title", cid),
            "publisher": "HERA regulatory cards",
            "jurisdiction": fm.get("jurisdiction"),
            "url": fm.get("official_url"),
            "page": 0,
        }
        meta = {k: v for k, v in meta.items() if v is not None}  # Chroma rejects None
        ids, docs, metas = [], [], []
        for i, chunk in enumerate(chunk_text(body)):
            ids.append(f"card_{cid}::c{i:02d}")
            docs.append(chunk)
            metas.append(dict(meta))
        if ids:
            coll.add(ids=ids, documents=docs, metadatas=metas)
            total += len(ids)
    log.info("Ingested %d chunks from %d cards", total, len(files))
    return total


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reset", action="store_true", help="Drop the collection first.")
    ap.add_argument("--only", action="append", help="Only ingest these doc ids.")
    ap.add_argument("--cards", action="store_true",
                    help="Ingest the curated cards_rich/*.md corpus instead of the PDFs.")
    ap.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL)
    args = ap.parse_args(argv)

    run_dir = new_run_dir(prefix="rag_ingest")
    configure_logging(run_dir)

    if not MANIFEST_PATH.exists():
        log.error("Manifest not found: %s", MANIFEST_PATH)
        return 1
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    log.info("Embedding model: %s", args.embedding_model)
    log.info("Chroma persistent dir: %s", CHROMA_DIR.relative_to(REPO_ROOT))

    _, coll = get_collection(args.reset, args.embedding_model)

    if args.cards:
        ingest_cards(coll)
        log.info("Collection size now: %d chunks", coll.count())
        return 0

    indexed = already_indexed_docs(coll)
    log.info("Already indexed: %d docs (%s)", len(indexed),
             ", ".join(sorted(indexed)) if indexed else "none")

    total_chunks = 0
    for doc in manifest["documents"]:
        did = doc["id"]
        if args.only and did not in args.only:
            continue
        if did in indexed and not args.reset:
            log.info("⏭  %-22s already indexed, skipping", did)
            continue
        fname = doc.get("filename")
        if not fname:
            log.info("⏭  %-22s no filename (paywalled / book) — skipping", did)
            continue
        pdf_path = DOCS_DIR / fname
        if not pdf_path.exists():
            log.warning("⏭  %-22s PDF missing: %s — download first", did, pdf_path.name)
            continue

        log.info("→  %-22s ingesting (%s)", did, pdf_path.name)
        n = ingest_doc(coll, doc, pdf_path)
        total_chunks += n

    log.info("\nTotal chunks indexed this run: %d", total_chunks)
    log.info("Collection size now: %d chunks", coll.count())
    return 0


if __name__ == "__main__":
    sys.exit(main())
