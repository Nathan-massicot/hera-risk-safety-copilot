# Batch 07

Paste this entire batch into the Claude.ai project chat. Claude should reply
with a single JSON object `{"dialogues": [...]}` containing **5 dialogues**.
Save Claude's reply (only the JSON) to `responses/batch_07.json`.

---

Produce **5 dialogues** for the following (archetype, dimensions) pairs.

For each dialogue:
- Use `metadata.archetype_id` = the id below.
- Use `metadata.covered_dimensions` = the dimension IDs from the list (you may add 1–2 adjacent if natural).
- Follow ALL quality rules from the project instructions.

### Dialogue 1 — `derm_sf`

**Archetype.** Dermatology store-and-forward (`telemedicine`, uses_ai=False, data_sensitivity=high, vulnerable_pop=False, markets=EU).
**Description.** Patient submits photos + form; a dermatologist replies asynchronously within 48h with a diagnosis and prescription if relevant.

**Dimensions to cover (7).**
- [P4.D4] User-Centered Design & Usability Testing: Has the app been designed and tested with real end users?
- [P1.D2] Contraindications & Adverse Effects: Could the app cause harm to specific patient groups or in certain conditions?
- [P2.D4] Third-Party Data Sharing: Is health data shared with third parties, and are users aware of this?
- [P7.D4] GDPR Compliance (DPO, DPIA): Is the app fully compliant with GDPR requirements for health data?
- [P7.D1] Medical Device Classification (SaMD): Is the app a Software as a Medical Device, and is it classified correctly?
- [P3.D3] Impact on Doctor-Patient Relationship: Could the app weaken the relationship between patient and healthcare provider?
- [P2.D5] Anonymization & Right to Erasure: Can users have their data deleted, and is shared data properly anonymized?

### Dialogue 2 — `cognitive_rehab`

**Archetype.** Cognitive rehab game for elderly (`rehabilitation`, uses_ai=False, data_sensitivity=medium, vulnerable_pop=True, markets=EU, CH).
**Description.** Game-based cognitive exercises post-stroke or in early dementia; physiotherapist sets goals and reviews progress.

**Dimensions to cover (5).**
- [P4.D1] App Stability & Error Handling: Does the app handle failures gracefully without risking patient safety?
- [P6.D1] Data & Clinical Rule Bias: Are the data or clinical rules underlying the app biased toward certain populations?
- [P2.D4] Third-Party Data Sharing: Is health data shared with third parties, and are users aware of this?
- [P2.D1] Informed Consent: Do users fully understand what data is collected and how it is used?
- [P3.D4] Dynamic Consent & Withdrawal Rights: Can users change their mind about participation and data sharing at any time?

### Dialogue 3 — `cognitive_rehab`

**Archetype.** Cognitive rehab game for elderly (`rehabilitation`, uses_ai=False, data_sensitivity=medium, vulnerable_pop=True, markets=EU, CH).
**Description.** Game-based cognitive exercises post-stroke or in early dementia; physiotherapist sets goals and reviews progress.

**Dimensions to cover (7).**
- [P1.D1] Clinical Evidence & Validation: Has the app's clinical effectiveness been validated through appropriate studies?
- [P3.D1] Right to Make Decisions: Does the app respect the patient's right to make their own health decisions?
- [P6.D2] Digital Divide & Socioeconomic Access: Is the app accessible to users regardless of their socioeconomic status or digital literacy?
- [P5.D3] Decision Traceability & Logging: Can decisions and recommendations be traced back and audited?
- [P7.D4] GDPR Compliance (DPO, DPIA): Is the app fully compliant with GDPR requirements for health data?
- [P2.D5] Anonymization & Right to Erasure: Can users have their data deleted, and is shared data properly anonymized?
- [P1.D4] Delayed Medical Consultation: Could the app cause users to postpone seeking professional medical care?

### Dialogue 4 — `vaccine_kids`

**Archetype.** Vaccination schedule reminder for kids (`preventive`, uses_ai=False, data_sensitivity=medium, vulnerable_pop=True, markets=EU, CH).
**Description.** Parents enter their child's birth date; the app sends notifications matching the Swiss BAG/Bundesamt für Gesundheit vaccination schedule.

**Dimensions to cover (6).**
- [P4.D4] User-Centered Design & Usability Testing: Has the app been designed and tested with real end users?
- [P2.D5] Anonymization & Right to Erasure: Can users have their data deleted, and is shared data properly anonymized?
- [P7.D1] Medical Device Classification (SaMD): Is the app a Software as a Medical Device, and is it classified correctly?
- [P4.D3] Accessibility (WCAG, Literacy, Language): Is the app usable by people with disabilities, low literacy, or different languages?
- [P6.D3] Cross-Cultural & Multilingual Validation: Has the app been validated across cultures and languages?
- [P7.D5] Post-Market Surveillance & Vigilance: Is there a system to monitor the app's safety and performance after launch?

### Dialogue 5 — `ppd_screening`

**Archetype.** Postpartum depression screening (`mental-health`, uses_ai=False, data_sensitivity=high, vulnerable_pop=True, markets=EU).
**Description.** Administers the EPDS questionnaire weekly post-birth; flags scores ≥10 and recommends contacting the midwife or GP.

**Dimensions to cover (5).**
- [P7.D7] Lifecycle & Documentation Management: Is the app's entire lifecycle documented and governed?
- [P1.D2] Contraindications & Adverse Effects: Could the app cause harm to specific patient groups or in certain conditions?
- [P1.D3] False Sense of Security: Could the app give users unwarranted confidence in their health status?
- [P1.D6] System Dependency & Over-reliance: Could users become overly dependent on the app for health management?
- [P3.D3] Impact on Doctor-Patient Relationship: Could the app weaken the relationship between patient and healthcare provider?


Now produce the JSON object with all 5 dialogues, in the same order.
