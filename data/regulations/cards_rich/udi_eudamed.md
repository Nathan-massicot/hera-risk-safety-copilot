---
id: udi_eudamed
title: "UDI & EUDAMED registration"
jurisdiction: EU
official_url: https://health.ec.europa.eu/medical-devices-eudamed/overview_en
key_articles: ["MDR Art. 27-31 (UDI)", "MDR Art. 33-34 (EUDAMED)", "Decision (EU) 2025/2371", "Regulation (EU) 2024/1860"]
status: rich-draft
---

# UDI & EUDAMED registration

## Why this concerns you (purpose)
If you place a CE-marked SaMD on the EU market, the device and **you, the
manufacturer**, must be traceable in the EU's central database. The MDR requires
a **Unique Device Identifier (UDI)** so any device can be tracked from production
to use, and registration in **EUDAMED** (the European Database on Medical Devices)
so authorities, notified bodies and the public can see who placed what on the
market. Until now EUDAMED use was largely **voluntary** — that ends in 2026: skip
registration after the deadline and your device is no longer lawfully on the market.

## When it is triggered (scope)
Triggered as soon as **both** hold:
- you place a **CE-marked medical device / SaMD** (any class) on the EU market, or
  you are an importer, authorised representative, system/procedure-pack producer,
  or sponsor of a clinical investigation;
- the device is intended for the **EU/EEA market** (not pure R&D or non-EU export).

It applies to **software regardless of risk class** (even Class I self-certified)
and **even to legacy MDD devices** still benefiting from the transition period
([[mdr_transition]]). It does **not** make your device traceable on the Swiss
market — Switzerland is a third country and uses its own swissdamed; EUDAMED is
inaccessible to Swissmedic ([[swiss_stack]]).

## Concrete obligations
- Obtain a **Basic UDI-DI** (the key device-model identifier used in EUDAMED and
  documentation) and a **UDI-DI** for each commercial version/configuration of the
  software, plus a **UDI-PI** (production identifier, e.g. software version).
- Register as an **economic operator** first: obtain a Single Registration Number
  (**SRN**) via the Actor registration module.
- Register the **device** in the UDI/Device module **before** placing it on the
  market. The **first four modules become mandatory on 28 May 2026** (Decision (EU)
  2025/2371, published 27 Nov 2025, triggering the 6-month period under Reg. (EU)
  2024/1860): Actor registration, UDI/Device, Notified Bodies & Certificates, and
  Market Surveillance.
- **Devices already on the market** before 28 May 2026 must be registered by
  **28 November 2026** (12 months after the notice).
- For software, assign a **new UDI-DI** on a significant change and a **new UDI-PI**
  on each new version per the device's change-control rules.

## Checklist
- [ ] Obtain your Basic UDI-DI and per-version UDI-DI/UDI-PI from an issuing entity (e.g. GS1, HIBCC).
- [ ] Register as an actor and secure your SRN well before 28 May 2026.
- [ ] Register every device in the UDI/Device module before placing it on the EU market.
- [ ] Diarise the 28 Nov 2026 backlog deadline for devices already on the market.
- [ ] Wire UDI assignment into your release/versioning process (new version -> new UDI-PI).

## Examples (mHealth)
- A Class IIa diabetes-management app newly CE-marked in 2026 -> obtain Basic UDI-DI
  + UDI-DI, register as actor (SRN), and register the device before launch
  ([[mdr_class_iia]]).
- A legacy MDD symptom-checker app on the market since 2020 under the transition
  -> still needs an SRN and must be EUDAMED-registered by 28 November 2026.
- A purely Swiss teleconsultation SaMD with **no** EU placement -> out of EUDAMED
  scope; it registers in swissdamed instead, not EUDAMED.

## HERA dimensions touched
- **Traceability & registration** · **EU market access** · **Lifecycle/versioning**
- Cross-links: [[mdr_class_iia]] (per-class registration), [[pms_lifecycle]] (vigilance feeds Market Surveillance), [[mdr_transition]] (legacy backlog)

## Official sources
- European Commission — EUDAMED overview: https://health.ec.europa.eu/medical-devices-eudamed/overview_en
- European Commission — "EUDAMED four first modules mandatory from 28 May 2026" (27 Nov 2025): https://health.ec.europa.eu/latest-updates/eudamed-four-first-modules-will-be-mandatory-use-28-may-2026-2025-11-27_en
