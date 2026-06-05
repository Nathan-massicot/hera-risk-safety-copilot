APPROACH UNDER REVIEW: `prompt-only`

SCENARIO ID: scenario_08
APP DESCRIPTION: RecoverNow is a recovery companion for people with eating disorders (anorexia and bulimia). Users log meals, urges, and emotions; an AI flags risky patterns (skipped meals streaks, urge spikes) and suggests coping skills from a CBT toolbox. We co-designed it with a clinical team at a French eating-disorder clinic. EU market.

DEVELOPER PERSONA: Clinical psychologist turned product lead, deeply familiar with the patient population, less so with regulation.

EXPECTED HERA DIMENSIONS (gold standard): P1.D1, P1.D2, P1.D4, P2.D1, P2.D5, P2.D6, P3.D1, P3.D2, P5.D2, P5.D4, P6.D3, P7.D1, P7.D2, P7.D3

TRANSCRIPT:
### USER
RecoverNow is a recovery companion for people with eating disorders (anorexia and bulimia). Users log meals, urges, and emotions; an AI flags risky patterns (skipped meals streaks, urge spikes) and suggests coping skills from a CBT toolbox. We co-designed it with a clinical team at a French eating-disorder clinic. EU market.

### ASSISTANT
What specific data types (e.g., meal logs, emotional states, AI-generated insights) does RecoverNow collect, and how are they stored or transmitted?

### USER
Meal logs (free text + structured), urge intensity, emotion tags, weight (optional, hidden by default), photo-based food log (optional).

### ASSISTANT
What specific measures have you implemented to ensure the confidentiality and integrity of users' meal logs and emotional data, especially given the sensitive nature of eating disorder data [P2.D3], and how does this align with GDPR Article 30?

### USER
Our users are in recovery from anorexia and bulimia so I'm very aware they're a vulnerable group, but the consent assessment is self-administered in the app and we don't currently require or formally loop in the treating clinician at the consent stage.

### ASSISTANT
What specific steps have you taken to ensure that users’ optional weight data, which is both sensitive and potentially used for clinical risk assessment [P2.D4], is stored securely and only accessible to authorized personnel, in line with GDPR Article 30 and ISO 82304-2?

### USER
Risk-flagging algorithm: sensitivity 88%, specificity 80% on labeled 500-case set from clinic.

### ASSISTANT
What specific validation processes have you conducted to ensure the risk-flagging algorithm's performance metrics [P3.D10] are reliable and transparent, and how does this align with the EU AI Act's requirements for high-risk systems?

### USER
We use a small LSTM and rule-based logic for the risk-flagging, but we haven't done an EU AI Act risk classification or mapped our AI components against it — regulation isn't really my background.

### ASSISTANT
What specific steps have you taken to ensure that the AI-generated coping skill suggestions [P3.D11] are evidence-based, culturally appropriate, and do not inadvertently reinforce harmful behaviors, in line with the EU AI Act’s transparency and non-discrimination requirements?

### USER
When the AI flags a risky pattern it suggests a coping skill from our CBT toolbox, and a clinician reviews every flagged case afterward, but we don't currently have an automatic hard escalation that pushes the user to contact their clinician in real time during an acute episode.

### ASSISTANT
What specific mechanisms have you implemented to ensure that users who experience acute distress or urgent need during a flagged episode [P3.D12] are promptly connected to emergency support, and how does this align with the EU AI Act’s requirement for human oversight in high-risk systems?

### USER
Patient-research-partner panel of 5 users in recovery + 3 clinicians. Continuous co-design.

### ASSISTANT
What specific safeguards have you put in place to ensure that the co-design process with patients in recovery [P1.D1] includes ongoing ethical oversight, particularly around data use and risk mitigation, and how does this align with the EU AI Act’s requirement for human oversight and accountability?

### USER
We co-designed RecoverNow with a French eating-disorder clinic, and we validated the risk-flagging algorithm on a labeled 500-case set from that clinic (88% sensitivity, 80% specificity), but we haven't run a formal prospective clinical trial or pilot yet.

### ASSISTANT
What specific steps have you taken to ensure that the risk-flagging algorithm’s performance in real-world use [P3.D10] is continuously monitored and validated, and how does this align with the EU AI Act’s requirement for ongoing risk management and transparency in high-risk systems?

### USER
Direct clinician review of every flagged risk case. Weekly clinical safety meeting.

### ASSISTANT
What specific documentation and audit trails have you established to ensure that clinician reviews of flagged cases [P3.D10] are consistently recorded, traceable, and compliant with GDPR Article 30 and the EU AI Act’s transparency requirements?

### USER
Detailed onboarding video + signed consent form (digital). Consent re-confirmed every 6 months.

