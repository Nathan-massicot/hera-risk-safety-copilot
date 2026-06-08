---
id: nlpd_sensitive
title: "nFADP — health data as sensitive personal data (Art. 5 let. c ch. 2)"
jurisdiction: CH
official_url: https://www.fedlex.admin.ch/eli/cc/2022/491/en
key_articles: ["revFADP Art. 5 let. c ch. 2", "revFADP Art. 6 al. 7 let. a", "revFADP Art. 8", "OPDo (SR 235.11) Art. 14", "revFADP Art. 22", "revFADP Art. 23"]
status: final
---

# nFADP — health data as sensitive personal data (Art. 5 let. c ch. 2)

## Why this concerns you (purpose)
If your app processes the **health data** of people in Switzerland, that data is
**sensitive personal data** under the revised Federal Act on Data Protection
(**revFADP / nLPD, SR 235.1**, in force since **1 September 2023**). This is the Swiss
counterpart to **GDPR Art. 9** — but it is a **distinct regime**, not a translation of it.
Treating a GDPR Art. 9 setup as automatically nFADP-compliant is a common and costly
mistake: the lawfulness logic, the consent rule, the authority and the thresholds differ.
See [[nlpd_base]] for the Swiss baseline and [[gdpr_art9]] for the EU counterpart.

## When it is triggered (scope)
Triggered as soon as you process **sensitive data** of people in Switzerland (or with an
effect in Switzerland). Under **Art. 5 let. c** the category covers, among others
(**ch. 2**) data on **health**, plus data on the **intimate sphere** and **racial/ethnic
origin**, as well as religious/ideological/political views, genetic and biometric data
identifying a person, and data on administrative/criminal proceedings. Mood, mental-state,
symptom, medication and physiological data all qualify as health data.

## Concrete obligations
- **No general consent mandate, but a stricter consent standard.** Unlike GDPR Art. 9,
  the revFADP does **not** require a special legal basis to process sensitive data:
  private processing is lawful unless it unlawfully breaches the data subject's
  personality (Art. 30-31). **However, where you DO rely on consent, it must be EXPRESS**
  for sensitive data (**Art. 6 al. 7 let. a**) — implied/bundled consent is insufficient.
- **Disclosure to third parties / high-risk uses** can require justification, and
  consent must be express where it is the basis.
- **Security (Art. 8 + OPDo, SR 235.11):** appropriate technical and organisational
  measures; the Data Protection Ordinance sets minimum requirements (logging, access
  control) that bite harder for sensitive data at scale.
- **Data protection impact assessment (Art. 22):** mandatory where processing entails a
  **high risk** to personality/fundamental rights — explicitly the case for **large-scale
  processing of sensitive data** or systematic high-risk profiling (criteria detailed in
  **OPDo Art. 14**). If residual high risk remains, **consult the FDPIC beforehand
  (Art. 23)** — unless you have appointed a data protection adviser.
- **Authority: the FDPIC** (Federal Data Protection and Information Commissioner) — **not**
  an EU supervisory authority.

## Checklist
- [ ] Classify your health/mental-state data as **sensitive (Art. 5 let. c ch. 2)** and document it.
- [ ] If consent is your basis, make it **express** and unbundled (Art. 6 al. 7 let. a).
- [ ] Apply Art. 8 security measures (OPDo minimums) proportionate to sensitive data.
- [ ] Run a **DPIA (Art. 22)** for large-scale sensitive processing or high-risk profiling; keep it on file.
- [ ] If residual high risk, **consult the FDPIC (Art. 23)** or rely on an appointed data protection adviser.

## Examples (mHealth)
- A Swiss-only mental-wellness app logging daily mood → mood = sensitive health data
  (Art. 5 let. c ch. 2); if consent is the lawful basis it must be **express**; a
  large-scale roll-out triggers a **DPIA (Art. 22)**.
- A symptom-checker offered to both EU and Swiss users → satisfy **both** [[gdpr_art9]]
  (special-category, explicit-consent default) **and** the nFADP sensitive-data regime in
  parallel; one GDPR notice does not cover the Swiss obligations.
- A Swiss diabetes app sharing pseudonymised glucose data with a research partner →
  express consent if consent-based, plus DPIA given large-scale sensitive processing.

## HERA dimensions touched
- **Data protection — sensitive data (Swiss)** · **Lawful basis & express consent** · **DPIA / FDPIC consultation** · **Security of special-category data**
- Cross-links: [[nlpd_base]] (Swiss baseline & FDPIC), [[gdpr_art9]] (EU special-category counterpart — satisfy both for dual markets), [[nlpd_automated_dpia]] (Swiss automated decisions & DPIA), [[gdpr_dpia]] (EU DPIA)

## Official sources
- Fedlex — Federal Act on Data Protection (revFADP / nLPD, SR 235.1): https://www.fedlex.admin.ch/eli/cc/2022/491/en
- Fedlex — Data Protection Ordinance (OPDo, SR 235.11): https://www.fedlex.admin.ch/eli/cc/2022/568/en
- FDPIC — official website: https://www.edoeb.admin.ch/en
