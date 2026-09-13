---
type: evaluation
project: Construction-Estimate-OS
created: 2026-09-13
tags: [agentic-os, construction, estimating, evaluation, grandvista, comparison]
author: Brian H. Doan
source: "~/Downloads/grandvista-os-docs-v3.zip (63 files, ~24k words: AGENTS.md, README, docs/00–16, docs/agents/*, docs/agents/trade-agents/*, docs/modules/*)"
related: ["[[00-plan]]", "[[02-research-gc-estimating-workflow]]", "[[03-research-drawing-reading-tech]]"]
---

# GrandVista OS v3 vs Construction-Estimate-OS — evaluation

> **One-line verdict.** They are not competing plans; they are different products that overlap on one module. GrandVista OS is a **company operating system** for a TI-heavy commercial GC (leads → ROM estimate → proposal → project → daily log → customer update → reports) built as a multi-user web app by an AI coding agent. Construction-Estimate-OS is a **deep estimating instrument** (bid package → traceable Class 2 estimate) built on the fleet engine, single operator, files-first. GrandVista's estimating module is where the two meet — and that module is the weakest part of his plan and the strongest part of ours. Each should borrow from the other; a concrete integration exists (§6).

---

## 1. What GrandVista OS v3 is (as read)

- **Company:** GrandVista Construction Group LLC — restaurant build-outs, salons, medical/dental, retail TI, office, white box, plus ground-up retail and industrial/warehouse aspirations. Named people in the docs: Danson (owner, sets ROM strategy prices), Minh (estimator, corrects quantities).
- **Spine:** Lead → Estimate → Proposal → Project → Daily Log → Customer Update → Weekly/Monthly Report. Ten modules (dashboard, CRM, estimating, projects, daily logs, customer updates, subcontractors, documents, reports, admin).
- **Two "killer workflows":** (1) lead to same-day ROM estimate draft in ≤ 10 minutes after intake; (2) field daily log in ≤ 60 seconds → approved customer update by email.
- **Stack:** Next.js / TypeScript / Tailwind / shadcn, Supabase (Postgres, Auth, Storage, RLS), OpenAI Agents SDK, Inngest jobs, Gmail/Drive later. Built by "Astra 6" (an AI coding agent) with a docs-as-constitution method: `AGENTS.md` (15 non-negotiables), `CURRENT_TASK.md` (one task at a time), `NOT_NOW.md`, a six-role coding-agent split (Architect / Backend / Frontend / AI Workflow / Jobs / QA "App-Killer").
- **Data model:** ~40 tables incl. estimates / versions / line items with protected cost fields, trade_estimates (agent JSON), historical_unit_prices, markup_rules, exclusion_library, bid_requests / sub_bids, ai_runs (every AI call logged), plus a learning layer (ai_memory_records, estimate_actuals, project_lessons_learned, model_feedback_events, project_type_playbooks).
- **Roles:** 7 (owner_admin, estimator, PM, field, sales, client, subcontractor) with a permission matrix; internal cost visible only to owner_admin + estimator; external comms approval-gated; audit log on every major action; source-of-truth hierarchy (signed contract > CO > proposal/SOV > RFI > schedule > daily log > note > AI).
- **Estimating AI:** AI Manager → Estimate Intake → Plan Review → Scope → Trade Router → **14 trade agents** (demo, framing/drywall, paint, flooring, ceiling, plumbing, HVAC, electrical, hood/kitchen, fire sprinkler, fire alarm, concrete/slab, millwork, general conditions), each returning scope items with **low/target/high budget** and a `pricing_basis` enum (historical | manual | allowance | sub_bid | online_check) → Historical Pricing Agent (comparables, $/SF) → Online Pricing Agent (commodity materials only) → Scope Gap → Risk → **Chief Estimator Agent** (low/target/high ROM + recommended client price) → human approval → Proposal Agent (client-facing, cannot invent price). Final estimates add sub bid requests + a Bid Leveling Agent. Takeoff is a **manual OpenTakeoff-style viewer** (scale, area, length, count, per-measurement provenance) with a Takeoff Review Agent; "advanced AI takeoff automation without human review" is explicitly not MVP.
- **Learning memory:** approved-only memory (AI output is not memory until reviewed and tagged), strategy-priced ROMs tagged so they never become cost benchmarks, actuals-vs-estimate at closeout, versioned playbooks for 8–9 project types, similarity retrieval by type/SF/city/trades/scope, fine-tune only after 50–100 clean examples.
- **Build order:** Sprint 0 docs → 1 shared core → 2 CRM → 3 projects + daily logs → 4 customer updates + reports → 5 estimating database → 6 AI estimating MVP → 7 sub bids → 8 hardening → 9 learning memory. Rule: "build the business system before the AI system."

