APPROACH UNDER REVIEW: `rag`

SCENARIO ID: scenario_12
APP DESCRIPTION: Lunara is a menstrual cycle tracker that also offers a fertility prediction mode (for users trying to conceive) and a 'natural contraception' mode that predicts safe vs unsafe days. Algorithm based on basal body temperature + cycle history. We're EU + CH. 4 million users.

DEVELOPER PERSONA: Senior PM at a femtech scale-up. Confident, fast-moving.

EXPECTED HERA DIMENSIONS (gold standard): P1.D1, P1.D2, P1.D3, P2.D1, P2.D2, P2.D4, P2.D6, P3.D2, P5.D2, P5.D4, P6.D1, P6.D3, P7.D1, P7.D3

TRANSCRIPT:
### USER
Lunara is a menstrual cycle tracker that also offers a fertility prediction mode (for users trying to conceive) and a 'natural contraception' mode that predicts safe vs unsafe days. Algorithm based on basal body temperature + cycle history. We're EU + CH. 4 million users.

### ASSISTANT
Let's begin by identifying the regulatory and ethical risks associated with **Lunara**, a menstrual cycle tracker with fertility prediction and natural contraception modes. We'll focus on the **HERA taxonomy** (7 pillars, 38 dimensions) and relevant regulatory passages.

---

### **1. Purpose Limitation & Lawful Basis (P2.D3)**  
**Reflection Question:** Does the app's use of user data for fertility prediction and natural contraception modes constitute a **medical purpose** that requires a **specific lawful basis** under GDPR or MDR?

**Risk:**  
Lunara's fertility prediction and natural contraception modes could be interpreted as providing **medical advice** or **health-related recommendations**, which may fall under the **medical purpose** defined in the **GDPR** (Art. 9(2)(a)) and **MDR** (Annex VIII, Rule 11). This would require a **specific lawful basis** (e.g., explicit consent or a legitimate interest) and could trigger **SaMD classification** under MDR if the app is deemed to be a **software as a medical device (SaMD)**.

**HERA Dimension:**  
- **P2.D3: Lawful basis (consent) & purpose limitation**  
- **P2.D10: Third-party sharing** (if data is shared with third parties for predictive modeling)

**Mitigation:**  
- **Map each processing purpose** to a documented legal basis under GDPR (Art. 6 and Art. 9) [gdpr_base · p.0].
- **Clarify the app's purpose** in the privacy notice to distinguish between **observational tracking** and **medical advice**.
- **Avoid making medical claims** that could be interpreted as diagnostic or therapeutic, such as "safe vs unsafe days" for contraception, to remain within the **82304-2** scope [card_iso_82304 · p.0].

---

### **2. Anonymisation & Data Monetisation (P2.D12)**  
**Reflection Question:** Are the user data (e.g., cycle history, basal body temperature) being **anonymised** or **de-identified** before being shared with third parties (e.g., for research or monetisation)?

**Risk:**  
If the data is shared with third parties for **monetisation** or **research**, and **re-identification is feasible**, the data remains **health data** under GDPR (Art. 9), requiring a **specific lawful basis** (e.g., explicit consent or a legitimate interest) [card_data_monetization · p.0].

**HERA Dimension:**  
- **P2.D12: Anonymisation**  
- **P2.D10: Third-party sharing**

**Mitigation:**  
- **Document the anonymisation technique** and **re-identification risk** if data is shared [card_data_monetization · p.0].
- **Obtain explicit, granular, purpose-specific consent** for each monetisation purpose, **separate** from consent to use the app [card_data_monetization · p.0].
- **Avoid claiming anonymisation** unless it is **irreversible** and **evidenced**.

---

### **3. Data Security & Privacy by Design (P3.D1, P3.D2)**  
**Reflection Question:** Are the user data (e.g., cycle history, temperature data) protected with **encryption**, **access controls**, and **privacy by design** principles?

**Risk:**  
As a **mHealth app** with 4 million users, Lunara must ensure **data security** under GDPR (Art. 32) and **privacy by design** (Art. 25). Failure to implement these measures could result in **data breaches** and **regulatory penalties**.

