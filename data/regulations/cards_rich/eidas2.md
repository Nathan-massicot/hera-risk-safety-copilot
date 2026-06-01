---
id: eidas2
title: "eIDAS 2 — EU Digital Identity Wallet"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1183
key_articles: ["Regulation (EU) 2024/1183", "Electronic Attestations of Attributes (EAA)"]
status: rich-draft
---

# eIDAS 2 — EU Digital Identity Wallet

## Why this concerns you (purpose)
If your app needs to **strongly identify a patient or a healthcare professional** —
before a teleconsultation, an e-prescription, or access to a medical record — eIDAS 2
sets the EU-wide rails. Regulation **(EU) 2024/1183** (in force 20 May 2024) obliges
every Member State to offer an **EU Digital Identity Wallet (EUDI Wallet)** by **end
2026**. For mHealth this matters two ways: (1) you may be able to **rely on** the wallet
for high-assurance identity instead of building your own KYC; (2) under the EHDS, health
roles/credentials are issued **into** the wallet as Electronic Attestations of
Attributes (EAA), which your app may need to **accept and verify**.

## When it is triggered (scope)
Relevant when your app performs **strong identity proofing / authentication** of:
- **patients** (e.g. to grant access to their record, enroll in télésurveillance);
- **healthcare professionals** (e.g. to authorise prescribing or signing a care act).

It is **not** mandatory for a B2C wellness app that needs no high-assurance identity.
And note: eIDAS 2 binds **EU/EEA** Member States — **Switzerland is out of scope**
(it runs its own e-ID, federal Act adopted 2024, planned 2026), so a Swiss-only app does
not inherit the EUDI Wallet obligations.

## Concrete obligations
- **Member States** must provide at least one **EUDI Wallet** by end 2026 (24 months
  after the implementing acts; the first technical/certification implementing
  regulations were adopted in 2024-2025). You as a service provider do not issue it.
- **Relying-party** duties: if you accept the wallet, register as a relying party,
  request only the **attributes strictly necessary** (data minimisation), and verify
  EAAs against their authentic source.
- **Health attributes as EAA**: under the **EHDS** identity-management implementing
  rules, Member States issue **HCP** (and relevant patient) attributes as EAAs into the
  wallet, and healthcare providers must be able to **accept** them. Design your app to
  consume **qualified/non-qualified EAAs** for role-based authorisation.
- Use the wallet's **qualified electronic signature/seal** capability where a signed
  clinical act is required (couples well with [[telehealth_national]] act traceability).

## Checklist
- [ ] Decide whether your app is a relying party (consumes the wallet) and register as such.
- [ ] Request only strictly necessary attributes; document the data-minimisation rationale (GDPR).
- [ ] Implement verification of EAAs (incl. EHDS health/HCP attributes) against authentic sources.
- [ ] Support qualified e-signature/seal via the wallet for signed clinical acts where needed.
- [ ] Track national rollout dates (wallet availability per Member State by end 2026).

## Examples (mHealth)
- A teleconsultation platform lets a doctor authenticate with the EUDI Wallet and present
  an **HCP EAA** → app verifies the role attribute, then authorises e-prescribing.
- A patient unlocks access to their national record via the wallet → high-assurance
  identity reused instead of bespoke KYC, with consent and minimised attributes.
- A **Swiss-only** mood-tracking app with simple email login → eIDAS 2 does **not** apply
  (Switzerland not bound; the Swiss e-ID regime governs instead).

## HERA dimensions touched
- **Strong identity & authentication** · **Trust services / e-signature** · **Cross-border interoperability** · **Data minimisation (GDPR)**
- Cross-links: [[ehds]] (health attributes issued as EAA), [[telehealth_national]] (HCP/patient identification for the act), [[national_ehealth]] (record access identity)

## Official sources
- EUR-Lex — Regulation (EU) 2024/1183 (eIDAS 2): https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1183
- European Commission — EU Digital Identity Wallet: https://ec.europa.eu/digital-building-blocks/sites/spaces/EUDIGITALIDENTITYWALLET/pages/915931811/The+European+Digital+Identity+Regulation
