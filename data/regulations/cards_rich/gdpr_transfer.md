---
id: gdpr_transfer
title: "GDPR Chapter V — international transfers"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
key_articles: ["Art. 44-49"]
status: rich-draft
---

# GDPR Chapter V — international transfers

## Why this concerns you (purpose)
If your health data leaves the EEA — even just to a cloud sub-processor or a third-party AI
API hosted abroad — GDPR **Chapter V** (Art. 44-49) governs the transfer. The rule: you may
only transfer if the destination ensures a level of protection **essentially equivalent** to
the GDPR. For sensitive health data this is one of the highest-scrutiny areas, and "it's on
AWS/Azure" is not an answer by itself: you must identify the **transfer mechanism** and, after
*Schrems II*, assess the destination country's laws.

## When it is triggered (scope)
Triggered whenever personal (health) data is **transferred to or accessed from a third country**
(outside the EEA) or an international organisation — including:
- storage/processing by a **non-EEA cloud** or sub-processor;
- **remote support/admin** access from a third country;
- calls to a **third-party AI/LLM API** hosted abroad.

Switzerland is a special case: the GDPR does not apply to a Swiss-only flow, and **Switzerland
maintains its own adequacy list** (Annex 1 of the Swiss Data Protection Ordinance, overseen by
the **FDPIC**), distinct from the EU's. The EU-Swiss flow itself benefits from mutual adequacy.

## Concrete obligations
- Identify a **valid transfer tool**: an **adequacy decision** (Art. 45 — e.g. Switzerland,
  UK; US only via the Data Privacy Framework for certified importers), or **appropriate
  safeguards** (Art. 46) such as the **2021 Standard Contractual Clauses** (Decision 2021/914),
  or a narrow **Art. 49 derogation**.
- Where you rely on SCCs, perform a **Transfer Impact Assessment (TIA)**: document that the
  destination's laws/practices do not undermine the SCCs, and add **supplementary measures**
  (encryption, pseudonymisation, access controls) where needed.
- Map the **full data path including sub-processors**; flow down SCCs/obligations contractually.
- For Swiss flows, use the **Swiss-adapted SCCs** (FADP references, FDPIC as authority) and
  check the Swiss adequacy list separately from the EU's.

## Checklist
- [ ] Map every third-country transfer and access point, including sub-processors and AI APIs.
- [ ] Assign a valid Chapter V mechanism to each (adequacy / 2021 SCCs / Art. 49 derogation).
- [ ] Complete and document a TIA + supplementary measures where you rely on SCCs.
- [ ] For Swiss data, use Swiss-adapted SCCs and check the FDPIC adequacy list.
- [ ] Re-assess on sub-processor changes; coordinate with French hosting rules — see [[hds_certification]].

## Examples (mHealth)
- A patient app whose backend runs on a **US-region cloud** → adequacy only if the importer is
  DPF-certified; otherwise 2021 SCCs + TIA + encryption.
- An EU app calling a **non-EEA LLM API** to summarise clinical notes → that call is a transfer:
  needs SCCs/TIA and an Art. 28 DPA, with strong supplementary measures for the health content.
- (Edge/negative) Data hosted and processed **entirely within the EEA (or EU↔CH)** with no
  third-country access → no Chapter V transfer; but verify *support/admin* never reaches in
  from abroad (a common hidden transfer).

## HERA dimensions touched
- **Cross-border transfers** · **Vendor/sub-processor mapping** · **Data sovereignty**
- Cross-links: [[hds_certification]], [[gdpr_dpia]], [[data_monetization]], [[gdpr_art9]]

## Official sources
- EUR-Lex — GDPR Chapter V (Art. 44-49): https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
- EU Commission — 2021 Standard Contractual Clauses (Decision 2021/914): https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/new-standard-contractual-clauses-questions-and-answers-overview_en
- CNIL — Transfer Impact Assessment practical guide (Jan 2025): https://www.cnil.fr/sites/default/files/2025-07/guide_tia.pdf
