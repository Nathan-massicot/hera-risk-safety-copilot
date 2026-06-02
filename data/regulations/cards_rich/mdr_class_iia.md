---
id: mdr_class_iia
title: "SaMD Class IIa (MDR)"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02017R0745-20230320
key_articles: ["Annex VIII Rule 11", "Art. 52"]
status: final
---

# SaMD Class IIa (MDR)

## Why this concerns you (purpose)
Class IIa is the **default landing zone for most clinical mHealth software**. Under
MDR Rule 11, *any* software that provides information used to take **diagnostic or
therapeutic decisions** is Class IIa unless the potential harm pushes it higher. The
practical leap from [[mdr_class_i]] is that you can **no longer self-certify**: a
**Notified Body** must assess your quality system (and a sample of your technical
documentation) before you may CE-mark. This card is the one to read carefully — most
teams that assumed "Class I" actually sit here.

## When it is triggered (scope)
Triggered when, under **Rule 11 / MDCG 2019-11**:
- the software provides information **used to take decisions with diagnosis or
  therapeutic purposes** (Rule 11(a)) and the worst plausible consequence of an error
  is **moderate** (not serious harm, not death/irreversible deterioration); **or**
- the software is intended to **monitor physiological processes/parameters** that are
  **not** vital (Rule 11(b) baseline).

If a wrong output could cause **serious harm** → [[mdr_class_iib]]; if **death or
irreversible deterioration** → [[mdr_class_iii]]. If it merely displays/stores data →
[[mdr_class_i]]. If it analyses a specimen → [[ivdr_class]].

## Concrete obligations
- **Notified Body conformity assessment** (Art. 52): typically **Annex IX** (QMS +
  assessment of technical documentation on a *representative sample basis*). The NB
  audits your premises and issues the certificate.
- **ISO 13485 quality management system** must be operational and audited (part of
  [[samd_standards]]; ISO 13485 & ISO 14971 are harmonised under MDR).
- Full **General Safety & Performance Requirements** (Annex I) evidenced via IEC 62304
  (lifecycle), ISO 14971 (risk), IEC 62366-1 (usability).
- **Clinical evaluation** demonstrating scientific validity, technical performance and
  clinical benefit — the 3-pillar MDCG 2020-1 model ([[clinical_eval_mdsw]]).
- **Proactive PMS** with a PMS plan and **Periodic Safety Update Report (PSUR)**, plus
  vigilance reporting ([[pms_lifecycle]]).
- UDI assignment + EUDAMED registration ([[udi_eudamed]]).

## Checklist
- [ ] Engage a designated Notified Body early (capacity is a bottleneck).
- [ ] Stand up an ISO 13485 QMS and the Annex II/III technical file.
- [ ] Produce a Rule 11 classification rationale that justifies IIa over IIb.
- [ ] Build the clinical evaluation report (3 pillars) under [[clinical_eval_mdsw]].
- [ ] Plan the PSUR cadence and PMCF as part of [[pms_lifecycle]].

## Examples (mHealth)
- A symptom-checker that **suggests a likely condition / triage level** to inform a
  non-urgent care decision → Rule 11(a), moderate consequence → Class IIa.
- An app computing an **insulin-dose suggestion** from logged values where an error
  has only moderate, correctable impact → IIa (escalates to IIb if serious harm is
  plausible — see [[mdr_class_iib]]).
- **Edge/negative:** an app monitoring a **vital** parameter (e.g. continuous cardiac
  rhythm with alarms) is **not** IIa — Rule 11(b) places vital-sign monitoring with
  immediate-danger potential at **IIb** ([[mdr_class_iib]]) or higher.

## HERA dimensions touched
- **Device qualification & class** · **Notified Body route** · **Clinical evidence** · **EU market access**
- Cross-links: [[mdr_class_i]] · [[mdr_class_iib]] · [[mdr_class_iii]] · [[ivdr_class]] ·
  [[samd_standards]] · [[clinical_eval_mdsw]] · [[pms_lifecycle]] · [[udi_eudamed]]

## Official sources
- MDR (consolidated 2017/745) — Annex VIII Rule 11, Art. 52: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02017R0745-20230320
- MDCG 2019-11 rev.1 (June 2025) — qualification & classification of MDSW: https://health.ec.europa.eu/latest-updates/update-mdcg-2019-11-rev1-qualification-and-classification-software-regulation-eu-2017745-and-2025-06-17_en
