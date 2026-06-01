"""Thin wrapper around the Ollama HTTP API + HERA system-prompt builder.

Reuses the prompt-construction logic from `src/baseline/copilot.py` so the web
chatbot stays in sync with the Gradio prototype.
"""

from __future__ import annotations

import json
from functools import lru_cache

import requests

from .config import TAXONOMY_PATH, settings


@lru_cache(maxsize=1)
def load_taxonomy() -> dict:
    with open(TAXONOMY_PATH, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def build_system_prompt() -> str:
    taxonomy = load_taxonomy()

    pillar_summaries = []
    for pillar in taxonomy["pillars"]:
        dims = ", ".join(d["name"] for d in pillar["dimensions"])
        pillar_summaries.append(
            f"**{pillar['id']} — {pillar['name']}** ({pillar['focus']}): {dims}"
        )
    pillars_text = "\n".join(pillar_summaries)

    questions_ref = []
    for pillar in taxonomy["pillars"]:
        for dim in pillar["dimensions"]:
            qs = "; ".join(dim["reflection_questions"][:2])
            questions_ref.append(f"[{dim['id']}] {dim['name']}: {qs}")
    questions_text = "\n".join(questions_ref)

    return f"""You are the HERA Risk & Safety Copilot, an expert assistant that helps mHealth app developers identify ethical and regulatory risks.

## Your Knowledge Base: HERA Taxonomy
HERA (Health Ethical & Regulatory Assessment) is a structured taxonomy with 7 pillars and 37 dimensions, covering ALL mHealth apps (with or without AI).

### Pillars
{pillars_text}

### Reflection Questions Reference
{questions_text}

## Your Conversation Protocol
1. FIRST: Understand the app. Ask clarifying questions about: app type, purpose, target users, data collected, technology used, deployment markets.
2. THEN: Systematically explore relevant HERA pillars. For each relevant dimension:
   - Ask a specific, targeted reflection question (not generic)
   - Listen to the developer's answer
   - If a risk is identified: name it clearly, explain why it matters, suggest a concrete mitigation
   - If the answer is satisfactory: acknowledge it and move on
3. PRIORITIZE: Start with the highest-risk dimensions for this specific app type.
4. BE SPECIFIC: Reference the exact HERA dimension ID (e.g., [P1.D3]) when discussing risks.
5. AT THE END: When the developer says they're done or you've covered the key dimensions, produce a structured risk report.

## Your Tone
- Professional but approachable — you're a helpful colleague, not an auditor
- Be direct about risks — don't sugarcoat safety issues
- Acknowledge good practices when you see them
- Use concrete examples relevant to their specific app

## Important Rules
- Every pillar can apply to non-AI apps. A medication reminder has autonomy, privacy, and reliability risks without any AI.
- Always cite regulatory frameworks when relevant (GDPR, MDR, EU AI Act, ISO 82304-2).
- If the app might be a Software as a Medical Device (SaMD), flag this early — it changes everything.
- Don't ask more than 1-2 questions per message. Keep the conversation flowing naturally."""


def system_prompt_with_profile(profile_dict: dict | None) -> str:
    base = build_system_prompt()
    if not profile_dict:
        return base
    profile_block = (
        "\n\n## App Under Review (provided during onboarding)\n"
        f"- **Name**: {profile_dict.get('app_name', 'n/a')}\n"
        f"- **Type**: {profile_dict.get('app_type', 'n/a')}\n"
        f"- **Purpose**: {profile_dict.get('app_purpose', 'n/a')}\n"
        f"- **Target users**: {profile_dict.get('target_users', 'n/a')}\n"
        f"- **Data collected**: {profile_dict.get('data_collected', 'n/a')}\n"
        f"- **Technology**: {profile_dict.get('technology', 'n/a')}\n"
        f"- **Uses AI**: {'yes' if profile_dict.get('has_ai') else 'no'}\n"
        f"- **Deployment markets**: {profile_dict.get('deployment_markets', 'n/a')}\n"
        f"- **Notes**: {profile_dict.get('extra_notes', '')}\n"
        "\nUse this context to skip basic questions and dive into the most relevant HERA pillars."
    )
    return base + profile_block


# ---------------------------------------------------------------------------
# Ollama HTTP calls
# ---------------------------------------------------------------------------

def check_ollama() -> tuple[bool, str]:
    try:
        r = requests.get(f"{settings.ollama_url}/api/tags", timeout=5)
        if r.status_code != 200:
            return False, f"Ollama returned status {r.status_code}"
        models = [m["name"] for m in r.json().get("models", [])]
        if any(settings.ollama_model.split(":")[0] in m for m in models):
            return True, f"Connected to Ollama. Model: {settings.ollama_model}"
        available = ", ".join(models[:5]) if models else "none"
        return False, (
            f"Ollama is running but model '{settings.ollama_model}' not found. "
            f"Available: {available}. Run: ollama pull {settings.ollama_model}"
        )
    except requests.ConnectionError:
        return False, "Cannot connect to Ollama. Run: ollama serve"


def chat(messages: list[dict], temperature: float = 0.7, max_tokens: int = 1024) -> str:
    payload = {
        "model": settings.ollama_model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature, "num_predict": max_tokens},
    }
    try:
        r = requests.post(
            f"{settings.ollama_url}/api/chat",
            json=payload,
            timeout=settings.ollama_timeout_seconds,
        )
        r.raise_for_status()
        return r.json()["message"]["content"]
    except requests.ConnectionError as exc:
        raise RuntimeError("Cannot connect to Ollama. Is it running? (ollama serve)") from exc
    except requests.Timeout as exc:
        raise RuntimeError("Ollama request timed out. The model may still be loading.") from exc
