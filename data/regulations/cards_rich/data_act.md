---
id: data_act
title: "Data Act — access & portability of connected-product data"
jurisdiction: EU
official_url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32023R2854
key_articles: ["Art. 3", "Art. 4-5", "Chapter III", "Chapter VI"]
status: rich-draft
---

# Data Act — access & portability of connected-product data

## Why this concerns you (purpose)
If your mHealth offering pairs with a **connected product** (a wearable, a glucometer,
a smart scale, a sensor), the Data Act (Reg. (EU) 2023/2854) gives the **user** a right
to the data that product generates — to access it, to use it, and to have it ported to a
**third party of their choice**. You can no longer treat sensor data as a locked-in
proprietary asset. The Act also targets **cloud lock-in**: if you sell a data-processing
service, customers must be able to switch providers. The Data Act has been **applicable
since 12 September 2025**. It is a *data-economy* rule and works **alongside the GDPR**:
where the data is personal health data, GDPR (Art. 9) and the Data Act both apply.

## When it is triggered (scope)
Triggered when **any** of the following hold:
- you place on the EU market a **connected product** (IoT device/wearable) or a
  **related service** that generates usage/performance/environment data;
- you are a **data holder** controlling access to that connected-product data;
- you provide a **data-processing service** (cloud/edge) to EU customers (switching rules).

Edge: a **standalone app** with no connected object and no cloud service offered to
customers is largely out of the connected-product obligations (though the cloud-switching
chapter can still reach the services you buy).

## Concrete obligations
- **Access by design / by default**: where feasible, the connected product and related
  service should make data directly accessible to the user (Art. 3-4).
- **Pre-contractual information**: tell users, before they buy, what data is generated,
  how to access it, and whether you (the holder) intend to use it.
- **Sharing on FRAND terms**: on the user's request, share data with a third party on
  **fair, reasonable and non-discriminatory** terms; protect trade secrets proportionately;
  do not use shared data to compete against the connected product.
- **Cloud anti-lock-in / switching** (Chapter VI): contractual + technical portability,
  removal of switching obstacles; **switching charges abolished from 12 January 2027**.

## Checklist
- [ ] Map the data your connected product/wearable generates and design a user-access path.
- [ ] Add Data Act **pre-contractual disclosures** to your terms (what data, how to get it, FRAND).
- [ ] Build a third-party data-portability flow and FRAND sharing terms (with trade-secret safeguards).
- [ ] If you resell or rely on cloud, check switching/exit terms and the **Jan 2027** fee phase-out.

## Examples (mHealth)
- A continuous glucose monitor + app: the patient can require their raw glucose readings
  be sent to a competing analytics service → you must enable FRAND portability.
- A sleep-tracking ring whose vendor refuses to export historical heart-rate data →
  non-compliant; the user has an access/portability right under the Data Act.
- A purely manual food-diary app with no sensor and no cloud service sold to others →
  the connected-product obligations are not triggered.

## HERA dimensions touched
- **Connected-device data rights** · **Data portability / FRAND** · **Cloud anti-lock-in**
- Cross-links: [[gdpr_art9]] (personal health data overlay), [[ehds]] (health data sharing & interoperability)

## Official sources
- EUR-Lex — Regulation (EU) 2023/2854: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32023R2854
- EUR-Lex (PDF, OJ L 2023/2854): https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202302854
