"""The three RLM agents: Generator, Critic, Selector.

Each agent is a thin wrapper around the base Ollama copilot with a specialized
system prompt that constrains the model to a narrow role. Inputs/outputs are
JSON strings parsed defensively (the small base model occasionally adds prose).

Adapted from Deng, Viganò & Hauser (2025) "Using LLMs to Foster Ethical
Awareness", in which the same Generator/Critic/Selector triad reasons over the
HIEDE taxonomy. We re-target it at HERA.
"""

from __future__ import annotations

import json
import logging
import re

from src.baseline.inference import OllamaCopilot

log = logging.getLogger("rlm.agents")

JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


def extract_json(text: str) -> dict | list:
    text = text.strip()
    m = JSON_FENCE_RE.search(text)
    if m:
        text = m.group(1)
    return json.loads(text)


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------


GENERATOR_SYSTEM = """You are the GENERATOR agent in a multi-agent HERA Risk & Safety Copilot.

Your job: given the conversation so far and a list of HERA dimensions already covered, propose **exactly 3 candidate reflection questions**. Each candidate must:
- target a *different* HERA dimension (preferably uncovered)
- be specific to THIS developer's app, not generic
- cite the dimension ID in square brackets, e.g. `[P2.D3]`
- be a single question (one `?`)

Output strict JSON:

```json
{
  "candidates": [
    {"question": "<question text>", "dimension": "P2.D3", "rationale": "why this dim now"},
    {"question": "...", "dimension": "P7.D1", "rationale": "..."},
    {"question": "...", "dimension": "P3.D2", "rationale": "..."}
  ]
}
```

No commentary, no markdown headers, just the JSON object."""


def generator_step(model: OllamaCopilot, conversation: list[dict], covered_dims: list[str]) -> list[dict]:
    """Returns up to 3 candidate questions, each {"question", "dimension", "rationale"}."""
    convo_text = "\n".join(
        f"### {m['role'].upper()}\n{m['content']}" for m in conversation
    )
    user = (
        f"COVERED DIMENSIONS SO FAR: {', '.join(covered_dims) if covered_dims else '(none)'}\n\n"
        f"CONVERSATION:\n{convo_text}\n\n"
        "Now produce the JSON object with 3 candidate questions."
    )
    model.system_prompt = GENERATOR_SYSTEM
    turn = model.chat([{"role": "user", "content": user}])
    try:
        payload = extract_json(turn.content)
        raw = payload.get("candidates", []) if isinstance(payload, dict) else []
    except (json.JSONDecodeError, AttributeError) as exc:
        log.warning("Generator JSON parse failed: %s", exc)
        return []
    # Normalise: the small base model often omits/renames keys. Guarantee every
    # candidate has question/dimension/rationale so downstream agents never KeyError.
    norm: list[dict] = []
    for c in raw:
        if not isinstance(c, dict):
            continue
        q = str(c.get("question") or c.get("q") or "").strip()
        if not q:
            continue
        norm.append({
            "question": q,
            "dimension": str(c.get("dimension") or c.get("dim") or "").strip(),
            "rationale": str(c.get("rationale") or "").strip(),
        })
    return norm[:3]


# ---------------------------------------------------------------------------
# Critic
# ---------------------------------------------------------------------------


CRITIC_SYSTEM = """You are the CRITIC agent in a multi-agent HERA Risk & Safety Copilot.

You receive 3 candidate reflection questions proposed by the Generator. Score each on three 1–5 dimensions and produce a brief critique:

- **relevance**: how well does it apply to THIS developer's specific app?
- **depth**: does it drill into specifics (regulation article, scenario, data flow), or stay generic?
- **novelty**: does it open a dimension that has NOT been covered yet?

Output strict JSON:

```json
{
  "scores": [
    {"index": 0, "relevance": 4, "depth": 5, "novelty": 3, "critique": "..."},
    {"index": 1, "relevance": 5, "depth": 4, "novelty": 5, "critique": "..."},
    {"index": 2, "relevance": 2, "depth": 3, "novelty": 4, "critique": "..."}
  ]
}
```

No commentary, no markdown headers, just the JSON object."""


def critic_step(model: OllamaCopilot, conversation: list[dict], candidates: list[dict],
                covered_dims: list[str]) -> list[dict]:
    """Returns scores for each candidate."""
    if not candidates:
        return []
    convo_text = "\n".join(
        f"### {m['role'].upper()}\n{m['content']}" for m in conversation
    )
    cand_text = "\n".join(
        f"  [{i}] dim={c.get('dimension', '?')} — {c.get('question', '')}"
        for i, c in enumerate(candidates)
    )
    user = (
        f"COVERED DIMENSIONS SO FAR: {', '.join(covered_dims) if covered_dims else '(none)'}\n\n"
        f"CONVERSATION:\n{convo_text}\n\n"
        f"CANDIDATE QUESTIONS:\n{cand_text}\n\n"
        "Now produce the JSON object with scores for all 3."
    )
    model.system_prompt = CRITIC_SYSTEM
    turn = model.chat([{"role": "user", "content": user}])
    try:
        payload = extract_json(turn.content)
        return payload.get("scores", [])
    except (json.JSONDecodeError, AttributeError) as exc:
        log.warning("Critic JSON parse failed: %s", exc)
        return [{"index": i, "relevance": 3, "depth": 3, "novelty": 3, "critique": "(critic failed)"}
                for i in range(len(candidates))]


# ---------------------------------------------------------------------------
# Selector
# ---------------------------------------------------------------------------


