---
id: gdpr_children
title: "GDPR Art. 8 — children"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
key_articles: ["Art. 8"]
status: final
---

# GDPR Art. 8 — children

## Why this concerns you (purpose)
If your mHealth app is offered **directly to children** and relies on **consent**, GDPR
Art. 8 sets an age below which the child cannot consent alone: you need consent from a
**holder of parental responsibility**. Children are deemed less aware of the risks, so the
GDPR (Recital 38) requires *specific protection*. In a health context — where Art. 9
sensitive data is also in play — the bar for clear information and verification is high.

## When it is triggered (scope)
Triggered when **all** of the following hold:
- your service is an **information society service** (an app/online service) offered
  **directly to a child**;
- your **legal basis is consent** (Art. 6(1)(a) / Art. 9(2)(a)); and
- the user is **below the applicable age threshold**.

The threshold is **16 by default**, but Member States may lower it to **no less than 13**:
Germany, the Netherlands, Ireland = 16; **France = 15**; Spain = 14; Belgium = 13. You must
apply the threshold of the user's country. If your basis is *not* consent (e.g. a care contract), Art. 8 itself
does not bite — but the child-protection principles still apply.

## Concrete obligations
- Determine the **applicable national age** for each market and gate accordingly.
- Below the threshold, obtain and **verify** consent from the holder of parental
  responsibility, making *reasonable efforts* given available technology (Art. 8(2)).
- Provide **child-friendly transparency**: plain-language notices a minor can understand
  (Recital 58); align with the ICO Age-Appropriate Design Code as best practice.
- Apply **data minimisation and privacy-by-default**; avoid profiling/targeted ads to minors.
- Note the exception: **preventive or counselling services offered directly to a child** do
  not require parental authorisation (Recital 38), as they serve the child's best interests.

## Checklist
- [ ] Map your age threshold per target Member State (13-16) and add an age gate.
- [ ] Build a verifiable parental-consent flow for under-threshold users.
- [ ] Write child-friendly privacy information and a separate parent-facing notice.
- [ ] Disable behavioural advertising and unnecessary profiling for minors by default.
- [ ] Document whether the preventive/counselling exception applies to your service.

## Examples (mHealth)
- A teen **mental-wellness app** in France (threshold 15) relying on consent → needs
  verified parental consent for users under 15.
- A youth **sleep/step tracker** processing heart-rate data → Art. 8 *and* Art. 9 stack:
  parental consent plus a DPIA-grade assessment of the sensitive data — see [[gdpr_dpia]].
- (Edge/negative) A **confidential self-harm counselling chat** aimed directly at minors →
  falls under the preventive/counselling exception: parental consent could defeat its
  purpose, so it is not required, but child-friendly safeguarding still applies.

## HERA dimensions touched
- **Lawful basis (consent)** · **Vulnerable data subjects** · **Transparency / UX**
- Cross-links: [[gdpr_art9]], [[gdpr_dpia]], [[data_monetization]], [[eprivacy_terminal]]

## Official sources
- EUR-Lex — GDPR Art. 8: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
- EU Commission — safeguards for children's data: https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/legal-grounds-processing-data/are-there-any-specific-safeguards-data-about-children_en
