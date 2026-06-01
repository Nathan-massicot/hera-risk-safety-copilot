---
id: diga_germany
title: "DiGA (Germany) — fast-track reimbursement for digital health apps"
jurisdiction: DE
official_url: https://www.bfarm.de/EN/Medical-devices/Tasks/DiGA-and-DiPA/Digital-Health-Applications/_node.html
key_articles: ["§139e SGB V", "DiGAV", "DVG 2019", "BSI TR-03161", "AbEM (2026)"]
status: rich-draft
---

# DiGA (Germany) — fast-track reimbursement for digital health apps

## Why this concerns you (purpose)
DiGA ("Digitale Gesundheitsanwendung") is Germany's **fast-track** route to getting your
app **prescribed and reimbursed by statutory health insurance (GKV)** — covering ~73M
insured people. It is the most mature digital-therapeutics reimbursement scheme in
Europe. CE marking only lets you *sell*; DiGA listing in the **BfArM directory** is what
makes a doctor able to prescribe your app and a sickness fund obliged to pay. The bar is
specific: a medical-device class, a demonstrated **positive care effect**, and certified
**security + interoperability**.

## When it is triggered (scope)
Relevant when you seek **GKV reimbursement in Germany** for a digital app that is:
- a **CE-marked medical device, class I or IIa** — and, since the **DiGAV amendment in
  force 2026-02-01**, **certain low-risk class IIb** devices too;
- with a **primary digital function** supporting the detection, monitoring, treatment or
  alleviation of disease (a "low-risk" digital health application under **§139e SGB V**).

It is **not** for hardware-centric devices, pure wellness apps (no medical purpose), or
class IIb/III above the low-risk cut-off. A drug-companion or high-risk diagnostic SaMD
typically falls outside DiGA and follows the ordinary MDR + reimbursement route.

## Concrete obligations
- **Device class**: hold a CE certificate as class I/IIa (or low-risk IIb from
  2026-02-01). See [[mdr_class_iia]].
- **Positive care effect (positiver Versorgungseffekt)**: either a **medical benefit** or
  a **patient-relevant improvement of structure/processes**, evidenced by a comparative
  study (RCT preferred) — required for permanent listing.
- **Security**: **BSI TR-03161** certification is **mandatory since 2025-01-01** (a
  dedicated security assessment of mobile app, web app and backend, beyond the old
  self-declaration).
- **Interoperability**: support **ePA** (electronic patient record), **GesundheitsID**
  (insured identity) and the **INA** interoperability requirements; data protection per
  GDPR + national rules.
- **Provisional vs permanent**: a **provisional listing of 12 months** (extendable to 24)
  to generate evidence, then permanent listing on proven positive care effect.
- **From 2026**: mandatory **application-accompanying success measurement (AbEM)** with
  periodic anonymised/aggregated reporting to BfArM (first submissions due 2027), and a
  shift toward **success-dependent / outcome-based pricing**.

## Checklist
- [ ] Confirm your device class qualifies (I/IIa, or low-risk IIb from 2026-02-01).
- [ ] Obtain BSI TR-03161 certification (mandatory since 2025-01-01) for app + backend.
- [ ] Plan the comparative study proving the positive care effect (medical or structural/process).
- [ ] Implement ePA + GesundheitsID + INA interoperability requirements.
- [ ] Prepare AbEM data collection and a success-dependent pricing model for the 2026 regime.

## Examples (mHealth)
- A CBT-based app for depression, CE class IIa, with an RCT showing symptom reduction →
  strong DiGA candidate: provisional listing → permanent on the positive care effect.
- A tinnitus therapy app starts with a **12-month provisional** listing while it runs the
  trial, then must show the effect to stay listed — and from 2026 reports AbEM data.
- A **wellness step-counter** with no medical purpose, or a high-risk class IIb diagnostic
  above the low-risk cut-off → **not eligible** for DiGA; pursue another route.

## HERA dimensions touched
- **German market access / GKV reimbursement** · **Medical-device classification** · **Security certification (BSI)** · **Interoperability (ePA/GesundheitsID)** · **Clinical evidence**
- Cross-links: [[mdr_class_iia]] (device class prerequisite), [[reimbursement_other_eu]] (parallel national schemes), [[national_ehealth]] (ePA interoperability), [[eidas2]] (digital identity)

## Official sources
- BfArM — Digital Health Applications (DiGA): https://www.bfarm.de/EN/Medical-devices/Tasks/DiGA-and-DiPA/Digital-Health-Applications/_node.html
- BSI — Technical Guideline TR-03161 (security requirements for digital health apps): https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/Technische-Richtlinien/TR-nach-Thema-sortiert/tr03161/TR-03161_node.html
