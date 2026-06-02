---
id: ivdr_class
title: "IVDR — in-vitro diagnostic software (Regulation (EU) 2017/746)"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32017R0746
key_articles: ["IVDR Art. 2(2)", "IVDR Annex VIII (rules 1-7)", "MDCG 2019-11", "MDCG 2020-16 rev.4"]
status: final
---

# IVDR — in-vitro diagnostic software (Regulation (EU) 2017/746)

## Why this concerns you (purpose)
If your app provides information **by analysing data derived from a specimen taken from
the human body** (blood, urine, tissue, genetic/DNA data, biomarkers), it is **not** an
MDR device — it is **IVD medical device software (IVD-MDSW)** under the IVDR, with its
**own classification rules A-D**. This is a hard fork: the wrong regulation means the
wrong classification, wrong conformity route and wrong clinical evidence. Many "lab
result" or "genetic insight" apps sit here, often surprised to learn that IVDR routes
**most software to a Notified Body** (only Class A is self-certified).

## When it is triggered (scope)
Triggered when:
- the software qualifies as a medical device **and** provides information based on the
  **in-vitro examination of specimens** (IVDR Art. 2(2)) — per **MDCG 2019-11** this is
  the MDR-vs-IVDR switch criterion;
- it is then classified **A / B / C / D** under the **seven classification rules of IVDR
  Annex VIII**, per **MDCG 2020-16 rev.4** (March 2025).

If the app interprets **other** clinical/physiological data (not from a specimen) → it is
MDR SaMD instead → [[mdr_class_iia]] / [[mdr_class_iib]] / [[mdr_class_iii]]. If there is
no medical purpose at all → [[iso_82304]].

## Concrete obligations
- **Classify under Annex VIII (rules 1-7):** Class **A** (low individual/public-health
  risk, e.g. general lab tools), **B** (default/residual), **C** (e.g. detection of
  sexually transmitted agents, genetic testing, cancer staging, companion diagnostics),
  **D** (highest: e.g. blood-screening / transmissible agents threatening life).
- **Conformity assessment by class:** Class **A is self-declared** (except A sterile);
  Classes **B, C, D require a Notified Body**; **Class D** adds **EU reference
  laboratory** batch verification and the most stringent scrutiny.
- Apply the **GSPR (IVDR Annex I)** via the [[samd_standards]] (IEC 62304, ISO 14971,
  IEC 62366-1, ISO 13485 QMS).
- **Performance evaluation** (scientific validity, analytical & clinical performance) —
  the IVDR analogue of the MDR clinical evaluation ([[clinical_eval_mdsw]]).
- UDI + EUDAMED registration ([[udi_eudamed]]); PMS + performance follow-up
  ([[pms_lifecycle]]).

## Checklist
- [ ] Confirm the input is genuinely a **specimen** → IVDR (not MDR).
- [ ] Run the Annex VIII rules 1-7 with MDCG 2020-16 rev.4 to fix the A/B/C/D class.
- [ ] If Class B/C/D, engage a Notified Body (Class D: factor in EU reference lab).
- [ ] Build the performance evaluation (validity + analytical + clinical performance).
- [ ] Register UDI + EUDAMED and set up PMS before placing on the market.

## Examples (mHealth)
- An app that **interprets a home blood-glucose or HbA1c value** to give a result →
  IVD-MDSW (typically Class C for diabetes management software).
- A consumer **genetic-risk app** parsing DNA sequencing data for disease predisposition
  → IVD-MDSW, commonly **Class C** (genetic testing rule).
- **Edge/negative:** a **meal-logging coaching** app that takes no specimen data, only
  self-reported food, is **not** IVDR — and if it merely tracks without clinical
  interpretation it may not even be a device (see [[iso_82304]]).

## HERA dimensions touched
- **Device qualification (IVDR vs MDR)** · **IVD class A-D** · **Performance evaluation** · **EU market access**
- Cross-links: [[mdr_class_iia]] · [[mdr_class_iib]] · [[mdr_class_iii]] · [[samd_standards]] ·
  [[clinical_eval_mdsw]] · [[pms_lifecycle]] · [[udi_eudamed]] · [[iso_82304]]

## Official sources
- IVDR (Regulation (EU) 2017/746) — Art. 2(2), Annex VIII: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32017R0746
- MDCG 2020-16 rev.4 (Mar 2025) — IVDR classification rules: https://health.ec.europa.eu/document/download/12f9756a-1e0d-4aed-9783-d948553f1705_en?filename=md_mdcg_2020_guidance_classification_ivd-md_en.pdf
- MDCG 2019-11 rev.1 (June 2025) — software qualification & classification: https://health.ec.europa.eu/latest-updates/update-mdcg-2019-11-rev1-qualification-and-classification-software-regulation-eu-2017745-and-2025-06-17_en
