"""RLM multi-agent HERA Copilot.

Orchestrates the Generator/Critic/Selector agents in sequence on every turn.
Implements the `Copilot` Protocol so the eval runner can swap it in transparently.

Tradeoff: 3× more Ollama calls per turn vs prompt-only, so latency is ~3×.
Upside: each turn is the result of "propose multiple → critique → pick best",
which produces deeper / more on-target questions for the same base model.
"""

from __future__ import annotations

import logging
import os
import re
import time
from collections.abc import Iterable

from src.baseline.inference import OllamaCopilot
from src.copilot_base import ChatTurn, default_system_prompt
from src.rlm.agents import critic_step, generator_step, selector_step

log = logging.getLogger("copilot.rlm")

DEFAULT_RLM_MODEL = os.environ.get(
    "HERA_RLM_MODEL", "qwen3:8b"  # generic Qwen3-8B = same base as the fine-tuned SLM (fair comparison)
)
DIM_RE = re.compile(r"\bP(\d)\.D(\d+)\b")


class RLMCopilot:
    name: str = "rlm"

    def __init__(
        self,
        model: str = DEFAULT_RLM_MODEL,
        max_turns: int = 10,
    ) -> None:
        # One shared base — each agent step rewrites system_prompt before calling
        self._base = OllamaCopilot(model=model, name="rlm-inner", system_prompt="")
        self._max_turns = max_turns
        self._covered_dims: set[str] = set()
        self._turn_count: int = 0

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def reset(self) -> None:
        self._covered_dims = set()
        self._turn_count = 0

    def _update_covered(self, messages: Iterable[dict]) -> None:
        for m in messages:
            for a, b in DIM_RE.findall(m["content"]):
                self._covered_dims.add(f"P{a}.D{b}")

    # ------------------------------------------------------------------
    # Copilot Protocol
    # ------------------------------------------------------------------

    def chat(self, messages: list[dict]) -> ChatTurn:
        t0 = time.time()
        self._turn_count += 1
        self._update_covered(messages)

        # Strip any incoming system message — RLM owns its own per-agent prompt
        convo = [m for m in messages if m["role"] != "system"]

        # 1. Generator → 3 candidates
        candidates = generator_step(self._base, convo, sorted(self._covered_dims))

        # 2. Critic → scores
        scores = critic_step(self._base, convo, candidates, sorted(self._covered_dims))

        # 3. Selector → decision + user-facing message
        budget_left = max(0, self._max_turns - self._turn_count)
        decision = selector_step(
            self._base, convo, candidates, scores,
            sorted(self._covered_dims), turn_budget_remaining=budget_left,
        )

        content = decision.get("user_facing_message", "")
        # If selector picked an ask, also stamp the dimension in the visible output
        # in case the model forgot — guarantees citation for metrics.
        chosen_dim = decision.get("chosen_dimension")
        if chosen_dim and chosen_dim not in content:
            content = f"{content.strip()} [{chosen_dim}]"

        return ChatTurn(
            content=content,
            latency_s=time.time() - t0,
            extra={
                "rlm_decision": decision.get("decision"),
                "rlm_chosen_dimension": chosen_dim,
                "n_candidates": len(candidates),
                "candidate_dimensions": [c.get("dimension") for c in candidates],
                "covered_dims_count": len(self._covered_dims),
            },
        )
