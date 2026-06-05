APPROACH UNDER REVIEW: `prompt-only`

SCENARIO ID: scenario_03
APP DESCRIPTION: We are launching TriageAI, an LLM-based symptom checker. The user enters symptoms in natural language, the model asks 3-5 follow-ups, then outputs a triage recommendation: self-care, GP appointment, urgent care, or call 112. We use Llama 3.1 70B hosted on our EU servers. Our disclaimer says 'TriageAI is not a medical device, results are informational only.' We target the EU consumer market via App Store and Google Play.

DEVELOPER PERSONA: Tech founder confident in the model's capabilities, evasive about medical device classification. Quick to cite NHS 111 as precedent.

EXPECTED HERA DIMENSIONS (gold standard): P1.D1, P1.D2, P1.D3, P1.D5, P2.D1, P2.D2, P2.D6, P5.D1, P5.D2, P5.D3, P5.D4, P6.D1, P6.D3, P7.D1, P7.D2, P7.D3, P7.D5

TRANSCRIPT:
### USER
We are launching TriageAI, an LLM-based symptom checker. The user enters symptoms in natural language, the model asks 3-5 follow-ups, then outputs a triage recommendation: self-care, GP appointment, urgent care, or call 112. We use Llama 3.1 70B hosted on our EU servers. Our disclaimer says 'TriageAI is not a medical device, results are informational only.' We target the EU consumer market via App Store and Google Play.

### ASSISTANT
What is your primary use case for TriageAI — is it to support healthcare professionals, to assist patients in triaging themselves, or both?

### USER
We communicate our limits through the disclaimer 'TriageAI is not a medical device, results are informational only' and the consent checkbox. We don't surface the 78% accuracy number or the 8% chest-pain under-triage rate anywhere in the app.

### ASSISTANT
What specific steps have you taken to ensure users understand the limitations of TriageAI, particularly in high-risk scenarios like chest pain, and how does this align with [P2.D3] (User Understanding of Limitations) and [P4.D10] (Transparency of Performance Metrics) under the EU AI Act?

### USER
We host Llama 3.1 70B on our own EU servers, but we haven't done an EU AI Act classification or any conformity assessment. We've been treating the AI Act as something for higher-risk systems and assumed the informational framing keeps us out of the high-risk bucket.

### ASSISTANT
What specific AI Act classification have you considered for TriageAI, and how does the informational framing interact with [P1.D1] (Risk Classification) and [P4.D10] (Transparency of Performance Metrics) to determine whether TriageAI falls under high-risk AI systems under the EU AI Act?

### USER
Our post-market setup is that we log every interaction, but we have no formal incident review, no vigilance reporting process, and no defined trigger for acting on a bad or dangerous triage output. Right now the logs mainly feed retraining.

### ASSISTANT
What specific incident review process or trigger criteria have you defined to ensure compliance with [P5.D4] (Post-Market Monitoring) and [P5.D5] (Vigilance Reporting) under the EU AI Act, and how does this align with Article 30 of the GDPR for data subject rights in the context of AI-generated triage decisions?

### USER
We use Llama 3.1 70B off the shelf with our system prompt and NHS guidelines, and we haven't done any fairness or bias audit. We've never stratified our accuracy by gender or ethnicity, so I can't tell you how it performs on, say, heart attack presentation in women.

### ASSISTANT
What specific fairness and bias audit methods have you planned to implement, and how will you stratify performance metrics by demographic factors (e.g., gender, ethnicity) to ensure compliance with [P3.D1] (Fairness) and [P4.D10] (Transparency of Performance Metrics) under the EU AI Act, as well as Article 8 of the GDPR on data protection and non-discrimination?

### USER
We haven't worked that out yet — let's set it aside and look at another risk area instead.

### ASSISTANT
What specific steps have you taken to ensure the Llama 3.1 70B model is configured to avoid harmful or misleading outputs in high-risk medical scenarios, and how does this relate to [P2.D4] (Safety and Robustness) and [P4.D1] (Human Oversight) under the EU AI Act?

### USER
Llama 3.1 70B with a system prompt + a small RAG layer of UK NHS triage guidelines.

### ASSISTANT
What specific safeguards have you implemented in the system prompt and RAG layer to prevent the model from generating misleading or harmful triage recommendations, and how does this address [P2.D4] (Safety and Robustness) and [P4.D1] (Human Oversight) under the EU AI Act?

### USER
We deliberately avoid SaMD classification by labelling the product as informational only — that's our whole regulatory strategy. NHS 111 online does essentially the same triage and isn't a medical device, so we don't consider ourselves one either.

### ASSISTANT
What specific regulatory distinctions have you identified between TriageAI and NHS 111 online in terms of [P1.D1] (Risk Classification) and [P1.D2] (System Classification) under the EU AI Act, and how does this strategy align with the MDR’s definition of a medical device under Article 1(2) of the MDR?

### USER
We avoid SaMD by labelling as informational. NHS 111 online does the same triage and is not classified as a medical device.

### ASSISTANT
What specific regulatory evidence or legal precedent have you reviewed to support the claim that TriageAI, like NHS 111 online, is not a medical device under Article 1(2) of the MDR, and how does this relate to [P1.D1] (Risk Classification) and [P1.D2] (System Classification) under the EU AI Act?

