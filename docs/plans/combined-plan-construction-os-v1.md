---
type: architecture
project: Construction-Estimate-OS
doc: combined-plan
version: "1.0"
status: draft-for-review
created: 2026-09-13
tags: [agentic-os, construction, estimating, company-os, plan, grandvista, combined]
author: Brian H. Doan
related: ["[[00-plan]]", "[[05-eval-grandvista-os-v3]]", "[[02-research-gc-estimating-workflow]]", "[[03-research-drawing-reading-tech]]"]
---

# Construction OS — combined plan v1

> **What this is.** One system for a commercial general contractor that merges the two plans: the **estimating engine** built in [[00-plan]] (Construction-Estimate-OS: vector-first takeoff, deterministic pricing, hard gates, provenance) and the **company operating spine** from GrandVista OS v3 (leads → estimate → proposal → project → daily log → customer update → reports, with roles, approvals, audit and a learning loop). The evaluation that motivates the merge is [[05-eval-grandvista-os-v3]].
> **The one sentence.** Two layers, one contract: the engine owns every number and every quantity; the app owns every person, approval and message. Nothing that reaches a client is a model's guess.

---

## 0. Decisions

| # | Decision | Comes from | Why |
|---|---|---|---|
| D1 | **Two layers, one contract.** Layer 1 = the Estimating Engine (Python, this repo) exposed as CLI, MCP and a small HTTP service. Layer 2 = the Company OS app (Next.js / Supabase, his stack) whose Estimating module calls Layer 1. The engine also runs standalone in Claude Code, as today. | both | Neither side rewrites the other; each keeps its stack; the boundary is a versioned JSON contract (§4). |
| D2 | **No LLM arithmetic anywhere.** Agents select assemblies, library rows and quantity assumptions; code multiplies. A missing price is `[UNPRICED]`, never a guess. Applies to ROMs too. | ours | Model-generated prices drift 50–70% run to run; deterministic dollars are auditable and repeatable. |
| D3 | **Every estimate states its AACE class and accuracy band.** ROM = Class 5/4 (−30/+50%, −20/+30%) from assemblies and $/SF models; Detailed = Class 3/2 from drawings; Final = Class 2/1 with sub bids. Printed on every proposal. | ours + AACE 56R-08 | A ROM without a band is a price. |
| D4 | **Deterministic gates before any human approval.** Our G1–G10 plus his rules turned into gates: every playbook trade covered or excluded with a reason, every allowance sourced, every high-severity risk has an exclusion or an RFI, client-facing text passes the sensitive-info filter. | both | A plausible wrong total must not pass because agents agreed. |
| D5 | **One provenance model.** Per quantity: sheet · revision · method · confidence. Per price: `pricing_basis` (historical \| assembly \| manual \| allowance \| sub_bid \| online_check) + row id + date. Per AI call: `ai_runs` (input, output, model, user, sources, approval). | both | His storage discipline plus our enforcement. |
| D6 | **Human gates (in order).** RFI pause → estimate approval (Stop 1) → proposal approval → external communications approval (client updates, reports, bid invites) → change orders. AI never sends anything. | both | His approval matrix is right for a multi-user company; our two gates sit inside it. |
| D7 | **Learning loop = his design on our memory layer.** Approved-only memory, feedback events, estimate actuals at closeout, versioned project-type playbooks, strategy-priced ROMs tagged `sales_strategy` and excluded from cost history, fine-tune only after 50–100 clean examples. | his | The correct discipline; our ledger/instincts machinery already exists to host it. |
| D8 | **Merged agent roster (§5).** Estimating: our 6 departments / 26 agents, with his 14 trade agents folded into **one parameterized trade agent driven by trade playbooks**. Operations: his 8 agents (lead intake, CRM follow-up, daily log, photo caption, customer update, sensitive-info filter, weekly/monthly report) live in the app layer. | both | Trade knowledge as data (playbooks), not as 14 near-identical prompts. |
| D9 | **Security = his model** for the app (7 roles, RLS, protected cost fields, audit logs, source-of-truth hierarchy) **plus our rule**: document text (plans, specs, emails, quotes, photos captions) is untrusted input and passes a quarantine screen before any agent reads it. | both | His plan has no prompt-injection policy; ours has no roles. |
| D10 | **Build order puts the bottleneck first.** Estimating core and the lead → ROM workflow ship before projects, daily logs and reports; portals and learning UI last. MVP = the two killer workflows, literally. | ours (fixing his §6 risk) | His plan reached the estimating AI in sprint 6 of 9. |
| D11 | **Accuracy is a launch criterion.** Final estimates: coverage × precision@25% on a golden set, 3 runs. ROMs: band hit-rate against actuals on ≥10 past projects before sales use them. | ours | His test plan measures permissions and schemas, not whether the number is close. |
| D12 | **Model-neutral schemas.** Engine calls bill the Claude Max subscription via `claude-cli` (Brian's ruling); the app may call the engine for all estimating work and keep OpenAI Agents SDK for ops agents if he prefers; every schema and `ai_runs` record is provider-neutral. | both | No lock-in on either side. |

---

## 1. Product spine (combined)

```
Lead → Estimate request → ESTIMATE (engine: ROM | detailed | final) → Proposal → Won → Project
     → Daily log → Customer update → Weekly / monthly report → Change orders → Closeout → LEARNING
```

Two killer workflows define the MVP:

1. **Lead → same-day ROM.** Sales creates a lead, uploads notes/photos/whatever plans exist, clicks "Request estimate". The engine's intake reads what it can (sheet register if drawings exist, otherwise the intake form), the project-type playbook selects the trades, the trade agent picks assemblies and quantity assumptions, the cost engine computes low/target/high from the assembly table, the risk checklist and RFI list come from the playbook, gates run, the Chief Estimator (human) approves, the Proposal Agent drafts, a human approves the proposal. Target: ROM draft in ≤ 10 minutes after intake with class, band, assumptions, exclusions, risks and open questions on it.
2. **Daily log → customer update.** Field user submits photos + voice/text in ≤ 60 s; the daily-log agent writes the internal log; the customer-update agent drafts; the sensitive-info filter screens; PM approves; email queue sends; the timeline records it.

Everything else (sub bids, reports, portals, learning UI) follows.

---

## 2. Architecture

```
┌──────────────────────── Company OS app (Next.js · Supabase · his stack) ────────────────────────┐
│  CRM / Leads   Projects   Daily logs   Customer updates   Reports   Subcontractors   Admin       │
│  Roles + RLS · approvals · email queue · Inngest jobs · audit_logs · ai_runs · learning tables   │
│  Estimating module UI: intake · plans & photos · takeoff viewer · scope by trade · pricing ·     │
│                        risk review · sub bids · proposal                                         │
└───────────────┬──────────────────────────────────────────────────────────────┬──────────────────┘
                │  Estimate Service contract v1 (JSON, §4)                     │  learning records
┌───────────────▼──────────────────────────────────────────────────────────────▼──────────────────┐
│  Estimating Engine (this repo · Python · Claude Max via claude-cli · CLI + MCP + HTTP)          │
│  intake → takeoff (vector/schedule/vision) → RFI → price (assemblies + library) → gates → report │
│  playbooks · cost library · benchmarks · markup policy · memory layer (ledger, instincts)        │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

- **Files stay the engine's truth** (an estimate folder per job); the app stores the contract outputs in its tables (`estimates`, `estimate_versions`, `estimate_line_items`, `trade_estimates`, `ai_runs`) and links back to the folder id. Nothing is computed twice.
- **Three delivery modes for the engine:** `ce-os estimate …` (CLI, today), MCP tools `bd_estimate_*` (Claude Desktop / Code), and `estimate-service` (FastAPI, loopback or private network) for the app.
- **Learning records flow both ways:** the app writes approved memory, feedback events and actuals into its tables; a nightly job exports them as JSON the engine ingests into its memory layer (and vice versa), so both sides retrieve the same approved lessons.

---

## 3. The estimating module, merged

| Estimate type | Class / band | Inputs | Quantities from | Prices from | Output |
|---|---|---|---|---|---|
| **ROM** | 5 (−30/+50%) or 4 (−20/+30%) if partial plans | intake form (type, SF, city, trades, notes, photos), playbook | playbook quantity assumptions per SF / per room / per fixture, plus any schedules or room tags the engine can read from partial plans | assembly table per project type × trade (low / target / high per unit) → computed, `pricing_basis: assembly` or `historical` | low / target / high with class + band, assumptions, exclusions, risks, RFIs, proposal draft |
| **Detailed** | 3 or 2 | full drawing set + Project Manual | our pipeline: register → schedules → vector → vision readers → ledger | cost library (BYO first, seed marked), location factor, escalation | single-point estimate with the ten gates, workbook, Basis of Estimate |
| **Final** | 2 or 1 | detailed + sub quotes | ledger | leveled sub bids replace library lines; plugs with provenance | bid form basis, scope letter, proposal |

**Adopted from his plan:** `pricing_basis` on every line; low/target/high for ROM; his eight project-type playbooks (restaurant TI, salon, medical/dental, retail TI, office, white box, ground-up retail, industrial/warehouse) as **data files** that seed trades, quantity assumptions, common RFIs, exclusions and risk checklists; the Proposal Agent that cannot invent price; the sensitive-info filter; historical and online-pricing checks as *warnings*, never as prices.
**Adopted from ours:** the extraction pipeline, the cost engine, the ten gates, provenance, the RFI pause with cost exposure, the golden fixture and the accuracy harness, Texas tax/retainage/bond handling, cited exclusions.

**Playbook file (engine data, versioned, approval-gated):**

```yaml
project_type: restaurant-ti
version: 1.0
typical_trades: [demo, framing-drywall, paint, flooring, ceiling, plumbing, hvac, electrical, hood-kitchen, fire-suppression, fire-alarm, general-conditions]
assemblies:                          # low / target / high per unit — the ONLY source of ROM dollars
  - code: 23-hood-type1-per-lf   ; unit: LF ; low: 1450 ; target: 1800 ; high: 2400 ; source: "GrandVista 2024–2026 buyouts [to load]"
  - code: 22-grease-waste-reroute; unit: LS ; low: 8000 ; target: 14000; high: 22000 ; source: "..."
quantity_rules:                      # how the trade agent turns intake facts into quantities
  - "hood LF = cookline LF from equipment plan or 1 LF per 40 SF of kitchen when no plan"
common_rfis: ["Is make-up air existing or new?", "Grease interceptor capacity and location?", "Gas and electrical service capacity confirmed?"]
common_exclusions: ["kitchen equipment purchase", "RTU replacement", "electrical service upgrade"]
risk_checklist: ["hood/MUA", "grease trap", "health department", "Fire Marshal", "RTU capacity", "gas load", "slab trenching"]
benchmarks: {per_sf_low: 220, per_sf_high: 360, source: "benchmarks.md"}
```

---

## 4. Estimate Service contract v1 (the boundary)

All bodies are JSON; every response carries `engine_version`, `estimate_folder`, `ai_runs[]` (model, prompt hash, sources) and `gates[]` where applicable. Files (PDFs, images) are exchanged by path or object-store key, never inline.

| Call | Input | Output |
|---|---|---|
| `POST /estimates/intake` | `{name, building_type, project_type, city, aace_class, gross_sf?, package: [file refs], intake_form?}` | `{folder, profile, sheet_register[], spec_index[], division_01[], cards[]}` |
| `POST /estimates/{id}/takeoff` | `{mode: seed \| readers, reader_lines?[]}` | `{ledger[], checks[], discrepancies[]}` |
| `POST /estimates/{id}/rfi` | — | `{questions[] with severity, citation, exposure}` |
| `POST /estimates/{id}/answers` | `{answers[]}` | `{questions[] updated}` |
| `POST /estimates/{id}/price` | `{library_refs?, policy_overrides?}` | `{lines[], general_conditions[], markups[], summary[], benchmark, flags}` |
| `POST /estimates/{id}/review` | `{judged?[]}` | `{verdict, gates[]}` |
| `POST /estimates/{id}/report` | `{narrative?}` | `{report_md, outputs: [xlsx, docx]}` |
| `POST /estimates/{id}/rom` | `{intake_form, playbook_version}` | `{low, target, high, class, band, lines[], assumptions[], exclusions[], risks[], questions[], gates[]}` (one call for workflow 1) |
| `POST /learning/import` / `GET /learning/export` | approved memory, actuals, feedback events, playbook versions | same shapes both ways |

Line schema (shared by engine ledger, app `estimate_line_items` and trade-agent JSON):

```json
{"id":"T-0012","division":"08","csi_code":"08 11 13","trade":"openings","item_code":"08-hm-door-single","description":"HM door 102",
 "qty":1,"unit":"EA","sheet":"A-601","revision":"2","method":"schedule","confidence":0.95,
 "pricing_basis":"historical","unit_low":1500,"unit_target":1650,"unit_high":1900,"source":"buyouts-2025.csv#row-41","quote_date":"2026-05-02",
 "assumptions":[],"exclusions":[],"tags":{"mark":"102"}}
```

---

## 5. Merged agent roster

| Layer | Department / group | Agents | Notes |
|---|---|---|---|
| Engine | 01 Bid coordination | bid-coordinator ⭐, document-controller, spec-analyst, rfi-coordinator, proposal-writer | his Estimate Intake Agent → bid-coordinator; his Plan Review Agent → document-controller + spec-analyst on top of the register and spec index (tooling, not raw vision) |
| Engine | 02 Civil & structural | civil-structural-lead ⭐, sitework, concrete, steel-masonry | his Concrete/Slab Agent folds in |
| Engine | 03 Architectural | architectural-lead ⭐, envelope, interiors, openings, specialties-equipment | his Demo, Framing/Drywall, Paint, Flooring, Ceiling, Millwork fold in |
| Engine | 04 MEP | mep-lead ⭐, hvac, plumbing-fire, electrical-lv | his HVAC, Plumbing, Fire Sprinkler, Fire Alarm, Hood/Kitchen fold in (hood/kitchen becomes a playbook + an assembly set, not an agent) |
| Engine | 05 Cost engineering | pricing-lead ⭐, general-conditions, risk-markup, sub-bid-leveler | his Historical Pricing → pricing-lead; Online Pricing → a `commodity_check` tool (warnings only); General Conditions Agent folds in |
| Engine | 06 Estimate review | chief-estimator ⭐, scope-gap-auditor, constructability-reviewer, benchmark-analyst | his Scope Gap, Risk and Chief Estimator agents fold in; the human Chief Estimator approves |
| Engine | **trade-agent (parameterized)** | one agent, one prompt, `trade` + playbook as parameters | replaces his 14 trade agents for ROM work; evaluated once, consistent everywhere |
| App | Operations | lead-intake, crm-follow-up, daily-log, photo-caption, customer-update, sensitive-info-filter, report (weekly / monthly by parameter) | his, unchanged in intent; sensitive-info filter also screens our proposal / scope letter |
| App | Orchestration | ai-manager (routing, approvals) | his; calls the engine for anything with a number in it |
| Both | Learning | learning-memory (extract → classify → link sources → human approves) | his design; runs on our memory layer, results mirrored to his tables |

26 engine agents + 1 parameterized trade agent + 9 app agents = 36 roles, but only ~20 distinct prompts.

---

## 6. Gates and approvals (merged, in order)

**Deterministic (engine, before any human sees a number):** G1 every measured sheet claimed · G2 provenance on every line · G3 every spec division and every playbook trade covered or excluded with a citation · G4 arithmetic ties · G5 units valid · G6 $/SF inside the project-type band · G7 every CRITICAL RFI answered or carried as a written assumption · G8 scale gate · G9 confidence floor · G10 unpriced lines under threshold · **G11** every allowance has an amount and a source · **G12** every high-severity risk has an exclusion or an RFI · **G13** client-facing text passed the sensitive-info filter (no cost, margin, blame, admissions, unapproved promises).

**Human (app):** estimate approval (Stop 1) → proposal approval → customer update / report / bid-invite approval → change-order approval → learning-memory approval. Roles per his matrix; audit log on each.

---

## 7. Data model (app) ↔ engine files

| App table (his) | Engine artefact (ours) | Rule |
|---|---|---|
| `estimates`, `estimate_versions` (+ `aace_class`, `accuracy_band`) | `02-Estimates/<slug>/00-project-profile.json` | one version per engine run; the folder id is the join key |
| `estimate_line_items` (+ `pricing_basis`, low/target/high, `sheet`, `revision`, `method`, `confidence`) | `04-takeoff-ledger.json` + `06-estimate.json` lines | never edited by AI after approval; edits create a new version |
| `trade_estimates` | reader / trade-agent JSON in `readers/` | stored verbatim as `agent_output_json` |
| `ai_runs` | engine usage log + per-call records | exported with every response |
| `bid_requests`, `sub_bids` | `readers/ce-sub-bid-leveler.json` + leveling matrix (Phase 3) | his statuses verbatim |
| `historical_unit_prices`, `markup_rules`, `exclusion_library` | `03-Cost-Library/*.csv`, `00-Brain/markup-policy.md`, playbooks | app is the editor, engine is the consumer; nightly sync |
| `ai_memory_records`, `estimate_actuals`, `project_lessons_learned`, `model_feedback_events`, `project_type_playbooks` | engine memory layer + `playbooks/*.yaml` | approval-gated both ways; strategy-priced ROMs tagged and excluded from cost history |

---

## 8. Build plan (owners and acceptance)

Two tracks run in parallel after Phase 0. **Engine** = this repo (Brian, Claude Code). **App** = his repo (his AI coding agent + his review). Weeks are effort-based, not calendar promises.

### Phase 0 — contract and cleanup (week 1, both)
- Engine: publish `docs/contracts/estimate-service.v1.md` (this §4) + JSON schemas; freeze the line schema.
- App: fix the document inconsistencies listed in [[05-eval-grandvista-os-v3]] §4.8 (Kanban vs statuses, missing agent cards, ground-up trades, "AI does not price" wording); add the untrusted-input rule and the class/band fields to `AGENTS.md`, `02_DATABASE_SCHEMA.md`, `08_SECURITY_RULES.md`; reorder sprints per D10.
- Both: agree the golden sets — our synthetic package for detailed; **10 of his past projects with known outcomes** for ROM.
- Acceptance: both repos reference the same contract file hash; the ROM golden set exists as a folder of intake forms + actuals.

### Phase 1 — estimating core, ROM mode (weeks 1–3, engine)
- `pricing_basis`, low/target/high on lines; `aace_class` + band on the profile; ROM stage `ce-os estimate rom` from an intake form + playbook; playbook files for his 8 project types (assemblies marked `[to load]` until his data arrives); the parameterized trade agent; G11–G13; sensitive-info filter tool; proposal / scope-letter renderer.
- `estimate-service` (FastAPI, loopback) + MCP tools `bd_estimate_*`; headless vision provider once `claude /login` is done.
- Accuracy harness: `ce-os estimate eval --set <folder>` reporting coverage × P@25% (detailed) and band hit-rate (ROM), 3 runs.
- Acceptance: ROM on the 10-project golden set lands inside the stated band on ≥ 7/10 targets (report the miss reasons); detailed run on the synthetic set still APPROVE; suite green.

### Phase 2 — company spine MVP (weeks 2–6, app)
- Sprint 1 shared core (auth, roles, RLS, audit, dashboard shell) → Sprint 2 CRM leads with `next_action` rule → **Sprint 3 estimating module calling the engine** (intake, plans & photos, ROM result view with class/band/gates, RFI answer screen, approve, proposal draft) → Sprint 4 projects + daily log (60-second mobile form) → Sprint 5 customer updates with approval inbox + email queue.
- Acceptance: the business end-to-end test from his `07_TEST_PLAN.md` steps 1–12, with the engine behind step 4–7; permission tests; no internal cost leak; every AI call in `ai_runs`.

### Phase 3 — sub bids, reports, learning (weeks 6–10, both)
- Engine: leveling matrix with plug provenance and the 15–20% outlier flag; learning import/export; playbook versioning with approval; actuals ingestion.
- App: subcontractor CRM + bid requests + quote upload (his Sprint 7); weekly/monthly reports (his Sprint 4 remainder); closeout learning review screen; playbook approval UI.
- Acceptance: a leveled trade with three quotes and one plug shows provenance end to end; a closeout produces ≥ 3 lessons that require approval before retrieval.

### Phase 4 — hardening, portals, integrations (after)
- His Sprint 8 hardening (QA agent), client/sub portals, Gmail/Drive; our Phase 3 integrations (Kreo API, Bluebeam MCP, Autodesk Takeoff, IfcOpenShell), micro-office view; fine-tuning only after 50–100 clean examples.

---

## 9. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Two teams, two stacks, one contract drifts | contract file is versioned and hashed in both repos; a contract test in each CI |
| ROM assemblies start empty (his data not loaded) | playbook assemblies ship `[to load]`; the ROM refuses to produce dollars for a trade with no assembly (`[UNPRICED]`), never a guess |
| His AI coder builds ahead of the contract | `CURRENT_TASK.md` lists the contract file; Architect agent reviews any estimating-module change |
| Engine latency on Max-plan queuing for reader agents | ROM path needs no vision; detailed path runs readers in parallel; headless provider has retry and timeout knobs |
| Learning loop poisons cost history | approved-only memory, `sales_strategy` tag excluded from benchmarks, versioned playbooks |
| Prompt injection via client emails / plans / quotes | quarantine screen in both layers; document text never becomes instructions |
| Scope creep back to ten modules | `NOT_NOW.md` enforced; MVP = the two workflows; phases gated by acceptance tests |

---

## 10. Open questions (answer before Phase 0 closes)

1. **Ownership and licensing.** Engine stays Apache-2.0 in Brian's repo; his app stays his. Is the engine used by GrandVista under the open license, or under a service arrangement? (Decide before any GrandVista data enters the engine's cost library.)
2. **Data.** Will GrandVista provide 10 past projects (intake facts + final numbers + actuals) for the ROM golden set, and their buyout history for assemblies? Without it, ROMs are `[UNPRICED]` by design.
3. **Who runs the engine for the app.** Loopback FastAPI on the same box as the app (simplest), or Brian hosts it and exposes it privately.
4. **Estimating UI.** His takeoff viewer (OpenTakeoff-style) pre-populated from our candidates, or our workbook/report first and the viewer later.
5. **Model billing.** Engine on Claude Max (Brian's ruling) is fine for one company; for GrandVista's volume, decide who pays for what.
6. **Names.** Keep `Construction-Estimate-OS` for the engine; the app is his `GrandVista OS`; the combined product name is for the two of you.

---

## 11. First ten tasks (start here)

1. Engine: write `docs/contracts/estimate-service.v1.md` + JSON schemas from §4; add a contract test.
2. Engine: add `pricing_basis`, `unit_low/target/high` to the ledger and priced lines; add `aace_class` + `accuracy_band` to the profile and report.
3. Engine: playbook loader + the eight playbook YAML files with `[to load]` assemblies; ROM stage `ce-os estimate rom`.
4. Engine: the parameterized trade agent (one prompt, playbook-driven) + G11–G13 + sensitive-info filter tool + scope-letter renderer.
5. Engine: `estimate-service` FastAPI wrapper + MCP `bd_estimate_*` tools; accuracy harness `ce-os estimate eval`.
6. Brian: `claude /login` with the vault binary; then the headless vision provider.
7. Friend: doc cleanup per [[05-eval-grandvista-os-v3]] §4.8; reorder sprints; add class/band fields and the untrusted-input rule.
8. Friend: assemble the 10-project ROM golden set and the buyout history export.
9. Both: run the golden sets, record the first accuracy numbers, decide the band policy.
10. Both: agree Phase 2 Sprint 3 (estimating module UI) against the contract before his coder starts it.
