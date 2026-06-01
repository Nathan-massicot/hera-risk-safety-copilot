---
id: gdpr_dpia
title: "GDPR Art. 35 — Data Protection Impact Assessment (DPIA)"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
key_articles: ["Art. 35", "Art. 36", "WP248 rev.01"]
status: rich-draft
---

# GDPR Art. 35 — Data Protection Impact Assessment (DPIA)

## Why this concerns you (purpose)
A DPIA is a documented, *before-the-fact* assessment of the risks your processing poses to
people's rights and freedoms, plus the measures that mitigate them. Under GDPR Art. 35 it is
**mandatory** whenever processing is "likely to result in a high risk" — and large-scale
processing of health data almost always qualifies. For an mHealth product, the DPIA is the
backbone document that ties together your lawful basis, security, and accountability.

## When it is triggered (scope)
A DPIA is required when processing is likely to result in a high risk, in particular for the
three Art. 35(3) cases, including **large-scale processing of special-category (health) data**
and **systematic large-scale monitoring**. To test "high risk", apply the **WP248 rev.01**
nine criteria: meeting **two or more** raises a presumption that a DPIA is needed (evaluation/
scoring, automated decisions with significant effect, systematic monitoring, sensitive data,
large scale, matching/combining datasets, vulnerable subjects, innovative technology,
preventing rights exercise). DPAs publish **mandatory-DPIA lists**: the **CNIL** list
(Deliberation 2018-327, 11 Oct 2018) expressly includes health/medico-social patient-care
systems, health data warehouses/registries, and biometric identification of vulnerable persons.

## Concrete obligations
- Produce the DPIA **before** processing starts; it must contain the four Art. 35(7) elements:
  systematic description, necessity & proportionality assessment, risk assessment, mitigation.
- **Seek the DPO's advice** (Art. 35(2)) and, where appropriate, the **views of data subjects**.
- If a **high residual risk** remains after mitigation, carry out **prior consultation** of
  the supervisory authority under **Art. 36** before going live.
- **Review/update** the DPIA when the processing changes; keep it as an accountability record.

## Checklist
- [ ] Screen against Art. 35(3) + WP248 rev.01 (2-criteria rule) and your DPA's mandatory list (e.g. CNIL).
- [ ] Draft the four Art. 35(7) sections; involve the DPO and, if relevant, data subjects.
- [ ] Identify and implement mitigations (encryption, minimisation, access controls, retention).
- [ ] If high residual risk remains, file an Art. 36 prior consultation before launch.
- [ ] Run the Swiss equivalent if you also serve CH users — see [[nlpd_automated_dpia]].

## Examples (mHealth)
- A chronic-disease app **monitoring 50,000 patients' vitals continuously** → large-scale
  health data + systematic monitoring: two WP248 criteria → DPIA mandatory.
- An AI symptom-triage feature combining health, location and behavioural data → sensitive
  data + scoring + innovative tech: DPIA mandatory, likely Art. 36 consultation.
- (Edge/negative) A solo physiotherapist's app holding **a few dozen local patient notes**,
  no profiling → not "large scale"; a DPIA may not be strictly mandatory, but document the
  reasoned screening decision anyway.

## HERA dimensions touched
- **Risk assessment & accountability** · **Sensitive-data processing** · **Supervisory liaison**
- Cross-links: [[gdpr_art9]], [[nlpd_automated_dpia]], [[gdpr_biometric]], [[gdpr_automated]]

## Official sources
- EUR-Lex — GDPR Art. 35-36: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
- CNIL — list of processing requiring a DPIA: https://www.cnil.fr/fr/analyse-dimpact-relative-la-protection-des-donnees-publication-dune-liste-des-traitements-pour
- WP248 rev.01 (Art. 29 WP DPIA guidelines): https://ec.europa.eu/newsroom/article29/items/611236