### ASSISTANT
What specific measures have you implemented to ensure that the re-consent process [P2.D3] is both meaningful and not merely a checkbox exercise, and how does this align with GDPR Article 13 and the EU AI Act’s transparency and user control requirements?

### USER
Consent is a detailed onboarding video plus a digitally signed form, re-confirmed every six months; it's thorough but it's essentially all-or-nothing and we don't yet offer granular per-data-type consent.

### USER
Thanks for the conversation. Could you produce a brief structured risk report now? Use HERA dimension IDs (e.g. [P1.D2]) and group risks by severity. End the report with a list of dimensions you didn't get to cover.

### ASSISTANT
**HERA Risk & Safety Report for RecoverNow**  
*Applicable to EU market, mHealth app for eating disorder recovery*

---

### **High Severity Risks (Critical for Compliance & Safety)**

**[P2.D3] Data Confidentiality & Consent Management**  
- *Risk:* Current consent process is all-or-nothing, lacking granular per-data-type consent, which may overburden users and fail to meet GDPR Article 13’s transparency and user control requirements.  
- *Mitigation:* Implement granular consent options for data types (e.g., meal logs, emotional data, weight), with clear explanations of how each is used, in line with GDPR Article 6 and the EU AI Act’s transparency requirements.

**[P3.D10] AI Algorithm Performance & Reliability**  
- *Risk:* Risk-flagging algorithm has not been validated in real-world use, and lacks formal prospective clinical trials or ongoing monitoring, violating the EU AI Act’s requirement for high-risk AI systems to have robust performance validation.  
- *Mitigation:* Conduct a prospective clinical trial with a representative sample of users, and implement real-time performance monitoring tools (e.g., dashboards for sensitivity/specificity tracking), in line with EU AI Act Article 30 and ISO 82304-2.

**[P3.D12] Emergency Response & Human Oversight**  
- *Risk:* No automatic escalation to real-time clinician support during acute episodes, risking failure to meet the EU AI Act’s requirement for human oversight in high-risk systems.  
- *Mitigation:* Integrate real-time escalation mechanisms (e.g., push notifications to clinicians or emergency contacts) during flagged acute episodes, aligned with EU AI Act Article 5 and ISO 82304-2.

---

### **Medium Severity Risks (Important for Compliance & Safety)**

**[P1.D1] Co-Design & Ethical Oversight**  
- *Risk:* Co-design process lacks formal ethical oversight mechanisms for data use and risk mitigation, potentially violating the EU AI Act’s accountability and transparency requirements.  
- *Mitigation:* Establish a formal ethics review board or oversight panel, including clinicians and patient advocates, to review data use and risk mitigation strategies, in line with EU AI Act Article 7 and ISO 82304-2.

**[P2.D4] Sensitive Data Handling (Weight Data)**  
- *Risk:* Optional weight data is stored without explicit granular consent and access controls, increasing exposure risk for sensitive data, violating GDPR Article 30 and ISO 82304-2.  
- *Mitigation:* Implement access controls, encryption, and explicit granular consent for weight data, with separate storage and access protocols, in line with GDPR Article 30 and ISO 82304-2.

**[P3.D11] AI-Generated Recommendations & Non-Discrimination**  
- *Risk:* AI-generated coping skill suggestions lack formal evidence-based validation and cultural appropriateness checks, risking non-compliance with EU AI Act’s transparency and non-discrimination requirements.  
- *Mitigation:* Conduct evidence-based validation of coping skill suggestions, including cultural and contextual reviews, in line with EU AI Act Article 5 and ISO 82304-2.

---

### **Low Severity Risks (Minor but Worth Monitoring)**

**[P2.D2] Data Storage & Transmission Security**  
- *Risk:* No explicit details on encryption or secure storage of meal logs and emotional data, increasing exposure risk.  
- *Mitigation:* Implement end-to-end encryption for data in transit and at rest, and use secure storage protocols (e.g., GDPR Article 30, ISO 82304-2).

**[P2.D5] Data Retention & Deletion**  
- *Risk:* No clear policy on data retention periods or deletion procedures, potentially violating GDPR Article 5 and ISO 82304-2.  
- *Mitigation:* Define and document data retention periods, and implement automated deletion processes upon user request or end of service, in line with GDPR Article 5 and ISO 82304-2.

---

### **Dimensions Not Covered in This Report**  
The following HERA dimensions were not addressed in the current conversation and may require further exploration:

- **[P1.D2] User Autonomy & Control**  
- **[P1.D3] Equity & Inclusion**  
- **[P2.D1] Data Minimization**  
- **[P2.D6] Data Portability**  
- **[P3.D9] AI Transparency & Explainability**  
- **[P3.D13] AI Bias & Fairness**  
- **[P4.D1] Cybersecurity & Incident Response**  
- **[P5.D1] Regulatory Compliance & Audit Readiness**  
- **[P6.D1] Clinical

Now produce the JSON judgement object.