---

## 2. Side by side

| Dimension | GrandVista OS v3 | Construction-Estimate-OS (our plan, Phase 1 built) | Assessment |
|---|---|---|---|
| **Problem** | Whole-company bottlenecks: slow ROMs, slow sub pricing, missed follow-ups, scattered field comms | One bottleneck: a bid-ready, traceable estimate from a drawing set | Different problems. His is broader and shallower; ours is narrower and deeper. |
| **Estimate class** | ROM from notes/photos/partial plans (AACE Class 5/4, ±30–50%), final later with sub bids. Class and accuracy band are never stated | Class 2 from CDs (−10/+15%), class declared on every estimate with its band | His docs should state the class and band on every ROM; otherwise a "same-day ROM" reads as a price. |
| **Drawing reading** | Manual takeoff UI + Takeoff Review Agent; Plan Review Agent (LLM) lists sheets/conflicts; AI takeoff deferred | Vector-first + schedule-first extraction (register, text, tables, geometry), vision readers confirm on tiles; proven on a fixture (12/12 doors, 10/10 windows, 440 LF, 12,000 SF) | Ours is ahead; his is honest about VLM limits but leaves the biggest time sink manual. Our extractors are the natural backbone for his Plan Review / Takeoff Review agents (§6). |
| **Who prices** | **The trade agents (LLMs) generate low/target/high dollar ranges**; historical and online agents sanity-check; a human approves | **No LLM arithmetic**: agents choose library rows and assumptions, a deterministic cost engine computes; missing row → `[UNPRICED]`, never a guess | The biggest gap in his plan. Model-generated prices drift 50–70% run to run (Handoff coverage) and hallucinate. Fix is cheap: keep the JSON schema, make the numbers come from a $/SF or assembly table the agent *selects*, not invents. |
| **Quality gates** | Agents check each other (scope gap, risk, chief estimator) + human approval; ai_runs audit | Ten deterministic hard gates (sheets claimed, provenance, spec coverage, arithmetic ties, units, $/SF band, CRITICAL RFIs answered, scale gate, confidence floor, unpriced threshold) before the judged review | His has no machine-checked floor; a plausible but wrong number passes if the agents agree. Add gates before the human sees a total. |
| **Provenance** | Per manual measurement (sheet, scale, who, when, snapshot) and per AI run (input, output, model, sources, approval) | Per quantity (sheet · revision · method · confidence) and per price (library row, date); gates enforce it | Both take provenance seriously; ours enforces it, his stores it. |
| **Human gates** | Approvals everywhere external (proposal, emails, reports, bid invites, price changes) | Two: RFI pause and Stop 1 | His is right for a multi-user company; ours is right for one operator. |
| **Security / roles** | 7 roles, Supabase RLS, protected cost fields, audit logs, client/sub portals | Single operator, files in a vault, git history | His is far stronger and necessary for his users. Ours does not need it yet; it would if Brian's three managers use it. |
| **Cost data** | historical_unit_prices, markup_rules by project type/trade, exclusion library, online commodity checks; learning from actuals | BYO CSV library first, seed placeholders marked [UNCERTAIN], DFW benchmarks, markup policy in the Brain | Comparable intent; his has the better long-run loop (actuals → memory), ours has the better short-run honesty (placeholders labelled, benchmarks sourced). |
| **Learning** | Full design: approved memory, feedback events, actuals, playbooks, similarity retrieval, fine-tune later | Engine has a memory layer (ledger, instincts) but the estimate pipeline does not feed it yet | Borrow his design wholesale for Phase 2/3. |
| **Agent org** | 36 agents, trade-centric (how TI scope is bought) | 26 agents in 6 departments, discipline-centric (how drawing sets are read) | Both correct for their estimate class. His 14 trade agents share one schema — one parameterized agent with trade playbooks would be cheaper and more consistent. |
| **Evaluation** | Test plan covers permissions, workflows, AI schema validity, one business end-to-end test; **no accuracy measurement** | Ground-truth fixture; planned coverage × precision@25% harness, 3 runs | He needs an accuracy number before trusting ROMs on sales calls. |
| **Build risk** | Large product (10 modules, ~40 tables, 7 roles, mobile, email, jobs) built by an AI coding agent from docs; estimating AI arrives in sprint 6 of 9 | Phase 1 shipped in one session on an existing engine; no UI, no DB | His killer feature (same-day ROM) lands late; his docs discipline (CURRENT_TASK / NOT_NOW / QA agent) is the right way to run an AI coder. |
| **Stack / lock-in** | OpenAI Agents SDK, Supabase, Inngest | Python engine, claude-cli on Max, pdfplumber/pypdfium2, Obsidian | Both fine; his choice of OpenAI Agents SDK is a real commitment. |

