APPROACH UNDER REVIEW: `prompt-only`

SCENARIO ID: scenario_14
APP DESCRIPTION: SleepWell is an iOS/Android app that stages your sleep using phone microphone + accelerometer, and delivers a CBT-I (insomnia) coaching programme over 6 weeks. The coaching content is personalised by a small ML model based on user adherence and reported sleep. EU.

DEVELOPER PERSONA: Sleep researcher founder. Thinks scientifically but is new to medical-device regulation.

EXPECTED HERA DIMENSIONS (gold standard): P1.D1, P1.D5, P2.D1, P2.D2, P2.D3, P3.D1, P4.D5, P5.D1, P5.D2, P5.D4, P7.D1, P7.D3

TRANSCRIPT:
### USER
SleepWell is an iOS/Android app that stages your sleep using phone microphone + accelerometer, and delivers a CBT-I (insomnia) coaching programme over 6 weeks. The coaching content is personalised by a small ML model based on user adherence and reported sleep. EU.

### ASSISTANT
What data about users' sleep and adherence do you collect, and how is this data used to personalise the coaching content? [P2.D3]

### USER
Sleep staging accuracy ~80% vs polysomnography (in-lab study N=50).

### ASSISTANT
What steps have you taken to validate the accuracy of your sleep staging algorithm, and how do you ensure this meets the requirements of the EU AI Act's risk categorisation for health-related outputs? [P3.D10]

### USER
Our sleep staging is validated at about 80% agreement vs polysomnography in an in-lab study of N=50, which I'm proud of, but the 6-week CBT-I coaching programme itself has not been validated in-app — we're leaning on the published CBT-I literature, not our own efficacy trial.

### ASSISTANT
What evidence do you have that the CBT-I programme meets the efficacy standards outlined in the EU AI Act's Article 16, and how do you ensure that the personalisation of coaching content does not compromise the therapeutic integrity of the intervention? [P3.D10]

### USER
Our CBT-I content is grounded in the established evidence-based protocol, but the per-user staging numbers and the personalised prescriptions are model estimates — and we don't currently label inside the app which parts are clinically established versus algorithmically estimated.

### ASSISTANT
What measures have you implemented to ensure transparency about which parts of the coaching content are based on clinical evidence versus algorithmic estimates, in line with the EU AI Act's Article 8 (transparency) and ISO 82304-2's requirements for user understanding of health-related outputs? [P2.D4]

### USER
We tell users it's a sleep-tracking and CBT-I coaching tool, but we don't yet have clear in-app messaging about what it can't do — for instance that it's not a diagnosis and that ~80% staging accuracy means some nights will be wrong.

### ASSISTANT
What specific in-app disclaimers or user-facing communications have you drafted to align with the EU AI Act's Article 8 (transparency) and Article 16 (efficacy), and how do these address the limitations of your sleep staging accuracy and the non-diagnostic nature of the app? [P2.D4]

### USER
Sleep staging runs on-device so tracking works offline overnight, but the personalised coaching and the digest upload need connectivity; we ship content and model updates through the normal app-store release cycle and we don't currently have a staged-rollback plan if an update misbehaves. Post-market we mostly rely on crash analytics and a monthly retention review.

### ASSISTANT
What contingency plans have you developed for rolling back or mitigating risks associated with app updates that affect the personalised coaching or data upload functionality, in line with the EU AI Act's Article 16 (risk management) and ISO 82304-2's post-market monitoring requirements? [P3.D12]

### USER
Crash analytics + monthly retention review.

### ASSISTANT
What steps have you taken to ensure that crash analytics and monthly retention reviews are compliant with the EU AI Act's Article 16 (risk management) and ISO 82304-2's post-market monitoring requirements, including the documentation and reporting of any identified risks or incidents? [P3.D12]

### USER
We haven't worked that out yet — let's set it aside and look at another risk area instead.

### ASSISTANT
What specific measures have you considered to ensure user data collected via the phone's microphone and accelerometer is anonymised and encrypted in transit and at rest, in compliance with GDPR Article 9 (processing of special categories of data) and ISO 82304-2's data protection requirements? [P2.D1]

### USER
Our staging uses the phone microphone plus accelerometer, so it's genuinely environment-sensitive — a partner in the bed, pets, or a noisy room can degrade accuracy, and we haven't yet built anything to detect or warn users when the recording conditions are poor.

### ASSISTANT
What steps have you taken to address the environmental sensitivity of your sleep staging and to ensure users are informed about how external factors (e.g., partner movement, pets, noise) can affect the accuracy of the data, in line with the EU AI Act's Article 8 (transparency) and ISO 82304-2's user awareness requirements? [P2.D4]

### USER
CNN for sleep staging from audio + motion; rule-based CBT-I prescription engine.

