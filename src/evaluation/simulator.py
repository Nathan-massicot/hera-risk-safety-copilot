"""Simulated developer that answers the copilot's questions deterministically.

The eval needs every approach to receive consistent, reproducible developer answers
— so we cannot let a real LLM improvise (that would give each approach different
information and confound the comparison). Instead, each scenario ships a pool of
disclosed facts (`simulated_answers` + bootstrapped `dev_facts`), and the copilot's
question is routed to the most relevant *unused* fact.

Two routers, both deterministic:
- `SemanticDeveloper` (default) embeds the facts + the question with the same bge model
  RAG uses and picks the nearest fact by cosine — robust to phrasing, so a focused
  one-question turn still lands. Better questions hit closer facts → it doubles as a
  fair signal of question quality.
- `LexicalDeveloper` keeps the original keyword router (no ML deps) for fast tests.

If nothing matches, a short in-persona non-answer keeps the conversation moving without
leaking info beyond the scenario.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass

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
        # Tolerate morphological suffixes so a focused single question still matches:
        # "false.positive"→"false positives", "accessib"→"accessibility",
        # "consent"→"consenting". Only for hints long enough that a prefix match is
        # unambiguous; short tokens (ai, ml) keep a strict boundary so "ai" can't
        # hit "aid"/"air".
        tail = r"[a-z]*" if len(h) >= 4 else r"\b"
        if re.search(r"\b" + esc + tail, qn):
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


# ---------------------------------------------------------------------------
# Shared developer "voice" + the unified fact pool both routers draw from
# ---------------------------------------------------------------------------

DEV_SIM_MODEL = os.environ.get("HERA_DEV_SIM_MODEL", "BAAI/bge-small-en-v1.5")
# Calibrated on bge-small-en-v1.5: on-topic Q↔fact pairs score ~0.66-0.74, off-topic
# ~0.43-0.53. 0.60 sits in the gap → accepts real matches, rejects off-topic to fallback.
DEV_SIM_THRESHOLD = float(os.environ.get("HERA_DEV_SIM_THRESHOLD", "0.60"))

# Non-answers that move the conversation on WITHOUT replaying a prior answer or
# inviting a "what would good look like?" meta-loop.
PERSONA_FALLBACK = (
    "We haven't worked that out yet — let's set it aside and look at another "
    "risk area instead."
)
EXHAUSTED_NUDGE = (
    "I think we've covered the main points I can share. "
    "Want to pull this together into a summary of the key risks?"
)
NO_FACTS = "I'm not sure yet; let's discuss what would help."


@dataclass
class DevReply:
    """One simulated-developer turn. `matched` is False for non-answers (fallback /
    exhausted nudge) so the runner can detect a stalled conversation and wrap up."""

    text: str
    matched: bool
    fact_id: str | None = None


def _scenario_facts(scenario: dict) -> list[tuple[str, str]]:
    """Unified disclosed-fact pool: hand-written `simulated_answers` + bootstrapped
    `dev_facts`. Each entry is (stable_id, fact_text)."""
    facts: list[tuple[str, str]] = []
    for key, text in scenario.get("simulated_answers", {}).items():
        if text and text.strip():
            facts.append((f"sa:{key}", text.strip()))
    for i, f in enumerate(scenario.get("dev_facts", [])):
        text = (f.get("fact") or "").strip()
        if text:
            facts.append((f"df:{f.get('dimension', '?')}:{i}", text))
    return facts


def simulate_answer(
    scenario: dict,
    copilot_last_message: str,
    used_keys: set[str] | None = None,
) -> str:
    """Lexical keyword router over `simulated_answers` (no ML deps).

    `used_keys` (mutated in place when provided) records which probe categories the
    developer has already answered, so we never serve the same canned answer twice —
    a re-asked topic gets a move-on nudge instead of a replayed block. Kept as the
    fast, dependency-free path (tests / `runner --lexical-dev`); the default runner
    uses the embedding router `SemanticDeveloper` below.
    """
    answers: dict[str, str] = scenario.get("simulated_answers", {})
    if not answers:
        return NO_FACTS
    served = used_keys if used_keys is not None else set()
    candidates = set(answers) - served
    key = best_probe_key(copilot_last_message, candidates) if candidates else None
    if key is None:
        # All topics covered → steer toward a summary; else a neutral move-on.
        return EXHAUSTED_NUDGE if not candidates else PERSONA_FALLBACK
    if used_keys is not None:
        used_keys.add(key)
    return answers[key]


# ---------------------------------------------------------------------------
# Developer routers — one instance per eval run; reset() between scenarios
# ---------------------------------------------------------------------------


class LexicalDeveloper:
    """Keyword-routed developer (no ML deps). Deterministic; used for fast tests and
    `runner --lexical-dev`. Delegates to `simulate_answer` so the matching logic stays
    single-sourced."""

    name = "lexical"

    def __init__(self) -> None:
        self._used: set[str] = set()

    def reset(self) -> None:
        self._used = set()

    def answer(self, scenario: dict, question: str) -> DevReply:
        before = len(self._used)
        text = simulate_answer(scenario, question, self._used)
        return DevReply(text=text, matched=len(self._used) > before)


class SemanticDeveloper:
    """Embedding-routed developer. Embeds each scenario's disclosed-fact pool once and
    routes the copilot's question to the nearest UNUSED fact by cosine similarity.

    Deterministic (frozen bge weights, eval mode, argmax): the same question always
    yields the same fact, and the answer is identical across approaches whenever they
    ask semantically-equivalent questions. A sharper question lands a closer / still-fresh
    fact, so responsiveness doubles as a fair signal of question quality.
    """

    name = "semantic"

    def __init__(
        self,
        embedder=None,
        threshold: float = DEV_SIM_THRESHOLD,
        model_name: str = DEV_SIM_MODEL,
    ) -> None:
        self._embedder = embedder
        self._model_name = model_name
        self.threshold = threshold
        self._used: set[str] = set()
        self._cache: dict[str, tuple[list[str], list[str], object]] = {}

    def reset(self) -> None:
        self._used = set()

    def _get_embedder(self):
        if self._embedder is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:  # pragma: no cover - environment guard
                raise RuntimeError(
                    "SemanticDeveloper needs sentence-transformers — run the eval with "
                    "`--extra rag`, or pass `--lexical-dev`."
                ) from exc
            self._embedder = SentenceTransformer(self._model_name)
        return self._embedder

    def _embed(self, texts: list[str]):
        import numpy as np

        vecs = self._get_embedder().encode(list(texts), normalize_embeddings=True)
        return np.asarray(vecs, dtype="float32")

    def _facts(self, scenario: dict):
        sid = scenario.get("id")
        if not sid:
            raise ValueError(
                "SemanticDeveloper: scenario is missing 'id' — cannot cache embeddings "
                "safely (id-less scenarios would cross-contaminate the cache)."
            )
        if sid not in self._cache:
            pool = _scenario_facts(scenario)
            ids = [fid for fid, _ in pool]
            texts = [t for _, t in pool]
            mat = self._embed(texts) if texts else None
            self._cache[sid] = (ids, texts, mat)
        return self._cache[sid]

    def answer(self, scenario: dict, question: str) -> DevReply:
        import numpy as np

        ids, texts, mat = self._facts(scenario)
        if not ids:
            return DevReply(text=NO_FACTS, matched=False)
        avail = [i for i, fid in enumerate(ids) if fid not in self._used]
        if not avail:
            return DevReply(text=EXHAUSTED_NUDGE, matched=False)
        qv = self._embed([question])[0]
        sims = mat[avail] @ qv
        best = int(np.argmax(sims))
        if float(sims[best]) < self.threshold:
            return DevReply(text=PERSONA_FALLBACK, matched=False)
        gi = avail[best]
        self._used.add(ids[gi])
        return DevReply(text=texts[gi], matched=True, fact_id=ids[gi])


def build_developer(semantic: bool = True):
    """Factory used by the runner. Semantic by default; lexical for `--lexical-dev`."""
    return SemanticDeveloper() if semantic else LexicalDeveloper()
