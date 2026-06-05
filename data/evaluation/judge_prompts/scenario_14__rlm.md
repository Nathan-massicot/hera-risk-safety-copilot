APPROACH UNDER REVIEW: `rlm`

SCENARIO ID: scenario_14
APP DESCRIPTION: SleepWell is an iOS/Android app that stages your sleep using phone microphone + accelerometer, and delivers a CBT-I (insomnia) coaching programme over 6 weeks. The coaching content is personalised by a small ML model based on user adherence and reported sleep. EU.

DEVELOPER PERSONA: Sleep researcher founder. Thinks scientifically but is new to medical-device regulation.

EXPECTED HERA DIMENSIONS (gold standard): P1.D1, P1.D5, P2.D1, P2.D2, P2.D3, P3.D1, P4.D5, P5.D1, P5.D2, P5.D4, P7.D1, P7.D3

TRANSCRIPT:
### USER
SleepWell is an iOS/Android app that stages your sleep using phone microphone + accelerometer, and delivers a CBT-I (insomnia) coaching programme over 6 weeks. The coaching content is personalised by a small ML model based on user adherence and reported sleep. EU.

### ASSISTANT
SleepWell uses phone microphone and accelerometer to collect sleep data, which may involve sensitive health information. How does the app ensure user data privacy and compliance with EU regulations regarding health data collection? [P2.D3]

### USER
Microphone (continuous during sleep, kept on-device + a digest sent to cloud), accelerometer, sleep diary, CBT-I exercise completion.

### ASSISTANT
SleepWell collects accelerometer data and sleep diary entries, which are sensitive personal information. What measures does SleepWell implement to protect this data from unauthorized access or breaches? [P3.D2]

### USER
We ask for microphone permission with an onboarding video plus a separate consent step, but honestly it's basically a single 'turn on the mic for sleep tracking' flow — we haven't built a granular consent screen that spells out the on-device vs cloud-digest split, and I'll admit most users probably just tap through it.

### ASSISTANT
SleepWell uses the microphone for sleep tracking, with on-device processing and a digest sent to the cloud. How does SleepWell ensure users are fully informed about the data collected from the microphone and its on-device processing versus cloud transmission? [P2.D1]

### USER
Sleep staging runs on-device so tracking works offline overnight, but the personalised coaching and the digest upload need connectivity; we ship content and model updates through the normal app-store release cycle and we don't currently have a staged-rollback plan if an update misbehaves. Post-market we mostly rely on crash analytics and a monthly retention review.

### ASSISTANT
SleepWell collects continuous microphone data during sleep tracking, which may involve sensitive health information. How does SleepWell handle the potential risks of data breaches related to this data, especially given the lack of granular consent mechanisms for on-device processing versus cloud transmission? [P2.D3]

### USER
The on-device recording stays local and the cloud digest is auto-deleted after 30 days, and account deletion is supported; we rely on the platform's standard transport encryption and provider-managed encryption at rest, but I'll be honest, we haven't done a formal security audit or pen-test yet.

### ASSISTANT
SleepWell delivers personalized CBT-I coaching content without a staged-rollback plan for app updates. How does SleepWell ensure the reliability and safety of the CBT-I coaching content, especially considering the absence of a staged-rollback plan for app updates? [P7.D1]

### USER
Our sleep staging is validated at about 80% agreement vs polysomnography in an in-lab study of N=50, which I'm proud of, but the 6-week CBT-I coaching programme itself has not been validated in-app — we're leaning on the published CBT-I literature, not our own efficacy trial.

### ASSISTANT
SleepWell's sleep staging algorithm has been validated in an in-lab study with a small sample size of N=50. How does SleepWell ensure the accuracy and reliability of the sleep staging algorithm, especially given the limited validation in real-world conditions? [P3.D1]

### USER
Sleep staging accuracy ~80% vs polysomnography (in-lab study N=50).

### ASSISTANT
SleepWell's CBT-I coaching programme relies on published literature rather than in-app validation. How does SleepWell ensure the accuracy and reliability of the CBT-I coaching programme, given that it has not been validated in-app and relies solely on published literature? [P7.D2]

### USER
We tell users it's a sleep-tracking and CBT-I coaching tool, but we don't yet have clear in-app messaging about what it can't do — for instance that it's not a diagnosis and that ~80% staging accuracy means some nights will be wrong.

### ASSISTANT
SleepWell's sleep staging algorithm has been validated in an in-lab study with a small sample size. How does SleepWell ensure the generalizability and reliability of the sleep staging algorithm in real-world conditions, especially given the limited validation? [P3.D1]

### USER
CNN for sleep staging from audio + motion; rule-based CBT-I prescription engine.

### ASSISTANT
SleepWell's CBT-I prescription engine is rule-based, but how does the app ensure the effectiveness and adaptability of this engine when user adherence and reported sleep data vary across different populations? [P7.D2]

### USER
The coaching is personalised by the small ML model together with the rule-based CBT-I engine off the user's adherence and reported sleep, but right now we don't surface to the user which signals drove a given recommendation — they just see the next prescribed exercise.

### ASSISTANT
SleepWell's CBT-I recommendations are personalized using a small ML model and a rule-based engine based on user adherence and reported sleep, but users aren't shown which signals influenced a given recommendation. How does SleepWell ensure transparency and explainability in the CBT-I recommendation process, especially since users are not shown which signals influenced a given recommendation? [P7.D2]

### USER
We classify ourselves as wellness coaching, not SaMD, because we don't diagnose insomnia — but I'm new to medical-device regulation and I haven't actually mapped us against MDR Rule 11 or talked to a notified body, so I can't tell you with confidence we'd stay below the device line if challenged on the CBT-I side.

### USER
Thanks for the conversation. Could you produce a brief structured risk report now? Use HERA dimension IDs (e.g. [P1.D2]) and group risks by severity. End the report with a list of dimensions you didn't get to cover.

### ASSISTANT
**High**  
[P2.D3] SleepWell collects continuous microphone data during sleep tracking without granular consent mechanisms, increasing the risk of unauthorized data use. Mitigation: Implement a granular consent screen explaining on-device processing vs. cloud digest transmission, in line with GDPR Article 6(1)(a) and Article 13.  

**Medium**  
[P3.D1] Sleep staging accuracy is limited to ~80% in an in-lab study (N=50), raising concerns about real-world reliability. Mitigation: Conduct a real-world validation study with a larger, diverse sample to ensure algorithm accuracy and generalizability, in line with ISO 82304-2.  
[P7.D2] CBT-I recommendations are based on a rule-based engine and unvalidated ML model, without in-app efficacy testing. Mitigation: Perform an in-app efficacy trial to validate coaching outcomes, in line with MDR Rule 11 and EU AI Act Article 54.  
[P7.D1] Lack of a staged-rollback plan for app updates could compromise the reliability of CBT-I content. Mitigation: Implement a staged-rollback mechanism for app updates, in line with EU AI Act Article 16.  

**Low**  
[P2.D1] Users are not fully informed about how microphone data is processed on-device versus transmitted to the cloud. Mitigation: Provide clear in-app messaging explaining data handling, in line with GDPR Article 13 and Article 14.  
[P3.D2] Sleep diary and accelerometer data are collected without explicit user consent for specific purposes. Mitigation: Obtain explicit consent for each data type and purpose, in line with GDPR Article 6(1)(a).  

Not yet covered: P1.D2, P4.D1, P5.D1, P6.D1, P8.D1

Now produce the JSON judgement object.