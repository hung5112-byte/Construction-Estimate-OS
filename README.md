# Construction-Estimate-OS — an AI preconstruction department for commercial GCs

> **A bid package goes in; a traceable estimate comes out.** Agents read the drawings and the Project Manual by discipline, take off quantities with sheet-level provenance, ask the questions a senior estimator asks the architect, price against *your* cost library, review the estimate the way a chief estimator does, and hand you a bid-ready report, workbook and Basis of Estimate.
> **It is a pipeline with two human gates — not a debate.** The RFI gate pauses for your answers; Stop 1 waits for your approval. No number reaches you unscored, no quantity without a sheet, no price without a source.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-750+-brightgreen.svg)](#tests)
[![LLM arithmetic](https://img.shields.io/badge/LLM_arithmetic-0-brightgreen.svg)](#design-rules)

> ⚠️ Every price in the shipped seed library is a national-average **placeholder marked [UNCERTAIN]**. Load your buyout history into `03-Cost-Library/` before trusting a dollar figure. The Brain ships with a **fictional** DFW general contractor (Blackland Commercial Builders) — replace it with yours.

---

## Who it is for

A **commercial general contractor's preconstruction team** — 2–4 estimators who bid ground-up office, tilt-wall industrial, retail/restaurant, medical office, K-12 and tenant improvements — and the Chief Estimator who signs the bid.

| You face | Before | With Construction-Estimate-OS |
|---|---|---|
| A 60-sheet set lands Monday, bid Friday | Estimators split the sheets, read specs if there is time | `ce-os estimate intake` logs every sheet with scale and revision, indexes the manual, and hands each discipline its cards and tiles |
| Doors counted from the plan, schedule says otherwise | Found at buyout as a change order | The schedule is the count; the vector pass and the vision reader confirm it; disagreements become questions before the bid |
| "Where did this number come from?" | Someone's spreadsheet | Every ledger line: sheet · revision · method · confidence. Every price: the library row and its date |
| Bid-day review at 4 pm | A checklist nobody has time for | Ten deterministic gates run in seconds; the Chief Estimator agent judges what the gates cannot |
| Site work by separate contract, half the team prices it anyway | Scope gap | Division 00/01 is read first; cited exclusions are on the report and the gates honour them |

---

## How a real estimating department works, and how this one mirrors it

| Real role | Department here | Agents |
|---|---|---|
| Bid coordinator, document control, precon manager | `01-bid-coordination` 📂 | bid-coordinator ⭐ · document-controller · spec-analyst · rfi-coordinator · proposal-writer |
| Civil / structural estimators | `02-civil-structural` 🏗️ | civil-structural-lead ⭐ · sitework · concrete · steel-masonry |
| Architectural estimators | `03-architectural` 🏢 | architectural-lead ⭐ · envelope · interiors · openings · specialties-equipment |
| MEP estimators | `04-mep` ⚡ | mep-lead ⭐ · hvac · plumbing-fire · electrical-lv |
| Cost engineer, GC estimator, risk | `05-cost-engineering` 💵 | pricing-lead ⭐ · general-conditions · risk-markup · sub-bid-leveler |
| Chief estimator's review + ops | `06-estimate-review` 🔍 (standing skeptic) | chief-estimator ⭐ · scope-gap-auditor · constructability-reviewer · benchmark-analyst |

26 agents in `01-Departments/` (the source of truth for every prompt), mirrored as Claude Code subagents in `.claude/agents/`.

---

## The pipeline

```
ce-os estimate intake <package>   S0  sheet register · spec index · shadow cards · tiles · project profile
ce-os estimate takeoff <folder>   S1  deterministic seed takeoff (schedules + vector geometry + derived lines)
        /estimate (Claude Code)   S1' discipline reader agents in parallel confirm, correct, add — with tiles
ce-os estimate rfi <folder>       S3  05-clarification.md   ⏸ PAUSE — you answer (or --auto-assume for an unattended run)
ce-os estimate resume <folder>
ce-os estimate price <folder>     S4  cost library (yours first, seed second) · GCs by duration · markups per policy · benchmark
ce-os estimate review <folder>    S5  hard gates G1–G10 (+ the chief-estimator agent's judged review)
ce-os estimate report <folder>    S6  08-estimate-report.md   ⏹ STOP 1 — you approve
ce-os estimate approve <folder>       03-Outputs/: estimate-workbook.xlsx · basis-of-estimate.docx
```

**Hard gates (deterministic, zero LLM):** every measured sheet claimed · provenance on every line · every spec division covered or excluded with a citation · arithmetic ties · units valid · $/SF inside the building-type band · every CRITICAL question answered or carried as a written assumption · scale gate · confidence floor · unpriced lines under the threshold. A failed blocking gate is a `REVISE`, whatever the narrative says.

---

## Quick start

```bash
git clone <this repo> && cd Construction-Estimate-OS
python3.12 -m venv .venv && .venv/bin/pip install -e ".[dev]"

# unattended run on the synthetic sample package (9 vector sheets + a 28-page Project Manual)
.venv/bin/ce-os estimate run docs/tests/fixtures/sample-set-prairie-creek \
    --name "Prairie Creek Office/Warehouse Bldg 2" --type office-warehouse --city Plano --vault .
```

That produces `02-Estimates/<slug>/` with the register, spec index, ledger, questions, estimate, scorecard and report, and `03-Outputs/<slug>/` with the workbook and the Basis of Estimate. With the agents, run `/estimate <package-dir>` inside Claude Code in this repo instead (see `.claude/commands/estimate.md`).

Regenerate the sample package (needs Chrome): `.venv/bin/python scripts/make_sample_set.py`.

---

## Design rules

1. **Vector-first, schedule-first.** Frontier vision models score 0.16–0.39 exact-match on door counts from plan images; vector geometry on CAD PDFs is exact and schedules are authoritative. The vision reader confirms and catches what vector missed; it does not count from scratch.
2. **No LLM arithmetic.** `docs/core/estimating/` prices, rolls up and gates with pure functions and unit tests. Agents choose library rows and explain; they never compute.
3. **Provenance is machine-checked.** `sheet · revision · method · confidence` on every quantity, a library row on every price, `[UNPRICED]` instead of a guess.
4. **Two human gates.** The RFI gate and Stop 1. Auto-assumed answers are stamped `AUTO-ASSUMED` and listed on the report.
5. **Drawing text is untrusted input.** It is data for the readers, never instructions.
6. **Permissive licenses only.** pdfplumber/pdfminer.six (MIT), pypdfium2 (Apache/BSD), ezdxf (MIT), openpyxl, python-docx. No PyMuPDF (AGPL), no YOLO (AGPL), no CC-BY-NC datasets.

---

## What ships

- **Engine** — the fleet engine (`docs/core/`: Brain, clarifier, critic, memory, retrieval, ingest, handoff, signals, MCP server) plus `docs/core/estimating/` (register, text, tables, geometry, render, spec index, ledger, cost engine, RFI, gates, workbook, report, pipeline) and 8 tool wrappers (`sheet_register`, `sheet_geometry`, `sheet_text`, `sheet_tables`, `spec_index`, `cost_engine`, `benchmark_check`, `review_gates`).
- **Brain** — `00-Brain/`: strategy, services, budget, headcount, laws (Texas retainage/bonds/sales tax, Davis-Bacon, codes), state, glossary, **markup-policy**, **benchmarks** (RLB Q2 2026 Dallas, Turner BCI), **bid-policy**, **cost-library** policy.
- **Fixture** — `docs/tests/fixtures/sample-set-prairie-creek/`: a 12,000 SF office/warehouse, 9 ARCH-D vector sheets (G/A/S/M/P/E with real schedules) + Project Manual, with `ground_truth.json`. The seed takeoff matches it: 12 doors, 10 windows, 440 LF perimeter, 12,000 SF, 16.66 tons of steel, 82 sprinkler heads.
- **Harness** — `/estimate` command, `estimate-takeoff` workflow (readers in parallel → spec analyst → RFI coordinator), `drawing-reading` skill, 26 subagents.
- **Templates** — 16 estimating templates (bid/no-bid scorecard, sheet register, RFI log, scope letter, Basis of Estimate, takeoff sheets, estimate summary, GC worksheet, leveling matrix, risk register, bid-day checklist, turnover package) + the generic library.

## Tests

```bash
.venv/bin/python -m pytest docs/tests -q      # engine suite + estimating extractors, ledger/cost engine, pipeline end-to-end
ruff check docs/core/ docs/tests/
```

## Status and roadmap

Phase 1 (this build): walking skeleton above, unattended path proven on the synthetic package, agent path wired in the harness. Phase 2: headless vision provider for `claude -p` runs, MCP tools `bd_estimate_*`, sub-bid leveling, cost-library import, a real DFW package and an accuracy eval (coverage × precision@25%, 3 runs). Phase 3: Kreo / Bluebeam MCP / Autodesk Takeoff / IfcOpenShell integrations, DXF takeoff, an in-house detector on your own labelled sheets. The plan and the research behind it live in the Brian1 vault under `04-Projects/Construction-Estimate-OS/`.

## Provenance

Built 2026-09-12 from the fleet engine (hardware-division-os bundle root `fc1bc64` + the Brian1 vault engine). Estimating practice from ASPE / AACE 56R-08 / CSI MasterFormat and published GC guidance; drawing-reading approach from AECV-Bench, TakeoffBench-v1 (Handoff-H1), DeepEyes/Set-of-Mark and the vector symbol-spotting literature — all cited in the research notes. Author: Brian H. Doan. License: Apache-2.0.
