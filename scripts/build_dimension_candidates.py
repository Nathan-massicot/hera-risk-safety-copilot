"""Precompute candidate regulatory citations for each HERA dimension.

Loads the bge retriever ONCE and runs one query per dimension (name + description +
reflection questions) against the Chroma corpus, writing the top-K candidate cards to
`data/taxonomy/_dim_candidates.json`. A downstream LLM workflow then picks the 2-4 truly
relevant citations per dimension and writes a one-line applicability note.
"""

from __future__ import annotations

import json
from pathlib import Path

from src.rag.retriever import Retriever

REPO = Path(__file__).resolve().parent.parent
TAX = REPO / "data/taxonomy/hera_taxonomy.json"
OUT = REPO / "data/taxonomy/_dim_candidates.json"
TOP_K = 8


def main() -> None:
    taxonomy = json.loads(TAX.read_text(encoding="utf-8"))
    retriever = Retriever()

    out: dict[str, dict] = {}
    for pillar in taxonomy["pillars"]:
        for dim in pillar["dimensions"]:
            query = " ".join(
                [dim["name"], dim["description"], *dim.get("reflection_questions", [])]
            )
            passages = retriever.search(query, top_k=TOP_K)
            out[dim["id"]] = {
                "name": dim["name"],
                "pillar": pillar["id"],
                "candidates": [
                    {
                        "cite": p.cite(),
                        "title": p.title,
                        "jurisdiction": p.jurisdiction,
                        "score": round(float(p.score), 3),
                        "snippet": p.text.strip()[:300],
                    }
                    for p in passages
                ],
            }
            print(f"{dim['id']:8s} {dim['name'][:40]:40s} -> {len(out[dim['id']]['candidates'])} cards")

    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {OUT.relative_to(REPO)} ({len(out)} dimensions)")


if __name__ == "__main__":
    main()
