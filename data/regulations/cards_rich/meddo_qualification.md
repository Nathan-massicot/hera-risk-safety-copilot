---
id: meddo_qualification
title: "MedDO — Swiss medical-device qualification & classification (adopts MDR rules)"
jurisdiction: CH
official_url: https://www.fedlex.admin.ch/eli/cc/2020/552/en
key_articles: ["MedDO Art. 15 (classification via Annex VIII EU-MDR + Annex 5a MedDO)", "MedDO Art. 23 (conformity assessment)", "MedDO Art. 24-28 (Swiss designated bodies)", "MDR (2017/745) Annex VIII Rule 11 (software)", "MedDO Art. 51 (CH-REP)", "Switzerland = MDR third country since 26 May 2021"]
status: final
---

# MedDO — Swiss medical-device qualification & classification (adopts MDR rules)

## Why this concerns you (purpose)
If your software is a **medical device** placed on the **Swiss** market, it is not the EU
MDR that applies directly but the **Swiss Medical Devices Ordinance (MedDO / ODim, SR
812.213)**. The key point — and a frequent source of confusion — is that the **MedDO
adopts the EU MDR's qualification and classification logic**: the same rules decide
whether your software is a device and which **risk class (I / IIa / IIb / III)** it falls
in. So the classification you obtain under the MDR generally **carries over** to
Switzerland. What changes is the **institutional layer**: the competent authority, the
conformity-assessment route, and the third-country/representative rules.

## When it is triggered (scope)
Triggered when your product (a) has a **medical purpose** and qualifies as **software as a
medical device (SaMD)**, **and** (b) is **made available on the Swiss market**. It
complements — it does **not** replace — the EU MDR class cards
([[mdr_class_i]], [[mdr_class_iia]], [[mdr_class_iib]], [[mdr_class_iii]]) when you target
both markets; for a **Switzerland-only** app it is the relevant device framework.

## Concrete obligations
- **Classification (MedDO Art. 15):** the risk class is determined by the classification
  rules of **Annex VIII of the EU MDR (2017/745)** — including **Rule 11** for software —
  read together with **Annex 5a MedDO**. Practically, the class matches the MDR result.
- **Conformity assessment (MedDO Art. 23):** the procedure depends on the risk class; for
  classes **above I**, a **Swiss designated body** must be involved (**Art. 24-28**),
  issuing certificates of conformity. Class I is largely self-declared.
- **Authority — Swissmedic:** the competent and designating authority for devices,
  including market surveillance and **vigilance reporting** (see [[swiss_stack]]).
- **Third-country status & CH-REP:** since the **EU-CH Mutual Recognition Agreement was
  not updated**, Switzerland has been an **MDR third country since 26 May 2021**. Any
  manufacturer **without a Swiss registered seat** (EU/EEA included) must appoint a
  **Swiss authorised representative (CH-REP, MedDO Art. 51)** before placing the device on
  the Swiss market — mirror of the EU-REP duty. See [[ch_rep_meddo]].
- **Lifecycle standards** (IEC 62304, ISO 14971, IEC 62366-1, ISO 13485) apply as under
  the MDR — see [[samd_standards]].

## Checklist
- [ ] Confirm the device **qualification** and reuse your **MDR Annex VIII class** (Rule 11 for software) under **MedDO Art. 15**.
- [ ] Pick the **conformity-assessment route (Art. 23)**; engage a **Swiss designated body** for class > I (Art. 24-28).
- [ ] Appoint a **CH-REP (Art. 51)** if your seat is outside Switzerland; register in swissdamed (see [[ch_rep_meddo]]).
- [ ] Set up **Swissmedic vigilance** reporting and post-market surveillance (see [[swiss_stack]]).
- [ ] Apply the SaMD lifecycle standards (IEC 62304 / ISO 14971 / IEC 62366-1 / ISO 13485) — see [[samd_standards]].

## Examples (mHealth)
- A Swiss-only insulin-dose-support app (Rule 11 → likely IIa/IIb) → MedDO applies;
  class taken from **MDR Annex VIII via Art. 15**, **Swiss designated body** for conformity,
  Swissmedic vigilance, and a **CH-REP** if the maker sits in the EU.
- An EU CE-marked symptom-triage app also sold in Switzerland → reuse the MDR class, but
  add the **MedDO/CH-REP** layer ([[ch_rep_meddo]]) and Swiss vigilance.
- A pure wellness app with no medical purpose → not a device under MedDO (stays
  [[iso_82304]] + data-protection rules).

## HERA dimensions touched
- **Device qualification & classification (Swiss)** · **Conformity assessment** · **Authority (Swissmedic)** · **Third-country / authorised representative**
- Cross-links: [[ch_rep_meddo]] (CH-REP & third-country), [[swiss_stack]] (Swissmedic vigilance + EPRA), [[mdr_class_iia]] (EU class equivalence), [[samd_standards]] (lifecycle standards), [[nlpd_sensitive]] (Swiss health-data regime)

## Official sources
- Fedlex — Medical Devices Ordinance (MedDO / ODim, SR 812.213): https://www.fedlex.admin.ch/eli/cc/2020/552/en
- Swissmedic — Medical devices, market access & CH-REP: https://www.swissmedic.ch/swissmedic/en/home/medical-devices/market-access/ch-rep.html
- EU MDR (Regulation (EU) 2017/745), Annex VIII (classification rules): https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32017R0745
