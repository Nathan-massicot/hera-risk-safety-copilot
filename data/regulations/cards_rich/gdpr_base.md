---
id: gdpr_base
title: "GDPR — baseline (legal basis & rights)"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
key_articles: ["Art. 6", "Art. 12-22", "Art. 28", "Art. 30", "Art. 32", "Art. 33-34", "Art. 37"]
status: rich-draft
---

# GDPR — baseline (legal basis & rights)

## Why this concerns you (purpose)
If your mHealth app touches **any personal data** of people in the EU/EEA, the GDPR
is your non-negotiable baseline — it applies regardless of where your company is
established (Art. 3 extraterritorial reach). It forces you to name a **legal basis**
for every processing operation, to be transparent with users, to honour their rights,
and to keep the data secure. For a health app this is the floor on top of which the
health-specific rules ([[gdpr_art9]]) and the device rules stack. Getting the baseline
wrong (no legal basis, no records, no DPA with your cloud) is the single most common
cause of enforcement fines, and it applies even before you process a byte of health data.

## When it is triggered (scope)
Triggered as soon as **any** of the following hold:
- you process **personal data** (anything identifying a natural person, incl. a device
  ID, email, or pseudonymised user ID) of people **in the EU/EEA**;
- you **target** the EU market (offer the app to EU users) or **monitor** their behaviour;
- you act as a **controller** (you decide why/how) or as a **processor** (you process on
  someone else's behalf).

It applies even to a free app, even with no monetisation, and even if your servers sit
outside the EU. Switzerland-only apps fall under a **distinct** regime — see [[nlpd_base]].

## Concrete obligations
- **Legal basis (Art. 6):** identify and document one per purpose (consent, contract,
  legitimate interest…). For health content you must *also* satisfy Art. 9 — see [[gdpr_art9]].
- **Transparency (Art. 12-14):** a clear, layered privacy notice at the point of collection.
- **Data-subject rights (Art. 15-22):** access, rectification, erasure, portability,
  objection — with a workable process to answer within **one month**.
- **Records of processing (Art. 30):** maintain a register of your processing activities.
- **Security (Art. 32):** appropriate technical/organisational measures (encryption at
  rest and in transit, access controls, pseudonymisation).
- **Breach notification (Art. 33-34):** notify the supervisory authority within **72 hours**
  of becoming aware; notify affected users if the breach is "high risk".
- **DPA (Art. 28):** a written data-processing agreement with **every** processor — cloud
  host, analytics vendor, third-party LLM API, crash reporting.
- **DPO (Art. 37(1)(c)):** mandatory if your **core activity** is large-scale processing of
  health data.

## Checklist
- [ ] Map each processing purpose to a documented Art. 6 legal basis (and Art. 9 condition).
- [ ] Sign an Art. 28 DPA with every processor (cloud, analytics, LLM API, support tools).
- [ ] Stand up a rights-request workflow that answers within one month.
- [ ] Maintain an Art. 30 record of processing and an Art. 32 security baseline (encryption, access control).
- [ ] Have a breach playbook that can notify the authority within 72 hours, and appoint a DPO if you process health data at scale.

## Examples (mHealth)
- A symptom-checker app collecting email + symptoms from EU users → GDPR applies fully;
  needs a legal basis, privacy notice, DPA with its cloud host, and (because of symptoms)
  an Art. 9 condition — see [[gdpr_art9]].
- A meditation app that stores only an anonymous random device token with **no** way to
  re-identify the user → still likely personal data via the identifier; baseline GDPR applies.
- A truly **anonymous**, aggregated usage statistic that cannot be linked back to any
  individual → out of GDPR scope (Recital 26), but the bar for "anonymous" is high and
  rarely met by raw event logs.

## HERA dimensions touched
- **Data protection baseline** · **Vendor/processor management** · **User rights & transparency**
- Cross-links: [[gdpr_art9]] (health = special category), [[gdpr_dpia]] (high-risk assessment), [[gdpr_transfer]] (data leaving the EEA), [[hds_certification]] (FR hosting), [[nlpd_base]] (the distinct Swiss regime)

## Official sources
- EUR-Lex — Regulation (EU) 2016/679 (GDPR), consolidated text: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
- EDPB — guidelines and recommendations: https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en