SELECTOR_SYSTEM = """You are the SELECTOR agent in a multi-agent HERA Risk & Safety Copilot.

Given the 3 candidate questions and the Critic's scores, you must:
1. Pick the strongest candidate (by combined score relevance+depth+novelty) AND
2. Decide whether the conversation should:
   - **ask** the chosen question now, OR
   - **wrap up** with a short risk-report stub IF coverage feels sufficient (≥ 6 distinct dimensions touched), the developer has been answering tersely for the last 2 turns, OR the budget hint says to wrap.

Produce a single user-facing reply that, when chosen to ask, references concrete elements of the developer's app (not a generic version of the candidate question).

Output strict JSON:

```json
{
  "decision": "ask" | "wrap_up",
  "chosen_index": <int 0-2 or -1 if wrap_up>,
  "chosen_dimension": "Pn.Dm" | null,
  "user_facing_message": "<the message the copilot should reply with>"
}
```

When `decision = "ask"`, the `user_facing_message` may rephrase the candidate question to be more concrete to the app under discussion, and MAY also surface a 1-sentence risk observation referencing the relevant HERA dimension before the question.

When `decision = "wrap_up"`, the `user_facing_message` is a brief HERA risk-report stub with `[Pn.Dm]` references and ends with a list of uncovered dimensions worth a future conversation.

No commentary, no markdown headers, just the JSON object."""


def selector_step(model: OllamaCopilot, conversation: list[dict], candidates: list[dict],
                  scores: list[dict], covered_dims: list[str], turn_budget_remaining: int) -> dict:
    """Returns the selection decision + user-facing message."""
    if not candidates or not scores:
        return {
            "decision": "wrap_up",
            "chosen_index": -1,
            "chosen_dimension": None,
            "user_facing_message": (
                "I think we've covered the main dimensions for now. "
                "Want me to produce a brief risk report?"
            ),
        }
    convo_text = "\n".join(
        f"### {m['role'].upper()}\n{m['content']}" for m in conversation
    )
    cand_text = "\n".join(
        f"  [{i}] dim={c.get('dimension', '?')} — {c.get('question', '')}  "
        f"(rel={_get_score(scores, i, 'relevance')}, "
        f"depth={_get_score(scores, i, 'depth')}, "
        f"nov={_get_score(scores, i, 'novelty')})"
        for i, c in enumerate(candidates)
    )
    user = (
        f"COVERED DIMENSIONS SO FAR ({len(covered_dims)}): "
        f"{', '.join(covered_dims) if covered_dims else '(none)'}\n"
        f"TURNS REMAINING IN BUDGET: {turn_budget_remaining}\n\n"
        f"CONVERSATION:\n{convo_text}\n\n"
        f"CANDIDATES (with Critic scores):\n{cand_text}\n\n"
        "Now produce the JSON decision object."
    )
    model.system_prompt = SELECTOR_SYSTEM
    turn = model.chat([{"role": "user", "content": user}])
    try:
        payload = extract_json(turn.content)
        return payload if isinstance(payload, dict) else {}
    except (json.JSONDecodeError, AttributeError) as exc:
        log.warning("Selector JSON parse failed: %s", exc)
        # Fallback: pick the highest-relevance candidate, ask it verbatim
        idx = _argmax_combined(scores)
        idx = idx if 0 <= idx < len(candidates) else 0
        chosen = candidates[idx]
        return {
            "decision": "ask",
            "chosen_index": idx,
            "chosen_dimension": chosen.get("dimension") or None,
            "user_facing_message": chosen.get("question", ""),
        }


def _get_score(scores: list[dict], idx: int, key: str) -> int:
    for s in scores:
        if s.get("index") == idx:
            return s.get(key, 0)
    return 0


def _argmax_combined(scores: list[dict]) -> int:
    best, best_score = 0, -1
    for s in scores:
        i = s.get("index", 0)
        total = s.get("relevance", 0) + s.get("depth", 0) + s.get("novelty", 0)
        if total > best_score:
            best, best_score = i, total
    return best


# ---------------------------------------------------------------------------
# Synthesizer
# ---------------------------------------------------------------------------


SYNTHESIZER_SYSTEM = """You are the SYNTHESIZER agent in a multi-agent HERA Risk & Safety Copilot.

The conversation is over and the developer has asked for a structured risk report.
Using ONLY what the conversation established about THIS app, write a concise HERA risk report:
- Group findings by severity: **High**, **Medium**, **Low**.
- For each finding: cite the HERA dimension ID in square brackets (e.g. `[P2.D3]`), state the risk in one line tied to the developer's specifics, and give ONE concrete, implementable mitigation (a recipe — NOT "ensure compliance") that references the precise regulation/article where relevant (GDPR, MDR, EU AI Act, ISO 82304-2).
- End with a line `Not yet covered:` listing HERA dimension IDs worth a future session.

Plain markdown. No preamble, no follow-up questions — this is the deliverable itself."""


def synthesizer_step(model: OllamaCopilot, conversation: list[dict], covered_dims: list[str]) -> str:
    """Produce the final, free-text HERA risk report (the closing deliverable)."""
    convo_text = "\n".join(
        f"### {m['role'].upper()}\n{m['content']}" for m in conversation
    )
    user = (
        f"COVERED DIMENSIONS SO FAR: {', '.join(covered_dims) if covered_dims else '(none)'}\n\n"
        f"CONVERSATION:\n{convo_text}\n\n"
        "Now write the structured HERA risk report."
    )
    model.system_prompt = SYNTHESIZER_SYSTEM
    turn = model.chat([{"role": "user", "content": user}])
    return turn.content