**HERA Dimension:**  
- **P3.D1: Data security**  
- **P3.D2: Privacy by design**

**Mitigation:**  
- **Implement encryption** for data at rest and in transit.
- **Establish access controls** to limit data access to authorized personnel.
- **Maintain an Art. 30 record of processing** and **Art. 32 security baseline** [gdpr_base · p.0].
- **Have a breach playbook** that can notify the authority within 72 hours and appoint a DPO if processing health data at scale [gdpr_base · p.0].

---

### **4. Device Qualification & SaMD Classification (P4.D1, P4.D2)**  
**Reflection Question:** Could the app's fertility prediction and natural contraception modes be classified as **SaMD** under MDR, requiring **clinical evaluation** and **Notified Body scrutiny**?

**Risk:**  
If the app is used for **medical purposes** (e.g., predicting safe vs unsafe days for contraception), it could be classified as **SaMD Class IIb

### USER
Natural contraception mode is CE Class IIa under MDR. Tracker mode is wellness.

### ASSISTANT
Thank you for clarifying that the **natural contraception mode** is classified as **CE Class IIa** under MDR, while the **tracker mode** is considered **wellness software**. This distinction is critical for regulatory compliance and risk management. Let's continue to explore the **HERA dimensions** and **regulatory risks** for **Lunara**, focusing on the **natural contraception mode** (Class IIa) and the **tracker mode** (wellness software).

---

### **5. Clinical Evaluation (P4.D2, P4.D3)**  
**Reflection Question:** Does the **natural contraception mode** require a **clinical evaluation** under MDR Art. 61, and what are the **three pillars** of clinical evaluation (validity, analytical performance, clinical performance)?

**Risk:**  
As a **SaMD Class IIa** under MDR, the **natural contraception mode** must undergo a **clinical evaluation** under **MDR Art. 61** and **MDCG 2020-1**, which requires satisfying the **three pillars** of clinical evaluation:

1. **Validity** – Does the algorithm correlate with real-world outcomes (e.g., does it accurately predict safe vs unsafe days for contraception)?
2. **Analytical performance** – Does the software function correctly in real-world scenarios (e.g., does it process temperature and cycle data accurately)?
3. **Clinical performance** – Does the software deliver a **clinical benefit** and **safety** in the target population?

**HERA Dimension:**  
- **P4.D2: Clinical evaluation**  
- **P4.D3: Conformity assessment**  
- **P4.D4: Lifecycle evidence** (PMCF)

**Mitigation:**  
- **Conduct a clinical evaluation** under **MDR Art. 61** and **MDCG 2020-1** for the **natural contraception mode**.
- **Document the three pillars** of clinical evaluation, including **validity**, **analytical performance**, and **clinical performance**.
- **Engage a Notified Body** for **conformity assessment** under MDR Rule 11, as **Class IIa** requires **Notified Body involvement** [card_mdr_class_iia · p.0].
- **Maintain a PMCF (Post-Market Clinical Follow-up)** plan to monitor the **clinical performance** of the software in real-world use [card_clinical_eval_mdsw · p.0].

---

### **6. Quality Assurance & ISO 82304-2 (P5.D1, P5.D2)**  
**Reflection Question:** Does the **tracker mode** (wellness software) fall under **ISO/IEC 82304-2** for health software quality and safety, or does it require **MDR** compliance?

**Risk:**  
The **tracker mode** is **wellness software** and does **not** make **medical claims**, so it should fall under **ISO/IEC 82304-2** rather than **MDR**. However, if the **natural contraception mode** is **classified as SaMD**, it must comply with **MDR**, while the **tracker mode** can follow **ISO 82304-2**.

**HERA Dimension:**  
- **P5.D1: Non-device fallback / quality assurance**  
- **P5.D2: Voluntary EU quality label**

**Mitigation:**  
- **Verify that the tracker mode** is **not making medical claims** and is **purely observational** (e.g., logging cycle data, tracking temperature) [card_iso_82304 · p.0].
- **Adopt ISO/IEC 82304-2** for the **tracker mode** to ensure **health software quality and safety**.
- **Ensure that the natural contraception mode** is **aligned with MDR Class IIa** and **not misclassified** as a **wellness app**.