---

## 3. What his plan gets right (and we should copy)

1. **The learning loop is designed correctly.** Approved-only memory, strategy-priced ROMs tagged so they never poison cost history, estimate actuals at closeout, versioned project-type playbooks, fine-tune last. This is exactly the discipline our memory layer needs when the estimate pipeline starts writing to it (Phase 2/3: `estimate_actuals`, `model_feedback_events`, playbooks).
2. **`pricing_basis` on every line** (historical | manual | allowance | sub_bid | online_check). Our lines carry `method` for the quantity and `source` for the price; adopting his enum for the price side is a one-field change.
3. **Low / target / high for ROM-class work.** Our engine is single-point, right for Class 2. When we add Class 5/4 from $/SF models (plan §10, Q6), his three-point structure is the format.
4. **Project-type playbooks as risk checklists.** Restaurant: hood/MUA/grease trap/gas load/RTU capacity/health department/Fire Marshal. Medical: accessibility/TDLR, equipment utilities. Ground-up: geotech, utilities, fire lane, long-lead steel. These become seeds for our risk register and the RFI generator per building type.
5. **Client-safe language + a Sensitive Info Filter** before anything leaves the company, and the source-of-truth hierarchy (signed contract > CO > proposal > RFI > schedule > log > note > AI). Our scope letter / Basis of Estimate path has no such filter.
6. **Role-based cost protection** thought through from day one. Not needed for one operator; mandatory the day a second person or a client touches the system.
7. **Docs-as-constitution for the AI coder** (`AGENTS.md`, `CURRENT_TASK.md`, `NOT_NOW.md`, Architect owns schema, QA agent attacks). This is close to our harness practice and worth mirroring in `docs/CLAUDE.md` for the new repo.
8. **Sub-bid leveling data model** (bid statuses, sub scores, inclusions/exclusions, plug numbers implied). Our Phase 2 leveling logic can adopt his statuses verbatim.

## 4. Where his plan is at risk (what we would tell him)

1. **LLM-generated prices.** Trade agents "create low/target/high budget ranges" and the Chief Estimator "recommends client price". With `pricing_basis: historical` the number should come from `historical_unit_prices` × quantity in code; with `allowance` it should be a stored allowance; only `manual` should be a human's number. Today nothing in the spec forces that. Consequence: two runs of the same restaurant ROM will disagree by tens of percent, and the historical agent can only warn after the fact. **Fix:** an assembly/$-per-SF table per project type + trade (his playbooks already have `pricing_benchmarks`), the agent picks the row and the quantity assumption, the app multiplies. Same JSON, deterministic dollars.
2. **No accuracy measurement.** The test plan checks schema validity and permissions, not whether the ROM is close. A ROM used on sales calls needs a measured band. **Fix:** 10 past projects with known outcomes as a golden set, score low/target/high against actuals before the feature ships; run each three times and report the spread.
3. **No hard gates before approval.** Scope gap, risk and chief estimator are all judgment agents; a wrong total with confident prose passes. **Fix:** deterministic checks before the human sees a number: every trade in the playbook covered or excluded with a reason; arithmetic ties; $/SF inside the project-type band; every high-severity risk has an exclusion or an RFI; every `allowance` line has an amount and a source.
4. **Estimate class never stated.** "ROM" is an accuracy claim only if the band is written down (AACE 56R-08 Class 5: −30/+50%). Add `aace_class` and `accuracy_band` to `estimates`; print them on every proposal.
5. **The takeoff stays manual.** His success metric is 10 minutes to a ROM draft, but final estimates still need quantities, and the plan only offers a manual viewer plus a review agent. The Plan Review Agent is asked to read "sheet list, missing sheets, plan conflicts" with no tooling — that is the part where raw VLMs fail (0.16–0.39 exact-match on door counts). See §6.
6. **Scope creep in the "MVP".** Ten modules, ~40 tables, 7 roles, mobile field app, email queue, background jobs, then AI. The estimating AI he says is the bottleneck is sprint 6 of 9. **Fix:** cut to the two killer workflows literally: CRM lead → estimate request → ROM (sprints 1, 2, 5, 6) and daily log → customer update (3, 4); defer subcontractor portal, client portal, reports, learning to v2. His own `NOT_NOW.md` shows he knows this; the sprint plan does not yet reflect it.
7. **Roster heavier than the work.** 36 agents. The 14 trade agents have identical schemas and skill cards that differ by a bullet list; one trade agent parameterized by a trade playbook is cheaper, easier to evaluate and easier to keep consistent. Likewise Weekly/Monthly Report agents are one agent with a period parameter.
8. **Internal inconsistencies to clean before Astra builds** (the kind his Sprint 0 asks Astra to find): the CRM Kanban has 10 columns but leads have 13 statuses (Needs Estimate vs Needs ROM Estimate; ROM Sent / Sub Bids Requested / Final Proposal Sent / Dead missing from the board); a Takeoff Review Agent, a Scope Agent and a Bid Leveling Agent are referenced in the spec/workflows/tests but have no card in `docs/agents/`; Stage 3 (ground-up/industrial) playbooks list site/civil, structural steel/PEMB and roofing trades that have no trade agent; `AGENTS.md` says AI does not control pricing while the trade agents generate prices (consistent only because a human approves — say so explicitly).
9. **Prompt-injection surface.** Client emails, sub quotes, plans and photos all flow into agents as context. Nothing in `08_SECURITY_RULES.md` treats document text as untrusted input. One line in `AGENTS.md` fixes the policy; a quarantine step fixes the code.
10. **Vendor commitment.** OpenAI Agents SDK first, LangGraph "later if complex" — fine, but structured-output schemas and `ai_runs` should be provider-neutral so the model can change.

