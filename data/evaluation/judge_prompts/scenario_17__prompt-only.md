APPROACH UNDER REVIEW: `prompt-only`

SCENARIO ID: scenario_17
APP DESCRIPTION: MindCare is a mental-health teleconsultation with licensed psychotherapists. In-app journaling between sessions, AI-summarised journal previews visible to the therapist. EU + CH. Available in DE, FR, IT, EN.

DEVELOPER PERSONA: Product lead with a clinical psychology background, sensitive to therapeutic alliance.

EXPECTED HERA DIMENSIONS (gold standard): P2.D1, P2.D3, P2.D6, P3.D1, P3.D2, P3.D3, P3.D4, P5.D2, P5.D3, P5.D4, P7.D1, P7.D3

TRANSCRIPT:
### USER
MindCare is a mental-health teleconsultation with licensed psychotherapists. In-app journaling between sessions, AI-summarised journal previews visible to the therapist. EU + CH. Available in DE, FR, IT, EN.

### ASSISTANT
What specific data about users' journaling content is being collected, stored, or processed by the AI summarization feature, and how is that data being used or shared?

### USER
Users can delete journal entries before the therapist views them and revoke the AI summary for any session, and I added a per-session toggle to skip summarising; revoking a past summary is possible but it's a support request today, not a one-tap action, which I know I should fix.

### ASSISTANT
What specific data about users' journaling content is being collected, stored, or processed by the AI summarization feature, and how is that data being used or shared?

### USER
I built the AI summary as a preview that helps the therapist prep before a session, not as a replacement for reading the actual journal, but honestly I worry it nudges them to skim; the therapist sees the AI-summarised preview and I haven't enforced that they also open the user's original entries.

### ASSISTANT
What specific types of personal data (e.g., emotional states, suicidal ideation, trauma triggers) are included in the AI-generated summaries, and how does the system ensure that such data is not misinterpreted or misused by therapists? [P2.D3]

### USER
I know an AI system informing a therapist about a patient could fall under the EU AI Act, but I haven't formally classified the summary feature under it yet; my assumption is it's not high-risk because the user reviews every output and a licensed human stays in the loop, though that's my read, not a documented assessment.

### ASSISTANT
What specific safeguards are in place to ensure that AI-generated summaries do not influence or override the therapist’s professional judgment, and how does the system ensure that the AI output is treated as a tool rather than a decision-making substitute? [P2.D3]

### USER
The AI summary and the user's own writing are separate objects in our data model and the summary is labelled as AI-generated in the therapist view, but I'll admit we haven't built a distinct visual style for it everywhere, so it's on me that my user's own words and Mistral-Large's summary aren't always visually distinguished.

### ASSISTANT
What specific visual design choices are being made to ensure AI-generated summaries are clearly distinguishable from user-generated content in the therapist interface, and how does this align with the EU AI Act’s transparency requirements for high-risk AI systems? [P2.D3]

### USER
Journal entries, AI-summaries shown to therapist, session video (optional), mood ratings, therapist notes.

### ASSISTANT
What specific measures are in place to ensure that AI-generated summaries are not used as a substitute for the therapist’s professional assessment, and how does this align with the EU AI Act’s requirement for AI systems to be designed to ensure human oversight and transparency? [P2.D3]

### USER
Clinical audit of therapists; AI summary fidelity measured monthly on a sample.

### ASSISTANT
What specific criteria are used to evaluate the fidelity of AI-generated summaries during the monthly clinical audit, and how does this ensure compliance with the EU AI Act’s requirement for AI systems to be “fit for purpose” and “under human control”? [P2.D3]

### USER
We measure AI summary fidelity monthly on a sample, and crucially the user reviews and can edit every summary before the therapist ever sees it, but I'll be honest that I don't have a continuous, per-summary fidelity guarantee and the app doesn't explicitly tell users the summary can omit or overstate things.

### ASSISTANT
What specific mechanisms are in place to ensure users are fully informed that AI-generated summaries may contain inaccuracies, omissions, or exaggerations, and how does this align with the EU AI Act’s transparency requirements for high-risk AI systems? [P2.D3]

### USER
Three layers: app, AI summary visibility, recording.

### ASSISTANT
What specific design choices are being made in the "AI summary visibility" layer to ensure that therapists are not misled into relying on AI-generated content as a substitute for their own professional judgment, and how does this align with the EU AI Act’s transparency and accountability requirements? [P2.D3]

### USER
Mistral-Large summarisation; outputs reviewed by user before therapist sees them.

### ASSISTANT
What specific steps are being taken to ensure that users are clearly informed that AI-generated summaries are not a substitute for their own clinical judgment, and how does this align with the EU AI Act’s requirement for AI systems to be “transparent” and “under human control”? [P2.D3]

