# Regulatory mapping — decision tree for review

**Version**: 0.3 · **Model**: accumulator · **EU + Switzerland**
**Total**: 37 questions · 44 regulations · 2 exits (out-of-scope + recap)

**Visuals** — two self-contained, shareable HTML files:

- **Static diagram**: `data/regulations/decision_tree.html` (Mermaid flowchart + card table)
- **Interactive walkthrough**: `data/regulations/decision_tree_interactive.html`
  (click through the questions, regulation cards stack live in a side panel, final recap)

Regenerate after each JSON change:

```bash
uv run python scripts/render_decision_tree.py              # static diagram + validation
uv run python scripts/render_interactive_tree.py           # interactive walkthrough + validation
uv run python scripts/render_interactive_tree.py --open    # + open in browser
```

Both scripts **validate** the structure automatically: every `next` points to an
existing node, every `adds` regulation exists, every question is reachable, no
orphan regulation. (Current status: ✓ consistent.)

---

## What changed in v0.3 vs v0.2

v0.3 comes from **in-depth multi-domain research** (6 axes: MDR/IVDR, AI Act,
operational GDPR + HDS, Swiss framework, EU horizontal digital law, national market
access). All dates and URLs verified for 2025-2026.

**1. Major structural fix — Q1 becomes a JURISDICTION gate.**
In v0.2, Q1 (EU *or* Switzerland → `gdpr_base`) was legally wrong: a **Swiss-only**
app falls under the **nFADP**, not the GDPR (authority FDPIC, not an EU DPA). Q1 now
offers 4 paths: EU→`gdpr_base` / Switzerland→`nlpd_base` (new baseline card) /
both→both baselines / none→exit.

**2. +18 new questions / +23 new cards** vs v0.2 (incl. the nFADP baseline; the last
review round added Q8b/Q8c/Q22b — combination products, MDR transition, eIDAS 2):

| Domain | New branches |
|---|---|
| Device | **IVDR** (Q5, in-vitro fork), **SaMD standards** (Q7: IEC 62304/ISO 14971/IEC 62366/ISO 13485), **clinical evaluation** (Q8, MDCG 2020-1), **UDI/EUDAMED** (Q28, deadline 28 May 2026) |
| AI | **AI Act timeline + Digital Omnibus** (card on Q9), **GPAI/LLM** (Q11, integrator vs fine-tuner), **deployer FRIA** (Q12, Art. 27) |
| Personal data | **DPIA** (Q16, Art. 35), **ePrivacy Art. 5(3)** SDKs/trackers (Q17), **HDS France** (Q20, L1111-8) |
| Switzerland | **CH-REP / MDR third country** (Q25, Art. 51 MedDO), **nFADP Art. 21+22** automated decision & DPIA (Q26) |
| Horizontal | **CRA** (Q29), **Data Act** (Q30), **PLD** (Q31) |
| Market access | **reimbursement DiGA (DE) / PECAN (FR) / other** (Q23, multichoice) |

**3. Existing cards enriched**: `gdpr_base` (DPO/72h/Art.28), `ai_act_high_risk`
(MDCG 2025-6 nuance: self-certified Class I ≠ high-risk), `ehds` (DGA note),
`pms_lifecycle` + `swiss_stack` (Swissmedic MIR vigilance, EPRA revision).

---

## ACCUMULATOR model recap

We walk through **all** questions and each answer **stacks** the applicable
regulations (`adds`). The side panel lights up as you go; the final RECAP lists
every triggered card.

- **Q1-Q8** = jurisdiction + product qualification (gates; Q2/Q3/Q4 short-circuit
  to the AI section when not applicable; Q5 forks IVDR vs MDR).
- **Q9-Q34** = cross-cutting modifiers that always stack and lead to the RECAP
  (Q9 skips the AI sub-section if no AI; Q24 skips the CH sub-section if not in Switzerland).

### Order of the 34 questions

