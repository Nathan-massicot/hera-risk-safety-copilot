---
id: telehealth_national
title: "Telehealth — national health codes"
jurisdiction: EU/CH
official_url: https://www.gesetze-im-internet.de/sgb_5/__33a.html
key_articles: ["PHC L1110-4", "PHC L4131-1", "MedPA", "SGB V §33a", "StGB §203", "SGB V §360", "ÄrzteG §54", "GTelG 2012"]
status: final
---

# Telehealth — national health codes

## Why this concerns you (purpose)
The moment your app lets a patient consult, be remotely monitored by, or exchange
clinical information with a **healthcare professional (HCP)**, you stop being "just an
app" and start operating inside the **practice-of-medicine** rules of each country.
These rules are national (not harmonised by the MDR or GDPR): they govern **who may
treat**, **medical confidentiality**, **informed consent for the remote act**, and
**how long the medical record must be kept**. Breaching them can void the lawfulness of
the care act itself — independently of your CE marking or GDPR posture.

## When it is triggered (scope)
Triggered as soon as your product **mediates a regulated health act**, e.g.:
- **teleconsultation** (a doctor consults a patient at a distance);
- **tele-expertise** (one HCP seeks the opinion of another);
- **remote monitoring / télésurveillance** of a patient by an HCP;
- **e-prescription** or transmission of medical results to/from an HCP.

It is **not** triggered by a pure self-care/wellness app with **no HCP in the loop**
(those stay under wellness + GDPR rules). A patient-facing symptom diary that no
clinician ever reads does not, by itself, trigger the telehealth regime.

## Concrete obligations
- **France** — medical confidentiality (PHC **Art. L1110-4**) covers *all* information
  known to anyone in contact with the care activity; teleconsultation must respect the
  acts framework (PHC **Art. L4131-1** for the practice of medicine, plus the
  télémédecine articles **R6316-1 et seq.**): HCP identification, patient information
  and consent, and traceability of the act in the record.
- **Retention** — the patient record must be kept **20 years** from the last
  stay/consultation (PHC **Art. R1112-7**), extended to the patient's 28th birthday for
  minors, and at least 10 years from death.
- **Switzerland** — the practice of medicine is governed by the **Medical Professions
  Act (MedPA / MedBG-LPMéd)** plus cantonal health laws; the **FMH professional rules
  (rev. 2023)** explicitly allow remote consultation provided the duties to **inform**
  and to **document** are met. Medical secrecy is protected (Swiss Criminal Code Art.
  321); patient records are generally kept **~20 years** (post-2020 limitation reform;
  some cantons/EPR rules differ).
- **Germany** — statutory health insurance and digital care sit in **SGB V**, including
  **§33a SGB V** (reimbursable digital health applications, *DiGA* — "app auf Rezept",
  with the BfArM directory under §139e) and the telemedicine/Telematikinfrastruktur rules
  (**§306 SGB V** defines the TI; **§360 SGB V** governs the **e-prescription / eRezept**,
  mandatory since 2024). Medical confidentiality is criminally protected by
  **§203 StGB** (*Verletzung von Privatgeheimnissen*); breaching it is punishable by up
  to one year's imprisonment or a fine. Connecting to the TI requires the gematik-issued
  HCP/institution identity (eHBA/SMC-B).
- **Austria** — physician confidentiality is set by **§54 Ärztegesetz 1998** (*Verschwiegenheitspflicht*;
  breach sanctioned via §121 StGB) and documentation/retention by **§51 ÄrzteG 1998**
  (medical records kept **≥10 years** in private practice, **30 years** for hospitals).
  Telehealth data exchange runs under the **Gesundheitstelematikgesetz 2012 (GTelG 2012,
  BGBl I 111/2012)**, which frames secure transmission of health data and the ELGA
  infrastructure (see [[national_ehealth]]).
- Keep an auditable **act log** (who, when, what) and a lawful **identification** of
  both patient and HCP (see [[eidas2]]).

## Checklist
- [ ] Map every act your app mediates to a regulated category (teleconsultation, télé-expertise, télésurveillance, e-prescription).
- [ ] Confirm only duly-registered HCPs can perform the act, with verified identity.
- [ ] Implement confidentiality + access controls per PHC L1110-4 / Swiss medical secrecy.
- [ ] Set record retention to 20 years (FR R1112-7) and document your CH cantonal basis.
- [ ] Log each act (HCP, patient, timestamp, content) for traceability and audit.

## Examples (mHealth)
- A teleconsultation app connecting French patients to GPs → full telehealth regime:
  HCP identification, L1110-4 confidentiality, consent for the remote act, 20-year record.
- A diabetes **télésurveillance** app where a nurse reviews glucose trends and adjusts
  follow-up → regulated remote-monitoring act (and may trigger reimbursement, see
  [[pecan_france]] LATM pathway).
- A meditation/sleep app with **no clinician** ever reviewing data → out of the telehealth
  regime (stays wellness + GDPR); confidentiality rules don't attach to a care act.

## HERA dimensions touched
- **Clinical act & professional rules** · **Medical confidentiality** · **Record retention** · **National market access**
- Cross-links: [[hds_certification]] (FR health-data hosting), [[national_ehealth]] (record interop), [[eidas2]] (HCP/patient identification), [[pecan_france]] (remote-monitoring reimbursement)

## Official sources
- Légifrance — Public Health Code (consolidated): https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006072665/
- Légifrance — PHC Art. L1110-4 (medical confidentiality): https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043895798
- Légifrance — PHC Art. R1112-7 (20-year record retention): https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036658351
- Fedlex — Swiss Medical Professions Act (MedBG/LPMéd): https://www.fedlex.admin.ch/eli/cc/2007/537/en
- gesetze-im-internet.de — §33a SGB V (DiGA): https://www.gesetze-im-internet.de/sgb_5/__33a.html
- gesetze-im-internet.de — §360 SGB V (eRezept) / §306 SGB V (Telematikinfrastruktur): https://www.gesetze-im-internet.de/sgb_5/__360.html
- gesetze-im-internet.de — §203 StGB (medical confidentiality): https://www.gesetze-im-internet.de/stgb/__203.html
- RIS — §54 Ärztegesetz 1998 (confidentiality): https://www.ris.bka.gv.at/eli/bgbl/i/1998/169/P54/NOR40080323
- RIS — Gesundheitstelematikgesetz 2012 (GTelG 2012): https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=Bundesnormen&Gesetzesnummer=20008120
