export const meta = {
  name: 'hera-llm-judge',
  description: 'LLM-as-judge (Depth & Actionability) over one approach’s 25 transcripts',
  phases: [
    { title: 'Judge', detail: 'one Claude agent per scenario, writes verdict JSON to disk' },
  ],
}

// NOTE: the Workflow `args` global did not propagate reliably in this session, so the
// target approach is hardcoded here and edited before each launch (prompt-only → fine-tuned → rag → rlm).
const APPROACH_OVERRIDE = 'rlm'
const approach = APPROACH_OVERRIDE

const RUBRIC = `You are an expert rater for the HERA Risk & Safety Copilot — a conversational AI helping mHealth app developers identify ethical and regulatory risks.

For each transcript you receive, score on two 1–5 scales:

**Depth** — how specifically did the copilot drill into the developer's actual app?
- 1 = entirely generic, copy-pastable to any health app
- 3 = some specifics (named features, regulations) but mostly templated
- 5 = laser-focused; questions and risks reference THIS developer's choices, data flows, target users, and the precise regulation/article that applies

**Actionability** — could a competent developer take the copilot's suggestions and implement them tomorrow?
- 1 = vague platitudes ("ensure compliance")
- 3 = directional advice ("do a DPIA")
- 5 = concrete recipes ("Implement a layered consent UI with a 1-paragraph summary + an expandable detail section; document the lawful basis under GDPR Art. 9(2)(a) in your privacy notice")

Be a strict, calibrated rater. Do NOT inflate scores. A generic, templated copilot deserves 1-2 even if polite.`

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    depth: { type: 'integer', minimum: 1, maximum: 5 },
    depth_justification: { type: 'string' },
    actionability: { type: 'integer', minimum: 1, maximum: 5 },
    actionability_justification: { type: 'string' },
    salient_examples: { type: 'array', items: { type: 'string' } },
  },
  required: ['depth', 'depth_justification', 'actionability', 'actionability_justification', 'salient_examples'],
}

const scenarios = Array.from({ length: 25 }, (_, i) => `scenario_${String(i + 1).padStart(2, '0')}`)

phase('Judge')
log(`Judging approach="${approach}" over ${scenarios.length} scenarios`)

const results = await parallel(scenarios.map((sid) => async () => {
  const caseFile = `data/evaluation/judge_prompts/${sid}__${approach}.md`
  const outFile = `data/evaluation/judge_ratings_semantic/${sid}__${approach}.json`
  const prompt = `${RUBRIC}

Your task:
1. Use the Read tool to read the case file at \`${caseFile}\`. It contains the approach under review, the scenario, the gold-standard HERA dimensions, and the FULL developer↔copilot transcript.
2. Apply the rubric above. Decide an integer Depth (1-5) and an integer Actionability (1-5), each with a 1-2 sentence justification grounded in THIS transcript, plus 2-4 short salient snippets copied from the transcript that drove your scores.
3. Use the Write tool to write your verdict as a single JSON object to \`${outFile}\`. The JSON MUST have exactly these keys: "scenario_id" (=\"${sid}\"), "approach" (=\"${approach}\"), "depth", "depth_justification", "actionability", "actionability_justification", "salient_examples".
4. Then return the judgement as your structured output (depth, depth_justification, actionability, actionability_justification, salient_examples).

If the case file is missing or the transcript is empty, score depth=1 and actionability=1 and say so in the justifications. Do not invent transcript content.`
  const v = await agent(prompt, {
    label: `judge:${approach}:${sid}`,
    phase: 'Judge',
    schema: SCHEMA,
    agentType: 'general-purpose',
  })
  return v ? { scenario_id: sid, approach, ...v } : null
}))

const ok = results.filter(Boolean)
const mean = (xs) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : 0)
const depthMean = mean(ok.map((r) => r.depth))
const actMean = mean(ok.map((r) => r.actionability))
log(`approach=${approach} judged=${ok.length}/${scenarios.length} depth_mean=${depthMean.toFixed(2)} action_mean=${actMean.toFixed(2)}`)

return {
  approach,
  judged: ok.length,
  total: scenarios.length,
  depth_mean: depthMean,
  actionability_mean: actMean,
  ratings: ok,
}