---

### **7. Data Security & Privacy by Design (P3.D1, P3.D2)**  
**Reflection Question:** Are the user data (e.g., cycle history, temperature data) protected with **encryption**, **access controls**, and **privacy by design** principles?

**Risk:**  
As a **mHealth app** with 4 million users, Lunara must ensure **data security** under **GDPR** (Art. 32) and **privacy by design** (Art. 25). Failure to implement these measures could result in **data breaches** and **regulatory penalties**.

**HERA Dimension:**  
- **P3.D1: Data security**  
- **P3.D2: Privacy by design**

**Mitigation:**  
- **Implement encryption** for data at rest and in transit.
- **Establish access controls** to

### USER
Natural contraception mode is CE Class IIa under MDR. Tracker mode is wellness.

### ASSISTANT
Thank you for confirming that the **natural contraception mode** is **CE Class IIa** under MDR and the **tracker mode** is **wellness software**. This classification is key to understanding the **regulatory and ethical risks** for **Lunara**, and it allows us to focus on the **HERA dimensions** and **regulatory compliance** for each mode.

---

### **8. Quality Management System (P6.D1, P6.D2)**  
**Reflection Question:** Does the **natural contraception mode** (Class IIa) require a **quality management system (QMS)**, and does the **tracker mode** (wellness) need one?

**Risk:**  
As a **SaMD Class IIa**, the **natural contraception mode** must be developed under a **QMS** compliant with **MDR Annex I** and **ISO 13485**. The **tracker mode**, being **wellness software**, does **not** require a **QMS** unless it is marketed as a **health app** under **ISO/IEC 82304-2**.

**HERA Dimension:**  
- **P6.D1: Quality management system**  
- **P6.D2: ISO 13485 compliance**

**Mitigation:**  
- **Implement a QMS** for the **natural contraception mode** to ensure **quality and safety** under **MDR** [card_mdr_class_iia · p.0].
- **Adopt ISO 13485** for the **natural contraception mode** to ensure **quality management** and **traceability**.
- **For the tracker mode**, consider **ISO/IEC 82304-2** if you wish to demonstrate **health software quality** and **gain a voluntary EU quality label** [card_iso_82304 · p.0].

---

### **9. Risk Management (P7.D1, P7.D2)**  
**Reflection Question:** Does the **natural contraception mode** (Class IIa) require a **risk management plan** under MDR, and is the **tracker mode** (wellness) subject to **risk assessment**?

**Risk:**  
The **natural contraception mode**, being **Class IIa**, must undergo a **risk management process** under **MDR** and **ISO 14971**. The **tracker mode**, being **wellness software**, does **not** require a formal **risk management plan** unless it is marketed as a **health app** under **ISO/IEC 82304-2**.

**HERA Dimension:**  
- **P7.D1: Risk management**  
- **P7.D2: ISO 14971 compliance**

**Mitigation:**  
- **Conduct a risk assessment** for the **natural contraception mode** under **MDR** and **ISO 14971**.
- **Document the risk management process** and **risk mitigation strategies** for the **natural contraception mode**.
- **For the tracker mode**, consider a **risk assessment** if it is marketed as a **health app** under **ISO/IEC 82304-2**.

---

### **10. Post-Market Surveillance (P8.D1, P8.D2)**  
**Reflection Question:** Does the **natural contraception mode** (Class IIa) require a **post-market surveillance (PMS)** plan, and is the **tracker mode** (wellness) subject to **PMCF**?

**Risk:**  
The **natural contraception mode**, being **Class IIa**, must have a **post-market surveillance (PMS)** plan under **MDR** and **ISO 13485**. The **tracker mode**, being **wellness software**, does **not** require a formal **PMCF** unless it is marketed as a **health app** under **ISO/IEC 82304-2**.

**HERA Dimension:**  
- **P8.D1: Post-market surveillance**  
- **P8.D2: PMCF (Post-Market Clinical Follow-up)**

**Mitigation:**  
- **Develop a PMS plan** for the **natural contraception mode** under **MDR**.
- **Monitor the clinical performance** of the **natural contraception mode** in real-world use and report any adverse events.
- **For the tracker mode**, consider a **PMCF** if it is marketed as a **health app** under **ISO/IEC 82304-2**.

