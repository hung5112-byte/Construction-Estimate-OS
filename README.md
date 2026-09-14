# Construction-Estimate-OS

**An AI preconstruction department for commercial general contractors.** A bid package goes in; a traceable estimate comes out. Agents read the drawings and the Project Manual by discipline, take off quantities with sheet-level provenance, ask the questions a senior estimator asks the architect, price against *your* cost library, review the estimate the way a chief estimator does, and hand you a bid-ready report, workbook, Basis of Estimate and proposal draft.

It is **a pipeline with two human gates, not a debate**: the RFI gate pauses for your answers, and Stop 1 waits for your approval. No quantity reaches you without a sheet, no price without a source, no number without a gate.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-780_passing-brightgreen.svg)](#development)
[![LLM arithmetic](https://img.shields.io/badge/LLM_arithmetic-0-brightgreen.svg)](#design-rules)

> **Read this before trusting a dollar figure.** Every price in the shipped seed library is a national-average **placeholder marked `[UNCERTAIN]`**, the Brain describes a **fictional** DFW general contractor (Blackland Commercial Builders), and the only drawing set the system has been validated on is the **synthetic** sample package in this repository. Load your buyout history, replace the Brain, and run a real package before using an output for a bid.

## Contents

1. [What it does](#what-it-does)
2. [How it mirrors a real estimating department](#how-it-mirrors-a-real-estimating-department)
3. [Architecture](#architecture)
4. [Install](#install)
5. [Log the headless Claude CLI in](#log-the-headless-claude-cli-in)
6. [How to use](#how-to-use)
   - [A. Try it on the sample package](#a-try-it-on-the-sample-package)
   - [B. Estimate a real bid package, stage by stage](#b-estimate-a-real-bid-package-stage-by-stage)
   - [C. Inside Claude Code: `/estimate` and `/rom`](#c-inside-claude-code-estimate-and-rom)
   - [D. Same-day ROM without drawings](#d-same-day-rom-without-drawings)
   - [E. Your cost data, your Brain, your building types](#e-your-cost-data-your-brain-your-building-types)
   - [F. HTTP service and MCP tools](#f-http-service-and-mcp-tools)
   - [G. Accuracy evals](#g-accuracy-evals)
7. [Reading the outputs](#reading-the-outputs)
8. [Design rules](#design-rules)
9. [Repository layout](#repository-layout)
10. [Development](#development)
11. [Status, limitations and roadmap](#status-limitations-and-roadmap)
12. [Provenance and license](#provenance-and-license)

---

## What it does

Three ways to price, one rule: an agent may only *select* a library row or a playbook assembly; the engine multiplies, and a missing price is `[UNPRICED]`.

| Mode | Input | AACE class | Output |
|---|---|---|---|
| **Detailed** | A bid package: PDF drawing set + Project Manual | 3 / 2 | Takeoff ledger with provenance, RFI questions, priced estimate with general conditions and markups, review scorecard, report, workbook, Basis of Estimate, proposal draft |
| **ROM** | An intake form (project type, gross SF, city, a few facts, notes, photos) | 5 / 4 | Low / target / high from a project-type playbook, assumptions written down, questions with cost exposure, risk register, client-safe proposal draft |
| **Final** | The detailed estimate plus leveled subcontractor bids | 2 / 1 | Sub bids swapped in by trade (leveling logic is on the roadmap) |

What it is **not**: it does not run a multi-layer meeting debate, it does not let a language model do arithmetic, and it does not guess a price.

## How it mirrors a real estimating department

| Real role | Department | Agents |
|---|---|---|
| Bid coordinator, document control, precon manager | `01-bid-coordination` | bid-coordinator (manager) · document-controller · spec-analyst · rfi-coordinator · proposal-writer |
| Civil / structural estimators | `02-civil-structural` | civil-structural-lead (manager) · sitework · concrete · steel-masonry |
| Architectural estimators | `03-architectural` | architectural-lead (manager) · envelope · interiors · openings · specialties-equipment |
| MEP estimators | `04-mep` | mep-lead (manager) · hvac · plumbing-fire · electrical-lv |
| Cost engineer, GC estimator, risk | `05-cost-engineering` | pricing-lead (manager) · general-conditions · risk-markup · sub-bid-leveler · rom-trade-estimator (parameterized by trade) |
| Chief estimator's review | `06-estimate-review` (the standing skeptic) | chief-estimator (manager) · scope-gap-auditor · constructability-reviewer · benchmark-analyst |

The 27 agent prompts live in `01-Departments/<dept>/agents/*.md` (the source of truth) and are mirrored as Claude Code subagents in `.claude/agents/ce-*.md` by `docs/scripts/dev/sync_harness_agents.py`. Playbook knowledge (assemblies, quantity rules, risks per project type) lives in YAML, not in new agents.

## Architecture

Two layers joined by one contract:

- **The engine** (`docs/core/`), Python, deterministic wherever money or quantities are involved: PDF extraction, sheet register, schedules, vector geometry, rendering, spec index, takeoff ledger, cost engine, RFI, review gates, workbook and report writers, playbooks, evals. It exposes a CLI (`ce-os`), an HTTP service (contract v1 in `docs/contracts/`), and MCP tools.
- **The readers and reviewers**, language-model agents that read cards, rendered tiles, specs, notes and photos and return lines and questions in the contract's line schema. They run either as Claude Code subagents (`/estimate`, `/rom`) or headless through `claude -p` on a Claude subscription (`ce-os estimate read`, `run --vision`).

The pipeline, stage by stage:

```
ce-os estimate intake <package>    S0  copy the package · sheet register (scale, revision, discipline) · spec index and Division 01 · shadow cards · renders · project profile
ce-os estimate takeoff <folder>    S1  deterministic seed takeoff: schedules govern, vector geometry confirms, derived rules fill in
ce-os estimate read <folder>       S2  headless vision readers (three discipline leads via claude -p) confirm, correct and add — or /estimate in Claude Code
ce-os estimate rfi <folder>        S3  05-clarification.md      ⏸ PAUSE: you answer (or --auto-assume for an unattended run)
ce-os estimate resume <folder>         record the answers
ce-os estimate price <folder>      S4  your cost library first, seed second (marked) · general conditions by duration · markups per policy · benchmark
ce-os estimate review <folder>     S5  deterministic gates G1–G13 · verdict APPROVE / REVISE
ce-os estimate report <folder>     S6  08-estimate-report.md    ⏹ STOP 1: you approve
ce-os estimate approve <folder>        03-Outputs/<slug>/: estimate-workbook.xlsx · basis-of-estimate.docx · proposal-draft.docx
```

Every stage writes ordinary files into `02-Estimates/<slug>/`, so any stage can be re-run, inspected or driven from another tool.

## Install

Prerequisites:

- macOS or Linux, **Python 3.11+** (macOS ships 3.9, so name the interpreter, e.g. `python3.12`)
- For the agents: **Claude Code** and a Claude subscription. The headless readers use the `claude` CLI on a subscription (Max recommended; a 9-sheet set is about 4.5 minutes of reader time). No Anthropic API key is needed or used.
- Chrome, only if you want to regenerate the synthetic sample package.

```bash
git clone https://github.com/hung5112-byte/Construction-Estimate-OS.git
cd Construction-Estimate-OS
python3.12 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/ce-os --version
.venv/bin/python -m pytest docs/tests -q        # 780 passed on 2026-09-13; no network, no LLM
```

## Log the headless Claude CLI in

Skip this if you will only use the deterministic path or the agents inside Claude Code. The headless readers need a `claude` binary signed in to a **subscription** account; the engine bills nothing to an API key and scrubs `ANTHROPIC_API_KEY` from every child process.

```bash
npm install -g @anthropic-ai/claude-code          # or use an existing binary, e.g. <vault>/.tools/node_modules/.bin/claude
env | grep -c ANTHROPIC_API_KEY                   # want 0; `unset ANTHROPIC_API_KEY` otherwise
claude auth login --claudeai                      # NOT --console (that bills the API)
claude auth status                                # want "loggedIn": true with a claude.ai auth method
claude -p "Reply with the single word OK" --tools "" --output-format json
```

Then tell the engine where the binary is (add to `~/.zshrc` or export per shell):

```bash
export BD_OS_LLM_PROVIDER=claude-cli BD_OS_CLAUDE_BIN="$(command -v claude)" BD_OS_LLM_TIMEOUT_SECONDS=420
```

## How to use

### A. Try it on the sample package

The repository ships a synthetic 12,000 SF office/warehouse (9 ARCH-D vector sheets: G, A, S, M, P, E with real schedules, plus a 28-page Project Manual) and its ground truth.

```bash
.venv/bin/ce-os estimate run docs/tests/fixtures/sample-set-prairie-creek \
    --name "Prairie Creek Office/Warehouse Bldg 2" --type office-warehouse --city Plano --vault .
```

That is the unattended path: every open question is auto-assumed, stamped `AUTO-ASSUMED`, and listed on the report. It takes about 20 seconds and needs no LLM. Add `--vision` to insert the headless readers (needs the login above), or `--render` to produce the tiles without running them.

### B. Estimate a real bid package, stage by stage

Put the PDFs in one folder. Drawings and the Project Manual are recognised by their title blocks and content; a `package.json` is optional.

**1. Intake.** `--type` must match a benchmark row (see [E](#e-your-cost-data-your-brain-your-building-types)); `--class` is the AACE class you are bidding at; `--render` produces the overview and tile PNGs the readers open.

```bash
F=$(.venv/bin/ce-os estimate intake ./bid-package --name "Cedar Springs MOB" --type "medical office" --city Dallas --class 2 --render --vault . | grep -o '02-Estimates/[^ ]*')
```

Writes `00-project-profile`, `01-sheet-register` (every sheet with discipline, type, scale, revision, and a completeness check), `02-spec-index` and `02-division-01` (sections, separate contracts, allowances), `03-sheets.json` (schedules, room tags, dimension strings, door and window candidates), one shadow card per sheet in `cards/`, and `renders/`.

**2. Seed takeoff.** Deterministic: schedules are the count, vector geometry confirms door swings, windows, walls and the exterior perimeter, derived rules fill in what the set implies.

```bash
.venv/bin/ce-os estimate takeoff $F
```

Writes `04-takeoff-ledger` (`.json` and `.md`), `03-takeoff-seed.json` and `03-takeoff-checks.json` (schedule-vs-vector cross checks).

**3. Readers.** The three discipline leads read the cards and tiles, confirm or correct the seed lines, add what the deterministic pass missed, and write questions with cost exposure. Same contract whether headless or in Claude Code.

```bash
.venv/bin/ce-os estimate read $F --vault .                 # all three leads in parallel; --reader mep-lead for one; --dry-run for prompt sizes
```

Each reader writes `readers/<lead>.json`; the lines merge into the ledger with an identity-based reconcile (a door mark, an equipment tag, a room, an assembly), so a confirmation never doubles a quantity and a disagreement is logged to `04-discrepancies.json` for the RFI stage. Manual counts beat schedules, schedules beat what the plan shows, the plan beats derived rules.

**4. RFI gate.** Everything the package does not answer becomes a question with a citation, a severity and the cost exposure: unscaled sheets, schedule-vs-plan disagreements, divisions with sections but no takeoff, Division 00/01 items an estimator always confirms, and the readers' questions.

```bash
.venv/bin/ce-os estimate rfi $F        # writes 05-clarification.md and 05-questions.json, then pauses
```

Open `05-clarification.md`. For each question tick one box (`[x]`), or write in the **Answer** block:

```
## Q3 [CRITICAL]
_Cite: A-101 rev 2 (keynote 3) / A-201 rev 2_

1-hr CMU demising wall at grid B: does it terminate at the office roof deck or run to the warehouse deck?

- [x] Carry as a written assumption (state it on the bid form)
- [ ] Issue a pre-bid RFI to the architect
- [ ] Resolved — see my note

**Answer:**
```
Carry to the office deck (+14'-0"); add 1,000 SF as a stated assumption.
```
```

Then record the answers. `--auto-assume` instead stamps every open question `AUTO-ASSUMED` (gate G7 requires every CRITICAL question answered or carried as a written assumption).

```bash
.venv/bin/ce-os estimate resume $F
```

**5. Price.** Your CSVs in `03-Cost-Library/` win over the seed library; every line gets a basis, a low, a target and a high; general conditions come from duration and the profile; markups from `00-Brain/markup-policy.md` by class; the $/SF is checked against the building-type band.

```bash
.venv/bin/ce-os estimate price $F --vault .        # writes 06-estimate.json / .md
```

**6. Review.** Thirteen deterministic gates, zero LLM. A failed blocking gate is a `REVISE` whatever the narrative says.

```bash
.venv/bin/ce-os estimate review $F                 # writes 07-review-scorecard.json / .md
```

**7. Report, Stop 1, approve.**

```bash
.venv/bin/ce-os estimate report $F                 # 08-estimate-report.md, 09-proposal-draft.md, 09-client-safe-findings
.venv/bin/ce-os estimate approve $F --vault .      # 03-Outputs/<slug>/estimate-workbook.xlsx, basis-of-estimate.docx, proposal-draft.docx
```

### C. Inside Claude Code: `/estimate` and `/rom`

Open this repository in Claude Code. The commands in `.claude/commands/` run the same stages with the subagents in `.claude/agents/` and the workflows in `.claude/workflows/`:

```
/estimate ./bid-package --name "Cedar Springs MOB" --type "medical office" --city Dallas
/rom --type restaurant-ti --name "Pho 88" --sf 3200 --city Plano --field hood_lf=14 --package ./notes-and-photos
```

`/estimate` runs intake and the seed takeoff, then the `estimate-takeoff` workflow: one reader per discipline in parallel over its own sheets, the spec analyst over the manual, the RFI coordinator to de-duplicate and rank every question. `/rom` runs the deterministic ROM, then the `rom-trades` workflow: one ROM trade estimator per activated trade reads your notes and photos and corrects the assembly quantities, then the folder is re-priced. The `drawing-reading` skill in `.claude/skills/` holds the reading protocol every agent follows.

### D. Same-day ROM without drawings

```bash
.venv/bin/ce-os estimate rom --type restaurant-ti --name "Pho 88" --sf 3200 --city Plano \
    --field hood_lf=14 --field fixture_count=9 --exclude fire-sprinkler --allowance signage=8000 \
    --notes "second-generation space, existing grease trap stays" --vault .
```

Playbooks: `restaurant-ti`, `salon-beauty`, `medical-dental`, `retail-ti`, `office-buildout`, `white-box`, `ground-up-retail`, `industrial-warehouse` (aliases such as "restaurant remodel" or "warehouse" resolve). Each playbook carries assemblies with low / target / high per unit, quantity rules, typical trades, common RFIs, exclusions, a risk checklist with mitigations and a benchmark band. Every default the playbook used is written down as an assumption and asked as a question; `--plans` makes it a Class 4 instead of 5; `--intake form.json` replaces the options. The result is the same folder layout as a detailed estimate, so `review`, `report` and `approve` work on it.

### E. Your cost data, your Brain, your building types

**Cost library.** Drop CSVs into `03-Cost-Library/` (git-ignored, so your buyout data never leaves the machine) with the columns

```
item_code, description, unit, labor, material, equipment, sub, source, quote_date, valid_until, location, notes
```

plus optional `unit_low`, `unit_high` and `pricing_basis` (`historical`, `assembly`, `manual`, `allowance`, `sub_bid`, `online_check`). Rows there win over `docs/core/tools/data/estimating/unit_costs_seed.csv`, whose 101 rows define the `NN-slug` vocabulary (MasterFormat division first) the seed takeoff uses. Without unit ranges the detailed path's low and high equal the target.

**Brain.** `00-Brain/` is the company: `markup-policy.md` (contingency by class, escalation, insurance, bond, sales-tax basis, fee), `benchmarks.md` ($/SF bands by building type, GC and labor shares, sources), `laws.md` (Texas retainage, bonds, sales tax, Davis-Bacon, codes), `bid-policy.md`, `cost-library.md`, `products.md`, `state.md`, `glossary.md`. Replace the fictional contractor with yours; the engine reads these files under strict headings.

**Building types** for `--type` come from `docs/core/tools/data/estimating/benchmarks_dfw_2026.csv` (or your `00-Brain/benchmarks.md`): `office-warehouse`, `tilt-wall industrial`, `warehouse shell`, `office low-rise`, `office prime`, `retail strip`, `retail restaurant`, `medical office`, `hotel 3-star`, `k-12 school`, `tenant improvement office`, `restaurant ti`, `salon ti`, `medical office ti`, `retail ti`, `white box`. Location factors are in `location_factors.csv`, waste factors in `waste_factors.csv`.

### F. HTTP service and MCP tools

The **Estimate Service** exposes the pipeline over HTTP for another UI (contract v1: `docs/contracts/estimate-service.v1.md` and ten JSON schemas in `docs/contracts/schemas/`). It binds to loopback by default; set `CE_SERVICE_TOKEN` to require an `X-Api-Key` header.

```bash
.venv/bin/ce-os estimate serve --port 8801 --vault .
```

| Route | Purpose |
|---|---|
| `GET /health` | liveness: engine and contract version, available playbooks |
| `POST /estimates/intake` · `POST /estimates/rom` | create an estimate folder from a package or an intake form |
| `POST /estimates/{id}/takeoff` · `rfi` · `answers` · `price` · `review` · `report` · `approve` | run one stage; `answers` takes the question answers as JSON |
| `GET /estimates/{id}/files/{name}` | fetch any file from the folder |

The **MCP server** registers the estimating tools (`bd_estimate_rom`, `bd_estimate_intake`, `bd_estimate_stage`, `bd_estimate_run`, `bd_estimate_status`) next to the fleet engine's tools in Claude Desktop or Claude Code:

```bash
.venv/bin/ce-os install-mcp --target both       # or desktop | claude-code; restart the host afterwards
```

### G. Accuracy evals

```bash
.venv/bin/ce-os estimate eval --set docs/tests/fixtures/sample-set-prairie-creek --runs 3 --tol 0.25 --vault .
```

Detailed sets score coverage × precision@tol against `ground_truth.json` (`expected_lines` of `item_code`, `qty`, `unit`); the composite is `coverage^0.4 × precision^0.6`. ROM sets are folders of `<case>/intake.json` + `actual.json` (`{"actual_total": N}`) from past projects and score the band hit-rate. Reports land in `03-Outputs/evals/`.

## Reading the outputs

**`08-estimate-report.md`** opens with the TL;DR (total, $/SF against the band, class and expected accuracy, verdict, open CRITICAL questions, unpriced and placeholder counts), then the estimate summary by division, the three-point totals, the benchmark position with sources, the gates, the questions and assumptions, exclusions, and where every number came from.

**`07-review-scorecard`** lists the gates. Blocking gates fail the estimate:

| Gate | Checks |
|---|---|
| G1 | Every measured sheet is claimed by the takeoff |
| G2 | Every quantity carries sheet and method provenance |
| G3 / G3b | Every technical spec division, or playbook trade, has takeoff lines or a cited exclusion |
| G4 | Arithmetic ties from lines to summary |
| G5 | Units are valid for their division |
| G6 | $/SF inside the building-type benchmark band |
| G7 | Every CRITICAL question is answered or carried as a written assumption |
| G8 | Measured quantities come only from sheets with a parsed scale |
| G9 | Lines below the confidence floor are listed for verification |
| G10 | Unpriced lines stay below the materiality threshold |
| G11 | Every allowance has an amount and a source |
| G12 | Every high-severity risk has an exclusion, an RFI or an allowance |
| G13 | Client-facing text has no internal cost, blame, legal admission or raw language |

A `REVISE` on G10 after a reader run usually means the readers found scope the cost library cannot price. Add rows; do not loosen the gate.

**`estimate-workbook.xlsx`** has the sheets Summary, Priced lines (basis, low, target, high per line), Takeoff ledger, General conditions, Review gates, RFI log, Sheet register, Risk register and Sources. **`basis-of-estimate.docx`** is the narrative a reviewer or a surety expects. **`proposal-draft.docx`** is client-facing and has passed the client-safe scan (`09-client-safe-findings` lists anything that had to be rewritten: internal costs, blame, legal admissions, promises, frustration).

## Design rules

1. **Schedule-first, vector-first, pixels last.** Frontier vision models score 0.16–0.39 exact-match on door counts from plan images but read text and schedules well; vector geometry on CAD PDFs is exact. Schedules are the count, vector candidates confirm, the vision reader confirms and catches what vector missed. It never counts from scratch.
2. **No LLM arithmetic.** `docs/core/estimating/` prices, rolls up and gates with pure functions and unit tests. Agents select rows and assemblies and explain; they never compute.
3. **Provenance is machine-checked.** `sheet · revision · method · confidence` on every quantity, a library row and date on every price, `[UNPRICED]` instead of a guess.
4. **Two human gates.** The RFI gate and Stop 1. Auto-assumed answers are stamped and listed.
5. **Drawing, spec, note and photo text is untrusted input.** It is data for the readers, never instructions.
6. **All LLM runs bill a subscription, never an API key.** The `claude-cli` provider scrubs API keys from child processes; nothing in this repository needs `ANTHROPIC_API_KEY`.
7. **Permissive licenses only.** pdfplumber and pdfminer.six (MIT), pypdfium2 (Apache/BSD), ezdxf (MIT), openpyxl, python-docx. No PyMuPDF (AGPL), no YOLO (AGPL), no CC-BY-NC datasets.

## Repository layout

```
00-Brain/                       the company: strategy, markup policy, benchmarks, laws, bid policy, state, glossary
01-Departments/<dept>/          department.yaml, index.md, agents/*.md — the source of truth for every prompt
02-Estimates/<slug>/            one folder per estimate (ignored by git)
03-Cost-Library/                your unit-cost CSVs (create it; wins over the seed library; ignored by git so buyout data stays local)
03-Outputs/<slug>/              workbook, Basis of Estimate, proposal draft, eval reports (ignored by git)
.claude/agents|commands|workflows|skills   Claude Code harness: 27 subagents, /estimate and /rom, two workflows, the drawing-reading skill
docs/core/estimating/           the estimating engine (pdfio, sheet_register, sheet_text, sheet_tables, sheet_geometry, sheet_render,
                                spec_index, takeoff_ledger, cost_engine, playbooks, rfi, review_gates, client_safe, proposal, workbook,
                                report, pipeline, headless_readers, service, evals)
docs/core/                      the fleet engine underneath (Brain reader, clarifier, critic, memory, retrieval, ingest, MCP server, CLI)
docs/core/tools/estimating_tools.py        eight BaseTool wrappers the tool router can call
docs/core/tools/data/estimating/           unit_costs_seed.csv, waste_factors.csv, benchmarks_dfw_2026.csv, location_factors.csv, playbooks/*.yaml
docs/contracts/                 estimate-service.v1.md and the JSON schemas
docs/departments/               pack copies of the six departments
docs/templates-us/              16 estimating templates plus the generic library
docs/tests/                     unit, integration and e2e suites; fixtures/sample-set-prairie-creek (the synthetic package + ground truth)
docs/scripts/dev/               sync_harness_agents.py, scaffold_departments.py, scaffold_playbooks.py, check-domain-neutral.sh
scripts/make_sample_set.py      regenerates the synthetic package (needs Chrome)
```

## Development

```bash
.venv/bin/python -m pytest docs/tests -q                                   # full suite, no network, no LLM
.venv/bin/ruff check docs/core docs/tests scripts                           # lint (CI runs the same)
cd docs && bash scripts/dev/check-domain-neutral.sh && cd ..               # the engine must stay domain-neutral; run it from docs/
.venv/bin/python docs/scripts/dev/sync_harness_agents.py                    # regenerate .claude/agents/ after editing 01-Departments/
```

Adding an agent: write `01-Departments/<dept>/agents/<id>.md` with the frontmatter the others use, list it in that department's `department.yaml`, copy it to `docs/departments/` without the `## Links` section, then run the sync script. Adding a project type: a new YAML in `docs/core/tools/data/estimating/playbooks/` (see `scaffold_playbooks.py`). Reader agents get a fake `claude` binary in tests (`docs/tests/unit/test_estimating_headless_readers.py`), so the suite never calls a model.

Measured on 2026-09-13 with the synthetic package:

| Check | Result |
|---|---|
| Seed takeoff vs ground truth (40 expected lines) | composite 1.000 |
| Headless readers, 9 sheets, 58 renders | 3 leads in parallel, 4.5 min wall, 83 lines, 24 questions |
| Merged ledger vs ground truth | composite 1.000, 0 discrepancies, 65 seed lines confirmed, 8 item codes added |
| Full chain | 29 questions (3 CRITICAL), $/SF inside the band, verdict APPROVE |

## Status, limitations and roadmap

**Proven:** the deterministic path end to end, the headless readers on a subscription, the merge and RFI plumbing, the ROM path with eight playbooks, the service contract, the MCP tools, the eval harness, 780 tests.

**Not yet:** validation on a real drawing set (real title blocks, schedules that are not neat grids, door blocks instead of arcs, scanned addenda); real prices (the seed is placeholders and has no unit ranges, so the detailed path's spread is zero until your library carries `unit_low`/`unit_high`); sub-bid leveling logic (the agent exists, the engine step does not); the learning loop that feeds awarded and lost bids back into the library; rotated dimension strings and hatch-based areas.

**Next:** run one real package; load buyout history; score the ROM playbooks against ten past projects; then the learning-loop endpoints, sub-bid leveling and whatever the real set demands. Kreo / Bluebeam / Autodesk Takeoff / IFC integrations and an in-house detector on your own labelled sheets come after that.

## Provenance and license

Built in September 2026 on the fleet engine (the Hardware Division OS / bd-business-os codebase) by Brian H. Doan. Estimating practice follows ASPE, AACE 56R-08 and CSI MasterFormat; the drawing-reading approach follows AECV-Bench, TakeoffBench-v1, Set-of-Mark prompting and the vector symbol-spotting literature. The sample package, the Brain and every price are synthetic.

Licensed under the Apache License 2.0; see `LICENSE` and `NOTICE`.
