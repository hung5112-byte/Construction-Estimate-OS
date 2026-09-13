export const meta = {
  name: 'rom-trades',
  description: 'One ROM trade estimator per activated playbook trade, in parallel, reading the intake notes/photos and correcting the deterministic assembly quantities',
  whenToUse: 'Called by /rom after `ce-os estimate rom` produced the folder. Do not call on a folder without 00-playbook.json.',
  phases: [{ title: 'Trades', detail: 'one parameterized trade agent per activated trade' }],
}

if (!args || !args.folder) {
  throw new Error('rom-trades needs args {folder: "02-Estimates/<slug>", trades?: [...]} — run /rom, which builds them')
}
const FOLDER = String(args.folder)
const TRADES = Array.isArray(args.trades) && args.trades.length ? args.trades : null

const TRADE_SCHEMA = {
  type: 'object',
  properties: {
    trade: { type: 'string' },
    lines: { type: 'array', items: { type: 'object', properties: {
      division: { type: 'string' }, item_code: { type: 'string' }, description: { type: 'string' }, qty: { type: 'number' }, unit: { type: 'string' },
      sheet: { type: 'string' }, method: { type: 'string' }, discipline: { type: 'string' }, confidence: { type: 'number' }, notes: { type: 'string' },
      tags: { type: 'object' }, pricing_basis: { type: 'string' } },
      required: ['division', 'item_code', 'description', 'qty', 'unit', 'sheet', 'method', 'discipline', 'confidence'] } },
    assumptions: { type: 'array', items: { type: 'string' } },
    questions: { type: 'array', items: { type: 'object', properties: { text: { type: 'string' }, citation: { type: 'string' }, severity: { type: 'string' }, exposure: { type: 'string' } }, required: ['text', 'citation', 'severity'] } },
    risks_added: { type: 'array' },
    sources_read: { type: 'array', items: { type: 'string' } },
  },
  required: ['trade', 'lines', 'assumptions', 'questions', 'sources_read'],
}

phase('Trades')
// The trade list comes from the folder's playbook snapshot; the first agent reads it if the caller did not pass one.
const trades = TRADES || (await agent(
  `Read ${FOLDER}/00-playbook.json and ${FOLDER}/00-project-profile.json. Return JSON {trades: [...]}: the playbook's typical_trades minus any trade excluded in profile.exclusions (keys "trade:<name>") and minus "general-conditions".`,
  { label: 'trades', phase: 'Trades', schema: { type: 'object', properties: { trades: { type: 'array', items: { type: 'string' } } }, required: ['trades'] } }
)).trades

log(`${trades.length} trade(s): ${trades.join(', ')}`)
const results = await parallel(trades.map(t => () => agent(
  `Estimate folder: ${FOLDER}. Your trade: ${t}. Follow your workflow: read 00-intake.json, 00-playbook.json, 04-takeoff-ledger.md and anything in package/ that touches ${t}; keep, correct or add assembly lines for ${t} only; state every assumption and question with cost exposure. Return the JSON described in your instructions and write it to ${FOLDER}/readers/rom-${t}.json.`,
  { label: `trade:${t}`, phase: 'Trades', agentType: 'ce-rom-trade-estimator', schema: TRADE_SCHEMA }
)))
const done = results.filter(Boolean)
log(`${done.length}/${trades.length} trade agents returned; ${done.reduce((n, r) => n + r.lines.length, 0)} lines, ${done.reduce((n, r) => n + r.questions.length, 0)} questions`)
return { trades, returned: done.map(r => ({ trade: r.trade, lines: r.lines.length, questions: r.questions.length, sources: r.sources_read.length })) }