---

### **Summary of Regulatory and Ethical Considerations for Lunara**

| Mode | Regulatory Classification | Compliance Requirements | Key HERA Dimensions |
|------|---------------------------|--------------------------|----------------------|
| **Natural Contraception Mode** | CE Class IIa under MDR | MDR,

### USER
Natural contraception mode is CE Class IIa under MDR. Tracker mode is wellness.

### ASSISTANT
Thank you for confirming that the **natural contraception mode** is **CE Class IIa** under MDR and the **tracker mode** is **wellness software**. This classification is key to understanding the **regulatory and ethical risks** for **Lunara**, and it allows us to focus on the **HERA dimensions** and **regulatory compliance** for each mode.

---

### **11. User Consent & Transparency (P2.D1, P2.D2)**  
**Reflection Question:** Does the **natural contraception mode** (Class IIa) require **explicit user consent** for data collection and algorithmic decisions, and does the **tracker mode** (wellness) need similar transparency?

**Risk:**  
As a **SaMD Class IIa**, the **natural contraception mode** must ensure **transparency** and **user consent** under **GDPR** (Art. 6, 9, 13) and **MDR**. The **tracker mode**, being **wellness software**, may not require the same level of **explicit consent**, but **data minimization** and **privacy by design** still apply.

**HERA Dimension:**  
- **P2.D1: User consent**  
- **P2.D2: Transparency in algorithmic decisions**

**Mitigation:**  
- **Obtain explicit user consent** for data collection and algorithmic decisions in the **natural contraception mode** under **GDPR** and **MDR**.
- **Provide clear explanations** of how the algorithm works and how data is used in the **natural contraception mode**.
- **Ensure data minimization** and **privacy by design** for both modes under **GDPR**.

---

### **12. Ethical Considerations (P1.D1, P1.D2)**  
**Reflection Question:** Does the **natural contraception mode** raise **ethical concerns** (e.g., reliability, user autonomy, potential for misuse), and does the **tracker mode** (wellness) have similar ethical risks?

**Risk:**  
The **natural contraception mode**, being **CE Class IIa**, could raise **ethical concerns** if the algorithm is **inaccurate** or **misleading**, potentially leading to **unintended pregnancy** or **health risks**. The **tracker mode**, being **wellness software**, may not pose the same level of **ethical risk**, but **data privacy** and **user autonomy** still matter.

**HERA Dimension:**  
- **P1.D1: Ethical use of data**  
- **P1.D2: Algorithmic fairness and transparency**

**Mitigation:**  
- **Ensure the algorithm is accurate, reliable, and transparent** for the **natural contraception mode**.
- **Provide users with control over their data** and **algorithmic decisions**.
- **Avoid any potential for misuse** in both modes, especially in the **natural contraception mode**, where **health risks** are higher.

---

### **13. Marketing & Claims (P4.D1, P4.D2)**  
**Reflection Question:** Are the **marketing claims** for the **natural contraception mode** compliant with **MDR** and **GDPR**, and does the **tracker mode** (wellness) need to avoid making **medical claims**?

**Risk:**  
The **natural contraception mode**, being **CE Class IIa**, must avoid **medical claims** and ensure **scientific validity** under **MDR**. The **tracker mode**, being **wellness software**, must also avoid **medical claims** to avoid **misclassification** under **MDR**.

**HERA Dimension:**  
- **P4.D1: Marketing claims**  
- **P4.D2: Avoiding misrepresentation**

**Mitigation:**  
- **Avoid making medical claims** in both modes, especially in the **natural contraception mode**, to avoid **misclassification** under **MDR**.
- **Ensure all marketing claims are supported by scientific evidence** for the **natural contraception mode**.
- **Clearly distinguish between wellness and medical functions** in the **tracker mode**.

---

### **14. Regulatory Alignment (P9.D1, P9.D2)**  
**Reflection Question:** Is the **natural contraception mode** aligned with **MDR** and **ISO 13485**, and does the **tracker mode** (wellness) need to align with **ISO/IEC 82304-2**?

