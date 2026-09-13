# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

**Construction-Estimate-OS** — an AI preconstruction / estimating department for a commercial general contractor, built on the fleet engine. A bid package (drawings + Project Manual) goes in; agents read the sheets by discipline, take off quantities with sheet-level provenance, ask the Chief Estimator the questions a real estimator asks the architect, price against the cost library, review the estimate through deterministic gates plus a judged review, and hand over a bid-ready report, workbook and Basis of Estimate.

**It is a pipeline with two human gates, not the three-round debate.** The debate graph (`docs/core/meeting/`) is still in the engine and off by default (`.bd-os.yaml` → `estimate.bid_review_debate`). Production LLM calls bill the Claude Max subscription via the `claude-cli` provider; the deterministic pipeline (`ce-os estimate …`) needs no model at all.

> Terminology: the human principal is the **Chief Estimator / Director of Preconstruction** (Brian H. Doan in this deployment). Core code still calls the approver the "Department Head". MCP tools keep the fleet `bd_*` names; the package is `construction-estimate-os`, the CLI `ce-os`.

> General information only — Texas retainage/bond/tax statements and every seed price are planning placeholders, not legal, tax or pricing advice.

## Commands

```bash
# Install (dev)
python -m venv .venv && .venv/Scripts/activate  # Windows
pip install -e ".[dev]"

# The estimating pipeline (no LLM needed)
ce-os estimate run docs/tests/fixtures/sample-set-prairie-creek --name "Prairie Creek" --type office-warehouse --city Plano --vault .
ce-os estimate intake|takeoff|rfi|resume|price|review|report|approve <folder>   # stage by stage

# Install the MCP server into Claude Desktop
ce-os install-mcp
ce-os install-mcp --vault "/path/to/vault"

# Run tests
python -m pytest docs/tests/ -q                        # all (750+ tests)
python -m pytest docs/tests/unit/test_router.py -q     # single file
python -m pytest docs/tests/unit/ -q                   # unit only
python -m pytest docs/tests/integration/ -q            # integration only

# Lint / format
ruff check docs/core/ docs/tests/
ruff format docs/core/ docs/tests/

# CLI (development)
ce-os status --vault <path>
ce-os run "brief" --vault <path>

# Memory layer (ADR-004 Addendum A)
ce-os index --vault <path> [--rebuild] [--no-embed]   # build/refresh the hybrid search index
ce-os search "query" --vault <path>                    # hybrid BM25+vector+graph search
ce-os doctor --vault <path>                            # label coverage + index/vector freshness
ce-os outcome <task-folder> --quality 0.8 --outcome "..."  # resolve a decision-ledger entry
```

## Architecture

### The estimating pipeline (primary)

```
intake → takeoff (seed) → [reader agents] → rfi ⏸ → resume → price → review → report ⏹ → approve
```

`docs/core/estimating/pipeline.py` owns the stages and the files in `02-Estimates/<slug>/`; `rfi.py` writes the clarification file in the engine's checkbox format; `review_gates.py` is the deterministic floor (G1–G10); `cost_engine.py` never guesses a price; `workbook.py`/`report.py` render the outputs. The harness path is `/estimate` (`.claude/commands/estimate.md`) → `.claude/workflows/estimate-takeoff.js` → `.claude/agents/ce-*.md` (generated from `01-Departments/` by `docs/scripts/dev/sync_harness_agents.py`). Fixture + ground truth: `docs/tests/fixtures/sample-set-prairie-creek/` (regenerate with `scripts/make_sample_set.py`, needs Chrome).

**ROM mode** (`pipeline.rom`, `ce-os estimate rom`): intake form × project-type playbook (`docs/core/tools/data/estimating/playbooks/*.yaml`, loader `playbooks.py`) → assemblies × quantity rules → three-point estimate with class/band, risk register, questions (defaults carried as assumptions), gates incl. G3b/G11/G12/G13, report, client-safe proposal (`proposal.py`, `client_safe.py`). **Contract v1**: `docs/contracts/` (schemas validated by `test_estimating_contract.py`); HTTP service `service.py` (`ce-os estimate serve`); MCP tools `bd_estimate_*` in `mcp_server.py`; accuracy harness `evals.py` (`ce-os estimate eval`). Playbooks are the place to add trade knowledge — not new agents.

### 5-Stage Flow (engine tasks — drafts, briefs, optional debates)

```
bd_run → PAUSE_CLARIFICATION → bd_resume → bd_meeting
       → PAUSE_DECISION_REPORT → bd_approve → bd_execute → DONE
```

`FlowController` (`docs/core/orchestrator/flow_controller.py`) coordinates everything. Two mandatory stops require Department Head approval before continuing.

### Core modules

