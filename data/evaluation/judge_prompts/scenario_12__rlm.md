APPROACH UNDER REVIEW: `rlm`

SCENARIO ID: scenario_12
APP DESCRIPTION: Lunara is a menstrual cycle tracker that also offers a fertility prediction mode (for users trying to conceive) and a 'natural contraception' mode that predicts safe vs unsafe days. Algorithm based on basal body temperature + cycle history. We're EU + CH. 4 million users.

DEVELOPER PERSONA: Senior PM at a femtech scale-up. Confident, fast-moving.

EXPECTED HERA DIMENSIONS (gold standard): P1.D1, P1.D2, P1.D3, P2.D1, P2.D2, P2.D4, P2.D6, P3.D2, P5.D2, P5.D4, P6.D1, P6.D3, P7.D1, P7.D3

TRANSCRIPT:
### USER
Lunara is a menstrual cycle tracker that also offers a fertility prediction mode (for users trying to conceive) and a 'natural contraception' mode that predicts safe vs unsafe days. Algorithm based on basal body temperature + cycle history. We're EU + CH. 4 million users.

### ASSISTANT
What measures are in place to ensure the fertility prediction mode does not reinforce harmful stereotypes or biases related to fertility and body image [P7.D1]? This is important as the app's fertility prediction mode could impact users' perceptions of fertility and body image, especially in a diverse EU and CH user base.

### USER
The clinical side is actually our strong point — the contraception mode has a real Pearl Index study, N=1500, which is what got us CE Class IIa. The tracker and fertility modes themselves don't have that same clinical trial backing; they're positioned as wellness.

### ASSISTANT
How does the app ensure that the natural contraception mode does not mislead users about the effectiveness or reliability of its predictions, especially given the lack of clinical trial backing? This is important as the app's contraception mode is marketed without the same clinical validation as its fertility prediction mode. [P3.D2]

### USER
The tracker mode is just wellness and the contraception mode is the regulated Class IIa one, but in the UI the line between them is softer than it should be. Switching into contraception mode doesn't currently force a confirmation that explains 'you are now relying on this to prevent pregnancy,' and I can see how a user might not realize which mode they're in.

### ASSISTANT
The UI currently doesn't force a confirmation when switching into the contraception mode, which could lead to users not realizing they're relying on a regulated feature for pregnancy prevention. How does the app ensure that the UI clearly distinguishes between the wellness tracker mode and the regulated contraception mode to prevent user confusion about the reliability and implications of each mode [P2.D3]?

### USER
Natural contraception mode is CE Class IIa under MDR. Tracker mode is wellness.

### ASSISTANT
The natural contraception mode is CE Class IIa under MDR, but the UI doesn't force a confirmation when switching into this mode. How does the app ensure that the natural contraception mode is clearly differentiated from the wellness tracker mode in terms of user experience and risk communication to prevent user confusion about the reliability and implications of each mode [P2.D3]?

### USER
We're clear on classification: the natural-contraception mode is registered as CE Class IIa under MDR and the plain tracker is treated as wellness, not a device. That split was deliberate and the IIa work is done.

### ASSISTANT
What measures are in place to ensure the natural contraception mode does not reinforce harmful stereotypes or biases related to fertility and body image, especially in a diverse EU and CH user base? This is important as the app's natural contraception mode is CE Class IIa under MDR and could impact users' perceptions of fertility and body image. [P7.D1]

### USER
Our model assumes a reasonably regular cycle, so I'll admit it's weakest exactly where it matters most — PCOS, very irregular cycles, post-partum and perimenopause. Right now we still try to predict for those users instead of refusing or flagging them, and we haven't built PCOS/irregular-cycle detection that pauses the contraception prediction.

### ASSISTANT
The natural contraception mode is CE Class IIa under MDR, but it currently lacks mechanisms to detect and flag users with PCOS, very irregular cycles, post-partum, or perimenopause. How are these specific user groups being addressed in the UI to prevent misleading predictions and ensure appropriate risk communication [P2.D3]?