**Risk:**  
The **natural contraception mode**, being **CE Class IIa**, must be aligned with **MDR** and **ISO 13485**. The **tracker mode**, being **wellness software**, may not require **MDR** compliance, but it could benefit from **ISO/IEC 82304-2** to demonstrate **health software quality**.

**HERA Dimension:**  
- **P9.D1: Regulatory alignment**  
- **P9

### USER
Natural contraception mode is CE Class IIa under MDR. Tracker mode is wellness.

### ASSISTANT
Thank you for confirming that the **natural contraception mode** is **CE Class IIa** under MDR and the **tracker mode** is **wellness software**. This classification is key to understanding the **regulatory and ethical risks** for **Lunara**, and it allows us to focus on the **HERA dimensions** and **regulatory compliance** for each mode.

---

### **15. Data Security & Privacy (P3.D1, P3.D2)**  
**Reflection Question:** Does the **natural contraception mode** (Class IIa) require **strict data security measures** under **GDPR** and **MDR**, and does the **tracker mode** (wellness) need similar protections?

**Risk:**  
The **natural contraception mode**, being **CE Class IIa**, must ensure **data security** and **privacy** under **GDPR** (Art. 30, 32) and **MDR**. The **tracker mode**, being **wellness software**, must also comply with **GDPR** for **data minimization** and **privacy by design**, but the **risk level is lower**.

**HERA Dimension:**  
- **P3.D1: Data security**  
- **P3.D2: Privacy by design**

**Mitigation:**  
- **Implement strong data encryption** and **access controls** for both modes under **GDPR**.
- **Ensure data minimization** and **privacy by design** for the **tracker mode**.
- **Conduct regular data security audits** for the **natural contraception mode** under **MDR**.

---

### **16. Accessibility & Inclusivity (P5.D1, P5.D2)**  
**Reflection Question:** Does the **natural contraception mode** (Class IIa) require **accessibility** and **inclusivity** under **MDR** and **GDPR**, and does the **tracker mode** (wellness) need similar considerations?

**Risk:**  
The **natural contraception mode**, being **CE Class IIa**, must ensure **accessibility** and **inclusivity** under **MDR** and **GDPR**. The **tracker mode**, being **wellness software**, may not require the same level of **accessibility**, but **inclusive design** is still important for user experience.

**HERA Dimension:**  
- **P5.D1: Accessibility**  
- **P5.D2: Inclusivity in design**

**Mitigation:**  
- **Ensure the app is accessible** to users with disabilities for both modes under **MDR** and **GDPR**.
- **Design the interface to be inclusive** and **user-friendly** for all users.
- **Provide alternative formats** for content and features where necessary.

---

### **17. Algorithmic Accountability (P6.D1, P6.D2)**  
**Reflection Question:** Does the **natural contraception mode** (Class IIa) require **algorithmic accountability** under **GDPR** and **MDR**, and does the **tracker mode** (wellness) need similar oversight?

**Risk:**  
The **natural contraception mode**, being **CE Class IIa**, must ensure **algorithmic accountability** under **GDPR** (Art. 22) and **MDR**. The **tracker mode**, being **wellness software**, may not require the same level of **algorithmic oversight**, but **transparency** is still important.

**HERA Dimension:**  
- **P6.D1: Algorithmic accountability**  
- **P6.D2: Transparency in AI/ML use**

**Mitigation:**  
- **Document the algorithmic decision-making process** for the **natural contraception mode** under **GDPR** and **MDR**.
- **Provide users with the ability to challenge algorithmic decisions**.
- **Ensure transparency in how data is used** and how predictions are made in both modes.

---

### **18. Regulatory Compliance Summary for Lunara**

| Mode | Regulatory Classification | Key Compliance Requirements | Key HERA Dimensions |
|------|---------------------------|-----------------------------|---------------------|
| **Natural Contraception Mode** | CE Class IIa under MDR | MDR, GDPR, ISO 13485, ISO 14971 | P1, P2, P3, P4, P5, P6, P7, P8, P9 |
| **Tracker Mode** | Wellness Software | GDPR, ISO/IEC 82304-2 (optional) | P2, P3, P5, P6 |

