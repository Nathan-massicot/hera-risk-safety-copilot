"""Synthesize the HERA Copilot fine-tune training set with Claude.

Reads:
- data/training/archetypes.json    35 mHealth app descriptions
- data/taxonomy/hera_taxonomy.json  HERA pillars + dimensions

For each (archetype, randomly-sampled dimension subset) pair, calls the
Anthropic API to produce ONE multi-turn dialogue between a developer (user)
and the HERA Copilot (assistant). Output is OpenAI messages JSONL.

Usage:
    cp .env.example .env  # then set ANTHROPIC_API_KEY
    uv sync --extra datagen
    uv run python scripts/build_training_set.py \\
        --n-per-archetype 8 \\
        --model claude-sonnet-4-6 \\
        --out data/training/conversations.jsonl

A dry run that prints the prompt without calling the API:
    uv run python scripts/build_training_set.py --dry-run --n-per-archetype 1
"""

from __future__ import annotations

import argparse
import json
import logging
import random
import re
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.utils.logging_config import (  # noqa: E402
    JsonlSink,
    configure_logging,
    load_dotenv,
    new_run_dir,
)

log = logging.getLogger("datagen")

ARCHETYPES_PATH = REPO_ROOT / "data/training/archetypes.json"
TAXONOMY_PATH = REPO_ROOT / "data/taxonomy/hera_taxonomy.json"
DEFAULT_OUT = REPO_ROOT / "data/training/conversations.jsonl"

DEFAULT_MODEL = "claude-sonnet-4-6"


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------

EXAMPLE_SCHEMA = {
    "type": "object",
    "required": ["messages", "metadata"],
    "properties": {
        "messages": {
            "type": "array",
            "minItems": 4,
            "items": {
                "type": "object",
                "required": ["role", "content"],
                "properties": {
                    "role": {"enum": ["system", "user", "assistant"]},
                    "content": {"type": "string", "minLength": 1},
                },
            },
        },
        "metadata": {
            "type": "object",
            "required": ["archetype_id", "covered_dimensions", "source"],
            "properties": {
                "archetype_id": {"type": "string"},
                "covered_dimensions": {"type": "array", "items": {"type": "string"}},
                "source": {"enum": ["synthetic", "synthetic-claude-ai", "manual"]},
                "model": {"type": "string"},
                "seed": {"type": "integer"},
            },
        },
    },
}


def validate_example(example: dict) -> tuple[bool, str]:
    from jsonschema import Draft202012Validator

    errors = sorted(Draft202012Validator(EXAMPLE_SCHEMA).iter_errors(example), key=str)
    if errors:
        return False, "; ".join(e.message for e in errors[:3])
    roles = [m["role"] for m in example["messages"]]
    if roles[0] != "system":
        return False, "first message must be system"
    if "user" not in roles or "assistant" not in roles:
        return False, "dialogue must contain at least one user and one assistant turn"
    if roles.count("assistant") < 2:
        return False, "dialogue too short (<2 assistant turns)"
    return True, "ok"


# ---------------------------------------------------------------------------
# Dimension sampling per archetype
# ---------------------------------------------------------------------------

# Heuristic mapping from archetype tags to HERA pillars that are MOST relevant.
# The generator still gets the full taxonomy; this just biases the sampling
# so dialogues stay realistic for the app type.
PILLAR_PRIORS = {
    "wellness": [2, 3, 4, 7],
    "self-report": [1, 2, 4, 5],
    "chronic-condition": [1, 2, 3, 4, 7],
    "monitoring": [1, 2, 4, 5, 7],
    "imaging": [1, 2, 4, 5, 7],
    "mental-health": [1, 2, 3, 6, 7],
    "reproductive": [1, 2, 3, 6, 7],
    "adherence": [1, 3, 4, 7],
    "oncology": [1, 2, 3, 4, 7],
    "telemedicine": [1, 2, 3, 4, 7],
    "ai-clinical": [1, 2, 5, 6, 7],
    "preventive": [1, 4, 6, 7],
    "rehabilitation": [1, 2, 3, 4],
}


def sample_dimensions(
    taxonomy: dict,
    archetype: dict,
    n_min: int = 4,
    n_max: int = 7,
    rng: random.Random | None = None,
) -> list[dict]:
    """Pick a subset of dimensions weighted toward the archetype's category."""
    rng = rng or random.Random()
    priors = PILLAR_PRIORS.get(archetype["category"], list(range(1, 8)))
    pool: list[dict] = []
    for pillar in taxonomy["pillars"]:
        # Extract integer pillar number (e.g., "P1" -> 1)
        m = re.match(r"P(\d+)", pillar["id"])
        if not m:
            continue
        pn = int(m.group(1))
        weight = 3 if pn in priors else 1
        for dim in pillar["dimensions"]:
            pool.extend([dim] * weight)
    n = rng.randint(n_min, n_max)
    seen: set[str] = set()
    sample: list[dict] = []
    rng.shuffle(pool)
    for dim in pool:
        if dim["id"] in seen:
            continue
        seen.add(dim["id"])
        sample.append(dim)
        if len(sample) >= n:
            break
    return sample


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

