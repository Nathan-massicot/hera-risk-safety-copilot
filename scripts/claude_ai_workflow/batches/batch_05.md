# Batch 05

Paste this entire batch into the Claude.ai project chat. Claude should reply
with a single JSON object `{"dialogues": [...]}` containing **5 dialogues**.
Save Claude's reply (only the JSON) to `responses/batch_05.json`.

---

Produce **5 dialogues** for the following (archetype, dimensions) pairs.

For each dialogue:
- Use `metadata.archetype_id` = the id below.
- Use `metadata.covered_dimensions` = the dimension IDs from the list (you may add 1–2 adjacent if natural).
- Follow ALL quality rules from the project instructions.

### Dialogue 1 — `contraception_pill`

**Archetype.** Contraception pill reminder (`reproductive`, uses_ai=False, data_sensitivity=medium, vulnerable_pop=False, markets=EU, CH).
**Description.** Daily reminder + miss-tracking + emergency contraception guidance; integrates with the user's calendar.

**Dimensions to cover (7).**
- [P7.D5] Post-Market Surveillance & Vigilance: Is there a system to monitor the app's safety and performance after launch?
- [P6.D3] Cross-Cultural & Multilingual Validation: Has the app been validated across cultures and languages?
- [P1.D2] Contraindications & Adverse Effects: Could the app cause harm to specific patient groups or in certain conditions?
- [P4.D1] App Stability & Error Handling: Does the app handle failures gracefully without risking patient safety?
- [P3.D1] Right to Make Decisions: Does the app respect the patient's right to make their own health decisions?
- [P1.D3] False Sense of Security: Could the app give users unwarranted confidence in their health status?
- [P7.D1] Medical Device Classification (SaMD): Is the app a Software as a Medical Device, and is it classified correctly?

### Dialogue 2 — `contraception_pill`

**Archetype.** Contraception pill reminder (`reproductive`, uses_ai=False, data_sensitivity=medium, vulnerable_pop=False, markets=EU, CH).
**Description.** Daily reminder + miss-tracking + emergency contraception guidance; integrates with the user's calendar.

**Dimensions to cover (5).**
- [P2.D2] Data Minimization: Does the app collect only the data strictly necessary for its function?
- [P7.D7] Lifecycle & Documentation Management: Is the app's entire lifecycle documented and governed?
- [P2.D3] Storage, Encryption & Security: Is personal health data properly secured at rest and in transit?
- [P1.D3] False Sense of Security: Could the app give users unwarranted confidence in their health status?
- [P7.D2] CE Marking & MDR Conformity: If the app is a medical device, does it have the required CE marking?

### Dialogue 3 — `ai_triage`

**Archetype.** AI symptom checker / triage (`ai-clinical`, uses_ai=True, data_sensitivity=high, vulnerable_pop=False, markets=EU, CH).
**Description.** Patient enters symptoms; LLM-based triage suggests self-care, GP, or A&E. Disclaimer says 'not a medical device' — but probably is one.

**Dimensions to cover (6).**
- [P7.D4] GDPR Compliance (DPO, DPIA): Is the app fully compliant with GDPR requirements for health data?
- [P1.D3] False Sense of Security: Could the app give users unwarranted confidence in their health status?
- [P4.D3] Accessibility (WCAG, Literacy, Language): Is the app usable by people with disabilities, low literacy, or different languages?
- [P5.D1] Understandable Output: Can users understand how the app produces its results or recommendations?
- [P1.D5] Measurement Reliability: Are the measurements and data captured by the app accurate and reliable?
- [P7.D2] CE Marking & MDR Conformity: If the app is a medical device, does it have the required CE marking?

### Dialogue 4 — `menopause`

**Archetype.** Menopause symptom tracker (`reproductive`, uses_ai=False, data_sensitivity=medium, vulnerable_pop=False, markets=EU).
**Description.** Logs hot flashes, mood, sleep quality; offers educational content about HRT and lifestyle; sells anonymized symptom data to a pharma partner.

**Dimensions to cover (4).**
- [P2.D5] Anonymization & Right to Erasure: Can users have their data deleted, and is shared data properly anonymized?
- [P6.D3] Cross-Cultural & Multilingual Validation: Has the app been validated across cultures and languages?
- [P7.D2] CE Marking & MDR Conformity: If the app is a medical device, does it have the required CE marking?
- [P2.D4] Third-Party Data Sharing: Is health data shared with third parties, and are users aware of this?

### Dialogue 5 — `epilepsy_logger`

**Archetype.** Epilepsy seizure logger (`chronic-condition`, uses_ai=False, data_sensitivity=high, vulnerable_pop=True, markets=EU).
**Description.** Seizure event logging with caregiver alerts via SMS; aggregates data for the patient's neurologist visit.

**Dimensions to cover (4).**
- [P1.D5] Measurement Reliability: Are the measurements and data captured by the app accurate and reliable?
- [P7.D6] Third-Party Audit & Certification: Has the app been independently audited or certified?
- [P3.D2] Emotional Manipulation & Excessive Nudging: Does the app use persuasive techniques that could undermine autonomous decision-making?
- [P7.D5] Post-Market Surveillance & Vigilance: Is there a system to monitor the app's safety and performance after launch?


Now produce the JSON object with all 5 dialogues, in the same order.
