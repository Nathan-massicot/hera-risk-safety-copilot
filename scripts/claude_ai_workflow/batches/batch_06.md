# Batch 06

Paste this entire batch into the Claude.ai project chat. Claude should reply
with a single JSON object `{"dialogues": [...]}` containing **5 dialogues**.
Save Claude's reply (only the JSON) to `responses/batch_06.json`.

---

Produce **5 dialogues** for the following (archetype, dimensions) pairs.

For each dialogue:
- Use `metadata.archetype_id` = the id below.
- Use `metadata.covered_dimensions` = the dimension IDs from the list (you may add 1–2 adjacent if natural).
- Follow ALL quality rules from the project instructions.

### Dialogue 1 — `chemo_companion`

**Archetype.** Chemo treatment companion (`oncology`, uses_ai=False, data_sensitivity=high, vulnerable_pop=True, markets=EU).
**Description.** Tracks chemotherapy cycles, side effects, oral medication intake, and shares structured updates with the oncology nurse team.

**Dimensions to cover (7).**
- [P6.D5] Representativeness in Validation Studies: Were the studies validating the app conducted with representative populations?
- [P7.D7] Lifecycle & Documentation Management: Is the app's entire lifecycle documented and governed?
- [P3.D5] Automation Bias (AI and Non-AI): Do users or clinicians over-trust the app's outputs, even when they are wrong?
- [P7.D5] Post-Market Surveillance & Vigilance: Is there a system to monitor the app's safety and performance after launch?
- [P7.D2] CE Marking & MDR Conformity: If the app is a medical device, does it have the required CE marking?
- [P1.D6] System Dependency & Over-reliance: Could users become overly dependent on the app for health management?
- [P4.D2] Interoperability & Data Exchange: Can the app exchange data with other health systems (EHR, FHIR)?

### Dialogue 2 — `cbt_chatbot`

**Archetype.** CBT-based mood & anxiety chatbot (`mental-health`, uses_ai=True, data_sensitivity=high, vulnerable_pop=True, markets=EU, CH).
**Description.** Conversational LLM-powered companion delivering structured CBT exercises for mild-to-moderate anxiety, with crisis-keyword detection that escalates to a hotline.

**Dimensions to cover (4).**
- [P7.D7] Lifecycle & Documentation Management: Is the app's entire lifecycle documented and governed?
- [P2.D5] Anonymization & Right to Erasure: Can users have their data deleted, and is shared data properly anonymized?
- [P7.D4] GDPR Compliance (DPO, DPIA): Is the app fully compliant with GDPR requirements for health data?
- [P3.D5] Automation Bias (AI and Non-AI): Do users or clinicians over-trust the app's outputs, even when they are wrong?

### Dialogue 3 — `ai_derm`

**Archetype.** AI dermatology diagnosis from photo (`ai-clinical`, uses_ai=True, data_sensitivity=high, vulnerable_pop=False, markets=EU, CH).
**Description.** CNN classifies skin lesions as benign / suspicious / urgent; intended as a triage tool for primary-care physicians.

**Dimensions to cover (4).**
- [P4.D2] Interoperability & Data Exchange: Can the app exchange data with other health systems (EHR, FHIR)?
- [P5.D1] Understandable Output: Can users understand how the app produces its results or recommendations?
- [P7.D1] Medical Device Classification (SaMD): Is the app a Software as a Medical Device, and is it classified correctly?
- [P6.D4] Impact on Existing Health Inequalities: Could the app widen the gap between those who have good health access and those who do not?

### Dialogue 4 — `mh_telecons`

**Archetype.** Mental health teleconsultation (`telemedicine`, uses_ai=False, data_sensitivity=high, vulnerable_pop=True, markets=EU, CH).
**Description.** Video sessions with licensed psychotherapists; in-app journaling between sessions; records visible to the clinician.

**Dimensions to cover (6).**
- [P2.D2] Data Minimization: Does the app collect only the data strictly necessary for its function?
- [P1.D3] False Sense of Security: Could the app give users unwarranted confidence in their health status?
- [P4.D4] User-Centered Design & Usability Testing: Has the app been designed and tested with real end users?
- [P3.D2] Emotional Manipulation & Excessive Nudging: Does the app use persuasive techniques that could undermine autonomous decision-making?
- [P1.D2] Contraindications & Adverse Effects: Could the app cause harm to specific patient groups or in certain conditions?
- [P7.D2] CE Marking & MDR Conformity: If the app is a medical device, does it have the required CE marking?

### Dialogue 5 — `ai_triage`

**Archetype.** AI symptom checker / triage (`ai-clinical`, uses_ai=True, data_sensitivity=high, vulnerable_pop=False, markets=EU, CH).
**Description.** Patient enters symptoms; LLM-based triage suggests self-care, GP, or A&E. Disclaimer says 'not a medical device' — but probably is one.

**Dimensions to cover (5).**
- [P5.D2] Clear Communication of Limitations: Does the app clearly communicate what it cannot do?
- [P2.D5] Anonymization & Right to Erasure: Can users have their data deleted, and is shared data properly anonymized?
- [P3.D2] Emotional Manipulation & Excessive Nudging: Does the app use persuasive techniques that could undermine autonomous decision-making?
- [P6.D4] Impact on Existing Health Inequalities: Could the app widen the gap between those who have good health access and those who do not?
- [P1.D6] System Dependency & Over-reliance: Could users become overly dependent on the app for health management?


Now produce the JSON object with all 5 dialogues, in the same order.