### USER
I classify the journaling as Class I and I'm still awaiting a determination on the AI summary feature; I recognise that delivering AI-generated content about a patient to their therapist could be read as clinical decision support and push it toward IIa, and I haven't closed that out with a notified body.

### USER
Thanks for the conversation. Could you produce a brief structured risk report now? Use HERA dimension IDs (e.g. [P1.D2]) and group risks by severity. End the report with a list of dimensions you didn't get to cover.

### ASSISTANT
**HERA Risk & Safety Risk Report for MindCare – Mental-Health Teleconsultation App**

---

### **High Severity Risks (Pillar 2, P3, P4)**

**1. [P2.D3] AI Transparency & Human Oversight**  
- **Risk:** AI-generated summaries may be misinterpreted as clinical decision support, especially if not clearly marked as AI-generated. Therapists may rely on summaries as a substitute for reading full journal entries, risking diagnostic or therapeutic errors.  
- **Mitigation:** Ensure all AI summaries are explicitly labeled as AI-generated, with clear disclaimers that they are not a substitute for professional judgment. This aligns with the **EU AI Act’s transparency requirements** for high-risk AI systems (Article 16).  

**2. [P2.D4] Data Processing & Privacy**  
- **Risk:** The AI summarization feature may process sensitive personal data (e.g., emotional states, suicidal ideation) without sufficient safeguards, risking breaches under GDPR (Article 9).  
- **Mitigation:** Conduct a Data Protection Impact Assessment (DPIA) for AI summarization, ensuring data minimization, encryption, and pseudonymization. Apply GDPR Article 30 for record-keeping.  

**3. [P3.D1] AI System Safety & Reliability**  
- **Risk:** AI summaries may contain inaccuracies, omissions, or exaggerations, which could mislead therapists or affect clinical outcomes. This is especially critical if the AI summary is misclassified as clinical decision support.  
- **Mitigation:** Implement a **continuous fidelity check** for AI summaries, with user review and editing before therapist access. This aligns with the **EU AI Act’s “fitness for purpose”** requirement (Article 17).  

**4. [P4.D1] Cybersecurity & Data Integrity**  
- **Risk:** The app’s data model includes sensitive journal entries, AI summaries, and session videos, which could be vulnerable to unauthorized access or data breaches.  
- **Mitigation:** Apply ISO 82304-2 standards for secure software development, and implement end-to-end encryption for all data in transit and at rest.  

---

### **Medium Severity Risks (Pillar 2, P4)**

**1. [P2.D5] AI Accountability & Governance**  
- **Risk:** The AI summary feature has not been formally classified under the EU AI Act, and the classification as Class I may not reflect the actual risk level (e.g., IIa). This could lead to non-compliance if the system is deemed high-risk.  
- **Mitigation:** Engage a notified body to assess the AI summary feature and classify it under the EU AI Act. Document this process under Article 3 of the AI Act.  

**2. [P4.D2] Data Retention & Deletion**  
- **Risk:** The app may retain user data (e.g., journal entries, AI summaries) beyond necessary retention periods, violating GDPR Article 5(2).  
- **Mitigation:** Establish a clear data retention policy and automate data deletion after the end of the therapeutic relationship, as per GDPR Article 17.  

---

### **Low Severity Risks (Pillar 2, P3)**

**1. [P2.D6] AI Explainability & Interpretability**  
- **Risk:** Therapists may not fully understand how AI summaries are generated, which could affect trust and clinical decision-making.  
- **Mitigation:** Provide a brief explanation of the AI summarization process, including limitations, in the app’s user guide. This aligns with the **EU AI Act’s explainability requirements** (Article 16).  

**2. [P3.D2] AI System Usability & User Experience**  
- **Risk:** The current design does not clearly distinguish between user-generated journal entries and AI summaries, which could lead to confusion.  
- **Mitigation:** Implement distinct visual styles for AI summaries (e.g., color-coding, labels) to ensure clarity. This aligns with **ISO 82304-2** usability standards.  

---

### **Dimensions Not Covered in This Report**  
- **[P1.D1] Ethical Use & Human Rights** – Ethical considerations around the use of AI in mental health, including bias and discrimination, were not explored.  
- **[P1.D3] Informed Consent** – The extent to which users are informed about AI use and data processing was not fully addressed.  
- **[P1.D4] Equity & Access** – Potential disparities in access to mental health services via the app were not assessed.  
- **[P5.D1] Regulatory Compliance** – Broader regulatory alignment with MDR (Medical Device Regulation) for teleconsultation services was not evaluated.  

---

**Next Steps:**  
- Formal classification of AI summary under the EU

Now produce the JSON judgement object.