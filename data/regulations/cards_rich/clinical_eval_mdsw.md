---
id: clinical_eval_mdsw
title: "Clinical evaluation of software (MDR Art. 61 / MDCG 2020-1)"
jurisdiction: EU
official_url: https://health.ec.europa.eu/system/files/2020-09/md_mdcg_2020_1_guidance_clinic_eva_md_software_en_0.pdf
key_articles: ["MDR Art. 61", "MDR Annex XIV", "MDR Annex XV", "MDCG 2020-1"]
status: rich-draft
---

# Clinical evaluation of software (MDR Art. 61 / MDCG 2020-1)

## Why this concerns you (purpose)
If your software is a classified medical device (SaMD), CE marking is not granted on
the basis that the code "works". You must show, with **clinical evidence**, that the
device actually delivers a **clinical benefit** and is **safe** for its intended
purpose. For software this is not a literature search bolted on at the end — MDCG
2020-1 lays out a **three-pillar model** that you must satisfy and keep current
throughout the product's life.

## When it is triggered (scope)
Triggered when your product is qualified as **medical device software** and
classified (>= MDR Class IIa, or an IVD-MDSW under the IVDR). A clinical evaluation
under **MDR Art. 61 + Annex XIV** is required for every such SaMD; the depth scales
with the risk class ([[mdr_class_iib]]). For **Class III and implantable** devices a
**clinical investigation** is the default route (Annex XV, **EN ISO 14155**). Pure
wellness software with no medical purpose is out of scope.

## Concrete obligations
- Build clinical evidence around the **three pillars** of MDCG 2020-1:
  1. **Valid clinical association / scientific validity** — the output is
     meaningfully linked to the targeted clinical condition or physiological state;
  2. **Technical / analytical performance** — the software correctly and reliably
     generates the intended output from the input data (verification & validation);
  3. **Clinical performance** — the output yields a clinically relevant, accurate and
     reliable result in the intended use, population and clinical setting.
- Document it in a **Clinical Evaluation Plan** and **Clinical Evaluation Report
  (CER)**, with state-of-the-art and benefit-risk analysis (Annex XIV Part A).
- For **Class III / implantable** SaMD, conduct a **clinical investigation** per
  Annex XV / EN ISO 14155 unless a documented exemption applies.
- **Keep it living**: update the CER from post-market clinical follow-up (PMCF)
  data over the lifecycle ([[pms_lifecycle]]).

## Checklist
- [ ] Confirm scientific validity (literature / state-of-the-art for the clinical claim).
- [ ] Verify and validate technical/analytical performance (algorithm correctness, data quality).
- [ ] Demonstrate clinical performance in the intended population and use setting.
- [ ] Write the Clinical Evaluation Plan and CER; link PMCF as a feedback loop.
- [ ] For Class III/implantable, plan a clinical investigation (Annex XV / EN ISO 14155).

## Examples (mHealth)
- A Class IIa app scoring melanoma risk from skin photos -> needs all three pillars:
  the score correlates with malignancy (validity), the model runs correctly on real
  images (analytical), and it performs in the target population (clinical).
- A Class IIb insulin-dosing decision-support SaMD -> deeper clinical performance
  evidence and a robust PMCF plan ([[mdr_class_iib]]).
- A meditation/relaxation app making **no medical claim** -> not a SaMD, so no MDR
  clinical evaluation is required (it sits under health-software quality standards
  instead).

## HERA dimensions touched
- **Clinical evidence** · **Conformity assessment** · **Lifecycle evidence**
- Cross-links: [[mdr_class_iib]] (depth by class), [[pms_lifecycle]] (PMCF keeps the CER live), [[samd_standards]] (V&V via IEC 62304)

## Official sources
- MDCG 2020-1 — Clinical/performance evaluation of medical device software: https://health.ec.europa.eu/system/files/2020-09/md_mdcg_2020_1_guidance_clinic_eva_md_software_en_0.pdf
- EUR-Lex — MDR (Regulation (EU) 2017/745), Art. 61 / Annex XIV-XV: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02017R0745-20230320
