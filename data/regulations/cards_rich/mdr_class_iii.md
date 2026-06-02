---
id: mdr_class_iii
title: "SaMD Class III (MDR)"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02017R0745-20230320
key_articles: ["Annex VIII Rule 11", "Art. 52(3)"]
status: final
---

# SaMD Class III (MDR)

## Why this concerns you (purpose)
Class III is the **strictest MDR regime**. Software lands here under Rule 11 when an
erroneous output could cause **death or an irreversible deterioration** of a person's
state of health. Compared with [[mdr_class_iib]], two things change qualitatively: a
**clinical investigation is in principle compulsory** (not just a literature-based
evaluation), and the **Notified Body examines the full design dossier per device** with
annual surveillance. This is rare for pure mHealth, but it is exactly where the most
aggressive AI-driven diagnostic/therapeutic apps can fall — plan for years, not months.

## When it is triggered (scope)
Triggered when, under **Rule 11(a) / MDCG 2019-11**, the software provides information
used to take **diagnostic or therapeutic decisions** and an error **may cause death or
an irreversible deterioration** of health. (Rule 11 routes the highest-consequence
decision-support software to Class III.)

If the worst case is "serious but recoverable" → [[mdr_class_iib]]; "moderate" →
[[mdr_class_iia]]. Specimen analysis → [[ivdr_class]] (its Class D is the IVDR analogue
of highest risk).

## Concrete obligations
- **Notified Body conformity assessment** (Art. 52(3)): **Annex IX QMS + full
  assessment of the technical/design documentation for each device** (or Annex X
  type-examination + Annex XI). The NB issues the certificate and conducts **annual**
  surveillance audits.
- **Clinical investigation** generally required (MDR Annex XV, EN ISO 14155), feeding a
  high-evidence **clinical evaluation** ([[clinical_eval_mdsw]]).
- **Clinical evaluation consultation procedure (CECP)**: for certain Class III devices
  the NB must seek a **scientific opinion from an MDCG expert panel** before certifying.
- **Annual PSUR** reviewed by the NB; intensive **PMS + PMCF** ([[pms_lifecycle]]).
- Full QMS + GSPR via [[samd_standards]]; UDI + EUDAMED ([[udi_eudamed]]).

## Checklist
- [ ] Confirm the Rule 11 worst-case really is death/irreversible harm (vs IIb serious harm).
- [ ] Budget and design a clinical investigation (EN ISO 14155) early.
- [ ] Anticipate the expert-panel scrutiny (CECP) timeline in your NB plan.
- [ ] Prepare a full design dossier for per-device NB examination.
- [ ] Lock annual PSUR + PMCF and EUDAMED/UDI registration before market entry.

## Examples (mHealth)
- An **autonomous AI** that issues a treatment/triage decision for a life-threatening
  condition where an error is non-recoverable → Rule 11(a) highest consequence → Class III.
- Software **controlling a life-sustaining therapy** (e.g. an algorithm that directly
  drives a critical infusion regimen) → Class III.
- **Edge/negative:** a clinician **decision-support** tool that only *recommends* and is
  always overridden by a doctor who makes the final call may be argued **down** to
  [[mdr_class_iib]] or [[mdr_class_iia]] — the level of human control and the immediacy
  of harm change the Rule 11 outcome.

## HERA dimensions touched
- **Device qualification & class** · **Clinical investigation** · **Full design-dossier review + annual audit** · **EU market access**
- Cross-links: [[mdr_class_i]] · [[mdr_class_iia]] · [[mdr_class_iib]] · [[ivdr_class]] ·
  [[samd_standards]] · [[clinical_eval_mdsw]] · [[pms_lifecycle]] · [[udi_eudamed]] · [[ai_act_high_risk]]

## Official sources
- MDR (consolidated 2017/745) — Annex VIII Rule 11, Art. 52(3), Annexes IX/X/XV: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02017R0745-20230320
- MDCG 2019-11 rev.1 (June 2025) — qualification & classification of MDSW: https://health.ec.europa.eu/latest-updates/update-mdcg-2019-11-rev1-qualification-and-classification-software-regulation-eu-2017745-and-2025-06-17_en
