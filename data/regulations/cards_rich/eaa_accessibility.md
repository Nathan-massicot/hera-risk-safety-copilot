---
id: eaa_accessibility
title: "European Accessibility Act (EAA)"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32019L0882
key_articles: ["Directive 2019/882", "EN 301 549"]
status: rich-draft
---

# European Accessibility Act (EAA)

## Why this concerns you (purpose)
The European Accessibility Act (Dir. (EU) 2019/882) requires that **consumer-facing
digital products and services** be usable by people with disabilities. For mHealth,
that means your **B2C app, its website and its purchasing/onboarding flows** must be
accessible — perceivable, operable, understandable and robust — to users who rely on
screen readers, high contrast, captions, or alternative input. The obligations have
**applied since 28 June 2025**. The practical benchmark is the harmonised standard
**EN 301 549**, which incorporates **WCAG 2.1 Level AA** for web content and extends it
to mobile apps and software: conforming to it gives a **presumption of compliance**.
This is a market-access and non-discrimination requirement, separate from any medical or
data-protection rules — but it sits on top of them for any patient-facing service.

## When it is triggered (scope)
Triggered when **all** of the following hold:
- your service/product is **consumer-facing (B2C)** and aimed at the general public;
- it falls in a **covered category** — e-commerce, consumer banking, e-readers,
  telecoms, ticketing, and **consumer-facing software/websites/mobile apps** generally;
- you place it on the **EU market** and are **not** an exempt microenterprise providing
  services (under 10 staff and ≤ €2M turnover have limited service exemptions).

Edge: a **strictly B2B / professional** tool used only by clinicians in a hospital is
generally outside the EAA's consumer scope (national public-sector web rules may still
apply).

## Concrete obligations
- Meet the EAA accessibility requirements for the **app, website and purchase journey**;
  use **EN 301 549 / WCAG 2.1 AA** as the compliance benchmark.
- Provide **accessibility information** (how the product meets the requirements) and keep
  the supporting documentation.
- Ensure assistive-technology compatibility: text alternatives, captions, keyboard/operable
  navigation, sufficient contrast, no reliance on a single sensory channel.
- Maintain accessibility through updates (it is an ongoing obligation, not a one-off audit).

## Checklist
- [ ] Confirm your service is consumer-facing and in scope (and whether the microenterprise carve-out applies).
- [ ] Audit the app + website + checkout/onboarding against **WCAG 2.1 AA / EN 301 549**.
- [ ] Fix and document accessibility (alt text, captions, contrast, keyboard navigation).
- [ ] Build accessibility regression checks into your release process to keep conformance over time.

## Examples (mHealth)
- A direct-to-consumer mental-health app with a subscription checkout → in scope; must be
  WCAG 2.1 AA accessible, including the payment/onboarding flow.
- A consumer symptom-checker website whose results are images with no text alternative →
  non-compliant for screen-reader users.
- A SaMD dashboard sold only to hospitals for clinician use (pure B2B) → outside the
  EAA's consumer scope, though good accessibility remains advisable.

## HERA dimensions touched
- **Digital accessibility (WCAG/EN 301 549)** · **Consumer (B2C) market access** · **Inclusive design**
- Cross-links: [[ehds]] (accessible patient access to health data)

## Official sources
- EUR-Lex — Directive (EU) 2019/882: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32019L0882
- European Commission — European Accessibility Act: https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en
