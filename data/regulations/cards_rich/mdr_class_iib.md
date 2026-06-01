---
id: mdr_class_iib
title: "SaMD Class IIb (MDR)"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02017R0745-20230320
key_articles: ["Annex VIII Rule 11", "Art. 52"]
status: rich-draft
---

# SaMD Class IIb (MDR)

## Why this concerns you (purpose)
Class IIb is for software whose erroneous output could cause **serious harm to health**.
Compared with [[mdr_class_iia]], the regime intensifies in two ways: the **clinical
evidence bar rises** and the **Notified Body looks at your technical documentation more
deeply and more often** (not just a representative sample). This is the class where
clinical and regulatory effort starts to dominate the project budget, so getting the
Rule 11 reasoning right — IIa vs IIb vs [[mdr_class_iii]] — is decisive.

## When it is triggered (scope)
Triggered when, under **Rule 11 / MDCG 2019-11**:
- the software provides information used for **diagnostic or therapeutic decisions** and
  an error could cause a **serious deterioration of health** or require **surgical
  intervention** (Rule 11(a) → IIb); **or**
- the software is intended to **monitor vital physiological parameters** where a
  variation could result in **immediate danger** (Rule 11(b) → IIb).

A worse outcome (death / irreversible deterioration) → [[mdr_class_iii]]; only moderate
consequence → [[mdr_class_iia]]. Specimen analysis → [[ivdr_class]].

## Concrete obligations
- **Notified Body conformity assessment** (Art. 52): Annex IX QMS audit **plus
  assessment of technical documentation**; for IIb the NB scrutiny is broader and at
  least one technical-documentation surveillance assessment occurs **annually** for
  implantable IIb (and proportionately for high-risk software).
- **In-depth clinical evaluation** with stronger clinical data; **PSUR updated at least
  annually** and reviewed by the NB ([[clinical_eval_mdsw]], [[pms_lifecycle]]).
- For **active IIb devices intended to administer/remove a medicinal product**, the NB
  must obtain an **expert-panel scientific opinion** on the clinical evaluation — note
  the overlap with drug-companion logic in [[combination_product]].
- Full QMS + GSPR via [[samd_standards]]; UDI + EUDAMED ([[udi_eudamed]]).
- Reinforced **post-market surveillance and PMCF** ([[pms_lifecycle]]).

## Checklist
- [ ] Document why the worst-case harm is "serious" (IIb) and not "irreversible/fatal" (III).
- [ ] Secure NB capacity and budget for per-device technical-documentation review.
- [ ] Strengthen the clinical evaluation; plan annual PSUR + PMCF.
- [ ] Check whether medicinal-product administration triggers the expert-panel route.
- [ ] Maintain ISO 13485 QMS and complete EUDAMED/UDI before market entry.

## Examples (mHealth)
- A **closed-loop dosing / titration** app where a wrong recommendation could cause
  serious (but recoverable) deterioration → Rule 11(a) serious harm → Class IIb.
- An app providing **alarms on a vital parameter** (e.g. apnoea/arrhythmia alerting)
  where missing an event poses immediate danger → Rule 11(b) → IIb.
- **Edge/negative:** the *same* closed-loop app, if a dosing error could cause **death
  or irreversible** harm, is **not** IIb — Rule 11 escalates it to [[mdr_class_iii]],
  triggering a clinical investigation and design-dossier examination.

## HERA dimensions touched
- **Device qualification & class** · **Deep Notified Body scrutiny** · **Strengthened clinical evidence** · **EU market access**
- Cross-links: [[mdr_class_i]] · [[mdr_class_iia]] · [[mdr_class_iii]] · [[ivdr_class]] ·
  [[samd_standards]] · [[clinical_eval_mdsw]] · [[pms_lifecycle]] · [[udi_eudamed]] · [[combination_product]]

## Official sources
- MDR (consolidated 2017/745) — Annex VIII Rule 11, Art. 52, Annex IX: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02017R0745-20230320
- MDCG 2019-11 rev.1 (June 2025) — qualification & classification of MDSW: https://health.ec.europa.eu/latest-updates/update-mdcg-2019-11-rev1-qualification-and-classification-software-regulation-eu-2017745-and-2025-06-17_en
