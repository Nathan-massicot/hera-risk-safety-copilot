"""RAG-aware HERA Copilot.

Same base model as the prompt-only baseline, but each turn the system prompt
is augmented with the top-K most relevant passages retrieved from the
regulatory corpus. Citations are returned in `ChatTurn.retrieved_context`.
"""

from __future__ import annotations

import logging
import os
import time

from src.baseline.inference import OllamaCopilot
from src.copilot_base import ChatTurn, default_system_prompt
from src.rag.retriever import Passage, Retriever

log = logging.getLogger("copilot.rag")

DEFAULT_TOP_K = int(os.environ.get("HERA_RAG_TOP_K", "5"))
DEFAULT_RAG_MODEL = os.environ.get(
    "HERA_RAG_MODEL", "mistral:7b-instruct-v0.3-q4_K_M"
)


class RAGCopilot:
    """Same base model as prompt-only, but RAG-augmented at every turn."""

    name: str = "rag"

    def __init__(
        self,
        model: str = DEFAULT_RAG_MODEL,
        top_k: int = DEFAULT_TOP_K,
        retriever: Retriever | None = None,
        jurisdictions: list[str] | None = None,
    ) -> None:
        self._model_id = model
        self._top_k = top_k
        self._retriever = retriever or Retriever()
        self._jurisdictions = jurisdictions
        self._base = OllamaCopilot(model=model, name="rag-inner", system_prompt="")

    def _build_query(self, messages: list[dict]) -> str:
        """Concatenate the last user message + recent assistant turn (if any)."""
        last_user = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"), ""
        )
        # Add a touch of context from the previous assistant turn (1 sentence)
        last_assistant = next(
            (m["content"] for m in reversed(messages) if m["role"] == "assistant"), ""
        )
        ctx = last_assistant.split(".")[0][:200] if last_assistant else ""
        if ctx:
            return f"{last_user} | {ctx}"
        return last_user

    @staticmethod
    def _format_passages(passages: list[Passage]) -> str:
        if not passages:
            return ""
        lines = ["\n## Retrieved regulatory passages (cite when relevant)\n"]
        for p in passages:
            lines.append(
                f"### {p.cite()} {p.title}\n"
                f"_jurisdiction: {p.jurisdiction or 'n/a'} · score={p.score:.2f}_\n\n"
                f"{p.text.strip()[:900]}\n"
            )
        lines.append(
            "\nWhen you reference a passage in your reply, end the sentence "
            "with the citation tag in square brackets (e.g., `[mdr_2017_745 · p.32]`).\n"
        )
        return "\n".join(lines)

    def chat(self, messages: list[dict]) -> ChatTurn:
        t0 = time.time()

        # 1) retrieve
        query = self._build_query(messages)
        passages: list[Passage] = []
        if query:
            try:
                passages = self._retriever.search(
                    query, top_k=self._top_k, jurisdictions=self._jurisdictions
                )
            except Exception as exc:
                log.warning("Retrieval failed: %s", exc)

        # 2) build the augmented system prompt
        system_prompt = default_system_prompt() + self._format_passages(passages)
        augmented = [{"role": "system", "content": system_prompt}]
        for m in messages:
            if m["role"] == "system":
                continue  # already overridden
            augmented.append(m)

        # 3) call the base Ollama copilot
        inner_turn = self._base.chat(augmented)

        return ChatTurn(
            content=inner_turn.content,
            latency_s=time.time() - t0,
            prompt_tokens=inner_turn.prompt_tokens,
            completion_tokens=inner_turn.completion_tokens,
            retrieved_context=[
                {
                    "chunk_id": p.chunk_id,
                    "doc_id": p.doc_id,
                    "page": p.page,
                    "score": p.score,
                    "snippet": p.text[:200],
                }
                for p in passages
            ],
            extra={"query": query, "retrieved_n": len(passages)},
        )

    def reset(self) -> None:
        return None
