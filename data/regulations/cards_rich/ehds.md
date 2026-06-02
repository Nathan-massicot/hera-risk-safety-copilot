---
id: ehds
title: "EHDS — European Health Data Space"
jurisdiction: EU
official_url: https://health.ec.europa.eu/ehealth-digital-health-and-care/european-health-data-space_en
key_articles: ["Primary use", "Secondary use", "EEHRxF", "DGA (EU 2022/868)"]
status: final
---

# EHDS — European Health Data Space

## Why this concerns you (purpose)
The European Health Data Space (Reg. (EU) 2025/327, **in force since 26 March 2025**)
builds a common EU framework for health data on **two legs**. **Primary use**: patients
get cross-border access to and control over their electronic health records, and EHR
systems must support a common exchange format (**EEHRxF**) so data is portable between
providers and countries. **Secondary use**: health data can be reused for research,
innovation, policy and regulation, but only through **Health Data Access Bodies (HDABs)**
that grant permits and serve data in secure processing environments. If your mHealth app
writes to or reads from EHRs, or you want to make/obtain health data for research, EHDS
shapes how. It dovetails with the **Data Governance Act** (Reg. (EU) 2022/868) on data
altruism and intermediation. General application lands **26 March 2027**, with primary-use
data exchange phasing in from **26 March 2029**.

## When it is triggered (scope)
Triggered when **any** of the following hold:
- you supply an **EHR system** or an app that interoperates with EHRs (primary use →
  EEHRxF conformity, registration, possible self-certification regime for "wellness" apps
  claiming interoperability with EHRs);
- you are a **data holder** of electronic health data (you may have to make it available
  for secondary use via an HDAB on request);
- you are a **data user** seeking health data for research/innovation → you apply to an
  **HDAB** for a data permit and work inside a secure processing environment.

Edge: purely **primary-care delivery** that never touches the EEHRxF exchange or HDAB
permits is governed by GDPR/national law, not yet by the EHDS technical obligations.

## Concrete obligations
- **Primary use**: support patient access/portability and the **EEHRxF** format; EHR
  systems must meet essential requirements and undergo conformity assessment; "wellness"
  apps claiming EHR interoperability fall under a labelling/self-certification scheme.
- **Secondary use**: data holders make defined health-data categories available to HDABs;
  data users obtain a **data permit**, process only inside the **secure processing
  environment**, and may not re-identify individuals.
- Respect **opt-out** mechanisms for secondary use as provided by national implementation.
- Articulate with **DGA** (data altruism/intermediation) and with **GDPR Art. 9** as the
  personal-data baseline (see [[gdpr_art9]]).

## Checklist
- [ ] Decide if you are a data holder, data user, or EHR/interoperable-app provider under EHDS.
- [ ] If you touch EHRs: plan EEHRxF support, conformity assessment / wellness-app labelling.
- [ ] For research data: route requests through a **Health Data Access Body** permit, not bilateral deals.
- [ ] Track the phased dates (general application **26 Mar 2027**; primary-use exchange from **26 Mar 2029**).

## Examples (mHealth)
- A patient-portal app that imports a national patient summary → must support the EEHRxF
  exchange format and the patient's primary-use access rights.
- A research team wanting real-world data from your diabetes app → they apply to an HDAB
  for a permit; you serve data into the secure processing environment, no re-identification.
- An internal B2B analytics tool that never connects to EHRs and never feeds HDAB secondary
  use → the EHDS technical/permit obligations are not triggered (GDPR still applies).

## HERA dimensions touched
- **Health-data interoperability (EEHRxF)** · **Secondary use / HDAB permits** · **Patient data control**
- Cross-links: [[eidas2]] (identity & EAA attestations for access), [[gdpr_art9]] (personal-data baseline)

## Official sources
- European Commission — European Health Data Space: https://health.ec.europa.eu/ehealth-digital-health-and-care/european-health-data-space_en
- EUR-Lex (ELI) — Regulation (EU) 2025/327: https://eur-lex.europa.eu/eli/reg/2025/327/oj/eng
