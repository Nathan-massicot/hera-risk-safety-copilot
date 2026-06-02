---
id: nis2_cyber
title: "NIS2 — cybersecurity & incident notification"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022L2555
key_articles: ["NIS2 Art. 21", "NIS2 Art. 23", "MDR Annex I §17"]
status: final
---

# NIS2 — cybersecurity & incident notification

## Why this concerns you (purpose)
NIS2 (Dir. (EU) 2022/2555) governs the **cybersecurity of your organisation**, not your
product. If you operate in the health sector as an **essential or important entity** —
healthcare providers, but also certain manufacturers of medical devices and providers of
digital health services — you must put in place **cyber risk-management measures** and
**notify significant incidents** to your national authority/CSIRT on a strict clock.
NIS2 is the **organisational counterpart** to the CRA's product rules (see [[cra]]) and
overlaps with the device-cybersecurity requirements of MDR Annex I §17: a SaMD maker can
face both the device security duties and NIS2 entity obligations at once.

## When it is triggered (scope)
Triggered when **all** of the following hold:
- you are an **entity** providing services in a NIS2 sector — **health** is listed
  (healthcare providers; also medical-device and IVD manufacturers as relevant);
- you meet the **size threshold** (generally medium/large) **or** are otherwise
  designated essential/important by a Member State;
- you provide services in / are established in the **EU**.

Note: classification as **essential** (proactive, ex-ante supervision) vs **important**
(ex-post supervision) changes the intensity of oversight, not the core duties.

## Concrete obligations
- Implement the **Art. 21 risk-management measures**: risk analysis & security policies,
  incident handling, business continuity/backup, supply-chain security, vulnerability
  handling/disclosure, encryption, access control, MFA — proportionate to risk.
- **Incident notification (Art. 23)** for significant incidents, in stages:
  **early warning within 24h**, **incident notification within 72h**, and a **final
  report within one month**.
- Ensure **management bodies approve and oversee** cyber risk measures (and can be held
  accountable); train staff.
- Register your entity with the competent national authority and align device-side
  controls with **MDR Annex I §17** where you make SaMD.

## Checklist
- [ ] Determine whether you are an essential/important entity (sector + size threshold) and register.
- [ ] Implement the Art. 21 measures (backup, supply-chain, vulnerability handling, MFA, encryption).
- [ ] Stand up an incident-response runbook hitting the **24h / 72h / 1-month** Art. 23 deadlines.
- [ ] Reconcile NIS2 controls with MDR Annex I §17 device cybersecurity and CRA product duties.

## Examples (mHealth)
- A telemedicine platform classed as an essential health entity suffers a ransomware
  outage → must send an early warning within 24h and a full notification within 72h.
- A medium-sized SaMD manufacturer → likely an important entity: must run the Art. 21
  programme even though its *product* security also sits under the CRA.
- A two-person wellness-app startup below the size threshold and not designated →
  generally outside NIS2 entity scope (but the CRA can still apply to its product).

## HERA dimensions touched
- **Organisational cybersecurity** · **Incident notification (24h/72h)** · **Supply-chain security**
- Cross-links: [[cra]] (product security counterpart, SBOM, vuln handling)

## Official sources
- EUR-Lex — Directive (EU) 2022/2555: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022L2555
- EUR-Lex (ELI) — Directive (EU) 2022/2555: https://eur-lex.europa.eu/eli/dir/2022/2555/oj/eng
