---
id: gdpr_art9
title: "GDPR Art. 9 — health data (special category)"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
key_articles: ["Art. 9(1)", "Art. 9(2)", "Art. 35"]
status: final
---

# GDPR Art. 9 — health data (special category)

## Why this concerns you (purpose)
Health data is a **special category** under GDPR Art. 9(1) and its processing is
**prohibited by default**. For an mHealth app this flips the usual logic: a normal Art. 6
legal basis is **not enough** — you must *additionally* clear one of the narrow Art. 9(2)
exceptions before you may process symptoms, conditions, medication, biometrics, mental
state or any health-related behaviour. This is the rule that most distinguishes a health
app from an ordinary one, and it routinely drags in a mandatory impact assessment
([[gdpr_dpia]]). Treat Art. 9 as a gate that sits *on top of* the [[gdpr_base]] baseline.

## When it is triggered (scope)
Triggered as soon as you process **data concerning health** (Art. 4(15)) of EU/EEA users.
This is read **broadly**: it covers not just clinical records but anything from which a
person's health status can be **inferred** — wearable heart-rate and sleep data, mood/mental
state, menstrual or fertility tracking, medication adherence, even step counts when used to
infer a condition. **Genetic** and **biometric** data (when used to identify) are separate
special categories under the same article — see [[gdpr_biometric]]. When in doubt, assume
the data is health data.

## Concrete obligations
- **Find an Art. 9(2) exception** — the practical ones for mHealth are:
  - **(a) explicit consent** — the default for consumer apps; must be a clear affirmative
    act that *specifically* references the health data and purpose (not bundled, not implied),
    and freely withdrawable;
  - **(h) healthcare / medical diagnosis / care** — usable when processing is done by or
    under the responsibility of a health professional bound by confidentiality (Art. 9(3));
  - **(i) public health**, **(c) vital interests** (emergencies), **(j) research** — narrower,
    and (h)/(i)/(j) require a basis in EU or Member State law.
- **Explicit consent done right:** separate, granular, opt-in per purpose; logged; as easy
  to withdraw as to give. Reusing a generic "I accept the terms" tick-box is non-compliant.
- **DPIA (Art. 35):** a Data Protection Impact Assessment is effectively required for
  large-scale or systematic health-data processing — see [[gdpr_dpia]].
- **Member State overlay:** Art. 9(4) lets states add stricter conditions for health/genetic/
  biometric data (e.g. French health-data rules), so check the national layer too.

## Checklist
- [ ] Confirm an Art. 9(2) condition for **each** health-data purpose (usually 9(2)(a) consent or 9(2)(h) care).
- [ ] Implement **explicit, granular, per-purpose** opt-in consent with easy withdrawal and an audit log.
- [ ] Keep health-data purposes **separate** from marketing/analytics consents (no bundling).
- [ ] Run a **DPIA** before launch for any large-scale or systematic health processing → [[gdpr_dpia]].
- [ ] Check the **national** Art. 9(4) overlay for each target Member State.

## Examples (mHealth)
- A diabetes-logging app storing glucose readings and insulin doses → health data under
  Art. 9; relies on **explicit consent (9(2)(a))** for the consumer version, plus a DPIA.
- A teleconsultation platform where a doctor records a diagnosis → can rely on **9(2)(h)**
  (care provided by a confidentiality-bound professional) instead of consent.
- A "fitness-only" step counter that **infers and flags a likely cardiac condition** → even
  though marketed as wellness, the *inference* makes it health data; the "we're not health"
  disclaimer does **not** remove it from Art. 9 (edge/negative case).

## HERA dimensions touched
- **Special-category health data** · **Lawful basis & explicit consent** · **Impact assessment**
- Cross-links: [[gdpr_base]] (the baseline Art. 9 sits on), [[gdpr_dpia]] (Art. 35 assessment), [[gdpr_biometric]] (genetic/biometric special categories), [[nlpd_base]] (Swiss "sensitive data" equivalent, Art. 5(c))

## Official sources
- EUR-Lex — Regulation (EU) 2016/679 (GDPR), Art. 9: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
- EDPB — guidelines on processing of special categories of data: https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en
