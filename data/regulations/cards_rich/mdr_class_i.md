---
id: mdr_class_i
title: "SaMD Class I (MDR)"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02017R0745-20230320
key_articles: ["Annex VIII Rule 11", "Art. 52(7)"]
status: rich-draft
---

# SaMD Class I (MDR)

## Why this concerns you (purpose)
Your software has a **medical purpose** and qualifies as Software as a Medical Device
(SaMD), but it sits at the **lowest risk class** under MDR Rule 11. Class I is the only
SaMD class you can in principle **self-certify** — no Notified Body audits your file
before you sell. That is a real advantage, but it is also the **most fragile position**:
Rule 11 is written so that *almost everything that drives a clinical decision lands in
IIa or above*. Most apps that think they are Class I are actually [[mdr_class_iia]]. Use
this card to confirm you genuinely fall in Class I and to size the (still real) obligations.

## When it is triggered (scope)
Triggered when **all** of the following hold:
- the software provides information for a medical purpose (it is SaMD, not wellness —
  if not, fall back to [[iso_82304]]);
- under **Rule 11 (Annex VIII)** the information it provides is **not** used to take
  decisions with diagnosis or therapeutic purposes, and it does **not** monitor vital
  physiological processes/parameters;
- per **MDCG 2019-11**, it falls in the **Rule 11(c) residual bucket** ("all other MDSW"),
  which defaults to **Class I** — e.g. simple data display, storage, communication, or
  archiving without clinical interpretation.

If it influences diagnosis/therapy → [[mdr_class_iia]] or higher. If it analyses a
specimen → [[ivdr_class]] instead.

## Concrete obligations
- **Self-declaration of conformity** (Art. 52(7)): you draw up the EU Declaration of
  Conformity and affix the CE mark **without** a Notified Body — *except* if the device
  is Class I with a measuring function, sterile, or reusable surgical (rare for SaMD).
- Build the **technical documentation** (Annexes II & III) and keep it current.
- Apply the **General Safety & Performance Requirements** (Annex I) using the
  [[samd_standards]] (IEC 62304, ISO 14971, IEC 62366-1; a QMS per ISO 13485).
- Run a **clinical evaluation** proportionate to the low class ([[clinical_eval_mdsw]]).
- Register as an actor and the device → UDI + EUDAMED ([[udi_eudamed]]).
- Operate **post-market surveillance** and vigilance ([[pms_lifecycle]]).

## Checklist
- [ ] Re-run the Rule 11 / MDCG 2019-11 test: confirm you are truly Rule 11(c), not 11(a)/11(b).
- [ ] Confirm no measuring/sterile/reusable-surgical trigger (else a Notified Body is needed).
- [ ] Assemble the technical file (Annex II/III) before placing on the market.
- [ ] Register actor (SRN) + device in EUDAMED and assign UDI.
- [ ] Set up a PMS plan even at Class I (it is not optional).

## Examples (mHealth)
- A medication-reminder app that **only stores and displays** a clinician-set schedule,
  with no dosing logic → Rule 11(c), Class I.
- A secure messaging/archiving app moving clinical data between HCPs **without
  interpreting** it → Class I.
- **Edge/negative:** an app that flags "your glucose trend looks dangerous, see a doctor"
  *interprets* data to drive a decision → this is **not** Class I; Rule 11(a) pushes it
  to at least [[mdr_class_iia]] (or higher if serious harm is possible).

## HERA dimensions touched
- **Device qualification & class** · **Self-certification route** · **EU market access**
- Cross-links: [[mdr_class_iia]] · [[mdr_class_iib]] · [[mdr_class_iii]] · [[ivdr_class]] ·
  [[samd_standards]] · [[clinical_eval_mdsw]] · [[pms_lifecycle]] · [[udi_eudamed]] · [[iso_82304]]

## Official sources
- MDR (consolidated 2017/745) — Annex VIII Rule 11, Art. 52(7): https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02017R0745-20230320
- MDCG 2019-11 rev.1 (June 2025) — qualification & classification of MDSW: https://health.ec.europa.eu/latest-updates/update-mdcg-2019-11-rev1-qualification-and-classification-software-regulation-eu-2017745-and-2025-06-17_en
