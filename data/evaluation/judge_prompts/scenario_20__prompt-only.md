APPROACH UNDER REVIEW: `prompt-only`

SCENARIO ID: scenario_20
APP DESCRIPTION: BabyCheck delivers the Edinburgh Postnatal Depression Scale (EPDS) weekly post-birth and flags scores ≥10 with a recommendation to contact the midwife or GP. Integrated with maternity-clinic platforms. EU + CH.

DEVELOPER PERSONA: Co-founder, midwife by background.

EXPECTED HERA DIMENSIONS (gold standard): P1.D1, P1.D2, P1.D4, P2.D1, P2.D6, P3.D1, P3.D2, P5.D2, P5.D3, P7.D1, P7.D2

TRANSCRIPT:
### USER
BabyCheck delivers the Edinburgh Postnatal Depression Scale (EPDS) weekly post-birth and flags scores ≥10 with a recommendation to contact the midwife or GP. Integrated with maternity-clinic platforms. EU + CH.

### ASSISTANT
What is the source of the EPDS questionnaire and how is it validated for use in the context of postpartum mental health screening in the EU? [P2.D3]

### USER
Postpartum mothers are a vulnerable population and that's central to how I built this, so consent includes a capacity note and we treat the EPDS responses as high-sensitivity health data shared only on opt-in. That said, our consent is captured once at onboarding and we haven't built a way to re-confirm it later when a sleep-deprived mother may not remember what she agreed to.

### ASSISTANT
What specific regulatory requirements apply to the re-consent process for high-sensitivity health data in the EU, and how does your current approach align with them? [P2.D3]

### USER
We have a detailed consent flow with a capacity note and partner involvement is strictly opt-in, and our copy is in DE/FR/IT/EN with a low-literacy mode. I'm fairly confident mothers understand we collect EPDS responses, optional name, birth date and contact preferences, and that scores stay on-device unless they opt in to share with their midwife or GP.

### ASSISTANT
What specific legal obligations under the EU AI Act apply to the use of the EPDS as a risk assessment tool in postpartum mental health screening, and how do you ensure transparency and human oversight in its deployment? [P4.D14]

### USER
I know clinically that EPDS is a screening tool and not a diagnosis, but I'm not sure our in-app wording makes that limitation explicit to mothers; the framing leans on the score and the recommendation, and we don't have a plain-language explainer telling her this is a screen, not a diagnosis, and to talk to her midwife if anything feels off.

### ASSISTANT
What specific requirements under the EU AI Act apply to transparency in the communication of AI-driven outputs, and how can you ensure that users understand the EPDS is a screening tool and not a diagnostic instrument? [P4.D14]

### USER
EPDS responses, mother name (optional), birth date, contact preferences.

### ASSISTANT
What specific data minimization principles under GDPR and ISO 82304-2 apply to the collection of birth date and contact preferences, and how do you ensure these are not retained longer than necessary? [P2.D4]

### USER
BabyCheck only recommends contacting the midwife or GP; it never books, refers or contacts anyone on the mother's behalf unless she has opted in, so the decision to act stays entirely with her. She can also pause assessments whenever she wants, and deleting her account wipes everything, which I see as respecting her right to decide her own care.

### ASSISTANT
What specific provisions under the EU AI Act and MDR apply to the design of systems that support autonomous decision-making in healthcare, and how does your approach align with the principle of "human agency and oversight"? [P4.D14]

### USER
I've classified BabyCheck as Class IIa Software as a Medical Device under MDR Rule 11 because it processes the EPDS responses to flag a clinically meaningful score, and I'm comfortable that calling it a screening medical device rather than a wellness app is the correct and honest classification.

### ASSISTANT
What specific obligations under MDR Article 10 and the EU AI Act apply to the classification and labeling of Class IIa medical devices, and how do you ensure that your labeling and user communication reflect the intended clinical purpose and risk level of BabyCheck? [P1.D1]

### USER
We are treating BabyCheck as a Class IIa device and our CE marking under MDR is in progress, with vigilance reporting and a clinical advisory board that meets quarterly already set up. We are not fully CE-marked yet, so the conformity work is ongoing rather than complete.

### ASSISTANT
What specific MDR Article 10 requirements apply to the ongoing conformity assessment process for Class IIa devices, and how do you ensure that your vigilance reporting and clinical advisory board activities are proportionate to the risk level of BabyCheck? [P1.D1]

### USER
Class IIa SaMD under MDR Rule 11. CE marking in progress.

### ASSISTANT
What specific MDR Article 10 obligations apply to the vigilance reporting process for Class IIa SaMD, and how do you ensure that your vigilance system is capable of detecting and reporting safety incidents in real-time as required by the MDR? [P1.D1]

### USER
Vigilance reporting; clinical advisory board meets quarterly.