---

## 5. Where our plan is at risk by comparison

1. **Single-operator only.** No roles, no client/sub surfaces, no email. Fine for Brian's use; not a product for a company like GrandVista without the shared-core work his plan describes.
2. **No learning loop yet.** The engine's memory layer exists but the estimate pipeline does not write actuals, corrections or playbooks. His design is the template.
3. **Single-point estimates.** Right for Class 2, wrong for the ROM conversation his sales team has every day. Add low/target/high for Class 5/4.
4. **No client-facing outputs.** Our Basis of Estimate is internal; a proposal/scope letter with a sensitive-info filter is missing.
5. **No CRM linkage.** A bid package arrives by folder, not by lead. If Brian ever wants the company spine, his docs are a good map.

---

## 6. A concrete integration (if the two of you want to collaborate)

Our `docs/core/estimating/` produces provider-neutral JSON: sheet register, schedules, room tags, door/window candidates with coordinates, spec index with Division 00/01 items, a takeoff ledger with provenance, priced lines, gate results. Every one of those maps onto a GrandVista agent input:

| GrandVista agent / screen | What our engine hands it |
|---|---|
| Plan Review Agent | `01-sheet-register.json` (sheets, disciplines, scales, revisions, scanned flags), cover-sheet index completeness, `02-spec-index.json` + Division 00/01 items, notes/keynotes per sheet |
| Takeoff screen (OpenTakeoff-style) | door/window/room candidates with PDF-point coordinates as pre-placed measurements the estimator confirms (Set-of-Mark), schedules as tables, wall LF and perimeter |
| Takeoff Review Agent | `04-takeoff-ledger.json` seed lines with method and confidence, cross-checks (schedule vs vector vs room tags) |
| Scope Gap / Risk agents | `05-questions.json` (unscaled sheets, missing schedules, divisions with no lines, discrepancies with cost exposure) |
| Chief Estimator Agent | `07-review-scorecard.json` — the ten hard gates as a floor under his judged review |

Delivery options: a CLI his Inngest job shells out to (`ce-os estimate intake/takeoff/rfi`), a small HTTP wrapper, or an MCP server (Phase 2 for us anyway). Licenses on our side are Apache/MIT/BSD only, so embedding is clean. What we would take back: his `estimate_actuals` / `model_feedback_events` / playbook tables as the schema for our learning loop, and his `pricing_basis` enum.

---

## 7. Bottom line for Brian

- **Different products, one shared module.** Do not merge the plans. Keep Construction-Estimate-OS as the estimating instrument; treat GrandVista OS as a company OS whose estimating module could run on our engine.
- **If your friend asks for one change, it is this:** take the dollar arithmetic out of the trade agents (assemblies and $/SF tables the agent selects, code multiplies), add deterministic gates and a measured accuracy band before any ROM reaches a client, and state the AACE class on every estimate.
- **If he asks for a second:** shrink the MVP to the two killer workflows and build the estimating core earlier; one parameterized trade agent instead of fourteen.
- **What we adopt from him now:** `pricing_basis` on priced lines, low/target/high for ROM classes, project-type risk checklists as RFI seeds, a sensitive-info filter on anything client-facing, and his learning-loop schema for Phase 2.
