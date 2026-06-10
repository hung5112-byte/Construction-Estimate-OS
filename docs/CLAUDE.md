# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

AI Operating System for a hardware engineering & supply chain division of a Texas electronics company, run by the VP (the human principal). The VP chats → 5 manager-led departments of AI agents debate (teams give short takes, the manager synthesizes, managers debate across departments) → reach a decision → generate `.docx/.xlsx` aligned with US federal + Texas law. Runs through MCP sampling in Claude Desktop — no separate Anthropic API key needed.

> General information only — the legal/tax content is not legal or tax advice. Confirm with a licensed Texas attorney and CPA.

> Terminology: core code and prompts call the human principal the "Department Head" — the role that approves Stop 1/Stop 2. Each deployment maps it to a real person; in this one that's **Brian H. Doan, VP of Hardware Development, Quality & Supply Chain** (the repo's author), and his vault documents say "Brian". Legacy `vn_*` tool names and the `vn-one-person-company` package name are kept for API stability.

## Commands

```bash
# Install (dev)
python -m venv .venv && .venv/Scripts/activate  # Windows
pip install -e ".[dev]"

# Install the MCP server into Claude Desktop
vn-os install-mcp
vn-os install-mcp --vault "F:/work/xyz-vault"   # inject vault path

# Run tests
python -m pytest docs/tests/ -q                        # all (277 tests)
python -m pytest docs/tests/unit/test_router.py -q     # single file
python -m pytest docs/tests/unit/ -q                   # unit only
python -m pytest docs/tests/integration/ -q            # integration only

# Lint / format
ruff check docs/core/ docs/tests/
ruff format docs/core/ docs/tests/

# CLI (development)
vn-os status --vault <path>
vn-os run "brief" --vault <path>
```

## Architecture

### 5-Stage Flow

```
vn_run → PAUSE_CLARIFICATION → vn_resume → vn_meeting
       → PAUSE_DECISION_REPORT → vn_approve → vn_execute → DONE
```

`FlowController` (`docs/core/orchestrator/flow_controller.py`) coordinates everything. Two mandatory stops require Department Head approval before continuing.

### Core modules

| Module | Role |
|--------|------|
| `docs/core/brain/` | Read the vault `00-Brain/` → `BrainContext` (strategy, products, budget, headcount) |
| `docs/core/clarifier/` | Detect gaps in the Brain → generate questions with citations, write `03-clarification.md` |
| `docs/core/orchestrator/` | Router classifies the task, FlowController, research phase, execution planner |
| `docs/core/meeting/` | LangGraph debate graph — Pro/Con Advocate rounds → Perspective Debators → Synthesizer |
| `docs/core/agents/` | Agent loader + registry, base agent, pack loader |
| `docs/core/translator/` | Jargon detector → simplifier → TL;DR (3 modes: off/final_only/all_intermediate) |
| `docs/core/tools/` | `us_law_search`, `competitor_research`, `tax_calculator`, `web_search`, etc. Cache 24h. |
| `docs/core/obsidian/` | Vault read/write, wikilinks, template resolver (BYOT 3-level priority) |
| `docs/core/llm/providers.py` | `MCPSamplingProvider` (Claude Desktop), `ClaudeProvider` (direct API), `DeepSeekProvider` |

### LLM routing

Priority (`docs/core/mcp_server.py:_pick_llm`): env `DEEPSEEK_API_KEY` → `ANTHROPIC_API_KEY` → MCP sampling (Claude Desktop subscription, no key needed). API keys are read from `<vault>/.env`; behavior config (translator_mode, meeting rounds) from `<vault>/.vncoderc` (fallback `~/.vncoderc`).

### Departments + Packs (V2 — VP org layout)

