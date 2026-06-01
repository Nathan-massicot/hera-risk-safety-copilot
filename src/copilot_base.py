"""Common Copilot interface used by every approach (prompt-only, fine-tuned, RAG, RLM).

The eval runner depends only on this interface, so swapping approaches in the
comparison matrix is a one-line change.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol


REPO_ROOT = Path(__file__).resolve().parent.parent
TAXONOMY_PATH = REPO_ROOT / "data/taxonomy/hera_taxonomy.json"


def load_taxonomy() -> dict:
    return json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))


def default_system_prompt() -> str:
    """Compact HERA system prompt — the same one used during fine-tune training."""
    return (
        "You are the HERA Risk & Safety Copilot. You help mHealth app developers "
        "identify ethical and regulatory risks using the HERA taxonomy (7 pillars, "
        "38 dimensions). Ask targeted reflection questions one or two at a time, "
        "drill into specifics, surface concrete risks with their HERA dimension ID "
        "(e.g., [P2.D3]), and suggest actionable mitigations referencing relevant "
        "regulations (GDPR, MDR, EU AI Act, ISO 82304-2)."
    )


@dataclass
class ChatTurn:
    """One assistant response + the prompt that produced it, with bookkeeping."""

    content: str
    latency_s: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    retrieved_context: list[dict] = field(default_factory=list)
    extra: dict = field(default_factory=dict)


class Copilot(Protocol):
    """Every approach implements this Protocol."""

    name: str

    def chat(self, messages: list[dict]) -> ChatTurn:
        """Generate the next assistant turn given the conversation so far.

        `messages` follows the OpenAI shape: [{"role": "system|user|assistant", "content": "..."}].
        The first turn from the eval runner is the developer's app description as a `user` message.
        """
        ...

    def reset(self) -> None:
        """Optional: clear per-scenario state. Default = no-op."""
        ...
