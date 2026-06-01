---
id: combination_product
title: "Combination products device + medicine (MDR Art. 1(8)/1(9), Art. 117)"
jurisdiction: EU
official_url: https://health.ec.europa.eu/system/files/2023-06/mdcg_2022-5_en.pdf
key_articles: ["MDR Art. 1(8)", "MDR Art. 1(9)", "MDR Art. 117", "MDCG 2022-5 rev.1", "Dir. 2001/83/EC"]
status: rich-draft
---

# Combination products device + medicine (MDR Art. 1(8)/1(9), Art. 117)

## Why this concerns you (purpose)
When your app or device sits next to a **medicinal product** — a companion app that
sets a dose or drives adherence, or a device that incorporates or administers a drug
— you are in **borderline territory** between two legal worlds: the MDR and the
medicines framework (Dir. 2001/83/EC). Getting the qualification wrong means filing
under the wrong regulator entirely. The deciding test is the **principal mode of
action**, and MDCG 2022-5 is the map.

## When it is triggered (scope)
Triggered when your product **combines a device function with a medicinal substance
or product**, e.g.:
- a device that **incorporates** a medicinal substance (Art. 1(8)); or
- a device **intended to administer** a medicinal product (Art. 1(9)); or
- a **drug-companion app** for dosing, titration or adherence tied to a specific
  medicine.

If the software simply records symptoms with no link to a medicine, this card does
not apply ([[clinical_eval_mdsw]]).

## Concrete obligations
- Determine the **principal mode of action** (PMOA) per MDCG 2022-5:
  - substance has an **ancillary** action to the device -> regulated as a **medical
    device under the MDR** (the substance is assessed within the device dossier);
  - substance has the **principal** action -> regulated as a **medicinal product**
    (Dir. 2001/83/EC), and the device component must still meet the relevant MDR
    Annex I General Safety and Performance Requirements (GSPR).
- Where a device is part of a medicinal product's marketing-authorisation dossier
  (e.g. a device administering the drug), obtain a **notified body opinion (NBOp)**
  on the device part under **MDR Art. 117** before/with the MA application.
- For a **drug-companion app**, decide whether it is a **standalone SaMD** (its own
  CE route + clinical evaluation) or **part of the medicine's labelling/MA** — and
  document the rationale.
- Consult the relevant **medicines authority** where the qualification is unclear.

## Checklist
- [ ] State the product's principal mode of action and the resulting regime (MDR vs medicine).
- [ ] If a device is in an MA dossier, secure the Art. 117 notified-body opinion.
- [ ] For a companion app, classify it as standalone SaMD or part of the MA, with justification.
- [ ] Ensure the device component meets MDR Annex I GSPR even under the medicines regime.
- [ ] Document the borderline analysis against MDCG 2022-5 rev.1.

## Examples (mHealth)
- An app that **calculates an insulin dose** specific to a branded insulin and is
  required for safe use of that medicine -> likely tied to the medicinal product's
  MA; assess under the medicines framework (with device GSPR for the app).
- A **standalone** dose-tracking app usable across many drugs, providing decision
  support -> qualifies as a SaMD under the MDR with its own clinical evaluation
  ([[clinical_eval_mdsw]]).
- A **simple pill-reminder** app with no dose calculation and no medical claim ->
  **not** a combination product and not a medical device at all.

## HERA dimensions touched
- **Product qualification (borderline)** · **Regulator routing** · **Conformity assessment**
- Cross-links: [[clinical_eval_mdsw]] (if it qualifies as standalone SaMD), [[mdr_class_iib]] (risk class if MDR), [[pms_lifecycle]] (post-market duties either way)

## Official sources
- MDCG 2022-5 rev.1 — Borderline between medical devices and medicinal products under MDR: https://health.ec.europa.eu/system/files/2023-06/mdcg_2022-5_en.pdf
- EUR-Lex — MDR (Regulation (EU) 2017/745), Art. 1(8)/1(9), Art. 117: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02017R0745-20230320
