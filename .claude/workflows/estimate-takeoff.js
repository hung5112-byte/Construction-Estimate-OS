export const meta = {
  name: 'estimate-takeoff',
  description: 'Discipline reader agents take off a bid package in parallel (civil/structural, architectural, MEP), the spec analyst extracts requirements, the RFI coordinator consolidates questions',
  whenToUse: 'Called by /estimate after `ce-os estimate intake` and `takeoff` have produced the folder. Do not call on a folder without cards/ and renders/.',
  phases: [
    { title: 'Read', detail: 'one reader per discipline group, in parallel, over its own sheets' },
    { title: 'Specs', detail: 'spec analyst: Division 00/01 items and cost-driving requirements' },
    { title: 'Questions', detail: 'RFI coordinator merges and ranks every question' },
  ],
}

if (!args || !args.folder) {
  throw new Error('estimate-takeoff needs args {folder: "02-Estimates/<slug>"} — run /estimate, which builds it')
}
const FOLDER = String(args.folder)

const LINE_SCHEMA = {
  type: 'object',
  properties: {
    lines: { type: 'array', items: { type: 'object', properties: {
      division: { type: 'string' }, item_code: { type: 'string' }, description: { type: 'string' }, qty: { type: 'number' },
      unit: { type: 'string' }, sheet: { type: 'string' }, revision: { type: 'string' }, method: { type: 'string' },
      confidence: { type: 'number' }, notes: { type: 'string' }, tags: { type: 'object' } },
      required: ['division', 'item_code', 'description', 'qty', 'unit', 'sheet', 'method', 'confidence'] } },
    questions: { type: 'array', items: { type: 'object', properties: {
      text: { type: 'string' }, citation: { type: 'string' }, severity: { type: 'string' }, exposure: { type: 'string' } },
      required: ['text', 'citation', 'severity'] } },
    tiles_read: { type: 'array', items: { type: 'string' } },
  },
  required: ['lines', 'questions', 'tiles_read'],
}

const READERS = [
  { id: 'ce-civil-structural-lead', disc: 'C, L, S sheets — sitework, concrete, masonry, structural steel (Divisions 03/04/05/31/32/33)' },
  { id: 'ce-architectural-lead', disc: 'A and I sheets — envelope, interiors, openings, specialties (Divisions 06–14)' },
  { id: 'ce-mep-lead', disc: 'M, P, FP, E, T, FA sheets — mechanical, plumbing, fire protection, electrical, low voltage (Divisions 21/22/23/26/27/28)' },
]

phase('Read')
const reads = await parallel(READERS.map(r => () => agent(
  `Estimate folder: ${FOLDER}. You own: ${r.disc}. Follow the reader protocol in your instructions and the drawing-reading skill: cards first, then overview and tiles, confirm vector candidates, add what was missed, questions not assumptions. Return the JSON described (lines, questions, tiles_read). Also write the same JSON to ${FOLDER}/readers/${r.id}.json.`,
  { label: `read:${r.id}`, phase: 'Read', agentType: r.id, schema: LINE_SCHEMA }
)))

phase('Specs')
const specs = await agent(
  `Estimate folder: ${FOLDER}. Read 02-spec-index.md and package/*Manual*.pdf (via the cards and the spec index). Return JSON {requirements: [{division, section, requirement, cost_effect}], questions: [{text, citation, severity, exposure}]} and write it to ${FOLDER}/readers/ce-spec-analyst.json.`,
  { label: 'specs', phase: 'Specs', agentType: 'ce-spec-analyst', schema: { type: 'object', properties: { requirements: { type: 'array' }, questions: { type: 'array' } }, required: ['requirements', 'questions'] } }
)

phase('Questions')
const allQ = reads.filter(Boolean).flatMap(r => r.questions).concat(specs ? specs.questions : [])
log(`${reads.filter(Boolean).length}/${READERS.length} readers returned; ${allQ.length} raw questions`)
const rfi = await agent(
  `Estimate folder: ${FOLDER}. Here are ${allQ.length} raw questions from the readers and the spec analyst as JSON: ${JSON.stringify(allQ).slice(0, 60000)}. De-duplicate, answer the ones the package itself answers (cite the sheet/section), rank the rest CRITICAL/WARN/INFO with cost exposure, and write the result to ${FOLDER}/readers/ce-rfi-coordinator.json as {resolved: [...], open: [...]}. Return the same JSON.`,
  { label: 'rfi', phase: 'Questions', agentType: 'ce-rfi-coordinator', schema: { type: 'object', properties: { resolved: { type: 'array' }, open: { type: 'array' } }, required: ['resolved', 'open'] } }
)
return { readers: reads.filter(Boolean).map((r, i) => ({ id: READERS[i].id, lines: r.lines.length, tiles: r.tiles_read.length })), open_questions: rfi ? rfi.open.length : null }
