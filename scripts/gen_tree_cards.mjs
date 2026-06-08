export const meta = {
  name: 'hera-tree-cards',
  description: 'Draft + adversarially verify new/extended regulatory cards for the decision tree',
  phases: [
    { title: 'Draft', detail: 'one drafter per card' },
    { title: 'Verify', detail: '2 independent legal-accuracy reviewers per card' },
    { title: 'Reconcile', detail: 'merge draft + reviews into a final card' },
  ],
}

// Each item: the card we need, with fixed id/jurisdiction/role; agents fill+verify content.
const ITEMS = [
  {
    id: 'nlpd_sensitive',
    jurisdiction: 'CH',
    fires_at: 'Q2 (processes health data?) = yes, when Switzerland is in scope',
    brief:
      'Swiss nFADP/revFADP (revDSG, SR 235.1) treatment of HEALTH DATA as SENSITIVE personal data — the Swiss counterpart to GDPR Art. 9. Cover: definition of sensitive data incl. health (Art. 5 let. c ch. 2), explicit consent requirement for sensitive data (Art. 6 al. 7 let. a), data security (Art. 8 + DPO/OPDo ordinance), data protection impact assessment / AIPD (Art. 22), and that the supervisory authority is the FDPIC (not an EU DPA). Make clear it is a DISTINCT regime from the GDPR.',
    existing: null,
  },
  {
    id: 'meddo_qualification',
    jurisdiction: 'CH',
    fires_at: 'Q6 (medical-device classification step), when Switzerland is in scope',
    brief:
      'Swiss medical-device qualification & classification under the MedDO / ODim (Ordonnance sur les dispositifs médicaux, RS 812.213). KEY POINT: the MedDO ADOPTS the EU MDR (2017/745) qualification and classification rules (incl. Annex VIII rules, e.g. Rule 11 for software) — so the same class (I / IIa / IIb / III) applies. Differences vs EU: competent authority = Swissmedic (not a Notified Body system per se; conformity assessment via Swiss-recognised bodies), Swiss vigilance reporting to Swissmedic, and Switzerland is a third country for the MDR since 26 May 2021 (CH-REP needed). It complements the EU MDR class cards for a Swiss-market app.',
    existing: null,
  },
  {
    id: 'telehealth_national',
    jurisdiction: 'EU/CH',
    fires_at: 'Q21 (teleconsultation / e-prescription / interacts with HCPs) = yes',
    brief:
      'Extend the existing "Telehealth — national health codes" card to ADD Germany and Austria, while KEEPING France and Switzerland. DE: SGB V (statutory health insurance incl. §33a DiGA, telemedicine), medical confidentiality §203 StGB, e-prescription (eRezept) + telematics infrastructure. AT: Ärztegesetz §54 (medical confidentiality), GTelG 2012 / telehealth rules, record retention. Keep FR (Public Health Code L1110-4, L4131-1) and CH (MedPA/LPMéd, HMA) lines. Produce the FULL replacement summary (one compact paragraph) covering FR, CH, DE, AT.',
    existing: {
      summary:
        'FR: Public Health Code L1110-4 (medical confidentiality) + L4131-1. CH: MedPA (Medical Professions Act), HMA. Record retention 20 years FR / ~20 years CH (post-2020 reform; cantonal variation).',
      key_articles: ['PHC L1110-4', 'PHC L4131-1', 'MedPA'],
      official_url: 'https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006072665/',
    },
  },
  {
    id: 'national_ehealth',
    jurisdiction: 'EU/CH',
    fires_at: 'Q22 (integrates with national electronic health records?) = yes',
    brief:
      'Extend the existing "eHealth — national profiles" card to ADD Germany and clarify Austria, keeping CH and FR. DE: Telematics Infrastructure (TI) + electronic patient record (ePA, opt-out since 2025) governed by gematik, SGB V §291 ff. AT: ELGA (Elektronische Gesundheitsakte) under GTelG 2012. Keep CH (EPRA/EPDG + Swiss eHealth certification) and FR (Ségur certification, FHIR DMP profile). Produce the FULL replacement summary (one compact paragraph) covering CH, FR, DE, AT.',
    existing: {
      summary:
        'CH: EPRA/EPDG + Swiss eHealth certification (full revision under way, bill before Parliament since Nov 2025, opt-out targeted ~2028). FR: Segur certification, FHIR DMP profile. AT: ELGA G-TG.',
      key_articles: ['EPRA', 'IHE XDS', 'FHIR R4'],
      official_url: 'https://www.fedlex.admin.ch/eli/cc/2017/203/en',
    },
  },
]

