---
id: gdpr_automated
title: "GDPR Art. 22 — automated decisions"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
key_articles: ["Art. 22"]
status: final
---

# GDPR Art. 22 — automated decisions

## Why this concerns you (purpose)
If your mHealth app makes a decision about a user **solely by automated means** that
produces **legal effects** or **similarly significantly affects** them (triage outcome,
treatment eligibility, insurance/risk scoring), GDPR Art. 22 gives the person the right
**not to be subject** to it — unless a narrow exception applies *and* you put safeguards in
place. This is not just "explain your algorithm": it is a default prohibition with carve-outs.

## When it is triggered (scope)
Triggered when **all** of the following hold:
- the decision is **based solely on automated processing** (including profiling); and
- it produces **legal effects** or **similarly significant** effects on the individual.

"Solely" is read broadly: per the CJEU **SCHUFA** ruling (C-634/21, 7 Dec 2023), a score
that a downstream actor predictably relies on counts as the decision, and a human who merely
**rubber-stamps** the algorithm does *not* take it out of Art. 22 — the human intervention
must be **meaningful**. With health data, Art. 22(4) adds that such decisions may only rest
on Art. 9 special-category data with **explicit consent** or a substantial-public-interest basis.

## Concrete obligations
- Establish a lawful **exception** (Art. 22(2)): necessary for a contract, authorised by
  Union/Member-State law, or **explicit consent** — and for health data meet Art. 22(4).
- Implement **safeguards** (Art. 22(3)): the right to obtain **human intervention**, to
  **express a point of view**, and to **contest** the decision; design a genuine human review,
  not a sign-off.
- Provide **transparency** (Art. 13-15): inform the person that automated decision-making
  exists and give **meaningful information about the logic** and the consequences.
- Where the system is AI-driven, coordinate with AI Act human-oversight duties
  ([[ai_act_high_risk]]) and run a DPIA ([[gdpr_dpia]]).

## Checklist
- [ ] Map which user-facing decisions are *solely* automated and *significant*.
- [ ] Pick and document a valid Art. 22(2) exception (+ Art. 22(4) for health data).
- [ ] Build a meaningful human-review path (not a rubber-stamp) plus contest/appeal flow.
- [ ] Add Art. 13-15 notices describing the logic and significance.
- [ ] Cross-check Swiss equivalent if you also serve CH users — see [[nlpd_automated_dpia]].

## Examples (mHealth)
- An app that **auto-refuses a teleconsultation** or auto-assigns an emergency triage level
  with no clinician in the loop → Art. 22 decision: needs an exception + human-review safeguards.
- A symptom checker that **scores cardiovascular risk** which an insurer then uses for pricing
  → SCHUFA-style: the score is the significant decision; Art. 22 + explicit consent apply.
- (Edge/negative) An app that flags a borderline reading and a **clinician genuinely reviews
  and decides** each case → not "solely" automated; Art. 22 does not bite (but log the review).

## HERA dimensions touched
- **Automated decision-making** · **Human oversight** · **Transparency**
- Cross-links: [[nlpd_automated_dpia]], [[gdpr_dpia]], [[ai_act_high_risk]], [[gdpr_art9]]

## Official sources
- EUR-Lex — GDPR Art. 22: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
- CJEU SCHUFA Holding (Scoring), C-634/21: https://curia.europa.eu/juris/liste.jsf?num=C-634/21