- `docs/departments/` — 5 manager-led departments (29 agents: 5 managers + 24 teams). The **manager is the `default_speaker`**; team agents give short takes in the intra-department round and are also directly routable via `routing_rules`:
  - `01-hardware-engineering` (mgr + 4): me-team, ee-team, fw-embedded-team, system-architecture
  - `02-npi-program-management` (mgr + 6): hardware-pm, certification, bom-eco-plm, launch-readiness, sourcing-buyer, odm-program-mgmt
  - `03-quality-reliability` (mgr + 5, debate role: con): qa-system, qc-inspection, validation-reliability, firmware-qa, field-quality-rma-fa
  - `04-mfg-supplier-quality` (mgr + 4): odm-quality, supplier-quality, manufacturing-engineering, factory-test-yield
  - `05-service-operations` (mgr + 5): repair, fulfillment, inventory, deployment-support, logistics
- **Intra-department round** (`meeting.intra_department_round`, default **true**): each team speaks ≤150 words → the manager synthesizes the department perspective → managers debate. Cost: ~1 LLM call per team per participating department (5-dept meeting ≈ 29 round-1 calls). Turn off in `.vncoderc` for quick/cheap meetings.
- Agent prompts cross-reference each other with `[[wikilinks]]` ("Works with" sections); dept hubs render the org chart (manager ⭐ + teams) and "Works with" links from `depends_on` — Obsidian's graph shows the org and its handoffs.
- `docs/packs/` — optional overlay mechanism (kept); no packs ship by default
- `docs/templates-us/` — 245 default templates: 81 division templates in the 5 dept folders (HW Eng 9, NPI&PM 19, Q&R 16, MSQ 14, SvcOps 23) + 9 `_orchestrator` + 155 generic business templates parked in `_shared/` (BYOT source material; not resolved by dept code). All authored/adapted by Brian H. Doan; upstream attribution in `NOTICE`.

### Vault structure (runtime)

```
<vault>/
├── 00-Brain/          strategy.md, products.md, budget.md, headcount.md, state.md
├── 00-Templates-Custom/   Department Head custom templates (highest priority — BYOT)
├── 02-Tasks/<slug>/   00-brief.md, 03-clarification.md, 07-decision-report.md, 08-execution-plan.md
├── 03-Outputs/        .docx, .xlsx rendered
└── .vncoderc          vault config (packs, translator_mode, meeting rounds)
```

## 6 RULES (must not be violated)

1. **Brain-first** — Read the Brain before asking the Department Head. Questions must cite `file:section`. If the Brain is sufficient, don't ask.
2. **Domain-neutral** — Don't let TradingAgents jargon leak (trade/market/Bull/Bear/ticker). CI check: `docs/scripts/dev/check-domain-neutral.sh`.
3. **Single source of truth** — The Obsidian vault is canonical. SQLite is only a crash-recovery cache.
4. **Department-Head-friendly** — Output in plain English, with a TL;DR, define a term on first use, avoid heavy technical jargon.
5. **Live research + citations** — Tools must return `ToolResult.sources: list[str]` + `retrieved_at`. Cache 24h.
6. **BYOT** — Template priority: `vault/00-Templates-Custom/` > pack refs > `repo/docs/templates-us/`.

## Key patterns

**Adding a new tool** — Inherit from `docs/core/tools/base_tool.py`, return a `ToolResult` with `sources` + `retrieved_at`. Register it in `docs/core/tools/tool_router.py` (`_FULL_TOOL_DESCRIPTIONS`) and wire it in `docs/core/orchestrator/research_phase.py`.

**Adding a department** — Create a folder `docs/departments/XX-name/` with a `department.yaml`. Agents auto-load via `AgentLoader`.

**Adding a pack** — Create a folder `docs/packs/<name>/` with a `pack.yaml` + override templates. Department Head enables it via `.vncoderc`.

**Template resolver** — `docs/core/obsidian/template_resolver.py` checks 3 paths in the correct BYOT order.

**Tests** — Unit tests mock the LLM (no real API call). Integration tests use `docs/tests/fixtures/`. E2E tests in `docs/tests/e2e/` skip if there is no `TAVILY_API_KEY`.
