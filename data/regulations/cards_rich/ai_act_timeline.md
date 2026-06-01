---
id: ai_act_timeline
title: "EU AI Act — staggered application timeline (+ Digital Omnibus)"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng
key_articles: ["Art. 113 (date of application)", "Art. 5", "Art. 4", "Art. 50", "Digital Omnibus 2025/2026"]
status: rich-draft
---

# EU AI Act — staggered application timeline (+ Digital Omnibus)

## Why this concerns you (purpose)
The EU AI Act (Regulation (EU) 2024/1689) does **not** apply all at once. It entered
into force on 1 Aug 2024 and switches on in **waves** through 2027-2028. If your
mHealth app uses AI, the only way to know what you must do *today* versus what is
merely *coming* is to read the calendar. Getting this wrong cuts both ways: you may
panic-build for obligations that are still deferred, or — worse — overlook the
prohibitions and GPAI rules that are **already binding right now**.

## When it is triggered (scope)
Triggered as soon as your app **uses any AI system or general-purpose AI model**
placed on the EU market or whose output is used in the EU. The relevant date then
depends on *which* obligation:
- **prohibited practices** (Art. 5) and **AI literacy** (Art. 4) — the earliest wave;
- **GPAI model** obligations (Chapter V) — second wave;
- **transparency** (Art. 50) and **high-risk** (Annex III, Art. 9-15) — later waves,
  partly affected by the pending Digital Omnibus.

## Concrete obligations
- **Since 2 Feb 2025** — Art. 5 prohibitions (e.g. certain emotion recognition,
  social scoring, exploitative manipulation) and the Art. 4 AI-literacy duty are
  **already in force and enforceable**.
- **Since 2 Aug 2025** — obligations on **GPAI model providers** (Art. 53/55) apply;
  the GPAI Code of Practice was published 10 Jul 2025.
- **2 Aug 2026** — **Art. 50 transparency** obligations apply (chatbot disclosure,
  AI-content marking; see [[ai_act_transparency]]).
- **CAUTION — pending change:** the **Digital Omnibus** reached only a *provisional
  political agreement on 7 May 2026* and is **NOT yet adopted / not yet in the OJ**.
  *If* adopted as agreed, it **would** defer standalone **Annex III high-risk**
  obligations from 2 Aug 2026 to **2 Dec 2027**, and AI **embedded in a regulated
  product** (e.g. a medical device) to **2 Aug 2028**. Treat these later dates as
  *conditional* until publication in the Official Journal.

## Checklist
- [ ] Confirm none of your AI features fall under the Art. 5 prohibitions (binding now).
- [ ] Verify the Art. 4 AI-literacy measures cover your staff and relevant users.
- [ ] If you rely on an LLM, check the provider met its GPAI duties (binding since Aug 2025).
- [ ] Plan Art. 50 transparency for 2 Aug 2026 — do not bank on the Omnibus deferral.
- [ ] Track the Digital Omnibus until it appears in the OJ before relying on 2027/2028 dates.

## Examples (mHealth)
- A symptom-checker chatbot must already respect Art. 5 (no manipulative design) and
  Art. 4 literacy; its Art. 50 chatbot-disclosure duty lands on 2 Aug 2026.
- A diagnostic SaMD using AI is Annex III high-risk: its full Art. 9-15 obligations
  would, *if* the Omnibus is adopted, shift to 2 Aug 2028 (embedded in a CE-marked device).
- **Edge case:** a team assumes "nothing applies until 2026" and ships an emotion-recognition
  wellness feature — wrong: the Art. 5 restriction has bound them since 2 Feb 2025.

## HERA dimensions touched
- **AI governance** · **Regulatory calendar / readiness** · **EU market access**
- Cross-links: [[ai_act_high_risk]], [[ai_act_transparency]], [[ai_act_gpai_provider]], [[ai_act_gpai_downstream]]

## Official sources
- EUR-Lex — Regulation (EU) 2024/1689 (AI Act): https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng
- European Commission — AI Act overview & timeline: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
