---
id: ai_act_fria
title: "EU AI Act — Fundamental Rights Impact Assessment (FRIA, Art. 27)"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng
key_articles: ["Art. 27", "Art. 26"]
status: rich-draft
---

# EU AI Act — Fundamental Rights Impact Assessment (FRIA, Art. 27)

## Why this concerns you (purpose)
The FRIA is the **deployer's** duty, not the maker's — but it shapes whether your
customer can buy at all. If your high-risk AI is deployed by a hospital, clinic,
health insurer or public body, **they** must run a Fundamental Rights Impact
Assessment before first use. In practice the burden lands on you too: procurement
teams will demand the inputs (intended purpose, affected groups, mitigation, oversight
design) from your documentation. Anticipating the FRIA turns a sales blocker into a
selling point.

## When it is triggered (scope)
Under **Art. 27**, a FRIA is required before first use of a **high-risk AI system**
(see [[ai_act_high_risk]]) where the **deployer** is:
- a **body governed by public law**, or a **private entity providing public services**
  (public **and** private **healthcare providers** are expressly covered); or
- a deployer of high-risk AI for **creditworthiness scoring** or **risk assessment and
  pricing in life/health insurance**.
It is the **customer-deployer's** obligation (linked to the Art. 26 deployer duties),
not the provider's — but it conditions adoption of your product.

## Concrete obligations
- **Describe** the deployer's processes in which the high-risk AI will be used and the
  period/frequency of use.
- **Identify** the categories of natural persons and groups likely to be affected.
- **Assess** the specific risks of harm to **fundamental rights**, and define
  **mitigation** measures and **human-oversight** arrangements (per Art. 14).
- **Notify** the market-surveillance authority of the FRIA results (using the
  template/questionnaire to be provided by the AI Office).
- A prior GDPR **DPIA** can be reused/complemented but does **not** replace the FRIA.

## Checklist
- [ ] Identify whether your buyers are public bodies / healthcare providers (FRIA-bound deployers).
- [ ] Package "FRIA-ready" inputs: intended purpose, affected persons, risks, mitigations, oversight.
- [ ] Map overlaps with the customer's GDPR DPIA so neither is duplicated nor skipped.
- [ ] Provide clear human-oversight instructions (Art. 14) the deployer can operationalise.

## Examples (mHealth)
- A public hospital deploying your AI triage SaMD must complete a FRIA and notify its
  authority before go-live; expect them to request your documentation.
- A private clinic offering publicly funded care deploys your AI risk-scoring tool: as a
  provider of public services, it is FRIA-bound.
- **Edge / negative case:** a purely B2C wellness chatbot sold to consumers has no public-body
  or public-service deployer, so no Art. 27 FRIA — though [[ai_act_transparency]] may still apply.

## HERA dimensions touched
- **AI governance** · **Deployer / customer obligations** · **Fundamental-rights risk**
- Cross-links: [[ai_act_high_risk]], [[ai_act_timeline]], [[gdpr_automated]]

## Official sources
- EUR-Lex — Regulation (EU) 2024/1689, Art. 27: https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng
- AI Act Service Desk — Art. 27 (Fundamental rights impact assessment): https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-27