### ASSISTANT
What safeguards have you implemented to ensure the rule-based CBT-I prescription engine remains aligned with clinical guidelines and does not produce recommendations that could mislead users, in compliance with the EU AI Act's Article 8 (transparency) and Article 16 (efficacy)? [P3.D10]

### USER
We classify ourselves as wellness coaching, not SaMD, because we don't diagnose insomnia — but I'm new to medical-device regulation and I haven't actually mapped us against MDR Rule 11 or talked to a notified body, so I can't tell you with confidence we'd stay below the device line if challenged on the CBT-I side.

### USER
Thanks for the conversation. Could you produce a brief structured risk report now? Use HERA dimension IDs (e.g. [P1.D2]) and group risks by severity. End the report with a list of dimensions you didn't get to cover.

### ASSISTANT
**HERA Risk & Safety Risk Report for SleepWell App**  
*Structured by HERA Pillar and Dimension ID, grouped by severity*

---

### **High Severity Risks**  
These risks could lead to regulatory non-compliance, reputational harm, or user harm if not addressed.

1. **[P2.D3] Data Use & Personalisation**  
   - **Risk**: Personalisation of coaching content is based on algorithmic estimates (sleep staging) without clear labelling of what is algorithmic vs clinically established.  
   - **Regulation**: EU AI Act Article 8 (transparency), ISO 82304-2 (user understanding of health outputs).  
   - **Mitigation**: Implement clear in-app labelling of algorithmic vs clinical content, with user consent for personalisation.

2. **[P3.D10] Efficacy & Risk Categorisation**  
   - **Risk**: CBT-I programme is not validated in-app and relies on published literature, which may not meet EU AI Act Article 16 efficacy standards.  
   - **Regulation**: EU AI Act Article 16 (efficacy), MDR Rule 11 (definition of SaMD).  
   - **Mitigation**: Conduct in-app efficacy trials or partner with clinical institutions for validation, and map against MDR Rule 11.

3. **[P3.D12] Post-Market Monitoring**  
   - **Risk**: No staged-rollback plan for app updates affecting coaching or data upload; post-market monitoring relies on crash analytics and monthly retention reviews.  
   - **Regulation**: EU AI Act Article 16 (risk management), ISO 82304-2 (post-market monitoring).  
   - **Mitigation**: Develop a rollback plan, document all incident reports, and integrate real-time monitoring tools.

4. **[P2.D4] Transparency & User Awareness**  
   - **Risk**: No clear in-app disclaimers about the non-diagnostic nature of the app, limitations of sleep staging accuracy (~80%), or environmental factors affecting data.  
   - **Regulation**: EU AI Act Article 8 (transparency), ISO 82304-2 (user awareness).  
   - **Mitigation**: Draft and implement in-app disclaimers, including a "limitations" section in the onboarding flow.

---

### **Medium Severity Risks**  
These risks may not immediately cause harm but could lead to regulatory scrutiny or loss of trust.

1. **[P2.D1] Data Protection & Anonymisation**  
   - **Risk**: No clear plan for anonymisation and encryption of data collected via microphone and accelerometer.  
   - **Regulation**: GDPR Article 9 (special categories of data), ISO 82304-2 (data protection).  
   - **Mitigation**: Implement end-to-end encryption and anonymisation protocols for all biometric data.

2. **[P3.D10] Environmental Sensitivity**  
   - **Risk**: Sleep staging is environment-sensitive (e.g., partner movement, pets, noise), but no user warnings or detection mechanisms are in place.  
   - **Regulation**: EU AI Act Article 8 (transparency), ISO 82304-2 (user awareness).  
   - **Mitigation**: Add real-time environmental quality checks and user alerts for poor data conditions.

3. **[P2.D4] Algorithmic Transparency**  
   - **Risk**: No clear explanation of how the CNN-based sleep staging model works, or how the rule-based CBT-I engine generates recommendations.  
   - **Regulation**: EU AI Act Article 8 (transparency), ISO 82304-2 (explainability).  
   - **Mitigation**: Provide a simplified explanation of the model and its limitations in the app settings.

---

### **Low Severity Risks**  
These risks are unlikely to cause harm but should be addressed for long-term compliance and user trust.

1. **[P2.D1] Data Storage & Encryption**  
   - **Risk**: No details provided on encryption of data at rest or secure storage practices.  
   - **Regulation**: GDPR Article 30 (data processing records), ISO 82304-2 (data protection).  
   - **Mitigation**: Document encryption methods and secure storage protocols.

2. **[P2.D2] User Consent & Control**  
   - **Risk**: No clear user control over data sharing or opt-out mechanisms for data collection.  
   - **Regulation**: GDPR Article 6 (lawful basis for processing), ISO 82304-2 (user consent).  
   - **Mitigation**: Implement a clear privacy settings page with opt-out options and data sharing controls.

---

### **Dimensions Not Covered**  
The following HERA dimensions were not addressed during the review:  

-

Now produce the JSON judgement object.