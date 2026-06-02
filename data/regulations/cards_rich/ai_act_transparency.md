---
id: ai_act_transparency
title: "EU AI Act — transparency obligations (Art. 50)"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202401689
key_articles: ["Art. 50"]
status: final
---

# EU AI Act — transparency obligations (Art. 50)

## Why this concerns you (purpose)
Even when your AI is **not** high-risk, Art. 50 still imposes a baseline of honesty:
people must know when they are talking to a machine, when they are being scanned by
an emotion- or biometric-categorisation system, and when content was made or altered
by AI. For an mHealth app — where users are often anxious patients — undisclosed AI
erodes trust and breaches the Act. These are *light-touch but mandatory* duties.

## When it is triggered (scope)
Triggered if your app (as **provider** or **deployer**) does any of:
- runs a **chatbot / conversational agent** that interacts directly with users;
- uses an **emotion-recognition** or **biometric-categorisation** system on users
  (common in mental-health, mood or stress-monitoring apps — see [[gdpr_biometric]]);
- **generates or substantially manipulates** content (synthetic text, image, audio,
  video / deepfakes), e.g. AI-written health summaries or generated illustrations.
Out of scope only where an explicit Art. 50 exemption applies (e.g. AI legally
authorised to detect/prevent crime).

## Concrete obligations
- **Chatbot disclosure:** inform users they are interacting with an AI system, unless
  it is obvious to a reasonably informed person.
- **Emotion-recognition / biometric-categorisation notice:** inform the exposed
  persons that the system is operating (and process biometric data per GDPR Art. 9).
- **AI-content marking:** mark AI-generated/manipulated outputs in a **machine-readable**
  format and ensure they are **detectable** as artificially generated.
- **Timing:** Art. 50 applies from **2 Aug 2026**. Per the 7 May 2026 Digital Omnibus
  *provisional* agreement, the grace period for the content-marking duty on systems
  already in service is shortened, with a compliance date of **2 Dec 2026** (treat as
  conditional until the Omnibus is in the OJ).

## Checklist
- [ ] Add a clear "you are chatting with an AI assistant" notice to any conversational feature.
- [ ] If you do mood/emotion/biometric inference, notify users and secure GDPR Art. 9 basis.
- [ ] Implement machine-readable marking (e.g. watermark/metadata) for AI-generated content.
- [ ] Diarise 2 Aug 2026 (and the 2 Dec 2026 content-marking grace date) for go-live readiness.

## Examples (mHealth)
- A mental-wellness companion chatbot must state up front that responses are AI-generated.
- A stress app inferring emotion from voice/face must notify users and meet biometric rules.
- **Edge case:** a purely rule-based reminder bot with no AI and no synthetic content is
  outside Art. 50 — but if a templated "AI tip" is actually LLM-generated, marking applies.

## HERA dimensions touched
- **AI governance** · **User transparency & trust** · **Biometric / sensitive-data interplay**
- Cross-links: [[ai_act_timeline]], [[gdpr_biometric]], [[ai_act_high_risk]]

## Official sources
- EUR-Lex — AI Act, Art. 50 (OJ L of 12 Jul 2024): https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202401689
- European Commission — Code of Practice on marking AI-generated content: https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content
