---
id: ai_act_gpai_provider
title: "EU AI Act — GPAI model provider (Art. 53/55)"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng
key_articles: ["Art. 53", "Art. 55", "Annex XI", "Annex XII"]
status: rich-draft
---

# EU AI Act — GPAI model provider (Art. 53/55)

## Why this concerns you (purpose)
Most mHealth teams assume they are only *users* of an LLM. But the moment you
**fine-tune a model substantially**, you can **become the provider of a new GPAI
model** — inheriting Art. 53 documentation, copyright and training-data duties, and,
above a compute threshold, the systemic-risk regime of Art. 55. This is a status you
can trigger by accident, so the boundary matters. The opposite, lighter case is the
sibling card [[ai_act_gpai_downstream]].

## When it is triggered (scope)
You become a **GPAI model provider** if you **place a general-purpose model on the EU
market**, including by **fine-tuning an existing model beyond an indicative ~1/3 of
the original training compute** (Commission GPAI guidelines, 18 Jul 2025; where the
original compute is unknown, the indicative reference is 1/3 of 10^23 FLOP). Below
that line you remain a downstream integrator ([[ai_act_gpai_downstream]]).
**Systemic risk** (Art. 55) is presumed above an indicative **10^25 FLOP** of total
training compute.

## Concrete obligations
- **Art. 53 (all GPAI providers):** maintain **technical documentation** (Annex XI),
  provide **downstream documentation** to integrators (Annex XII), put in place a
  **copyright policy**, and publish a **sufficiently detailed public summary of the
  training data**.
- **Art. 55 (systemic-risk models only):** model evaluation / adversarial testing,
  systemic-risk assessment and mitigation, serious-incident tracking and reporting,
  and adequate cybersecurity.
- **Timing & tooling:** GPAI obligations apply since **2 Aug 2025**; the **GPAI Code
  of Practice** (published **10 Jul 2025**) is the practical compliance route.

## Checklist
- [ ] Measure your fine-tuning compute against ~1/3 of the base model's training compute.
- [ ] If over the line, prepare Annex XI technical docs and Annex XII downstream docs.
- [ ] Draft a copyright policy and a public training-data summary.
- [ ] Check whether total training compute approaches 10^25 FLOP (systemic risk, Art. 55).
- [ ] Adopt the GPAI Code of Practice as your compliance baseline.

## Examples (mHealth)
- A startup heavily fine-tunes an open-weight model on a large clinical corpus, exceeding
  ~1/3 of original compute, and ships it: it is now a GPAI provider under Art. 53.
- A vendor pre-trains its own medical LLM from scratch and exposes it via API: clearly a
  provider; if training compute nears 10^25 FLOP, Art. 55 systemic-risk duties attach.
- **Edge / negative case:** light instruction-tuning well under the 1/3 threshold does
  **not** make you a provider — you stay downstream ([[ai_act_gpai_downstream]]).

## HERA dimensions touched
- **AI governance** · **Model development & supply chain** · **Copyright / training-data transparency**
- Cross-links: [[ai_act_gpai_downstream]], [[ai_act_high_risk]], [[ai_act_timeline]], [[ai_act_transparency]]

## Official sources
- EUR-Lex — Regulation (EU) 2024/1689, Art. 53 & 55: https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng
- European Commission — GPAI provider guidelines & Code of Practice: https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers
