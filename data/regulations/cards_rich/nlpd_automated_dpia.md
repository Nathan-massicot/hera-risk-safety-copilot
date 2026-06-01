---
id: nlpd_automated_dpia
title: "nFADP Art. 21 & 22 — automated decision + DPIA (Switzerland)"
jurisdiction: CH
official_url: https://www.fedlex.admin.ch/eli/cc/2022/491/en
key_articles: ["nFADP Art. 21", "nFADP Art. 22", "DPO ordinance (SR 235.11)"]
status: rich-draft
---

# nFADP Art. 21 & 22 — automated decision + DPIA (Switzerland)

## Why this concerns you (purpose)
The revised Swiss data-protection act (**nFADP**, in force since 1 September 2023) is a
**distinct regime from the GDPR**, with its own supervisory authority — the **FDPIC** (Federal
Data Protection and Information Commissioner). Two provisions bite directly on mHealth apps that
"decide" or that process health data at scale: **Art. 21** (automated individual decisions) and
**Art. 22** (data protection impact assessment). They look similar to GDPR Art. 22 / 35 but are
**not the same obligation** — doing a GDPR DPIA does **not** discharge the Swiss one, and the
triggers, wording and authority differ. If your app targets Switzerland, you must run the Swiss
analysis separately.

## When it is triggered (scope)
**Art. 21** is triggered when a decision is **based solely on automated processing** and
**produces legal effects or significantly affects** the data subject (e.g. automated triage,
risk scoring, eligibility or treatment-path decisions).

**Art. 22** (DPIA) is triggered when processing is **likely to entail a high risk** to the
data subject's personality or fundamental rights — including **large-scale processing of
sensitive data** (health data is sensitive under nFADP Art. 5(c)), **high-risk profiling**, or
**systematic large-scale monitoring**.

Both apply to apps targeting **Switzerland** under the nFADP, in parallel with their GDPR
counterparts ([[gdpr_automated]], [[gdpr_dpia]]) and on top of the nFADP baseline ([[nlpd_base]]).

## Concrete obligations
- **Art. 21:** **inform** the data subject that an automated individual decision is being made;
  on request, give them the **right to express their point of view** and to **obtain human
  review** of the decision.
- **Art. 22:** carry out a **DPIA** before high-risk processing — describing the intended
  processing, evaluating the risks to personality/fundamental rights, and setting the protective
  measures.
- **Residual high risk:** if the DPIA shows a high risk remains despite the planned measures,
  **consult the FDPIC beforehand** — unless you have appointed a **data protection adviser**
  (the Swiss DPO equivalent under SR 235.11) and consulted them on that processing.
- Keep the analysis **separate from your GDPR DPIA / Art. 22 record**: same product, two regimes.

## Checklist
- [ ] Map any solely-automated decisions with significant effect, and build the Art. 21 inform +
      human-review workflow.
- [ ] Run an Art. 22 DPIA whenever you process Swiss health data at large scale or do high-risk profiling.
- [ ] Decide your FDPIC route: prior consultation, or appoint a data protection adviser to avoid it.
- [ ] Document the Swiss DPIA distinctly from any [[gdpr_dpia]] you already hold.

## Examples (mHealth)
- A mental-health app that **auto-refuses crisis escalation** based only on an algorithm for Swiss
  users → Art. 21 applies: must inform and offer human review of the decision.
- A symptom-checker processing **large-scale Swiss health data** with risk profiling → Art. 22 DPIA
  required, even if a GDPR DPIA was already completed for the EU rollout.
- An app where a clinician **always reviews and signs off** every recommendation (no solely-automated
  decision) and that processes only a **handful** of Swiss users → **edge case: Art. 21 not triggered**
  (human in the loop) and Art. 22 likely not triggered (no large-scale/high-risk processing).

## HERA dimensions touched
- **Swiss data protection** · **Automated decision-making** · **Impact assessment / FDPIC**
- Cross-links: [[gdpr_automated]], [[gdpr_dpia]], [[nlpd_base]]

## Official sources
- Fedlex — Federal Act on Data Protection (nFADP, SR 235.1): https://www.fedlex.admin.ch/eli/cc/2022/491/en
- FDPIC — Federal Data Protection and Information Commissioner: https://www.edoeb.admin.ch/en
