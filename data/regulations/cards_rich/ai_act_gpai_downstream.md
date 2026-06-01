---
id: ai_act_gpai_downstream
title: "EU AI Act — integrator of a GPAI model (downstream obligations)"
jurisdiction: EU
official_url: https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai
key_articles: ["Art. 51-56", "Annex XII", "Art. 50", "Art. 8-15"]
status: rich-draft
---

# EU AI Act — integrator of a GPAI model (downstream obligations)

## Why this concerns you (purpose)
If your mHealth app simply **calls a third-party LLM** (GPT, Claude, Gemini, an
open-weight model) without retraining it, you are a **downstream integrator**, *not*
the GPAI provider — the model provider carries that status. But "not the provider"
does not mean "no obligations": you still depend on the provider's documentation, you
still owe Art. 50 transparency, and if the LLM feeds a clinical decision you inherit
the full high-risk regime. This card keeps the line clear so you do not accidentally
cross it (see the sibling card [[ai_act_gpai_provider]]).

## When it is triggered (scope)
Triggered when you **build on a general-purpose AI model you did not train**, and you
**do not** modify it beyond the threshold that would make you a provider. The dividing
line (Commission GPAI guidelines, 18 Jul 2025): you remain a downstream integrator as
long as any fine-tuning stays **below ~1/3 of the model's original training compute**.
Cross it and you become a provider — that is the [[ai_act_gpai_provider]] case.

## Concrete obligations
- **Rely on the provider's documentation:** the GPAI provider must give you the
  **Annex XII** downstream information; obtain and keep it to understand capabilities
  and limits for your medical use.
- **Art. 50 transparency:** disclose AI interaction and mark AI-generated content
  (see [[ai_act_transparency]]).
- **If the LLM feeds a high-risk system:** you must meet the relevant **Art. 8-15**
  obligations for that system (see [[ai_act_high_risk]]) — the GPAI layer does not
  exempt the high-risk layer.
- **Timing:** GPAI obligations apply since **2 Aug 2025**; the **GPAI Code of Practice**
  was published **10 Jul 2025** and helps providers (and indirectly you) demonstrate
  compliance.

## Checklist
- [ ] Confirm in writing that your LLM vendor is the GPAI provider and supplies Annex XII docs.
- [ ] Store the model documentation and assess its fitness/limits for your health use case.
- [ ] Apply Art. 50 disclosure and content-marking in the app.
- [ ] If the LLM informs clinical decisions, layer on the high-risk Art. 8-15 controls.
- [ ] Track whether any fine-tuning approaches the ~1/3 compute line (then re-read [[ai_act_gpai_provider]]).

## Examples (mHealth)
- A patient-FAQ assistant wrapping a hosted LLM via API: downstream integrator —
  Annex XII reliance + Art. 50 disclosure, no provider duties.
- A clinical-summary feature using an LLM whose output guides a Class IIb SaMD: still a
  downstream integrator for GPAI, but the high-risk Art. 8-15 regime also applies.
- **Edge case:** you "fine-tune" the LLM with a tiny domain prompt-set far below 1/3 of
  original compute — you stay downstream; only modest retraining does NOT flip you to provider.

## HERA dimensions touched
- **AI governance** · **Vendor / model-supply-chain management** · **Transparency**
- Cross-links: [[ai_act_gpai_provider]], [[ai_act_high_risk]], [[ai_act_transparency]], [[ai_act_timeline]]

## Official sources
- European Commission — GPAI Code of Practice: https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai
- European Commission — Guidelines for providers of general-purpose AI models: https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers
