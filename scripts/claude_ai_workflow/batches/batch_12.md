# Batch 12

Paste this entire batch into the Claude.ai project chat. Claude should reply
with a single JSON object `{"dialogues": [...]}` containing **5 dialogues**.
Save Claude's reply (only the JSON) to `responses/batch_12.json`.

---

Produce **5 dialogues** for the following (archetype, dimensions) pairs.

For each dialogue:
- Use `metadata.archetype_id` = the id below.
- Use `metadata.covered_dimensions` = the dimension IDs from the list (you may add 1–2 adjacent if natural).
- Follow ALL quality rules from the project instructions.

### Dialogue 1 — `diabetes_mgmt`

**Archetype.** Diabetes management (`chronic-condition`, uses_ai=False, data_sensitivity=high, vulnerable_pop=False, markets=EU, CH).
**Description.** Tracks blood glucose readings, insulin doses and meal carbs; sends reminders and produces a weekly trend report shared with the endocrinologist.

**Dimensions to cover (7).**
- [P2.D4] Third-Party Data Sharing: Is health data shared with third parties, and are users aware of this?
- [P3.D5] Automation Bias (AI and Non-AI): Do users or clinicians over-trust the app's outputs, even when they are wrong?
- [P7.D2] CE Marking & MDR Conformity: If the app is a medical device, does it have the required CE marking?
- [P3.D1] Right to Make Decisions: Does the app respect the patient's right to make their own health decisions?
- [P7.D1] Medical Device Classification (SaMD): Is the app a Software as a Medical Device, and is it classified correctly?
- [P1.D4] Delayed Medical Consultation: Could the app cause users to postpone seeking professional medical care?
- [P7.D5] Post-Market Surveillance & Vigilance: Is there a system to monitor the app's safety and performance after launch?

### Dialogue 2 — `asthma_inhaler`

**Archetype.** Asthma inhaler tracker (`chronic-condition`, uses_ai=False, data_sensitivity=medium, vulnerable_pop=True, markets=EU).
**Description.** Bluetooth inhaler companion that logs usage, detects over-use of rescue inhaler, and nudges children + parents to adhere to controller medication.

**Dimensions to cover (4).**
- [P3.D5] Automation Bias (AI and Non-AI): Do users or clinicians over-trust the app's outputs, even when they are wrong?
- [P4.D2] Interoperability & Data Exchange: Can the app exchange data with other health systems (EHR, FHIR)?
- [P2.D3] Storage, Encryption & Security: Is personal health data properly secured at rest and in transit?
- [P4.D1] App Stability & Error Handling: Does the app handle failures gracefully without risking patient safety?

### Dialogue 3 — `cbt_chatbot`

**Archetype.** CBT-based mood & anxiety chatbot (`mental-health`, uses_ai=True, data_sensitivity=high, vulnerable_pop=True, markets=EU, CH).
**Description.** Conversational LLM-powered companion delivering structured CBT exercises for mild-to-moderate anxiety, with crisis-keyword detection that escalates to a hotline.

**Dimensions to cover (4).**
- [P4.D1] App Stability & Error Handling: Does the app handle failures gracefully without risking patient safety?
- [P7.D4] GDPR Compliance (DPO, DPIA): Is the app fully compliant with GDPR requirements for health data?
- [P1.D1] Clinical Evidence & Validation: Has the app's clinical effectiveness been validated through appropriate studies?
- [P4.D2] Interoperability & Data Exchange: Can the app exchange data with other health systems (EHR, FHIR)?

### Dialogue 4 — `ibd_journal`

**Archetype.** IBD symptom journal (`chronic-condition`, uses_ai=False, data_sensitivity=high, vulnerable_pop=False, markets=EU, CH).
**Description.** Crohn's / UC patient diary tracking stool frequency, urgency, bleeding, food triggers; shares anonymized data with gastroenterology team.

**Dimensions to cover (7).**
- [P2.D6] Vulnerable Population Data: Are there special protections for data from children, elderly, or mental health patients?
- [P2.D5] Anonymization & Right to Erasure: Can users have their data deleted, and is shared data properly anonymized?
- [P7.D2] CE Marking & MDR Conformity: If the app is a medical device, does it have the required CE marking?
- [P6.D3] Cross-Cultural & Multilingual Validation: Has the app been validated across cultures and languages?
- [P7.D1] Medical Device Classification (SaMD): Is the app a Software as a Medical Device, and is it classified correctly?
- [P3.D2] Emotional Manipulation & Excessive Nudging: Does the app use persuasive techniques that could undermine autonomous decision-making?
- [P1.D3] False Sense of Security: Could the app give users unwarranted confidence in their health status?

### Dialogue 5 — `skin_photo_surv`

**Archetype.** Skin lesion photo surveillance (`imaging`, uses_ai=False, data_sensitivity=high, vulnerable_pop=False, markets=EU).
**Description.** Patients photograph moles monthly; the app stores standardized images and reminds them to consult a dermatologist if size/colour changes.

**Dimensions to cover (6).**
- [P6.D5] Representativeness in Validation Studies: Were the studies validating the app conducted with representative populations?
- [P7.D4] GDPR Compliance (DPO, DPIA): Is the app fully compliant with GDPR requirements for health data?
- [P7.D1] Medical Device Classification (SaMD): Is the app a Software as a Medical Device, and is it classified correctly?
- [P2.D3] Storage, Encryption & Security: Is personal health data properly secured at rest and in transit?
- [P7.D7] Lifecycle & Documentation Management: Is the app's entire lifecycle documented and governed?
- [P7.D3] EU AI Act Risk Classification: If the app uses AI, is it classified correctly under the EU AI Act?


Now produce the JSON object with all 5 dialogues, in the same order.
