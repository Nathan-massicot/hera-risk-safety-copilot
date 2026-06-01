---
id: swiss_stack
title: "Swiss stack (MedDO + Swissmedic + EPRA)"
jurisdiction: CH
official_url: https://www.fedlex.admin.ch/eli/cc/2020/552/en
key_articles: ["MedDO (SR 812.213)", "Swissmedic vigilance (MIR)", "EPRA"]
status: rich-draft
---

# Swiss stack (MedDO + Swissmedic + EPRA)

## Why this concerns you (purpose)
If you place your mHealth app on the Swiss market, you do **not** inherit EU compliance
automatically. Switzerland runs a **parallel regulatory stack**: the **MedDO/ODim**
(Medical Devices Ordinance, SR 812.213 — the MDR-equivalent), **Swissmedic** as the
competent authority and vigilance regulator, and the **EPRA/EPDG** electronic-patient-record
framework. Crucially, Switzerland is **not directly bound by the EU AI Act or the EHDS** —
those EU instruments do not extend across the border. Treating "CE-marked = Swiss-compliant"
is the classic mistake: it gets you most of the technical content, but none of the Swiss-specific
actor, registration and vigilance duties.

## When it is triggered (scope)
Triggered as soon as **any** of the following holds:
- you place a **medical device / SaMD** (per MedDO, which mirrors MDR qualification rules) on the **Swiss market**;
- you carry out **vigilance / post-market** activity for a device made available in Switzerland or Liechtenstein;
- you connect to or feed the **Swiss electronic patient record (EPR/EPD)** under the EPRA/EPDG.

It applies **on top of** Swiss data-protection law (the nFADP), not instead of it — combine this
card with [[nlpd_base]] and, for automated decisions / high-risk processing, [[nlpd_automated_dpia]].

## Concrete obligations
- Qualify and class your software under **MedDO (SR 812.213)**, which transposes the MDR
  substance (Rule 11, GSPR, technical documentation) into Swiss law.
- Operate **Swissmedic vigilance**: serious incidents occurring in **Switzerland or Liechtenstein**
  are reported to Swissmedic on the **Manufacturer Incident Report (MIR)** form — note that
  **MIR version 7.3.1 becomes mandatory for Swissmedic notifications from 1 May 2026**.
- Appoint the Swiss-specific actors when your seat is outside Switzerland (Swiss authorised
  representative / CH-REP, importer duties) — see [[ch_rep_meddo]].
- If you integrate with the Swiss **EPR**, track the **EPRA/EPDG full revision**: the bill was
  submitted to **Parliament on 5 November 2025** and moves the EPR toward an **opt-out** model
  with mandatory professional use, targeted to enter into force **around 2028 at the earliest**.
  See [[national_ehealth]].

## Checklist
- [ ] Confirm MedDO qualification/classification and keep the technical file Swiss-ready (SR 812.213).
- [ ] Set up a Swissmedic vigilance process and adopt the **MIR 7.3.1** form before **1 May 2026**.
- [ ] Verify whether a CH-REP and Swiss registration are required for your seat ([[ch_rep_meddo]]).
- [ ] Pair this stack with Swiss data-protection duties ([[nlpd_base]], [[nlpd_automated_dpia]]).
- [ ] Do **not** assume EU AI Act / EHDS apply in Switzerland — treat them as separate from this stack.

## Examples (mHealth)
- A German-made diabetes SaMD sold in Switzerland → must meet MedDO, appoint a CH-REP, and
  report any serious incident in Switzerland to Swissmedic via the MIR form.
- A Swiss telemonitoring app whose serious incident in Geneva occurs in **April 2026** → may still
  use the legacy MIR form, but from **1 May 2026** must switch to MIR 7.3.1 for Swissmedic.
- A **pure wellness** step-counter with no medical purpose and no Swiss device claim → **out of the
  MedDO/Swissmedic limb** of this stack (still subject to the nFADP if it processes Swiss data).

## HERA dimensions touched
- **Swiss market access** · **Medical-device qualification** · **Vigilance & post-market** · **National eHealth**
- Cross-links: [[ch_rep_meddo]], [[nlpd_base]], [[nlpd_automated_dpia]], [[national_ehealth]]

## Official sources
- Fedlex — MedDO / Medical Devices Ordinance (SR 812.213): https://www.fedlex.admin.ch/eli/cc/2020/552/en
- Swissmedic — Swiss authorised representative (CH-REP): https://www.swissmedic.ch/swissmedic/en/home/medical-devices/market-access/ch-rep.html
- eHealth Suisse — current status of the EPR (EPRA/EPDG revision): https://www.e-health-suisse.ch/en/coordination/electronic-patient-record/de-aktueller-stand
