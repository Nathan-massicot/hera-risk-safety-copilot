---
id: cra
title: "CRA — Cyber Resilience Act (products with digital elements)"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R2847
key_articles: ["Art. 13", "Art. 14", "Annex I", "Annex II (SBOM)"]
status: rich-draft
---

# CRA — Cyber Resilience Act (products with digital elements)

## Why this concerns you (purpose)
If you place a mHealth **app or software** on the EU market, the Cyber Resilience
Act (Reg. (EU) 2024/2847) treats it as a **"product with digital elements"** that
must be **secure by design and by default** for its whole supported lifetime. The
point is product security, not paperwork: you must ship without known exploitable
vulnerabilities, handle vulnerabilities as they appear, and keep users patched. The
CRA is **distinct from NIS2** — NIS2 governs how your *organisation* manages cyber
risk; the CRA governs the *product* you sell. A SaMD already CE-marked under the MDR
is not automatically off the hook: the cybersecurity essential requirements still
have to be met (in practice via the MDR route, see [[nis2_cyber]] and MDR Annex I §17).

## When it is triggered (scope)
Triggered when **all** of the following hold:
- you make available on the EU market a **software or hardware product with digital
  elements** (a mobile app, a connected-device firmware, a SaMD backend, an SDK);
- it can be **connected** (directly or indirectly) to a device or network;
- it is supplied in the **course of a commercial activity** (free + paid both count;
  pure open-source not monetised is largely carved out).

Edge: a service you run purely as a SaaS backend without distributing the software is
closer to NIS2 than CRA — but any component you *ship* (mobile app, on-device model)
is in CRA scope.

## Concrete obligations
- Design, develop and produce the product to meet the **essential cybersecurity
  requirements** of Annex I (no known exploitable vulnerabilities at release,
  secure default config, confidentiality/integrity protection, minimal attack surface).
- Run a **vulnerability-handling process** for the whole support period: maintain a
  **Software Bill of Materials (SBOM)** (Annex I Part II / Annex II), provide
  **free security updates**, and have a coordinated disclosure policy.
- **Report actively exploited vulnerabilities and severe incidents** to ENISA (single
  reporting platform) and the relevant CSIRT — early warning within **24h**, then
  staged updates — **from 11 Sep 2026**.
- Carry out conformity assessment, draw up technical documentation + EU Declaration of
  Conformity, and affix the **CE marking** — **full obligations from 11 Dec 2027**.

## Checklist
- [ ] Maintain an up-to-date SBOM for every shipped component and third-party dependency.
- [ ] Stand up a vulnerability-handling + coordinated-disclosure process and a security-update channel.
- [ ] Define and publish the **support period** during which you will issue free security updates.
- [ ] Wire up ENISA / CSIRT reporting before **11 Sep 2026**; plan CE conformity for **11 Dec 2027**.

## Examples (mHealth)
- A symptom-tracker app distributed via the App Store → product with digital elements;
  needs SBOM, secure defaults, update channel, CE marking by Dec 2027.
- A glucometer companion app whose Bluetooth pairing is found to be exploitable and is
  being attacked in the wild → must report to ENISA/CSIRT (early warning 24h) once the
  24-month reporting regime is live.
- A purely internal analytics dashboard never distributed outside your company →
  outside CRA scope (no product made available on the market), though NIS2 may still apply.

## HERA dimensions touched
- **Product cybersecurity** · **Vulnerability management / SBOM** · **EU market access (CE)**
- Cross-links: [[nis2_cyber]] (organisation vs product), [[pld]] (a missing security update can be a defect)

## Official sources
- EUR-Lex — Regulation (EU) 2024/2847: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R2847
- European Commission — Cyber Resilience Act: https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act
