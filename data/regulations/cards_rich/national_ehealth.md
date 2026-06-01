---
id: national_ehealth
title: "eHealth — national profiles (EPRA, DMP, ELGA)"
jurisdiction: EU/CH
official_url: https://www.fedlex.admin.ch/eli/cc/2017/203/en
key_articles: ["EPRA", "IHE XDS", "FHIR R4"]
status: rich-draft
---

# eHealth — national profiles (EPRA, DMP, ELGA)

## Why this concerns you (purpose)
If your app must **read from or write to a national electronic health record** — the
Swiss EPR/EPD, the French DMP/Mon espace santé, the Austrian ELGA — then "speaking
FHIR" is not enough. Each country layers **national profiles, terminologies and a
mandatory conformance/referencing process** on top of the international standards. You
cannot connect to these systems unless your software is **certified/referenced** against
the national framework. This is the integration gate that turns a standalone app into a
participant in the public health-data ecosystem.

## When it is triggered (scope)
Triggered when your app:
- **feeds or consults** a national shared record (DMP, EPR/EPD, ELGA);
- exchanges documents via the **national exchange infrastructure** (e.g. IHE XDS.b
  document sharing, FHIR R4 APIs, MSSanté secure messaging in France);
- claims **interoperability** as a condition of public funding or market access.

It is **not** triggered by purely internal data exchange that never touches a national
record system — but note that national reimbursement schemes ([[diga_germany]],
[[pecan_france]], [[reimbursement_other_eu]]) usually *require* this interoperability.

## Concrete obligations
- **Switzerland (EPRA/EPDG)** — conform to the EPR technical/integration profiles
  (IHE-based) and use a certified core community/portal. A **full revision** is under
  way: the Federal Council submitted the new act to Parliament on **5 Nov 2025**,
  replacing the current opt-in EPR with a near-**mandatory opt-out** electronic health
  record (HCP use mandated, patient control over access), targeted **~2028 at the
  earliest**. Plan for the model shift. See [[swiss_stack]].
- **France (Ségur du numérique / DMP)** — obtain **Ségur référencement** (Vague 1, now
  Vague 2): software must implement **CI-SIS**, **FHIR R4** for new developments, feed
  **Mon espace santé/DMP**, use **INS** (national patient identifier) and **MSSanté**.
  Ségur is shifting from incentives toward **mandatory** requirements around 2026-2027.
- **Austria (ELGA)** — comply with the ELGA Gesundheitstelematikgesetz (G-TG) profiles
  (IHE XDS, CDA/FHIR) to connect to e-Befund / e-Medikation.
- Cross-cutting: implement **IHE XDS** document sharing and/or **FHIR R4**, the national
  **terminologies** (SNOMED CT, LOINC) and the national **patient/HCP identity** scheme.

## Checklist
- [ ] Identify each national record you must connect to (EPR/EPD, DMP, ELGA) and its profiles.
- [ ] Implement FHIR R4 + IHE XDS and the required national terminologies (SNOMED CT, LOINC).
- [ ] Obtain the national conformance: Ségur référencement (FR), EPR certification (CH), G-TG conformance (AT).
- [ ] Integrate the national patient/HCP identifier (INS in FR) and secure messaging (MSSanté).
- [ ] Track the Swiss EPRA revision (opt-out ~2028) and the FR Ségur shift to mandatory (2026-2027).

## Examples (mHealth)
- A French chronic-care app that pushes care summaries to **Mon espace santé/DMP** → must
  pass **Ségur référencement**, use **INS** + FHIR R4 + CI-SIS, not just any FHIR server.
- A Swiss medication-management app integrating with the **EPR** → must connect via a
  certified community and IHE profiles; under the revision, prepare for the opt-out E-HR.
- An app that stores data **only in its own backend** and never connects to a national
  record → out of scope here (but interoperability may still be demanded for reimbursement).

## HERA dimensions touched
- **Interoperability & standards (FHIR/IHE)** · **National conformance/referencing** · **Patient/HCP identity** · **Public market access**
- Cross-links: [[swiss_stack]] (EPRA in the Swiss framework), [[telehealth_national]] (clinical records), [[eidas2]] (identity attestations), [[pecan_france]] (FR interop as a funding condition), [[ehds]] (EU-level primary use / EEHRxF)

## Official sources
- Fedlex — Swiss EPRA/EPDG (Federal Act on the Electronic Patient Record): https://www.fedlex.admin.ch/eli/cc/2017/203/en
- eHealth Suisse — Electronic Patient Record: https://www.e-health-suisse.ch/en/coordination/electronic-patient-record/the-epr
- ANS — Doctrine du numérique en santé / interopérabilité (FR): https://esante.gouv.fr/doctrine/interoperabilite
