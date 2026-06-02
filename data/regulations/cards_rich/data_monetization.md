---
id: data_monetization
title: "Data monetisation / third-party sharing"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
key_articles: ["GDPR Art. 9(2)(a)", "ePrivacy"]
status: final
---

# Data monetisation / third-party sharing

## Why this concerns you (purpose)
If your mHealth business model relies on **advertising, selling aggregated data, or sharing
data with third parties**, you are processing health data for purposes *beyond* providing
care. Under GDPR this needs its **own lawful basis per purpose**, and for special-category
(health) data that basis is essentially **explicit consent** (Art. 9(2)(a)). Bundling
monetisation consent into the "accept to use the app" flow is a classic failure mode that
regulators treat as invalid consent — and as unlawful processing of sensitive data.

## When it is triggered (scope)
Triggered when health (or health-derived) data is used for any purpose other than the core
requested service, in particular:
- **targeted advertising** or ad measurement;
- **sale or licensing** of data (including "aggregated" or "anonymised" sets);
- **sharing with third parties** (partners, brokers, model trainers).

Note: data is only outside GDPR if it is **truly anonymous** (irreversible, per Recital 26 and
WP29 Opinion 5/2014) — "pseudonymised" or weakly aggregated health data is still personal data.
If the monetisation also relies on device trackers/SDKs, **ePrivacy** consent is *additionally*
required and is a *separate* obligation — see [[eprivacy_terminal]].

## Concrete obligations
- Obtain **explicit, granular, purpose-specific consent** (Art. 9(2)(a)) for each monetisation
  purpose, **separate** from consent to use the app; make withdrawal as easy as giving it.
- Provide **layered transparency** (Art. 13): name the recipients/categories, the purposes,
  and any profiling logic; do not present monetisation as a condition of the service.
- Put a **GDPR Art. 28 data-processing agreement** (or controller-to-controller terms) in place
  with each recipient and verify their safeguards.
- If you claim anonymisation, **document the technique and re-identification risk**; if it is
  not irreversible, treat the data as personal/health data.
- Layer **ePrivacy consent** for any tracker/SDK used to enable the monetisation.

## Checklist
- [ ] List every monetisation purpose and the third parties involved.
- [ ] Build separate, granular explicit-consent toggles (not bundled, not pre-ticked).
- [ ] Sign Art. 28 DPAs / sharing terms and verify recipient safeguards.
- [ ] Justify and document any anonymisation claim against Recital 26 / WP29 Op. 5/2014.
- [ ] Pair with ePrivacy consent for the underlying trackers — see [[eprivacy_terminal]].

## Examples (mHealth)
- A free fertility app **sharing cycle data with advertisers** → explicit, separate consent per
  purpose; bundled "agree to use the app" consent is invalid.
- A nutrition app selling a **"de-identified" food-and-symptom dataset** to a CPG brand → if
  re-identification is feasible it remains health data and needs an Art. 9(2)(a) basis.
- (Edge/negative) Producing **truly anonymous, aggregate population statistics** (no individual
  re-identification possible) for internal benchmarking → outside GDPR; but you must be able to
  evidence the irreversibility.

## HERA dimensions touched
- **Lawful basis (consent) & purpose limitation** · **Third-party sharing** · **Anonymisation**
- Cross-links: [[eprivacy_terminal]], [[gdpr_art9]], [[gdpr_children]], [[gdpr_transfer]]

## Official sources
- EUR-Lex — GDPR (Art. 9, Recital 26): https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
- WP29 Opinion 05/2014 on anonymisation techniques (WP216): https://ec.europa.eu/justice/article-29/documentation/opinion-recommendation/files/2014/wp216_en.pdf
