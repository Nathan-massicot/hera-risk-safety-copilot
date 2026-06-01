---
id: reimbursement_other_eu
title: "Other national reimbursement schemes (Belgium mHealthBelgium, etc.)"
jurisdiction: EU
official_url: https://mhealthbelgium.be/validation-pyramid
key_articles: ["mHealthBelgium M1/M2/M3", "NIHDI/RIZIV reimbursement", "AFMPS notification"]
status: rich-draft
---

# Other national reimbursement schemes (Belgium mHealthBelgium, etc.)

## Why this concerns you (purpose)
Beyond Germany (DiGA) and France (PECAN), **most EU member states run their own**
statutory-insurance pathway for digital health apps — and the pattern is consistent:
CE marking is the entry ticket, but **national clinical/health-economic evidence plus a
national interoperability & security validation** are what unlock reimbursement. If your
business model depends on being **paid by a national payer**, you must navigate each
target country's scheme separately. Belgium's **mHealthBelgium** is the clearest
worked example.

## When it is triggered (scope)
Relevant when you seek **public reimbursement / payer listing** in an EU country **other
than DE or FR**, e.g.:
- **Belgium** — the **mHealthBelgium** validation pyramid (M1 → M2 → M3);
- other MS schemes (e.g. NL with its conditional evaluation routes, AT, the Nordics).

It is **not** triggered if you only place the device on the market without seeking public
funding (CE marking suffices to sell). Note these schemes are **national, additive** to
CE/MDR — clearing the MDR does **not** by itself grant any reimbursement.

## Concrete obligations
- **Belgium — mHealthBelgium 3-level pyramid** (apps always enter at the bottom and
  climb):
  - **M1** — basics: **CE marking** as a medical device, **GDPR** compliance, and
    **product notification to the AFMPS/FAGG** (the Belgian medicines & health-products
    agency).
  - **M2** — **interoperability & security** criteria via the eHealth platform (incl.
    user identification/authentication, connection to the eHealth services).
  - **M3** — **reimbursement**: demonstrate socio-economic added value to the **NIHDI/RIZIV
    (INAMI)**; reimbursement runs through conventions with the payer (the first M3 apps —
    chronic heart-failure remote monitoring — reached reimbursement via a NIHDI/RIZIV
    convention launched early 2025).
- **Cross-cutting (any MS)**: prepare **clinical + health-economic evidence**, meet the
  **national interoperability & security certification**, and host health data lawfully
  (HDS in France — see [[hds_certification]]; national rules elsewhere).
- Plan **per-country**: evidence requirements, tariffs and timelines differ; a single
  dossier rarely transfers across borders.

## Checklist
- [ ] Identify each target country's scheme and its evidence + interoperability requirements.
- [ ] For Belgium: secure M1 (CE + GDPR + AFMPS notification), then M2 (eHealth interop/security).
- [ ] Build the health-economic dossier needed for M3 / NIHDI-RIZIV (or the national payer).
- [ ] Map national security/interoperability certifications to your existing MDR + GDPR work.
- [ ] Budget separate clinical/health-economic studies per market (limited cross-border reuse).

## Examples (mHealth)
- A remote-monitoring app for **chronic heart failure** climbs Belgium's pyramid M1→M2→M3
  and is reimbursed through a NIHDI/RIZIV convention with participating hospitals.
- A CE-marked DTx already listed under **DiGA** in Germany → must still go through
  Belgium's M1/M2/M3 independently; the German listing does **not** carry over.
- A wellness app **not** seeking public funding → can be sold on CE marking alone; no
  mHealthBelgium validation needed (M2/M3 are only relevant if you want reimbursement).

## HERA dimensions touched
- **Multi-country market access / payer listing** · **Clinical & health-economic evidence** · **National interoperability & security** · **Notification to national authorities**
- Cross-links: [[diga_germany]] (German scheme), [[pecan_france]] (French scheme), [[hds_certification]] (FR health-data hosting), [[national_ehealth]] (national interoperability), [[mdr_class_iia]] (CE-marking prerequisite)

## Official sources
- mHealthBelgium — Validation pyramid (M1/M2/M3): https://mhealthbelgium.be/validation-pyramid
- mHealthBelgium — platform home: https://mhealthbelgium.be/
