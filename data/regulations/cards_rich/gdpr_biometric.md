---
id: gdpr_biometric
title: "GDPR Art. 9 — biometrics (+ AI Act Art. 5)"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
key_articles: ["GDPR Art. 9(1)", "GDPR Art. 35", "AI Act Art. 5"]
status: rich-draft
---

# GDPR Art. 9 — biometrics (+ AI Act Art. 5)

## Why this concerns you (purpose)
If your mHealth app processes **biometric data to uniquely identify a person** (face,
voice print, fingerprint, iris, gait, retina), that data is a **special category** under
GDPR Art. 9(1): processing is prohibited unless one of the Art. 9(2) exceptions applies.
On top of GDPR, the **EU AI Act Art. 5** now flatly *bans* some biometric uses regardless
of consent. So biometrics raise two independent gates: a **lawfulness gate** (Art. 9) and
a **prohibition gate** (AI Act). Getting consent does not save you if the use is prohibited.

## When it is triggered (scope)
Triggered when **either** of the following holds:
- you process biometric data **for the purpose of uniquely identifying** a natural person
  (Art. 9(1)) — e.g. face/voice login, biometric patient matching; note mere photos or
  voice recordings are *not* Art. 9 data until processed through specific technical means
  for identification;
- you run an AI system that **infers emotions** or **categorises people by biometric data**
  (AI Act Art. 5) — e.g. a mood/stress detector from facial or vocal cues.

It applies even to a small user base: scale affects the DPIA test, not the Art. 9 trigger.

## Concrete obligations
- Identify a valid Art. 9(2) basis — in consumer mHealth this is almost always
  **explicit consent** (Art. 9(2)(a)): freely given, specific, informed, separate from
  other consents, and as easy to withdraw as to give.
- Run a **DPIA** (Art. 35): processing biometric data for identification is on DPA
  mandatory-DPIA lists (e.g. CNIL) — see [[gdpr_dpia]].
- Check the **AI Act Art. 5** prohibitions, in force since **2 Feb 2025**: emotion
  recognition in the **workplace/education** is banned *except for medical or safety
  reasons*; biometric categorisation to infer sensitive traits (race, sexual orientation,
  political/religious belief) is banned. Penalties up to EUR 35M / 7% of turnover.
- Minimise: prefer **on-device** matching and avoid retaining raw biometric templates;
  offer a **non-biometric fallback** for authentication.

## Checklist
- [ ] Confirm whether your processing is for *unique identification* (Art. 9 trigger) or merely incidental.
- [ ] Document explicit, separable, withdrawable consent (Art. 9(2)(a)) and a non-biometric alternative.
- [ ] Screen the use against AI Act Art. 5 (emotion recognition / biometric categorisation bans).
- [ ] Complete a DPIA before go-live (see [[gdpr_dpia]]).
- [ ] Prefer on-device processing; define a retention/deletion rule for templates.

## Examples (mHealth)
- A dermatology app using **facial recognition** to match a returning patient to their
  record → Art. 9 biometric identification: explicit consent + DPIA required.
- A therapeutic VR app that **infers patient stress from facial expression** to adapt a
  session → emotion recognition, but plausibly within the AI Act Art. 5 **medical-reasons
  exception** (still: GDPR Art. 9 + DPIA, and document the medical justification).
- (Edge/negative) A wellness app storing a **selfie avatar** purely for display, never run
  through identification algorithms → *not* Art. 9 biometric data; ordinary Art. 6 applies.

## HERA dimensions touched
- **Sensitive-data lawfulness** · **AI prohibited practices** · **DPIA**
- Cross-links: [[gdpr_art9]], [[gdpr_dpia]], [[ai_act_high_risk]], [[ai_act_transparency]]

## Official sources
- EUR-Lex — GDPR (Art. 9, Art. 35): https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
- EU AI Act — Art. 5 prohibited practices: https://artificialintelligenceact.eu/article/5/