| Module | Role |
|--------|------|
| `docs/core/brain/` | Read the vault `00-Brain/` → `BrainContext`; `ledger.py` = episodic decision ledger (append at Stop-2, resolve via `bd-os outcome`/`bd_outcome`) |
| `docs/core/retrieval/` | Per-vault hybrid index (`<vault>/.cache/index.db`, rebuildable): FTS5 BM25 + sqlite-vec/fastembed vectors + wikilink-graph PPR, RRF-fused; `vault_search` tool + `bd-os index/search/doctor` |
| `docs/core/clarifier/` | Detect gaps in the Brain → generate questions with citations, write `03-clarification.md` |
| `docs/core/orchestrator/` | Router classifies the task, FlowController, research phase, execution planner |
| `docs/core/meeting/` | LangGraph debate graph — Pro/Con Advocate rounds → Perspective Debators → Synthesizer |
| `docs/core/agents/` | Agent loader + registry, base agent, pack loader |
| `docs/core/translator/` | Jargon detector → simplifier → TL;DR (3 modes: off/final_only/all_intermediate) |
| `docs/core/tools/` | `us_law_search`, `competitor_research`, `tax_calculator`, `web_search`, etc. Cache 24h. |
| `docs/core/obsidian/` | Vault read/write, wikilinks, template resolver (BYOT 3-level priority) |
| `docs/core/llm/providers.py` | `MCPSamplingProvider` (Claude Desktop), `ClaudeProvider` (direct Anthropic API) |

### LLM routing

Priority (`docs/core/mcp_server.py:_pick_llm`): env `BD_OS_LLM_PROVIDER` ∈ {claude-cli, anthropic-api, mcp-sampling} overrides everything (production sets `claude-cli` — subscription-billed, keys scrubbed from the subprocess env); unset → `ANTHROPIC_API_KEY` → MCP sampling. API keys are read from `<vault>/.env`; behavior config (translator_mode, meeting rounds, critic knobs) from `<vault>/.bd-os.yaml` (fallback `~/.bd-os.yaml`).

### Departments + Packs (estimating org)

- `docs/departments/` — 6 manager-led departments (26 agents): `01-bid-coordination` (bid-coordinator ⭐ + document-controller, spec-analyst, rfi-coordinator, proposal-writer), `02-civil-structural` (civil-structural-lead ⭐ + sitework, concrete, steel-masonry), `03-architectural` (architectural-lead ⭐ + envelope, interiors, openings, specialties-equipment), `04-mep` (mep-lead ⭐ + hvac, plumbing-fire, electrical-lv), `05-cost-engineering` (pricing-lead ⭐ + general-conditions, risk-markup, sub-bid-leveler), `06-estimate-review` (chief-estimator ⭐ + scope-gap-auditor, constructability-reviewer, benchmark-analyst; `debate_role: con`).
- The vault copies in `01-Departments/` are the source of truth (they carry the `## Links` block); the pack copies in `docs/departments/` have no `## Links` (onboarding appends it). `docs/scripts/dev/scaffold_departments.py` produced the first draft — edit the `.md` files directly now.
- `docs/templates-us/` — 16 estimating templates in the six dept folders + 9 `_orchestrator` + 155 generic `_shared` templates (BYOT source material).

### Vault structure (runtime)

```
<vault>/
├── 00-Brain/          strategy.md, products.md, budget.md, headcount.md, state.md
├── 00-Templates-Custom/   Department Head custom templates (highest priority — BYOT)
├── 02-Estimates/<slug>/  00-project-profile … 08-estimate-report (the pipeline files)
├── 02-Tasks/<slug>/   engine tasks (brief, clarification, decision report, execution plan)
├── 03-Cost-Library/   your unit costs and quotes (CSV) — highest pricing priority
├── 03-Outputs/        .docx, .xlsx rendered
└── .bd-os.yaml          vault config (packs, translator_mode, meeting rounds)
```

## 6 RULES (must not be violated)

1. **Brain-first** — Read the Brain before asking the Department Head. Questions must cite `file:section`. If the Brain is sufficient, don't ask.
2. **Domain-neutral** — Don't let TradingAgents jargon leak (trade/market/Bull/Bear/ticker). CI check: `docs/scripts/dev/check-domain-neutral.sh`.
3. **Single source of truth** — The Obsidian vault is canonical. SQLite is only a crash-recovery cache.
4. **Department-Head-friendly** — Output in plain English, with a TL;DR, define a term on first use, avoid heavy technical jargon.
5. **Live research + citations** — Tools must return `ToolResult.sources: list[str]` + `retrieved_at`. Cache 24h.
6. **BYOT** — Template priority: `vault/00-Templates-Custom/` > pack refs > `repo/docs/templates-us/`.

## Key patterns

**Adding an estimating rule** — seed-takeoff heuristics live in `docs/core/estimating/pipeline.py::seed_takeoff`; item codes must exist in `docs/core/tools/data/estimating/unit_costs_seed.csv` or they price as `[UNPRICED]` (honest, never silent).

**Adding a new tool** — Inherit from `docs/core/tools/base_tool.py`, return a `ToolResult` with `sources` + `retrieved_at`. Register it in `docs/core/tools/tool_router.py` (`_FULL_TOOL_DESCRIPTIONS`) and wire it in `docs/core/orchestrator/research_phase.py`.

**Adding a department** — Create a folder `docs/departments/XX-name/` with a `department.yaml`. Agents auto-load via `AgentLoader`.

**Adding a pack** — Create a folder `docs/packs/<name>/` with a `pack.yaml` + override templates. Department Head enables it via `.bd-os.yaml`.

**Template resolver** — `docs/core/obsidian/template_resolver.py` checks 3 paths in the correct BYOT order.

**Tests** — Unit tests mock the LLM (no real API call). Integration tests use `docs/tests/fixtures/`. E2E tests in `docs/tests/e2e/` skip if there is no `TAVILY_API_KEY`.