### USER
Our natural-contraception mode predicts safe vs unsafe days, and in practice that surfaces as a green 'safe day' tile. I'll admit a binary green light can read as 'guaranteed safe' when it really means 'lower probability.' We do show Bayesian uncertainty intervals, but the big green tile is what users actually act on.

### ASSISTANT
The green 'safe day' tile in the natural contraception mode can be perceived as a guaranteed safe day, especially for users with PCOS or very irregular cycles. How does the app ensure that this tile does not mislead users into believing it is a guaranteed safe day, given the inherent uncertainty in predictions for these user groups [P3.D2]?

### USER
Look, the honest number is a 6.5 Pearl Index in typical use — so yes, with 4 million users some unintended pregnancies are statistically baked in, and that's the headline harm with our contraception mode. We do warn that it's not 100%, but I'll concede we lean on the 'perfect use' framing more than we should.

### ASSISTANT
The natural contraception mode's 'perfect use' framing may mislead users into believing it is more effective than its actual Pearl Index of 6.5 in typical use. How does the app ensure this framing does not mislead users, especially for those with PCOS or very irregular cycles who are at higher risk of misinterpretation? [P3.D2]

### USER
Contraception mode: 6.5 Pearl Index in typical use (clinical study N=1500); 1.8 in perfect use.

### ASSISTANT
The natural contraception mode's 'perfect use' framing may mislead users into believing it is more effective than its actual Pearl Index of 1.8 in perfect use, especially for users with PCOS or very irregular cycles. How does the app ensure this framing does not mislead users about the effectiveness of the contraception mode? [P3.D2]

### USER
We quote the 1.8 perfect-use figure heavily in marketing because it sounds great, but I know most of our users aren't logging BBT at the same time every morning, so the 6.5 typical-use number is the one that actually applies to them. We haven't built a clear in-app explanation that real-world reliability is much lower than perfect use.

### ASSISTANT
The natural contraception mode's 'perfect use' framing in marketing may mislead users into believing it is more effective than its actual Pearl Index of 6.5 in typical use, especially for users who cannot consistently log basal body temperature. How does the app ensure this framing does not mislead users about the real-world reliability of the natural contraception mode? [P3.D2]

### USER
We share aggregated, anonymized cycle data with research partners and we don't run ads on health data — but we do pull IDFA for marketing attribution. I'll concede we haven't formally tested whether 'anonymized' cycle patterns could be re-identified; cycle signatures are pretty unique and that's not something we've audited.

### USER
Thanks for the conversation. Could you produce a brief structured risk report now? Use HERA dimension IDs (e.g. [P1.D2]) and group risks by severity. End the report with a list of dimensions you didn't get to cover.

### ASSISTANT
# HERA Risk Report

## High
[P3.D2] The natural contraception mode's marketing and UI framing of 'perfect use' may mislead users into believing it is more effective than its actual Pearl Index of 6.5 in typical use, which applies to most users. Mitigation: Clearly label all predictions with the actual Pearl Index (6.5) and distinguish between perfect use (1.8) and typical use in UI, referencing the MDR Article 10(1) on risk communication.

## Medium
[P2.D3] The natural contraception mode lacks clear UI differentiation from the wellness tracker mode, increasing the risk of user confusion about the reliability and implications of each mode. Mitigation: Implement a confirmation prompt when switching to the contraception mode, explaining that it is a regulated feature with known limitations, in line with MDR Article 10(1).

## Low
[P7.D1] The natural contraception mode may reinforce harmful stereotypes or biases related to fertility and body image, particularly for users with PCOS or irregular cycles. Mitigation: Conduct a bias audit of the algorithm and UI messaging, ensuring inclusive language and transparency about limitations, in line with the EU AI Act Article 17 (high-risk AI systems).

Not yet covered: P1.D2, P4.D1, P5.D3, P6.D2

Now produce the JSON judgement object.