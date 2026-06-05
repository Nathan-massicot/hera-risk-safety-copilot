APPROACH UNDER REVIEW: `prompt-only`

SCENARIO ID: scenario_12
APP DESCRIPTION: Lunara is a menstrual cycle tracker that also offers a fertility prediction mode (for users trying to conceive) and a 'natural contraception' mode that predicts safe vs unsafe days. Algorithm based on basal body temperature + cycle history. We're EU + CH. 4 million users.

DEVELOPER PERSONA: Senior PM at a femtech scale-up. Confident, fast-moving.

EXPECTED HERA DIMENSIONS (gold standard): P1.D1, P1.D2, P1.D3, P2.D1, P2.D2, P2.D4, P2.D6, P3.D2, P5.D2, P5.D4, P6.D1, P6.D3, P7.D1, P7.D3

TRANSCRIPT:
### USER
Lunara is a menstrual cycle tracker that also offers a fertility prediction mode (for users trying to conceive) and a 'natural contraception' mode that predicts safe vs unsafe days. Algorithm based on basal body temperature + cycle history. We're EU + CH. 4 million users.

### ASSISTANT
What data points about users' menstrual cycles and fertility do you collect, and how do you ensure they are anonymized and stored securely in compliance with GDPR and ISO 82304-2? [P2.D3]

### USER
We share aggregated, anonymized cycle data with research partners and we don't run ads on health data — but we do pull IDFA for marketing attribution. I'll concede we haven't formally tested whether 'anonymized' cycle patterns could be re-identified; cycle signatures are pretty unique and that's not something we've audited.

### ASSISTANT
What steps are you taking to audit and validate the uniqueness of anonymized cycle patterns, and how do you plan to mitigate the risk of re-identification, given the potential for unique cycle signatures under [P2.D3] and the requirements of GDPR Article 9?

### USER
We're EU and CH only and I treat that as solid, but I'll be straight that I haven't pinned down exactly where the cycle and partner-activity data physically lives, and we don't offer a zero-knowledge encryption option. Given the abortion-politics climate in parts of Europe I know cycle data is sensitive, but we haven't formalized a data-residency or law-enforcement-access stance.

### ASSISTANT
What is your current data residency strategy for cycle and partner-activity data, and how do you plan to formalize access controls and legal protections (e.g., data localization, law enforcement access limits) to address the sensitivity of reproductive health data under [P2.D3] and GDPR Article 9?

### USER
Consent is account creation accepting the privacy policy plus a 'sensitive data' onboarding flow for health processing. I'd be honest that it's a fairly standard click-through — I can't claim a typical user deeply understands that their cycle and partner-activity logs are GDPR Article 9 special-category data.

### ASSISTANT
What specific measures are you implementing to enhance user understanding of GDPR Article 9 obligations and the sensitivity of reproductive health data, particularly in the onboarding flow, to ensure meaningful consent under [P2.D3] and Article 6(1)(a) of GDPR?

### USER
Account creation requires accepting privacy policy. Health data processing in 'sensitive data' onboarding flow.

### ASSISTANT
What specific enhancements are you planning for the 'sensitive data' onboarding flow to ensure users comprehend the GDPR Article 9 implications of sharing reproductive health data, and how will you ensure this aligns with the "clear and specific" consent requirement under [P2.D3] and GDPR Article 6(1)(a)?

### USER
Account delete; data exported as CSV; takeoff GDPR portability.

### ASSISTANT
What specific steps are you taking to ensure that data exported in CSV format meets GDPR Article 17 (Right to Erasure) and Article 20 (Data Portability) requirements, particularly regarding the completeness, accuracy, and format of reproductive health data under [P2.D3] and ISO 82304-2?

### USER
Aggregated cycle data with research partners (anonymized). No advertising on health data.

### ASSISTANT
What specific mechanisms are you using to ensure that aggregated cycle data shared with research partners remains truly anonymized and cannot be re-identified, and how do these measures align with the GDPR Article 9(2)(a) and [P2.D3] requirements for processing special-category data?

### USER
Our model assumes a reasonably regular cycle, so I'll admit it's weakest exactly where it matters most — PCOS, very irregular cycles, post-partum and perimenopause. Right now we still try to predict for those users instead of refusing or flagging them, and we haven't built PCOS/irregular-cycle detection that pauses the contraception prediction.

### ASSISTANT
What specific safeguards are you implementing to detect and handle irregular cycles (e.g., PCOS, post-partum, perimenopause) in your fertility and contraception prediction models, and how do these measures address the risk of providing potentially misleading health guidance under [P2.D3] and the EU AI Act's transparency and accountability requirements?

### USER
We describe the model as a Bayesian ovulation predictor and we surface uncertainty intervals, but honestly we did our regulatory work through the MDR lens, not the EU AI Act. I haven't formally classified this system under the AI Act or checked whether a contraception-prediction AI lands in a higher-risk category there.

### ASSISTANT
What specific steps are you taking to classify your contraception-prediction AI system under the EU AI Act, particularly to determine whether it falls into a higher-risk category (e.g., "high-risk" under Article 5(2)) and how will you ensure compliance with transparency, accountability, and human oversight requirements under [P2.D3] and the AI Act's Article 8 and 10?