GENERATOR_SYSTEM = """You generate high-quality training data for the HERA Risk & Safety Copilot — a conversational AI that helps mHealth app developers identify ethical and regulatory risks via the HERA taxonomy (7 pillars, 38 dimensions).

You will produce a SINGLE multi-turn dialogue between:
- the USER: an mHealth app developer (concise, realistic, sometimes uncertain or defensive)
- the ASSISTANT: the HERA Copilot (asks targeted reflection questions, drills into specifics, surfaces risks, suggests concrete mitigations)

Output STRICTLY a single JSON object — no prose, no markdown fences, no commentary — with this shape:

{
  "messages": [
    {"role": "system",    "content": "<HERA system prompt — verbatim from input>"},
    {"role": "user",      "content": "<dev describes the app or answers a question>"},
    {"role": "assistant", "content": "<copilot asks 1-2 reflection questions referencing HERA dimension IDs like [P2.D3]>"},
    {"role": "user",      "content": "..."},
    ...
  ],
  "metadata": {
    "archetype_id": "<the archetype id you were given>",
    "covered_dimensions": ["P1.D2", "P2.D3", ...],
    "source": "synthetic"
  }
}

Quality requirements:
- 8 to 14 messages total (counting system + alternating turns)
- The assistant MUST cite specific HERA dimension IDs (e.g., [P1.D2]) when it raises risks
- The user's answers must stay in character and consistent with the archetype description
- Cover the dimensions provided in the input; you may also touch 1-2 adjacent dimensions if natural
- The final assistant turn should either: name a concrete mitigation, or summarize the risks identified so far
- Avoid generic advice; reference regulations (GDPR, MDR, EU AI Act, ISO 82304-2) when relevant
- Vary tone across examples: sometimes the dev is a junior PM, sometimes a senior engineer, sometimes defensive about scope creep
"""


def build_user_prompt(
    archetype: dict,
    dimensions: list[dict],
    system_prompt_for_dialogue: str,
) -> str:
    dim_block = "\n".join(
        f"- [{d['id']}] {d['name']}: {d.get('description', '').strip()[:160]}"
        for d in dimensions
    )
    return f"""ARCHETYPE
id: {archetype['id']}
name: {archetype['name']}
category: {archetype['category']}
uses_ai: {archetype['uses_ai']}
data_sensitivity: {archetype['data_sensitivity']}
vulnerable_population: {archetype['vulnerable_pop']}
target_markets: {', '.join(archetype['target_markets'])}
description: {archetype['description']}

DIMENSIONS TO COVER ({len(dimensions)})
{dim_block}

SYSTEM PROMPT TO EMBED (use verbatim as the first message)
<<<
{system_prompt_for_dialogue}
>>>

Now produce the JSON dialogue object."""


def build_dialogue_system_prompt(taxonomy: dict) -> str:
    """The system prompt that the FINE-TUNED model will see at inference time.
    Kept short — the model has the taxonomy internalised by training."""
    return (
        "You are the HERA Risk & Safety Copilot. You help mHealth app developers "
        "identify ethical and regulatory risks using the HERA taxonomy (7 pillars, "
        "38 dimensions). Ask targeted reflection questions one or two at a time, "
        "drill into specifics, surface concrete risks with their HERA dimension ID, "
        "and suggest actionable mitigations referencing relevant regulations "
        "(GDPR, MDR, EU AI Act, ISO 82304-2)."
    )


# ---------------------------------------------------------------------------
# Claude API call
# ---------------------------------------------------------------------------


def call_claude(
    client: Any,
    model: str,
    system: str,
    user: str,
    max_tokens: int = 4000,
    temperature: float = 1.0,
) -> str:
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text


JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


