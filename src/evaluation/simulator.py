"""Simulated developer that answers the copilot's questions deterministically.

The eval needs all 4 approaches to receive identical developer answers — so we
cannot let a real LLM improvise responses. Instead, each scenario has a
`simulated_answers` dict keyed by probe categories ('data_collected',
'consent_flow', 'regulatory_status', …). The simulator picks the closest key
to the copilot's last question via word-overlap and returns that canned answer.

If no key matches, fallback to a polite 'I don't know yet, but happy to dig in'
to keep the conversation moving without leaking info beyond the scenario.
"""

from __future__ import annotations

import re

# Common keywords that hint at a specific probe category. Tuned heuristically;
# extend as we learn what the copilots actually ask.
PROBE_HINTS = {
    "data_collected": {"data", "collect", "store", "stored", "field", "information",
                       "what.*type", "personal", "identifier", "record"},
    "consent_flow": {"consent", "opt.in", "agree", "disclosure", "privacy.policy",
                     "permission", "agreement", "informed"},
    "regulatory_status": {"regulat", "class", "samd", "device", "mdr", "ce.mark",
                          "wellness", "intended.purpose"},
    "user_research": {"user.research", "tested", "testing", "study", "pilot",
                      "validation", "evidence"},
    "accessibility": {"accessib", "wcag", "language", "screen.reader", "literacy",
                      "impair", "disabil"},
    "safety_validation": {"safety", "validation", "clinical.evidence",
                          "sensitivity", "specificity", "false.positive",
                          "false.negative", "accuracy"},
    "ai_or_algorithm": {"ai", "model", "algorithm", "ml ", "machine.learning",
                        "neural", "llm", "deep.learning", "prediction"},
    "post_market": {"post.market", "after.launch", "vigilance", "incident",
                    "complaint", "monitor"},
    "data_sharing": {"third.party", "share", "sharing", "advertising", "partner",
                     "vendor", "sub.processor", "research.partner"},
    "withdrawal_rights": {"delete", "withdraw", "erasure", "export", "portab",
                          "data.removal"},
}


def _normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower())


def _score_key(question: str, key: str, hints: set[str]) -> int:
    qn = _normalize(question)
    score = 0
    for h in hints:
        # Build a word-boundary pattern from the hint. We escape the whole hint
        # first so stray regex metachars can't blow up re.compile, then reinstate
        # the two tokens the hint vocabulary actually uses:
        #   "."  → optional separator [space/-/_]   (e.g. "opt.in" → "opt in")
        #   "*"  → wildcard gap                       (e.g. "what.*type")
        esc = re.escape(h)
        esc = esc.replace(r"\.", r"[ _\-]?").replace(r"\*", r".*")
        pattern = r"\b" + esc + r"\b"
        if re.search(pattern, qn):
            score += 1
    # Direct mention of the key as a word counts double
    if key.replace("_", " ") in qn:
        score += 2
    return score


def best_probe_key(question: str, available_keys: set[str]) -> str | None:
    """Return the highest-scoring probe key for this question, or None if no signal."""
    scored = [(_score_key(question, k, PROBE_HINTS.get(k, set())), k) for k in available_keys]
    scored = [(s, k) for s, k in scored if s > 0]
    if not scored:
        return None
    scored.sort(reverse=True)
    return scored[0][1]


def simulate_answer(
    scenario: dict,
    copilot_last_message: str,
    used_keys: set[str] | None = None,
) -> str:
    """Map the copilot's last message to a canned answer; fallback if no match.

    `used_keys` (mutated in place when provided) records which probe categories the
    developer has already answered this conversation. We never serve the same canned
    answer twice — if the copilot re-asks an answered topic we steer it forward
    instead of replaying the block, which is what stops the harness from manufacturing
    the verbatim looping that dragged down Depth across all approaches.
    """
    answers: dict[str, str] = scenario.get("simulated_answers", {})
    if not answers:
        return "I'm not sure yet; let's discuss what would help."
    served = used_keys if used_keys is not None else set()
    candidates = set(answers) - served
    key = best_probe_key(copilot_last_message, candidates) if candidates else None
    if key is None:
        if not candidates:
            # Everything we can volunteer has been said — steer toward a summary
            # rather than repeating a prior answer.
            return (
                "I think we've covered the main points I can share. "
                "Want to pull this together into a summary of the key risks?"
            )
        # The question doesn't map to anything scripted for this scenario.
        return (
            "Good question — we haven't pinned that down yet. "
            "Happy to think through it with you if you can sketch what 'good' would look like."
        )
    if used_keys is not None:
        used_keys.add(key)
    return answers[key]
