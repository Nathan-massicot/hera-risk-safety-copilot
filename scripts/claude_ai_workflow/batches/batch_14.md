# Batch 14

Paste this entire batch into the Claude.ai project chat. Claude should reply
with a single JSON object `{"dialogues": [...]}` containing **5 dialogues**.
Save Claude's reply (only the JSON) to `responses/batch_14.json`.

---

Produce **5 dialogues** for the following (archetype, dimensions) pairs.

For each dialogue:
- Use `metadata.archetype_id` = the id below.
- Use `metadata.covered_dimensions` = the dimension IDs from the list (you may add 1–2 adjacent if natural).
- Follow ALL quality rules from the project instructions.

### Dialogue 1 — `epilepsy_logger`

**Archetype.** Epilepsy seizure logger (`chronic-condition`, uses_ai=False, data_sensitivity=high, vulnerable_pop=True, markets=EU).
**Description.** Seizure event logging with caregiver alerts via SMS; aggregates data for the patient's neurologist visit.

**Dimensions to cover (4).**
- [P5.D4] Clinically Validated vs. Estimated Content: Is it clear to users which content is evidence-based and which is generated or estimated?
- [P4.D4] User-Centered Design & Usability Testing: Has the app been designed and tested with real end users?
- [P2.D5] Anonymization & Right to Erasure: Can users have their data deleted, and is shared data properly anonymized?
- [P1.D1] Clinical Evidence & Validation: Has the app's clinical effectiveness been validated through appropriate studies?

### Dialogue 2 — `addiction_recovery`

**Archetype.** Addiction recovery (substance-use logging) (`mental-health`, uses_ai=False, data_sensitivity=high, vulnerable_pop=True, markets=EU, CH).
**Description.** Anonymous substance-use diary with relapse risk score, peer-support chat, and integration with addiction clinics that opt in.

**Dimensions to cover (4).**
- [P7.D4] GDPR Compliance (DPO, DPIA): Is the app fully compliant with GDPR requirements for health data?
- [P1.D1] Clinical Evidence & Validation: Has the app's clinical effectiveness been validated through appropriate studies?
- [P3.D2] Emotional Manipulation & Excessive Nudging: Does the app use persuasive techniques that could undermine autonomous decision-making?
- [P6.D1] Data & Clinical Rule Bias: Are the data or clinical rules underlying the app biased toward certain populations?

### Dialogue 3 — `fitness_tracker`

**Archetype.** Generic fitness tracker (`wellness`, uses_ai=False, data_sensitivity=low, vulnerable_pop=False, markets=EU, CH).
**Description.** Step counting, workout logging, social challenges with friends; integrates with Apple Health and Google Fit.

**Dimensions to cover (5).**
- [P2.D2] Data Minimization: Does the app collect only the data strictly necessary for its function?
- [P7.D1] Medical Device Classification (SaMD): Is the app a Software as a Medical Device, and is it classified correctly?
- [P5.D3] Decision Traceability & Logging: Can decisions and recommendations be traced back and audited?
- [P4.D2] Interoperability & Data Exchange: Can the app exchange data with other health systems (EHR, FHIR)?
- [P3.D1] Right to Make Decisions: Does the app respect the patient's right to make their own health decisions?

### Dialogue 4 — `vaccine_kids`

**Archetype.** Vaccination schedule reminder for kids (`preventive`, uses_ai=False, data_sensitivity=medium, vulnerable_pop=True, markets=EU, CH).
**Description.** Parents enter their child's birth date; the app sends notifications matching the Swiss BAG/Bundesamt für Gesundheit vaccination schedule.

**Dimensions to cover (5).**
- [P7.D7] Lifecycle & Documentation Management: Is the app's entire lifecycle documented and governed?
- [P7.D2] CE Marking & MDR Conformity: If the app is a medical device, does it have the required CE marking?
- [P4.D4] User-Centered Design & Usability Testing: Has the app been designed and tested with real end users?
- [P7.D6] Third-Party Audit & Certification: Has the app been independently audited or certified?
- [P5.D2] Clear Communication of Limitations: Does the app clearly communicate what it cannot do?

### Dialogue 5 — `ai_derm`

**Archetype.** AI dermatology diagnosis from photo (`ai-clinical`, uses_ai=True, data_sensitivity=high, vulnerable_pop=False, markets=EU, CH).
**Description.** CNN classifies skin lesions as benign / suspicious / urgent; intended as a triage tool for primary-care physicians.

**Dimensions to cover (5).**
- [P7.D4] GDPR Compliance (DPO, DPIA): Is the app fully compliant with GDPR requirements for health data?
- [P6.D1] Data & Clinical Rule Bias: Are the data or clinical rules underlying the app biased toward certain populations?
- [P6.D2] Digital Divide & Socioeconomic Access: Is the app accessible to users regardless of their socioeconomic status or digital literacy?
- [P1.D2] Contraindications & Adverse Effects: Could the app cause harm to specific patient groups or in certain conditions?
- [P1.D5] Measurement Reliability: Are the measurements and data captured by the app accurate and reliable?


Now produce the JSON object with all 5 dialogues, in the same order.
