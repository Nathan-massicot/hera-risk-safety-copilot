---
id: ai_act_high_risk
title: "EU AI Act — high-risk AI (Annex III §1(a))"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202401689
key_articles: ["Art. 6(1)", "Annex III §1(a)", "Art. 9-15", "Art. 43(3)", "MDCG 2025-6"]
status: rich-draft
---

# EU AI Act — high-risk AI (Annex III §1(a))

## Why this concerns you (purpose)
If your AI drives a clinical decision, the AI Act may treat it as **high-risk** — the
heaviest tier short of prohibition. That means a full management system: risk
controls, data governance, technical documentation, logging, human oversight and
robustness (Art. 9-15). The good news for medical-device makers is that this can be
**folded into your existing MDR conformity assessment** rather than run as a parallel
track. The trap is misjudging whether you are in scope at all — the nuance below
decides whether you face Art. 9-15 or merely transparency.

## When it is triggered (scope)
Under **Art. 6(1)** + **Annex III §1(a)**, an AI system is high-risk when it is a
**safety component of, or itself, a medical device** AND that device is subject to
**third-party conformity assessment** by a Notified Body under the MDR/IVDR.
Per **MDCG 2025-6** (published 19 Jun 2025):
- a **self-certified Class I SaMD is NOT high-risk AI** (no Notified Body involved);
- AI in Class IIa/IIb/III devices (see [[mdr_class_iib]]), which *do* need a Notified
  Body, **is** high-risk;
- AI-as-high-risk does **not** raise the device's MDR risk class — the two
  classifications are independent.
Applicable dates: see [[ai_act_timeline]] (high-risk obligations may shift to
2 Aug 2028 for embedded medical-device AI if the Digital Omnibus is adopted).

## Concrete obligations
- **Art. 9** risk-management system across the lifecycle; **Art. 10** data and
  data-governance quality for training/validation/testing sets.
- **Art. 11** technical documentation; **Art. 12** automatic event logging.
- **Art. 13** transparency and instructions for use to deployers; **Art. 14**
  effective **human oversight**; **Art. 15** accuracy, robustness and cybersecurity.
- **Art. 43(3) integrated conformity assessment:** the AI assessment is carried out
  **within** the MDR/IVDR procedure — ideally by a single Notified Body designated
  under both regimes, avoiding a duplicate audit.

## Checklist
- [ ] Determine if a Notified Body is involved (Class IIa+): if yes, treat the AI as high-risk.
- [ ] Stand up the Art. 9 risk-management and Art. 10 data-governance documentation.
- [ ] Design genuine human-oversight controls (Art. 14), not a rubber-stamp "review" button.
- [ ] Coordinate one integrated MDR + AI Act conformity assessment (Art. 43(3)).
- [ ] Map Art. 9-15 evidence onto your existing MDR technical file to avoid duplication.

## Examples (mHealth)
- An AI triage tool recommending emergency vs routine care in a Class IIb SaMD is
  high-risk: full Art. 9-15 plus integrated MDR assessment.
- A diabetes app whose AI titrates insulin dosing (Notified-Body class) is high-risk AI.
- **Edge / negative case:** a self-certified **Class I** symptom-logging SaMD with a
  simple ML feature is **not** high-risk AI per MDCG 2025-6 — only [[ai_act_transparency]] applies.

## HERA dimensions touched
- **AI governance** · **Medical-device conformity** · **Clinical safety & human oversight**
- Cross-links: [[mdr_class_iib]], [[ai_act_timeline]], [[ai_act_transparency]], [[pms_lifecycle]]

## Official sources
- EUR-Lex — AI Act, Art. 6 & Annex III (OJ L of 12 Jul 2024): https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202401689
- MDCG 2025-6 — interplay of MDR/IVDR and the AI Act: https://health.ec.europa.eu/document/download/b78a17d7-e3cd-4943-851d-e02a2f22bbb4_en?filename=mdcg_2025-6_en.pdf