| Q | Topic | Card(s) triggered |
|---|---|---|
| Q1 | **Jurisdiction (gate)** | `gdpr_base` / `nlpd_base` / both / exit |
| Q2 | Health data? | `gdpr_art9` |
| Q3 | Medical purpose? | (no → `iso_82304`) |
| Q4 | Clinical decision/monitoring (SaMD)? | (no → `iso_82304`) |
| Q5 | **In-vitro diagnostic (IVDR)?** | `ivdr_class` (yes, skips Q6) |
| Q6 | Harm severity (MDR class) | `mdr_class_{i,iia,iib,iii}` |
| Q7 | **SaMD lifecycle standards?** | `samd_standards` |
| Q8 | **Clinical evidence?** | `clinical_eval_mdsw` |
| Q8b | **Linked to a medicinal product?** | `combination_product` |
| Q8c | **Legacy MDD vs new MDR cert?** | `mdr_transition` |
| Q9 | Uses AI/ML? | `ai_act_timeline` → Q10 |
| Q10 | AI for medical decision? | `ai_act_high_risk` / `ai_act_transparency` |
| Q11 | **GPAI / LLM model?** | `ai_act_gpai_downstream` (+`ai_act_gpai_provider` if fine-tune) |
| Q12 | **Deployed by public body / clinician (FRIA)?** | `ai_act_fria` |
| Q13 | Biometrics? | `gdpr_biometric` |
| Q14 | Minors < 16? | `gdpr_children` |
| Q15 | Automated decisions? | `gdpr_automated` |
| Q16 | **Large scale / systematic monitoring (DPIA)?** | `gdpr_dpia` |
| Q17 | **Cookies / SDKs / trackers?** | `eprivacy_terminal` |
| Q18 | Monetisation / third parties? | `data_monetization` |
| Q19 | Hosting outside EU/CH? | `gdpr_transfer` |
| Q20 | **French patients' data hosted (HDS)?** | `hds_certification` |
| Q21 | Telehealth / e-prescription? | `telehealth_national` |
| Q22 | National EHR integration (EPR/DMP/ELGA)? | `national_ehealth` |
| Q22b | **Strong identity / ID wallet (eIDAS 2)?** | `eidas2` |
| Q23 | **Public reimbursement (DE/FR/other, multi-select)?** | `diga_germany` / `pecan_france` / `reimbursement_other_eu` |
| Q24 | Switzerland? | `swiss_stack` (yes; no skips Q25-Q26) |
| Q25 | **MDR third country / CH-REP?** | `ch_rep_meddo` |
| Q26 | **nFADP automated decision / DPIA?** | `nlpd_automated_dpia` |
| Q27 | Long term > 1 year? | `pms_lifecycle` |
| Q28 | **CE device → UDI/EUDAMED?** | `udi_eudamed` |
| Q29 | **Commercial product (CRA)?** | `cra` |
| Q30 | **Pairs with connected device (Data Act)?** | `data_act` |
| Q31 | **Software/AI with harm risk (PLD)?** | `pld` |
| Q32 | Cybersecurity / essential entity? | `nis2_cyber` |
| Q33 | Interop / secondary use? | `ehds` |
| Q34 | Consumer-facing (B2C)? | `eaa_accessibility` |

---

## Review decisions (resolved)

The 9 open points from the earlier draft were reviewed and resolved as follows:

1. **Jurisdiction gate Q1** — kept the 4 paths (EU / CH / both / none). The
   "third country" dimension is already handled by Q19 (transfers); no 5th case.
2. **Swiss-only stacking** — *implemented*: the **interactive renderer filters by
   jurisdiction**. When Q1 = Switzerland only, EU-only cards (jurisdiction `EU`/`FR`/`DE`)
   are greyed and labelled "outside your territorial scope (shown for reference)" and
   excluded from the headline count; symmetric logic when Q1 = EU only (CH cards greyed).
   The JSON tree stays simple; the filtering lives in `render_interactive_tree.py`.
3. **Q5 IVDR** — *done*: added a concrete example to the question text
   (blood-glucose interpretation = IVD vs meal-logging coach = not).
4. **Q7/Q8** — kept both answers lighting the card (standards / clinical evidence) as
   a pedagogical checkpoint; a "No" flags a gap to close.
5. **Q11 GPAI** — kept as is (the ~1/3-compute fine-tuning criterion stays in the
   rationale + card).
6. **Q23 reimbursement** — *implemented*: true **multi-select** in the interactive
   renderer (tick DE + FR + BE, cards stack, then Continue). Driven by a new
   `"multiSelect": true` flag on the question.
7. **AI Act timeline** — kept the cautious wording (Digital Omnibus = provisional,
   not yet in the OJ) in the `ai_act_timeline` card; to reconfirm at adoption.
8. **Remaining gaps** — *added* three branches: combined products **Q8b**
   (`combination_product`, MDR Art. 117), legacy MDR transition **Q8c**
   (`mdr_transition`, Reg. 2023/607), and eIDAS 2 **Q22b** (`eidas2`). DSA stays out
   (niche).
9. **Outside EU/CH** — kept excluded (FDA/HIPAA/UK). The `X_OUT_OF_SCOPE` exit already
   points to FDA / UK DTAC / Health Canada.

The **rich content** of the cards (educational purpose, concrete obligations, 3-5
point checklist, 2-3 examples, HERA dimensions touched) is to be written next, now
that the structure is settled.