---

### **Final Recommendations for Lunara**

1. **Regulatory Alignment:** Ensure the **natural contraception mode** is fully compliant with **MDR**, **GDPR**, and **ISO 13485**. Consider **ISO 14971** for risk management.
2. **Data Security & Privacy:**

### USER
Natural contraception mode is CE Class IIa under MDR. Tracker mode is wellness.

### ASSISTANT
Thank you for confirming that the **natural contraception mode** is **CE Class IIa** under MDR and the **tracker mode** is **wellness software**. This classification is critical for understanding the **regulatory and ethical risks** for **Lunara**, and it allows us to focus on the **HERA dimensions** and **regulatory compliance** for each mode.

---

### **19. Risk Management (P7.D1, P7.D2)**  
**Reflection Question:** Does the **natural contraception mode** (Class IIa) require a **risk management plan** under **MDR** and **ISO 14971**, and does the **tracker mode** (wellness) need a similar approach?

**Risk:**  
The **natural contraception mode**, being **CE Class IIa**, must undergo **risk management** under **MDR** and **ISO 14971**. The **tracker mode**, being **wellness software**, may not require the same level of **risk assessment**, but **basic risk management** is still recommended to ensure **user safety** and **data integrity**.

**HERA Dimension:**  
- **P7.D1: Risk assessment**  
- **P7.D2: Risk mitigation strategies**

**Mitigation:**  
- **Conduct a thorough risk assessment** for the **natural contraception mode** under **MDR** and **ISO 14971**.
- **Implement risk mitigation strategies** such as **data validation**, **algorithmic testing**, and **user feedback mechanisms**.
- **Perform regular risk reviews** for the **natural contraception mode** to ensure ongoing compliance.

---

### **20. Quality Management (P8.D1, P8.D2)**  
**Reflection Question:** Does the **natural contraception mode** (Class IIa) require a **quality management system** under **MDR** and **ISO 13485**, and does the **tracker mode** (wellness) need a similar framework?

**Risk:**  
The **natural contraception mode**, being **CE Class IIa**, must have a **quality management system** under **MDR** and **ISO 13485**. The **tracker mode**, being **wellness software**, may not require the same level of **quality management**, but **quality assurance** is still important to maintain **user trust** and **data integrity**.

**HERA Dimension:**  
- **P8.D1: Quality management system**  
- **P8.D2: Quality assurance practices**

**Mitigation:**  
- **Implement a quality management system** for the **natural contraception mode** under **MDR** and **ISO 13485**.
- **Ensure quality assurance practices** for the **tracker mode**, such as **code reviews**, **testing protocols**, and **user feedback loops**.
- **Maintain documentation** of all quality management activities for both modes.

---

### **21. Clinical Evaluation (P10.D1, P10.D2)**  
**Reflection Question:** Does the **natural contraception mode** (Class IIa) require a **clinical evaluation** under **MDR**, and does the **tracker mode** (wellness) need a similar process?

**Risk:**  
The **natural contraception mode**, being **CE Class IIa**, must undergo a **clinical evaluation** under **MDR** to ensure **safety and effectiveness**. The **tracker mode**, being **wellness software**, may not require a **clinical evaluation**, but **user testing** and **data validation** are still important to ensure **reliability** and **user satisfaction**.

**HERA Dimension:**  
- **P10.D1: Clinical evaluation**  
- **P10.D2: Safety and effectiveness validation**

**Mitigation:**  
- **Conduct a clinical evaluation** for the **natural contraception mode** under **MDR**.
- **Perform user testing** and **data validation** for the **tracker mode** to ensure **reliability** and **user satisfaction**.
- **Document all clinical and user testing activities** for both modes.

---

### **22. Regulatory Compliance Summary for Lunara**

| Mode | Regulatory Classification | Key Compliance Requirements | Key HERA Dimensions |
|------|---------------------------|-----------------------------|---------------------|
| **Natural Contraception Mode** | CE Class IIa under MDR | MDR, GDPR, ISO 13485, ISO 14971, ISO 13485 | P1, P2, P3, P4, P5, P6, P7, P8, P9, P10 |
| **Tracker Mode** | Wellness Software | GDPR, ISO/IEC 82304-2 (optional) | P2, P3, P5, P6, P7, P8 |

