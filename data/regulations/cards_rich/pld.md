---
id: pld
title: "PLD — Product Liability Directive (software & AI)"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024L2853
key_articles: ["Art. 4", "Art. 7", "Art. 9", "Art. 10"]
status: final
---

# PLD — Product Liability Directive (software & AI)

## Why this concerns you (purpose)
The revised Product Liability Directive (Dir. (EU) 2024/2853, replacing 85/374/EEC)
makes **software and AI systems explicitly "products"**. That means if your mHealth
app, SaMD or AI model causes harm — physical injury, a damaged health outcome, even
data corruption — an injured person can claim compensation under a **no-fault (strict
liability)** regime: they do **not** have to prove you were negligent, only that the
product was **defective** and caused the damage. Crucially, the directive **eases the
burden of proof** for claimants in technically complex cases (presumption of
defectiveness/causation) and lets courts **order you to disclose evidence**. A missing
required security update or a wrong AI output can each be a "defect". Transposition is
due by **9 December 2026**, applying to products placed on the market after that date.

## When it is triggered (scope)
Triggered when **all** of the following hold:
- you place on the EU market (or put into service) **software, an AI system, or a
  digital product** — including firmware, apps and SaMD — **after 9 Dec 2026**;
- the product can be **defective** (does not provide the safety a person is entitled to,
  considering use, foreseeable misuse, and required updates);
- the defect **causes damage** to a natural person (death, personal injury, certain
  property damage, or destruction/corruption of data not used professionally).

Edge: harm a *deployer* or *user* causes through their own misuse, unconnected to a
defect, is not your strict-liability exposure — but inadequate instructions or a failure
to supply security updates can themselves make the product defective.

## Concrete obligations
- This is a **liability** regime, not a CE-marking checklist: the duties are practical
  risk-reduction and evidence readiness.
- Treat **failure to provide required security updates/upgrades** as a potential defect —
  align your update commitments with the CRA support period (see [[cra]]).
- Keep robust **technical documentation, logs and risk records** — courts can order
  disclosure, and gaps can trigger a **presumption of defectiveness** against you.
- Consider product-liability **insurance** and clear allocation of responsibility across
  your supply chain (component makers, model providers, integrators).

## Checklist
- [ ] Inventory which of your products will be "placed on the market after 9 Dec 2026" (in scope).
- [ ] Document defect-avoidance: risk management, change logs, security-update commitments.
- [ ] Ensure you can produce evidence on demand (disclosure duty) to rebut the eased-proof presumptions.
- [ ] Review insurance + contractual liability allocation with component and AI-model suppliers.

## Examples (mHealth)
- A dosing-support app that recommends an unsafe insulin dose because of a defect →
  the injured patient can claim under strict liability without proving fault.
- An AI triage assistant that misclassifies an emergency due to a flawed update →
  the defective update can ground PLD liability; weak logs trigger the proof presumption.
- A wellness step-counter with a cosmetic UI bug causing no injury or data loss →
  no recoverable damage, so no PLD claim arises.

## HERA dimensions touched
- **Product liability & defect exposure** · **Evidence/documentation readiness** · **AI accountability**
- Cross-links: [[cra]] (missing security update = potential defect), [[ai_act_high_risk]] (defective AI output)

## Official sources
- EUR-Lex — Directive (EU) 2024/2853: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024L2853
- EUR-Lex (ELI) — Directive (EU) 2024/2853: https://eur-lex.europa.eu/eli/dir/2024/2853/oj/eng
