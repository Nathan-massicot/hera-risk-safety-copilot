---
id: pms_lifecycle
title: "Post-Market Surveillance & lifecycle"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02017R0745-20230320
key_articles: ["MDR Art. 83-86", "AI Act Art. 72"]
status: rich-draft
---

# Post-Market Surveillance & lifecycle

## Why this concerns you (purpose)
CE marking is the start of your obligations, not the end. Once your SaMD is on the
market, the MDR requires you to **actively watch how it performs in the real world**,
feed problems back into your design, and report serious incidents. For software used
over the long term — and especially AI-driven software — this proactive
**post-market surveillance (PMS)** loop is where most ongoing compliance effort
lives, and it stacks an **AI Act** layer and a **separate Swiss** layer on top.

## When it is triggered (scope)
Triggered whenever your device/SaMD is **placed on the EU market and used over
time** (the long-term-use path). PMS scales with risk class. If the software uses
**high-risk AI**, AI Act post-market monitoring stacks on top ([[ai_act_high_risk]]).
If you are also on the **Swiss** market, a **distinct Swissmedic vigilance** regime
applies in parallel — Switzerland is a third country, so reporting does **not** flow
through EUDAMED ([[swiss_stack]]).

## Concrete obligations
- Maintain a **PMS system** proportionate to the device (MDR **Art. 83**) and a
  documented **PMS Plan** in the technical documentation (**Art. 84**, Annex III).
- **Class I**: keep a **PMS report** up to date (**Art. 85**). **Class IIa/IIb/III**:
  produce and update a **Periodic Safety Update Report (PSUR)** (**Art. 86**),
  summarising PMS data, benefit-risk conclusions and corrective actions.
- Run **post-market clinical follow-up (PMCF)** and feed it back into the clinical
  evaluation report ([[clinical_eval_mdsw]]).
- For **high-risk AI**, operate **AI Act Art. 72** post-market monitoring (collect
  and analyse performance data across the lifecycle), aligned where possible with
  the MDR PMS so you run one integrated system.
- **Switzerland**: report serious incidents to Swissmedic using the **Manufacturer
  Incident Report (MIR)** form — **MIR version 7.3.1 is mandatory from 1 May 2026**.

## Checklist
- [ ] Maintain a PMS Plan (Art. 84) and the matching PMS report or PSUR for your class.
- [ ] Define data sources, indicators and thresholds; run periodic benefit-risk review.
- [ ] Wire PMCF outputs back into the clinical evaluation report.
- [ ] If high-risk AI, integrate AI Act Art. 72 monitoring into the same loop.
- [ ] For the Swiss market, adopt the MIR 7.3.1 form for incident reports from 1 May 2026.

## Examples (mHealth)
- A Class IIa sleep-apnoea screening app -> PMS Plan + PSUR, with PMCF tracking
  real-world sensitivity/specificity drift ([[mdr_class_iia]]).
- An AI symptom-checker classified high-risk -> one integrated MDR + AI Act Art. 72
  monitoring loop watching for model performance degradation.
- A Class I wellness-adjacent logging app placed on the EU market -> still owes an
  Art. 85 PMS report; "low risk" does **not** mean "no PMS".

## HERA dimensions touched
- **Post-market surveillance & vigilance** · **AI lifecycle monitoring** · **Swiss vigilance**
- Cross-links: [[mdr_class_iia]] (PSUR by class), [[swiss_stack]] (Swissmedic MIR 7.3.1), [[clinical_eval_mdsw]] (PMCF loop), [[ai_act_high_risk]] (Art. 72)

## Official sources
- EUR-Lex — MDR (Regulation (EU) 2017/745), Art. 83-86: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02017R0745-20230320
- Swissmedic — Reporting incidents (MIR 7.3.1 mandatory from 1 May 2026): https://www.swissmedic.ch/swissmedic/en/home/medical-devices/reporting-incidents---fscas/hersteller---inverkehrbringer.html
