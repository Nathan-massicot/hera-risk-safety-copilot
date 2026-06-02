---
id: nlpd_base
title: "nFADP — baseline (Swiss Federal Act on Data Protection)"
jurisdiction: CH
official_url: https://www.fedlex.admin.ch/eli/cc/2022/491/en
key_articles: ["Art. 5(c)", "Art. 6", "Art. 8", "Art. 12", "Art. 19", "Art. 25"]
status: final
---

# nFADP — baseline (Swiss Federal Act on Data Protection)

## Why this concerns you (purpose)
If your mHealth app serves users **in Switzerland**, your data-protection baseline is the
**revised Federal Act on Data Protection (nFADP / revFADP, SR 235.1)**, in force since
**1 September 2023** — **not** the GDPR. This is a common and costly mistake: Switzerland is
a separate sovereign regime with its **own** supervisory authority, its **own** vocabulary
and its **own** thresholds. A GDPR-compliant setup is a good head start but does **not**
automatically satisfy the nFADP, and vice versa. If you target both markets, you must
satisfy **both** baselines in parallel — see [[gdpr_base]].

## When it is triggered (scope)
Triggered as soon as **any** of the following hold:
- you process personal data of people **in Switzerland**;
- your processing **has an effect in Switzerland** (the nFADP, like the GDPR, has
  extraterritorial reach for foreign controllers targeting CH users);
- your app handles **health data**, which the nFADP treats as **sensitive personal data**
  (Art. 5(c)) — a category that also covers genetic and biometric data.

Note the distinct concepts: the authority is the **FDPIC** (Federal Data Protection and
Information Commissioner), **not** an EU DPA; the in-house role is the **"data protection
adviser"** (not a GDPR "DPO"); and Switzerland keeps its **own** adequacy list for
transfers (Annex 1 DPO), separate from the EU's — see [[gdpr_transfer]].

## Concrete obligations
- **Principles (Art. 6):** lawfulness, good faith, proportionality, purpose limitation —
  no separate "legal basis" list as under GDPR Art. 6, but private processing is generally
  permitted unless it breaches a principle or personality rights.
- **Information at collection (Art. 19):** inform data subjects when collecting personal
  data (broader than the old law, which only required it for sensitive data).
- **Right of access (Art. 25):** answer access requests, in principle within 30 days.
- **Record of processing (Art. 12):** maintain a register (SMEs <250 employees with
  low-risk processing are exempt, but health data at scale removes that exemption).
- **Security (Art. 8 + DPO ordinance SR 235.11):** appropriate technical/organisational
  measures; specific minimum requirements set by ordinance.
- **Breach notification:** report breaches to the **FDPIC** "as quickly as possible"
  (Art. 24) — note this is **not** the GDPR's fixed 72-hour rule.
- **Data protection adviser:** optional but recommended; appointing one is the single
  point of contact with the FDPIC and can replace prior consultation for high-risk DPIAs.

## Checklist
- [ ] Confirm you are applying the **nFADP** (not the GDPR) to your Swiss user base.
- [ ] Treat health data as **sensitive data (Art. 5(c))** and document the processing.
- [ ] Provide an Art. 19 information notice at collection and an Art. 25 access workflow.
- [ ] Maintain the Art. 12 record of processing and Art. 8 security measures.
- [ ] Map breach reporting to the **FDPIC** ("as quickly as possible") and consider naming a data protection adviser.

## Examples (mHealth)
- A Swiss-only mental-wellness app logging mood entries → nFADP applies; mood/mental-state
  data is **sensitive** under Art. 5(c); report any breach to the FDPIC, not to an EU DPA.
- A French startup whose diabetes app is also offered to Swiss patients → must satisfy
  **both** [[gdpr_base]] and the nFADP; a single GDPR privacy notice is **not** sufficient.
- A B2B analytics tool used only by a Swiss hospital's internal staff (no CH consumer data
  exported) → still nFADP for employee/processing data, but the GDPR baseline does **not**
  apply absent EU users — a frequent over-stacking error.

## HERA dimensions touched
- **Data protection baseline (Swiss)** · **Sensitive-data handling** · **Authority & transfers (FDPIC)**
- Cross-links: [[gdpr_base]] (the distinct EU regime — satisfy both for dual markets), [[nlpd_automated_dpia]] (Swiss automated decisions & DPIA), [[swiss_stack]] (MedDO/Swissmedic/EPRA), [[gdpr_transfer]] (Swiss adequacy list, Annex 1 DPO)

## Official sources
- Fedlex — Federal Act on Data Protection (FADP, SR 235.1): https://www.fedlex.admin.ch/eli/cc/2022/491/en
- FDPIC — official website: https://www.edoeb.admin.ch/en
