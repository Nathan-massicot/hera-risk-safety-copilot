# Batch 02

Paste this entire batch into the Claude.ai project chat. Claude should reply
with a single JSON object `{"dialogues": [...]}` containing **5 dialogues**.
Save Claude's reply (only the JSON) to `responses/batch_02.json`.

---

Produce **5 dialogues** for the following (archetype, dimensions) pairs.

For each dialogue:
- Use `metadata.archetype_id` = the id below.
- Use `metadata.covered_dimensions` = the dimension IDs from the list (you may add 1–2 adjacent if natural).
- Follow ALL quality rules from the project instructions.

### Dialogue 1 — `ai_speech_mh`

**Archetype.** AI mental-health screening from speech (`ai-clinical`, uses_ai=True, data_sensitivity=high, vulnerable_pop=True, markets=EU).
**Description.** Records short voice samples in a hospital waiting room; ML model flags depression risk and suggests an appointment.

**Dimensions to cover (6).**
- [P5.D3] Decision Traceability & Logging: Can decisions and recommendations be traced back and audited?
- [P6.D5] Representativeness in Validation Studies: Were the studies validating the app conducted with representative populations?
- [P2.D4] Third-Party Data Sharing: Is health data shared with third parties, and are users aware of this?
- [P7.D2] CE Marking & MDR Conformity: If the app is a medical device, does it have the required CE marking?
- [P4.D2] Interoperability & Data Exchange: Can the app exchange data with other health systems (EHR, FHIR)?
- [P6.D2] Digital Divide & Socioeconomic Access: Is the app accessible to users regardless of their socioeconomic status or digital literacy?

### Dialogue 2 — `migraine_tracker`

**Archetype.** Headache & migraine tracker (`self-report`, uses_ai=True, data_sensitivity=medium, vulnerable_pop=False, markets=EU).
**Description.** Logs migraine episodes with environmental triggers (weather, sleep); applies a simple ML model to predict next attack window.

**Dimensions to cover (5).**
- [P4.D3] Accessibility (WCAG, Literacy, Language): Is the app usable by people with disabilities, low literacy, or different languages?
- [P3.D3] Impact on Doctor-Patient Relationship: Could the app weaken the relationship between patient and healthcare provider?
- [P4.D4] User-Centered Design & Usability Testing: Has the app been designed and tested with real end users?
- [P5.D2] Clear Communication of Limitations: Does the app clearly communicate what it cannot do?
- [P5.D1] Understandable Output: Can users understand how the app produces its results or recommendations?

### Dialogue 3 — `skin_photo_surv`

**Archetype.** Skin lesion photo surveillance (`imaging`, uses_ai=False, data_sensitivity=high, vulnerable_pop=False, markets=EU).
**Description.** Patients photograph moles monthly; the app stores standardized images and reminds them to consult a dermatologist if size/colour changes.

**Dimensions to cover (6).**
- [P6.D2] Digital Divide & Socioeconomic Access: Is the app accessible to users regardless of their socioeconomic status or digital literacy?
- [P1.D2] Contraindications & Adverse Effects: Could the app cause harm to specific patient groups or in certain conditions?
- [P2.D5] Anonymization & Right to Erasure: Can users have their data deleted, and is shared data properly anonymized?
- [P4.D5] Offline Functionality & Updates: Does the app work without internet, and are updates managed safely?
- [P5.D2] Clear Communication of Limitations: Does the app clearly communicate what it cannot do?
- [P2.D1] Informed Consent: Do users fully understand what data is collected and how it is used?

### Dialogue 4 — `chronic_pain_diary`

**Archetype.** Chronic pain diary (`self-report`, uses_ai=False, data_sensitivity=medium, vulnerable_pop=False, markets=EU).
**Description.** Daily pain-intensity logging with body-map annotation; exports a PDF the patient brings to their pain-clinic appointment.

**Dimensions to cover (7).**
- [P4.D2] Interoperability & Data Exchange: Can the app exchange data with other health systems (EHR, FHIR)?
- [P4.D3] Accessibility (WCAG, Literacy, Language): Is the app usable by people with disabilities, low literacy, or different languages?
- [P5.D2] Clear Communication of Limitations: Does the app clearly communicate what it cannot do?
- [P1.D1] Clinical Evidence & Validation: Has the app's clinical effectiveness been validated through appropriate studies?
- [P4.D1] App Stability & Error Handling: Does the app handle failures gracefully without risking patient safety?
- [P6.D3] Cross-Cultural & Multilingual Validation: Has the app been validated across cultures and languages?
- [P1.D4] Delayed Medical Consultation: Could the app cause users to postpone seeking professional medical care?

### Dialogue 5 — `gp_telecons`

**Archetype.** GP teleconsultation (`telemedicine`, uses_ai=False, data_sensitivity=high, vulnerable_pop=False, markets=EU, CH).
**Description.** Video consultation with a licensed GP, e-prescription, secure messaging, and integration with national eHealth records (DEP in CH).

**Dimensions to cover (5).**
- [P4.D4] User-Centered Design & Usability Testing: Has the app been designed and tested with real end users?
- [P3.D5] Automation Bias (AI and Non-AI): Do users or clinicians over-trust the app's outputs, even when they are wrong?
- [P4.D2] Interoperability & Data Exchange: Can the app exchange data with other health systems (EHR, FHIR)?
- [P7.D6] Third-Party Audit & Certification: Has the app been independently audited or certified?
- [P7.D2] CE Marking & MDR Conformity: If the app is a medical device, does it have the required CE marking?


Now produce the JSON object with all 5 dialogues, in the same order.