const CARD_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    id: { type: 'string' },
    title: { type: 'string' },
    jurisdiction: { type: 'string' },
    summary: { type: 'string' },
    key_articles: { type: 'array', items: { type: 'string' } },
    official_url: { type: 'string' },
  },
  required: ['id', 'title', 'jurisdiction', 'summary', 'key_articles', 'official_url'],
}

const REVIEW_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    accurate: { type: 'boolean' },
    issues: { type: 'array', items: { type: 'string' } },
    corrected_summary: { type: 'string' },
    corrected_articles: { type: 'array', items: { type: 'string' } },
  },
  required: ['accurate', 'issues', 'corrected_summary', 'corrected_articles'],
}

const CONTEXT = `These cards belong to "HERA — Which regulations apply to your mHealth app?", an orientation decision tree for EU + Switzerland mHealth developers. Cards must be: factually accurate, compact (1 dense paragraph summary), concrete (cite the exact act + article numbers), and honest about scope. This is an orientation tool, not legal advice — but every citation shown must be correct.`

phase('Draft')
const results = await pipeline(
  ITEMS,
  // Stage 1 — draft
  (item) =>
    agent(
      `${CONTEXT}\n\nDraft the regulatory card "${item.id}" (jurisdiction: ${item.jurisdiction}; fires at: ${item.fires_at}).\n\nWhat it must cover:\n${item.brief}\n\n${
        item.existing
          ? `This card ALREADY EXISTS — here is its current content; preserve the correct parts and EXTEND as instructed:\nsummary: ${item.existing.summary}\narticles: ${JSON.stringify(item.existing.key_articles)}\nurl: ${item.existing.official_url}\n\n`
          : ''
      }Return the card as structured output. Keep "id"="${item.id}" and "jurisdiction"="${item.jurisdiction}". official_url must be a real official source (Fedlex for CH, EUR-Lex for EU, gesetze-im-internet.de for DE, ris.bka.gv.at for AT, legifrance for FR). Summary <= 80 words, dense.`,
      { label: `draft:${item.id}`, phase: 'Draft', schema: CARD_SCHEMA, agentType: 'general-purpose' }
    ),
  // Stage 2 — two independent legal-accuracy reviewers, run concurrently
  (card, item) =>
    parallel(
      ['Swiss/EU regulatory lawyer', 'medical-device & data-protection compliance specialist'].map(
        (persona) => () =>
          agent(
            `${CONTEXT}\n\nYou are a ${persona}. Critically review this draft card for the decision tree. Flag ANY inaccuracy: wrong article numbers, wrong act names, wrong dates, over-broad claims, or scope errors (e.g. claiming an EU-only instrument binds Switzerland). Be strict.\n\nCard id: ${card.id} (jurisdiction ${card.jurisdiction})\nIt must cover: ${item.brief}\n\nDRAFT:\ntitle: ${card.title}\nsummary: ${card.summary}\narticles: ${JSON.stringify(card.key_articles)}\nurl: ${card.official_url}\n\nReturn: accurate (true/false), issues (list), corrected_summary (your best accurate version, <=80 words), corrected_articles (list).`,
            {
              label: `verify:${item.id}:${persona.split(' ')[0]}`,
              phase: 'Verify',
              schema: REVIEW_SCHEMA,
              agentType: 'general-purpose',
            }
          )
      )
    ).then((reviews) => ({ card, reviews: reviews.filter(Boolean), item })),
  // Stage 3 — reconcile draft + 2 reviews into a final card
  (bundle) => {
    if (!bundle) return null
    const { card, reviews, item } = bundle
    return agent(
      `${CONTEXT}\n\nProduce the FINAL version of card "${card.id}". You have a draft and two independent expert reviews. Incorporate every VALID correction; if reviewers disagree, pick the most precise, defensible wording. Keep id="${card.id}", jurisdiction="${card.jurisdiction}". Summary <=80 words.\n\nDRAFT:\n${JSON.stringify(card)}\n\nREVIEW 1:\n${JSON.stringify(reviews[0] || {})}\n\nREVIEW 2:\n${JSON.stringify(reviews[1] || {})}\n\nReturn the final card as structured output.`,
      { label: `final:${item.id}`, phase: 'Reconcile', schema: CARD_SCHEMA, agentType: 'general-purpose' }
    )
  }
)

const finals = results.filter(Boolean)
log(`Produced ${finals.length}/${ITEMS.length} final cards`)
return { cards: finals }
