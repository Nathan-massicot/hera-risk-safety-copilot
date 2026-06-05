export const meta = {
  name: 'hera-dimension-sources',
  description: 'Map 2-4 relevant regulatory citations (+ why) to each HERA dimension',
  phases: [{ title: 'Enrich', detail: 'one agent per HERA dimension, grounded in retrieved cards' }],
}

// HERA dimensions (id + name) — stable taxonomy (38 dimensions, 7 pillars).
const DIMS = [
  ['P1.D1', 'Clinical Evidence & Validation'],
  ['P1.D2', 'Contraindications & Adverse Effects'],
  ['P1.D3', 'False Sense of Security'],
  ['P1.D4', 'Delayed Medical Consultation'],
  ['P1.D5', 'Measurement Reliability'],
  ['P1.D6', 'System Dependency & Over-reliance'],
  ['P2.D1', 'Informed Consent'],
  ['P2.D2', 'Data Minimization'],
  ['P2.D3', 'Storage, Encryption & Security'],
  ['P2.D4', 'Third-Party Data Sharing'],
  ['P2.D5', 'Anonymization & Right to Erasure'],
  ['P2.D6', 'Vulnerable Population Data'],
  ['P3.D1', 'Right to Make Decisions'],
  ['P3.D2', 'Emotional Manipulation & Excessive Nudging'],
  ['P3.D3', 'Impact on Doctor-Patient Relationship'],
  ['P3.D4', 'Dynamic Consent & Withdrawal Rights'],
  ['P3.D5', 'Automation Bias (AI and Non-AI)'],
  ['P4.D1', 'App Stability & Error Handling'],
  ['P4.D2', 'Interoperability & Data Exchange'],
  ['P4.D3', 'Accessibility (WCAG, Literacy, Language)'],
  ['P4.D4', 'User-Centered Design & Usability Testing'],
  ['P4.D5', 'Offline Functionality & Updates'],
  ['P5.D1', 'Understandable Output'],
  ['P5.D2', 'Clear Communication of Limitations'],
  ['P5.D3', 'Decision Traceability & Logging'],
  ['P5.D4', 'Clinically Validated vs. Estimated Content'],
  ['P6.D1', 'Data & Clinical Rule Bias'],
  ['P6.D2', 'Digital Divide & Socioeconomic Access'],
  ['P6.D3', 'Cross-Cultural & Multilingual Validation'],
  ['P6.D4', 'Impact on Existing Health Inequalities'],
  ['P6.D5', 'Representativeness in Validation Studies'],
  ['P7.D1', 'Medical Device Classification (SaMD)'],
  ['P7.D2', 'CE Marking & MDR Conformity'],
  ['P7.D3', 'EU AI Act Risk Classification'],
  ['P7.D4', 'GDPR Compliance (DPO, DPIA)'],
  ['P7.D5', 'Post-Market Surveillance & Vigilance'],
  ['P7.D6', 'Third-Party Audit & Certification'],
  ['P7.D7', 'Lifecycle & Documentation Management'],
]

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    dimension_id: { type: 'string' },
    sources: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          cite: { type: 'string' },
          title: { type: 'string' },
          why: { type: 'string' },
        },
        required: ['cite', 'title', 'why'],
      },
    },
  },
  required: ['dimension_id', 'sources'],
}

phase('Enrich')
log(`Mapping regulatory citations to ${DIMS.length} HERA dimensions`)

const results = await parallel(DIMS.map(([id, name]) => async () => {
  const outFile = `data/taxonomy/_dim_sources/${id}.json`
  const prompt = `You are mapping regulatory sources to a HERA risk dimension for an interactive taxonomy explorer that mHealth developers will browse.

Dimension: **${id} — "${name}"**

Steps:
1. Use the Read tool to read \`data/taxonomy/_dim_candidates.json\` and locate the entry keyed "${id}". It contains "candidates": a list of regulatory cards (cite, title, snippet) retrieved for this dimension.
2. Select the **2-4 cards that are genuinely relevant** to THIS dimension. Discard off-topic ones (e.g. a device-classification card is NOT relevant to a pure accessibility/usability dimension; a children's-data card is NOT relevant to interoperability). Prefer precision over recall — a developer should trust every citation shown. If only 1 card is truly relevant, return just that one; if none, return an empty list.
3. For each selected card write ONE concise sentence (plain English, <= 25 words) on *why* it applies to this dimension.
4. Use the Write tool to write \`${outFile}\` containing exactly: {"dimension_id":"${id}","sources":[{"cite":"<exact cite>","title":"<exact title>","why":"<one sentence>"}, ...]}
5. Return the same object as your structured output.

Use ONLY cards present in the candidates list — never invent a citation. Keep "cite" and "title" byte-identical to the candidate.`
  const v = await agent(prompt, {
    label: `sources:${id}`,
    phase: 'Enrich',
    schema: SCHEMA,
    agentType: 'general-purpose',
  })
  return v || { dimension_id: id, sources: [] }
}))

const ok = results.filter(Boolean)
const totalCites = ok.reduce((n, r) => n + (r.sources?.length || 0), 0)
log(`Done: ${ok.length}/${DIMS.length} dimensions, ${totalCites} citations total`)

return { dimensions: ok.length, total_citations: totalCites }
