---
id: ch_rep_meddo
title: "MedDO — MDR third country & Swiss authorised representative (CH-REP)"
jurisdiction: CH
official_url: https://www.swissmedic.ch/swissmedic/en/home/medical-devices/market-access/ch-rep.html
key_articles: ["MedDO Art. 51(1)", "MedDO (SR 812.213)"]
status: final
---

# MedDO — MDR third country & Swiss authorised representative (CH-REP)

## Why this concerns you (purpose)
Most teams assume that holding a **CE mark** lets them sell into Switzerland. It does not, on
its own. Because the **EU–Switzerland Mutual Recognition Agreement (MRA) was never updated**
for the MDR, **Switzerland has been a third country for the MDR since 26 May 2021**. The direct
consequence: any manufacturer **without a registered seat in Switzerland — including EU/EEA
manufacturers** — must appoint a **Swiss authorised representative (CH-REP)** before placing a
device on the Swiss market. The relationship is **symmetric**: a Swiss manufacturer needs an
**EU authorised representative (EU-REP)** to sell into the EU. And because Switzerland is a third
country, **Swissmedic has no access to EUDAMED** — registration happens in the Swiss system.

## When it is triggered (scope)
Triggered as soon as **all** of the following hold:
- your product is (or could be) a **medical device / SaMD** under MedDO ([[swiss_stack]]);
- it is **placed on the Swiss market**;
- your manufacturer's **registered seat is outside Switzerland** (EU/EEA included).

The transition periods that once staggered the CH-REP obligation by risk class have **lapsed**,
so the requirement now applies across classes. The mirror case — a **Swiss-seated** manufacturer
selling into the EU — triggers the **EU-REP** requirement instead.

## Concrete obligations
- Appoint a **CH-REP** under **Art. 51(1) MedDO** with a written mandate; the CH-REP carries the
  formal and safety-related responsibilities of placing the device on the Swiss market.
- Put the CH-REP **name and address on the device/labelling** (the symbol or the wording
  "CH-REP" / "CH authorised representative"); a P.O. box, e-mail or phone number alone is **not** sufficient.
- **Register** the actors and the device in the Swiss database (**swissdamed**) and obtain the
  Swiss registration number (**CHRN**) — you cannot rely on an EUDAMED registration.
- For a Swiss manufacturer targeting the EU, appoint an **EU-REP** symmetrically (MDR Art. 11).
- Keep EU EUDAMED and Swiss swissdamed registrations **separate** — they do not interoperate;
  see [[udi_eudamed]] for the EU side.

## Checklist
- [ ] Determine your manufacturer's registered seat (in CH vs outside CH).
- [ ] If outside CH, sign a CH-REP mandate (Art. 51(1) MedDO) before any Swiss placement.
- [ ] Add the CH-REP name + address to labelling/IFU; register in **swissdamed** and obtain the CHRN.
- [ ] If Swiss-seated and selling into the EU, appoint an EU-REP and register in EUDAMED ([[udi_eudamed]]).
- [ ] Do not treat an EUDAMED entry as covering Switzerland — Swissmedic cannot see it.

## Examples (mHealth)
- A French Class IIa SaMD publisher selling in Switzerland → needs a **CH-REP** and a swissdamed/CHRN
  registration, even though it is fully MDR-compliant and EUDAMED-registered in the EU.
- A **Zurich-based** SaMD startup selling into Germany → needs an **EU-REP** (mirror obligation), not a CH-REP.
- A US wellness-only app with **no medical-device claim** and no Swiss device placement → **no CH-REP**
  needed under MedDO (the obligation attaches to medical devices, not to every app).

## HERA dimensions touched
- **Swiss market access** · **Economic operators / representation** · **Device registration**
- Cross-links: [[swiss_stack]], [[udi_eudamed]]

## Official sources
- Swissmedic — Swiss authorised representative (CH-REP): https://www.swissmedic.ch/swissmedic/en/home/medical-devices/market-access/ch-rep.html
- Swissmedic — Registering economic operators (CHRN): https://www.swissmedic.ch/swissmedic/en/home/medical-devices/market-access/registriernummer-chrn.html
- Fedlex — MedDO / Medical Devices Ordinance (SR 812.213): https://www.fedlex.admin.ch/eli/cc/2020/552/en
