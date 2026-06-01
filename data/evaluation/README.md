# HERA Copilot — Evaluation scenarios

This directory holds the gold-standard scenarios used to compare the 4 approaches
(prompt-only, fine-tuned, RAG, RLM).

## Files

- `scenarios.json` — 25 mHealth app scenarios with gold-standard expected
  dimensions, risks, mitigations, and regulations. Hand-authored.
- `scenarios.schema.json` — JSON schema each scenario must validate against.

## One scenario = one row in the comparison matrix

For each scenario, every approach receives:
1. The `app_description` as the first developer message.
2. Subsequent simulated developer answers drawn from `simulated_answers` based
   on which probe category the copilot's next question matches.

The runner then extracts the assistant's:
- Cited HERA dimensions (regex on `[Px.Dy]` tokens)
- Identified risks (one per assistant turn that contains "risk", "concern", "issue")
- Suggested mitigations

These are compared to `gold_standard.*` via the metrics in `src/evaluation/`.

## Schema overview

```json
{
  "id": "scenario_01",
  "app_description": "<dev's opening pitch — 3-5 sentences>",
  "app_metadata": {
    "category": "<chronic | mental-health | wellness | ai-clinical | ...>",
    "uses_ai": true,
    "data_sensitivity": "high",
    "vulnerable_pop": false,
    "target_markets": ["EU", "CH"]
  },
  "developer_persona": "Senior PM at a startup, defensive about scope.",
  "simulated_answers": {
    "data_collected": "...",
    "consent_flow": "...",
    "regulatory_status": "...",
    ...
  },
  "gold_standard": {
    "relevant_dimensions": ["P1.D1", "P2.D3", ...],
    "expected_risks": [
      {"dimension": "P2.D3", "risk": "...", "severity": "high"}
    ],
    "expected_mitigations": [
      {"dimension": "P2.D3", "mitigation": "..."}
    ],
    "expected_regulations_cited": ["GDPR Art. 9", "MDR 2017/745 Annex II"]
  },
  "notes": "Author notes — pitfalls, why this scenario is interesting."
}
```

## Coverage targets

The 25 scenarios cover:

- All 7 HERA pillars represented in `expected_risks` aggregate
- 14 mHealth categories spanning low-risk wellness → AI clinical
- Mix: 12 use_ai=true / 13 use_ai=false
- 11 vulnerable_population=true (mental health, paediatric, elderly)
- 18 EU + CH, 7 EU only — Swiss specifics (nLPD, MedDO, BAG) appear in 6 scenarios
