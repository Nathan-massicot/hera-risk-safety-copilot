---
id: eprivacy_terminal
title: "ePrivacy Art. 5(3) — access to terminal equipment (cookies, SDKs, trackers)"
jurisdiction: EU
official_url: https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-22023-technical-scope-art-53-eprivacy-directive_en
key_articles: ["Directive 2002/58/EC Art. 5(3)", "EDPB Guidelines 2/2023 v2.0"]
status: rich-draft
---

# ePrivacy Art. 5(3) — access to terminal equipment (cookies, SDKs, trackers)

## Why this concerns you (purpose)
Article 5(3) of the ePrivacy Directive requires **prior consent** before *any* storing of
information on, or reading of information from, a user's device — unless an exemption applies.
This is a **separate obligation from the GDPR**: it is about the *act of accessing the device*,
not about whether the data is personal. The EDPB's **Guidelines 2/2023 (final v2.0, 16 Oct
2024)** confirm a deliberately **broad** technical reading, so most mHealth apps that embed
any third-party tooling are caught — even before any "data" question arises.

## When it is triggered (scope)
Triggered whenever your app **stores or gains access to information** on the user's terminal
(phone, watch, IoT device). Per Guidelines 2/2023, this covers far more than cookies:
- **mobile SDKs** (analytics, crash reporting, attribution, ads),
- **tracking pixels** and URL tracking,
- **device fingerprinting** and unique identifiers,
- locally-generated data collected via an API, and on-device hashed identifiers,
- IoT / connected-device read-write.

It applies **regardless of monetisation** and **even for non-health data**. The narrow
**exemptions** are: access *strictly necessary* to carry out the transmission, or *strictly
necessary* to provide a service **the user explicitly requested**. Analytics, attribution,
crash reporting and advertising are **not** strictly necessary, so they need consent.

## Concrete obligations
- Obtain **prior, GDPR-standard consent** (freely given, specific, informed, unambiguous,
  as easy to refuse as to accept) **before** any non-exempt SDK/pixel/identifier fires.
- **Block non-essential trackers until consent** — no pre-ticked boxes, no firing on app open.
- Maintain an **inventory** of every SDK and tracker, its purpose, and its exemption status.
- Keep this **distinct from your monetisation analysis** ([[data_monetization]]): ePrivacy can
  apply even when you do not sell or share data; monetisation adds further GDPR-consent layers.

## Checklist
- [ ] Inventory every SDK, pixel, identifier and on-device read/write in the app.
- [ ] Classify each as strictly-necessary (exempt) or consent-required.
- [ ] Implement a consent gate that suppresses non-essential trackers until opt-in.
- [ ] Ensure "reject all" is as prominent and easy as "accept all".
- [ ] Re-audit after each SDK/dependency update and log consent records.

## Examples (mHealth)
- A symptom-tracker embedding a **Firebase/analytics or crash-reporting SDK** that sets a
  device identifier on launch → Art. 5(3) consent required before it initialises.
- A meditation app using a **marketing-attribution SDK / advertising pixel** → consent
  required, *plus* monetisation consent — see [[data_monetization]].
- (Edge/negative) Storing a **session token strictly necessary** to keep the user logged into
  the service they requested → exempt from consent (still inform under GDPR transparency).

## HERA dimensions touched
- **Tracking & consent UX** · **Third-party SDK governance** · **Device-level privacy**
- Cross-links: [[data_monetization]], [[gdpr_children]], [[data_act]], [[gdpr_dpia]]

## Official sources
- EDPB — Guidelines 2/2023 (page): https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-22023-technical-scope-art-53-eprivacy-directive_en
- EDPB — Guidelines 2/2023 final v2.0 (PDF): https://www.edpb.europa.eu/system/files/2024-10/edpb_guidelines_202302_technical_scope_art_53_eprivacydirective_v2_en_0.pdf