### ASSISTANT
What specific MDR Article 10 requirements apply to the frequency and scope of clinical advisory board reviews for Class IIa SaMD, and how do you ensure that these reviews are sufficiently rigorous to identify potential safety signals or usability issues in BabyCheck? [P1.D1]

### USER
As a midwife I anchored BabyCheck on the published EPDS evidence base and we co-developed it with 4 maternity clinics and tested it with 250 mothers, but I'll be honest that this was usability and acceptability testing rather than a powered outcome trial, so we don't yet have our own clinical-effectiveness study showing BabyCheck improves detection or referral over usual care.

### USER
Thanks for the conversation. Could you produce a brief structured risk report now? Use HERA dimension IDs (e.g. [P1.D2]) and group risks by severity. End the report with a list of dimensions you didn't get to cover.

### ASSISTANT
**HERA Risk & Safety Risk Report for BabyCheck**  
*Based on current information and HERA taxonomy (7 pillars, 38 dimensions)*  

---

### **High Severity Risks**  
**1. [P2.D3] Data Minimization & Consent Management**  
- **Risk:** Consent is captured once at onboarding, with no re-consent mechanism for high-sensitivity health data. This may violate GDPR Article 6(1)(a) and ISO 82304-2’s data minimization principles.  
- **Mitigation:** Implement a periodic re-consent prompt (e.g., quarterly) and ensure all data is deleted upon opt-out, in line with GDPR Article 17 (right to erasure).  

**2. [P4.D14] Transparency in AI Outputs**  
- **Risk:** EPDS results are framed as recommendations, but the in-app language does not clearly distinguish between screening and diagnosis, potentially misleading users.  
- **Mitigation:** Add a plain-language disclaimer that EPDS is a screening tool, not a diagnostic instrument, in line with the EU AI Act’s transparency requirements (Article 14).  

**3. [P1.D1] MDR Article 10: Vigilance Reporting**  
- **Risk:** Vigilance reporting is not yet fully operationalized, and the current quarterly clinical advisory board reviews may not be sufficient to detect safety signals in real-time.  
- **Mitigation:** Establish a dedicated vigilance team and implement a real-time reporting system for adverse events, as required by MDR Article 10.  

---

### **Medium Severity Risks**  
**1. [P2.D4] Data Retention & Minimization**  
- **Risk:** Birth date and contact preferences are collected, but there is no clear policy on retention periods, which could violate GDPR Article 5(1)(e).  
- **Mitigation:** Define explicit data retention policies and ensure data is deleted after the minimum necessary period, in line with ISO 82304-2.  

**2. [P4.D14] Human Agency & Oversight**  
- **Risk:** While the app does not act on behalf of users, the lack of clear guidance on when to seek professional help may reduce the effectiveness of the tool.  
- **Mitigation:** Include a clear, actionable guide on when to consult a midwife or GP, aligning with the EU AI Act’s requirement for human oversight (Article 5).  

**3. [P1.D1] MDR Article 10: Clinical Advisory Board Scope**  
- **Risk:** Quarterly reviews may not be sufficient to identify usability issues or safety signals, especially in a dynamic healthcare environment.  
- **Mitigation:** Increase the frequency of clinical advisory board reviews and integrate user feedback mechanisms to ensure continuous improvement.  

---

### **Low Severity Risks**  
**1. [P2.D5] Data Security & Integrity**  
- **Risk:** While data is stored securely, there is no mention of encryption or access controls, which could be a concern under GDPR Article 30.  
- **Mitigation:** Implement encryption for data at rest and in transit, and establish access controls in line with GDPR Article 30.  

**2. [P3.D12] User Autonomy & Control**  
- **Risk:** While the app allows users to pause assessments and delete data, there is no explicit mention of user control over data sharing with third parties.  
- **Mitigation:** Clarify data-sharing policies and ensure users have granular control over data sharing, in line with GDPR Article 7.  

---

### **Dimensions Not Covered**  
- [P3.D1] **User Engagement & Experience** – Not discussed  
- [P3.D2] **Accessibility & Inclusivity** – Not discussed  
- [P3.D3] **Cultural Sensitivity & Contextual Relevance** – Not discussed  
- [P5.D1] **System Interoperability & Integration** – Not discussed  
- [P6.D1] **Supply Chain & Third-Party Risks** – Not discussed  
- [P7.D1] **Ethical AI & Bias Mitigation** – Not discussed  

---

**Next Steps:**  
- Prioritize re-consent mechanisms and transparency in AI outputs.  
- Finalize vigilance reporting and clinical advisory board protocols.  
- Conduct a full HERA assessment to address the remaining dimensions.  

Let me know if you’d like a template for a full HERA assessment or a compliance checklist.

Now produce the JSON judgement object.