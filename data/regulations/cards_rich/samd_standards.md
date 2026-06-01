---
id: samd_standards
title: "SaMD lifecycle standards (IEC 62304, ISO 14971, IEC 62366-1, ISO 13485)"
jurisdiction: EU/CH
official_url: https://single-market-economy.ec.europa.eu/single-market/goods/european-standards/harmonised-standards/medical-devices_en
key_articles: ["MDR Annex I (GSPR)", "IEC 62304", "ISO 14971", "IEC 62366-1", "ISO 13485"]
status: rich-draft
---

# SaMD lifecycle standards (IEC 62304, ISO 14971, IEC 62366-1, ISO 13485)

## Why this concerns you (purpose)
Once your app is a medical device — at **any** MDR class ([[mdr_class_i]] →
[[mdr_class_iii]]) or as IVD software ([[ivdr_class]]) — you must show it meets the
**General Safety & Performance Requirements** (MDR/IVDR Annex I). You don't prove that
from scratch: you **apply a recognised set of standards** that the Notified Body and
auditors expect. These four are the backbone of every SaMD technical file. Skipping them
is the fastest way to fail an audit; applying them is how "we built it carefully" becomes
**demonstrable conformity**.

## When it is triggered (scope)
Triggered for **any classified SaMD or IVD-MDSW**, regardless of class. The four
standards play distinct, complementary roles:
- **IEC 62304** — medical-device **software lifecycle** (planning, requirements,
  architecture, verification, maintenance, problem resolution; software safety classes A/B/C).
- **ISO 14971** — **risk management** across the whole lifecycle (risk analysis,
  controls, benefit-risk, post-production monitoring).
- **IEC 62366-1** — **usability engineering** (design out use-errors that could harm).
- **ISO 13485** — the **quality management system** wrapping all of the above.

## Concrete obligations
- **Harmonisation status matters:** **ISO 14971** (risk) and **ISO 13485** (QMS) are
  **harmonised under MDR** — applying them gives a *presumption of conformity*.
- **IEC 62304** and **IEC 62366-1** are **not formally harmonised** but are accepted as
  **state of the art** (MDCG 2021-5 logic): Notified Bodies expect the **current edition**
  even absent harmonisation. (A revised IEC 62304 edition is expected ~Sep 2026 — track it.)
- Maintain a **traceable chain**: ISO 14971 risks → IEC 62304 software requirements/verification
  → IEC 62366-1 usability validation, all governed by the ISO 13485 QMS.
- Feed this evidence into the **clinical evaluation/performance evaluation**
  ([[clinical_eval_mdsw]]) and the **technical file** for the relevant class.
- Keep it **live** post-market: changes, CAPAs and vigilance loop back through the QMS
  and risk file ([[pms_lifecycle]]).

## Checklist
- [ ] Stand up an ISO 13485 QMS (or document a roadmap to it) sized to your class.
- [ ] Maintain an ISO 14971 risk-management file linked to design controls.
- [ ] Run IEC 62304 lifecycle activities at the correct software safety class (A/B/C).
- [ ] Complete IEC 62366-1 usability engineering incl. summative evaluation.
- [ ] Verify you cite the **current** editions (watch the upcoming IEC 62304 revision).

## Examples (mHealth)
- A Class IIa triage app: IEC 62304 (safety class likely B/C), ISO 14971 risk file,
  IEC 62366-1 usability study, all under an ISO 13485 QMS → audit-ready technical file.
- An IVD-MDSW genetic-risk app ([[ivdr_class]]) uses the **same four standards** to meet
  the IVDR Annex I GSPR — the standards are device-type-agnostic.
- **Edge/negative:** a **wellness** app (no medical purpose) is **not** obliged to apply
  these for conformity — it should look to [[iso_82304]] instead; borrowing ISO 14971
  risk discipline is good practice but not a regulatory requirement there.

## HERA dimensions touched
- **Standards & conformity evidence** · **QMS / lifecycle / risk / usability** · **Audit readiness**
- Cross-links: [[mdr_class_i]] · [[mdr_class_iia]] · [[mdr_class_iib]] · [[mdr_class_iii]] ·
  [[ivdr_class]] · [[clinical_eval_mdsw]] · [[pms_lifecycle]] · [[iso_82304]]

## Official sources
- European Commission — harmonised standards for medical devices (MDR): https://single-market-economy.ec.europa.eu/single-market/goods/european-standards/harmonised-standards/medical-devices_en
- IEC 62304 — medical device software life-cycle processes: https://www.iso.org/standard/38421.html
- ISO 14971:2019 — risk management for medical devices: https://www.iso.org/standard/72704.html