def extract_json(text: str) -> dict:
    """Robust JSON extraction — handles fenced and unfenced responses."""
    text = text.strip()
    m = JSON_FENCE_RE.search(text)
    if m:
        text = m.group(1)
    return json.loads(text)


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n-per-archetype", type=int, default=8,
                    help="Dialogues to generate per archetype (default: 8 → ~280 total)")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="Anthropic model id")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output JSONL path")
    ap.add_argument("--seed", type=int, default=1337, help="Seed for dimension sampling")
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--max-tokens", type=int, default=4000)
    ap.add_argument("--archetypes-limit", type=int, default=None,
                    help="Use only the first N archetypes (smoke-testing)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print one constructed prompt and exit (no API calls)")
    ap.add_argument("--resume", action="store_true",
                    help="Skip (archetype_id, idx) pairs already in --out")
    args = ap.parse_args(argv)

    run_dir = new_run_dir(prefix="datagen")
    configure_logging(run_dir)
    load_dotenv()

    rng = random.Random(args.seed)

    archetypes = json.loads(ARCHETYPES_PATH.read_text())
    if args.archetypes_limit:
        archetypes = archetypes[: args.archetypes_limit]
    taxonomy = json.loads(TAXONOMY_PATH.read_text())
    dialogue_system = build_dialogue_system_prompt(taxonomy)

    total_target = len(archetypes) * args.n_per_archetype
    log.info("Plan: %d archetypes × %d dialogues = %d examples target",
             len(archetypes), args.n_per_archetype, total_target)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    already: set[tuple[str, int]] = set()
    if args.resume and args.out.exists():
        for raw in args.out.read_text().splitlines():
            if not raw.strip():
                continue
            try:
                ex = json.loads(raw)
                meta = ex.get("metadata", {})
                already.add((meta.get("archetype_id"), meta.get("seed", 0)))
            except json.JSONDecodeError:
                continue
        log.info("Resume: %d examples already in output", len(already))

    if args.dry_run:
        a = archetypes[0]
        dims = sample_dimensions(taxonomy, a, rng=rng)
        prompt = build_user_prompt(a, dims, dialogue_system)
        print("=== SYSTEM ===")
        print(GENERATOR_SYSTEM)
        print("\n=== USER ===")
        print(prompt)
        return 0

    # Lazy import so --dry-run works without anthropic installed
    try:
        from anthropic import Anthropic
    except ImportError:
        log.error("anthropic package missing. Run: uv sync --extra datagen")
        return 2

    api_key = (REPO_ROOT / ".env").read_text() if (REPO_ROOT / ".env").exists() else ""
    import os
    if not os.environ.get("ANTHROPIC_API_KEY"):
        log.error("ANTHROPIC_API_KEY not set. Copy .env.example to .env and fill it.")
        return 2
    client = Anthropic()

    with (
        args.out.open("a", encoding="utf-8") as out_fh,
        JsonlSink(run_dir / "transcript.jsonl") as sink,
    ):
        kept = 0
        rejected = 0
        for a in archetypes:
            for i in range(args.n_per_archetype):
                ex_seed = args.seed * 1000 + hash(a["id"]) % 1000 + i
                if (a["id"], ex_seed) in already:
                    continue
                rng_local = random.Random(ex_seed)
                dims = sample_dimensions(taxonomy, a, rng=rng_local)
                user_prompt = build_user_prompt(a, dims, dialogue_system)
                t0 = time.time()
                try:
                    raw = call_claude(
                        client, args.model, GENERATOR_SYSTEM, user_prompt,
                        max_tokens=args.max_tokens, temperature=args.temperature,
                    )
                except Exception as exc:
                    log.warning("API error on %s#%d: %s", a["id"], i, exc)
                    sink.write({"event": "api_error", "archetype": a["id"], "i": i, "error": str(exc)})
                    time.sleep(2.0)
                    continue
                dt = time.time() - t0
                try:
                    example = extract_json(raw)
                except json.JSONDecodeError as exc:
                    log.warning("JSON parse failed on %s#%d: %s", a["id"], i, exc)
                    rejected += 1
                    sink.write({"event": "json_error", "archetype": a["id"], "i": i,
                                "raw_excerpt": raw[:300]})
                    continue
                example.setdefault("metadata", {})
                example["metadata"]["archetype_id"] = a["id"]
                example["metadata"]["source"] = "synthetic"
                example["metadata"]["model"] = args.model
                example["metadata"]["seed"] = ex_seed
                example["metadata"]["dimensions_requested"] = [d["id"] for d in dims]
                ok, msg = validate_example(example)
                if not ok:
                    log.warning("Schema fail on %s#%d: %s", a["id"], i, msg)
                    rejected += 1
                    sink.write({"event": "schema_error", "archetype": a["id"], "i": i, "error": msg})
                    continue
                out_fh.write(json.dumps(example, ensure_ascii=False) + "\n")
                out_fh.flush()
                kept += 1
                sink.write({"event": "ok", "archetype": a["id"], "i": i,
                            "elapsed_s": dt, "n_messages": len(example["messages"])})
                log.info("✓ %-22s %d/%d  kept=%d  rej=%d  %.1fs",
                         a["id"], i + 1, args.n_per_archetype, kept, rejected, dt)

    log.info("Done. kept=%d rejected=%d target=%d → %s",
             kept, rejected, total_target, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