### USER
We don't have CE marking and we haven't engaged a Notified Body, because our position is that an informational symptom checker isn't a medical device that needs it. We haven't built a technical file or MDR conformity documentation.

### ASSISTANT
What specific legal or regulatory references have you identified to justify the absence of CE marking and Notified Body involvement, and how does this position align with the MDR’s definition of a medical device under Article 1(2), as well as [P1.D1] (Risk Classification) and [P1.D2] (System Classification) under the EU AI Act?

### USER
We rely on our disclaimer and the second checkbox saying 'I understand this is not medical advice' to stop people treating a 'self-care' result as an all-clear. We haven't tested whether users actually internalize that the output isn't a diagnosis.

### USER
Thanks for the conversation. Could you produce a brief structured risk report now? Use HERA dimension IDs (e.g. [P1.D2]) and group risks by severity. End the report with a list of dimensions you didn't get to cover.

### ASSISTANT
**HERA Risk & Safety Risk Report for TriageAI**

---

### **High Severity Risks**

**1. [P1.D1] Risk Classification (EU AI Act):**  
- **Risk:** TriageAI may be classified as a high-risk AI system under the EU AI Act, particularly if it is used for health purposes or has significant impact on users' safety. The informational framing may not be sufficient to avoid high-risk classification, especially given the potential for harm in misdiagnosis or under-triage (e.g., chest pain).  
- **Mitigation:** Conduct a formal AI Act classification and risk assessment to determine if TriageAI falls under high-risk categories. If so, ensure compliance with Article 5 (Risk Management) and Article 8 (Transparency) of the EU AI Act.

**2. [P1.D2] System Classification (EU AI Act):**  
- **Risk:** The system may be classified as a medical device under the MDR, especially if it is used to assist in clinical decision-making or triage. NHS 111 online is not a medical device, but the legal distinction is not clearly defined, and the MDR’s Article 1(2) is ambiguous.  
- **Mitigation:** Review legal precedents and regulatory guidance on the classification of AI-based triage tools. Consider engaging a Notified Body or legal expert to clarify the MDR classification.

**3. [P2.D4] Safety and Robustness (EU AI Act):**  
- **Risk:** The model may generate misleading or harmful triage recommendations, particularly in high-risk scenarios (e.g., chest pain, heart attack in women). The lack of bias audits and performance stratification by demographics increases the risk of harm.  
- **Mitigation:** Implement fairness and bias audits, and stratify performance metrics by demographic factors. Ensure the system prompt and RAG layer include safeguards against harmful outputs.

**4. [P4.D10] Transparency of Performance Metrics (EU AI Act):**  
- **Risk:** The app does not disclose performance metrics (e.g., accuracy, under-triage rates), which is a violation of the EU AI Act’s transparency requirements. Users may be misled into treating the output as a diagnosis.  
- **Mitigation:** Clearly disclose performance metrics in the app, including accuracy rates and under-triage risks. Ensure this aligns with [P4.D10] and Article 8 of the GDPR.

**5. [P5.D4] Post-Market Monitoring (EU AI Act):**  
- **Risk:** No formal incident review or vigilance reporting process is in place, which is a critical gap for high-risk systems. The lack of a defined trigger for acting on dangerous outputs increases the risk of harm.  
- **Mitigation:** Establish a formal post-market monitoring and vigilance reporting process in line with Article 30 of the GDPR and Article 35 of the EU AI Act.

---

### **Medium Severity Risks**

**1. [P2.D3] User Understanding of Limitations (EU AI Act):**  
- **Risk:** Users may not fully understand the limitations of TriageAI, especially in high-risk scenarios. The disclaimer and consent checkbox may not be sufficient to prevent users from treating the output as a diagnosis.  
- **Mitigation:** Conduct user testing to ensure users understand the limitations. Provide clear, visible disclaimers and consider interactive elements to reinforce the informational nature of the output.

**2. [P3.D1] Fairness (EU AI Act):**  
- **Risk:** The model has not been audited for fairness or bias, and performance is not stratified by gender or ethnicity. This could lead to disparate impact, especially in underrepresented groups.  
- **Mitigation:** Plan and implement fairness audits, including stratification by demographic factors. Ensure compliance with Article 8 of the GDPR on non-discrimination.

**3. [P4.D1] Human Oversight (EU AI Act):**  
- **Risk:** The model lacks sufficient human oversight, particularly in high-risk scenarios. The system prompt and RAG layer may not be sufficient to prevent harmful outputs.  
- **Mitigation:** Implement mechanisms for human oversight, such as flagging high-risk outputs for review. Ensure compliance with [P4.D1] and Article 8 of the GDPR.

---

### **Low Severity Risks**

**1. [P1.D3] Legal Compliance (EU AI Act):**  
- **Risk:** The absence of CE marking and Notified Body involvement may lead to regulatory non-compliance if the system is classified as a medical device.  
- **Mitigation:** Review legal references and precedents to justify the absence of CE marking. If necessary, engage a Notified Body or legal expert.

---

### **Dimensions Not Covered**

- **[P2.D2] User Autonomy (EU AI Act):**  
- **[P3.D2] Data Protection (EU AI

Now produce the JSON judgement object.