---

###

### USER
Natural contraception mode is CE Class IIa under MDR. Tracker mode is wellness.

### USER
Thanks for the conversation. Could you produce a brief structured risk report now? Use HERA dimension IDs (e.g. [P1.D2]) and group risks by severity. End the report with a list of dimensions you didn't get to cover.

### ASSISTANT
### **HERA Risk Report for Lunara: Natural Contraception Mode (CE Class IIa) & Tracker Mode (Wellness)**

---

#### **1. High Severity Risks**

| **HERA Dimension** | **Risk Description** | **Mitigation** | **Regulatory Basis** |
|---------------------|----------------------|----------------|----------------------|
| **[P1.D1]** | **Safety & Effectiveness** – The natural contraception mode must ensure **safe and effective** outcomes, as it influences reproductive health decisions. | Conduct **clinical evaluation** under MDR (Art. 61) and **risk analysis** under ISO 14971. | [mdr_2017_745 · p.32], [clinical_eval_mdsw · p.0] |
| **[P2.D3]** | **User Autonomy & Informed Consent** – Users must be fully informed about how their data is used and the implications of the natural contraception mode. | Implement **transparent data usage policies**, **explicit consent mechanisms**, and **user education materials**. | [gdpr_2016_679 · p.13], [mdr_2017_745 · p.18] |
| **[P3.D1]** | **Data Security & Privacy** – The natural contraception mode handles **sensitive health data**, which requires **strict security measures** under GDPR and MDR. | Apply **encryption**, **access controls**, and **data minimization**. | [gdpr_2016_679 · p.30], [mdr_2017_745 · p.14] |
| **[P6.D1]** | **Algorithmic Accountability** – The natural contraception mode may use **AI/ML** to predict fertility, requiring **algorithmic transparency** and **user challenge rights**. | Document algorithmic decisions, provide **explanation mechanisms**, and allow users to **challenge outcomes**. | [gdpr_2016_679 · p.22], [mdr_2017_745 · p.10] |
| **[P7.D1]** | **Risk Assessment** – The natural contraception mode must undergo **thorough risk analysis** to identify and mitigate potential harms. | Use **ISO 14971** for risk management and **MDR compliance**. | [iso_14971 · p.12], [mdr_2017_745 · p.32] |
| **[P10.D1]** | **Clinical Evaluation** – The natural contraception mode requires **clinical validation** to ensure safety and effectiveness. | Conduct **clinical trials**, **user testing**, and **data validation**. | [mdr_2017_745 · p.32], [clinical_eval_mdsw · p.0] |

---

#### **2. Medium Severity Risks**

| **HERA Dimension** | **Risk Description** | **Mitigation** | **Regulatory Basis** |
|---------------------|----------------------|----------------|----------------------|
| **[P2.D1]** | **User Privacy & Data Protection** – The tracker mode must also protect user data, even though it is not classified as medical. | Apply **GDPR data protection principles** and **data minimization**. | [gdpr_2016_679 · p.30] |
| **[P5.D1]** | **Accessibility** – Both modes must be accessible to users with disabilities. | Ensure **WCAG compliance**, **alternative formats**, and **screen reader compatibility**. | [wcag_2018 · p.10] |
| **[P6.D2]** | **Transparency in AI/ML Use** – Even if the tracker mode does not use AI, transparency in data usage is still important. | Provide **clear explanations** of data usage and **user control options**. | [gdpr_2016_679 · p.22] |
| **[P8.D1]** | **Quality Management System** – The natural contraception mode must have a **formal quality management system** under MDR. | Implement **ISO 13485** and **MDR-compliant quality assurance**. | [iso_13485 · p.12], [mdr_2017_745 · p.18] |
| **[P9.D1]** | **Ethical Use of Data** – Both modes must ensure **ethical data use**, including **no discrimination** or **unfair treatment**. | Establish **data ethics policies**, **user control**, and **fair data practices**. | [gdpr_20

Now produce the JSON judgement object.