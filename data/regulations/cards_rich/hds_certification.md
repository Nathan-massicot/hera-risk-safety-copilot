---
id: hds_certification
title: "HDS — Health Data Host certification (France)"
jurisdiction: FR
official_url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049577902
key_articles: ["PHC Art. L1111-8", "PHC Art. R1111-9 to R1111-11", "Order of 26 Apr. 2024 (v2 framework)"]
status: rich-draft
---

# HDS — Health Data Host certification (France)

## Why this concerns you (purpose)
If you store the health data of French patients on a cloud or with any hosting
provider, French law requires that provider to hold the **HDS certification**
("Hébergeur de Données de Santé"). The obligation legally falls on **you, the data
controller**: you must verify your host is certified — not just assume the cloud
provider "is compliant". A non-certified host = unlawful processing, even if you are
otherwise GDPR-compliant.

## When it is triggered (scope)
Triggered as soon as **all** of the following hold:
- the data is **personal health data** (identifiable + relating to health);
- it is **hosted on behalf of a third party** (i.e. you use an external host/cloud,
  not purely on-premise self-hosting);
- the data concerns **patients in France** (collected during prevention, diagnosis,
  care or medico-social follow-up).

It applies **even if hosting is 100% inside the EU** — HDS is an extra French layer
*on top of* GDPR, distinct from the international-transfer question (Q19).

## Concrete obligations
- Use a host certified for the **relevant activities** among the 6 HDS scopes
  (physical sites, hardware infrastructure, application hosting platform, virtual
  infrastructure, IS administration/operation, backup).
- The v2 framework (order of 26 Apr. 2024, in force 16 May 2024) requires **physical
  hosting within the EEA** and alignment with **ISO/IEC 27001:2022**.
- Bring existing setups into compliance with v2 **by 16 May 2026** at the latest.
- Keep the host's certificate on file (valid 3 years, annual surveillance audits).

## Checklist
- [ ] Confirm your host appears on the official ANS list of HDS-certified hosts.
- [ ] Check the certificate covers your activities (esp. **application hosting** + **backup**).
- [ ] Verify physical hosting is within the EEA (v2 requirement).
- [ ] Reference HDS certification in your processor agreement (GDPR Art. 28 DPA).
- [ ] Diarise the certificate expiry and the 16 May 2026 v2 deadline.

## Examples (mHealth)
- A teleconsultation app storing French patient records on AWS → AWS must be HDS-certified
  for the hosting/backup activities used; the app publisher must verify it.
- A wellness app with **no** identifiable French health data → out of HDS scope.
- A SaMD whose backend runs on a French HDS-certified datacenter but whose analytics
  DB is on a non-certified provider → the analytics DB breaches HDS if it holds health data.

## HERA dimensions touched
- **Data hosting & sovereignty** · **Vendor/processor management** · **French market access**
- Cross-links: [[gdpr_base]] (Art. 28 DPA), [[gdpr_transfer]] (EEA hosting), [[telehealth_national]]

## Official sources
- Légifrance — PHC Art. L1111-8: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049577902
- ANS — list of HDS-certified hosts: https://esante.gouv.fr/offres-services/hds/liste-des-hebergeurs-certifies