### USER
The tracker mode is just wellness and the contraception mode is the regulated Class IIa one, but in the UI the line between them is softer than it should be. Switching into contraception mode doesn't currently force a confirmation that explains 'you are now relying on this to prevent pregnancy,' and I can see how a user might not realize which mode they're in.

### ASSISTANT
What specific UI design changes are you planning to implement to clearly distinguish between wellness and regulated contraception modes, and how will these changes ensure users are fully aware of the medical implications and regulatory obligations under [P2.D3] and the EU AI Act's Article 8 (transparency) and Article 10 (human oversight)?

### USER
Natural contraception mode is CE Class IIa under MDR. Tracker mode is wellness.

### USER
Thanks for the conversation. Could you produce a brief structured risk report now? Use HERA dimension IDs (e.g. [P1.D2]) and group risks by severity. End the report with a list of dimensions you didn't get to cover.

### ASSISTANT
**HERA Risk & Safety Risk Report for Lunara Menstrual Cycle Tracker**  
*Based on current practices and regulatory landscape (EU + CH)*  

---

### **High Severity Risks**  
**[P2.D3]** *Data Anonymization & Re-identification*  
- **Risk**: Anonymized cycle data may be re-identified due to unique cycle signatures. No audit or mitigation plan in place.  
- **Mitigation**: Conduct third-party re-identification audits, implement differential privacy, and formalize anonymization standards under GDPR Article 9(2)(a) and ISO 82304-2.  

**[P3.D1]** *AI System Classification & Risk Assessment*  
- **Risk**: Contraception mode (CE Class IIa) may fall under higher-risk AI under the EU AI Act, but classification is incomplete.  
- **Mitigation**: Classify system under the EU AI Act, conduct risk assessment per Article 5(2), and ensure transparency and human oversight under Articles 8 and 10.  

**[P4.D2]** *User Consent & Understanding*  
- **Risk**: Consent process is standard click-through; users may not grasp the sensitivity of reproductive data (GDPR Article 9).  
- **Mitigation**: Redesign onboarding flow with interactive consent, plain language, and visual cues under GDPR Article 6(1)(a) and [P2.D3].  

**[P5.D1]** *Data Residency & Legal Access*  
- **Risk**: No formal data residency strategy or law enforcement access limits for sensitive reproductive data.  
- **Mitigation**: Formalize data localization (e.g., EU/CH only), limit law enforcement access, and document under GDPR Article 9 and [P2.D3].  

**[P6.D1]** *Data Portability & Erasure*  
- **Risk**: CSV exports may lack completeness, accuracy, or structured format for GDPR Article 20 and Article 17.  
- **Mitigation**: Ensure structured, machine-readable exports and implement erasure protocols under GDPR Article 17 and ISO 82304-2.  

**[P7.D1]** *Model Transparency & Accountability*  
- **Risk**: Contraception mode lacks explicit user confirmation and may mislead users about medical efficacy.  
- **Mitigation**: Implement mode-switching confirmation, label all predictions as probabilistic, and align with EU AI Act Article 8 and [P2.D3].  

---

### **Medium Severity Risks**  
**[P2.D4]** *Data Security & Storage*  
- **Risk**: No zero-knowledge encryption, unclear data storage locations.  
- **Mitigation**: Implement end-to-end encryption, document data storage locations, and align with ISO 82304-2 and GDPR Article 30.  

**[P4.D3]** *User Awareness of AI Limitations*  
- **Risk**: Users may not understand the limitations of Bayesian ovulation prediction.  
- **Mitigation**: Add visual indicators of uncertainty, explain model limitations, and align with EU AI Act Article 8.  

**[P6.D2]** *Data Retention & Deletion*  
- **Risk**: No formal retention policy for reproductive health data.  
- **Mitigation**: Define data retention periods and implement automated deletion under GDPR Article 17 and ISO 82304-2.  

---

### **Low Severity Risks**  
**[P3.D3]** *Algorithmic Fairness & Bias*  
- **Risk**: Model may not account for PCOS, irregular cycles, or perimenopause.  
- **Mitigation**: Build detection mechanisms for irregular cycles, pause contraception predictions, and align with EU AI Act Article 5(2).  

**[P5.D2]** *Third-Party Data Sharing*  
- **Risk**: Aggregated data shared with research partners may lack formal safeguards.  
- **Mitigation**: Formalize data-sharing agreements, implement anonymization, and align with GDPR Article 9 and [P2.D3].  

---

### **Dimensions Not Covered**  
- **[P1.D1]** *User Safety & Harm Prevention*  
- **[P1.D3]** *Clinical Validation & Efficacy*  
- **[P3.D2]** *AI Risk Assessment & Impact*  
- **[P4.D4]** *User Control & Autonomy*  
- **[P5.D3]** *Data Transfer & Cross-border Compliance*  
- **[P7.D2]** *Human Oversight & Redress*  

---

**Next Steps**  
- Formalize AI Act classification and risk assessment.  
- Conduct third-party re-identification audits.  
- Redesign consent and onboarding flows for GDPR Article 9.  
- Implement zero-knowledge encryption and data residency strategy.  
- Define data retention and erasure policies

Now produce the JSON judgement object.