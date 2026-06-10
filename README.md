# Hardware Division OS — US One Person Company

> **An AI operating system for a hardware development, quality & supply chain division run by one VP.**
> You are the VP — 5 manager-led departments of AI agents (29 agents: 5 managers + 24 teams) debate like your real org: teams brief their manager, managers debate across departments, you approve. Output: decisions + `.docx/.xlsx` documents aligned with US federal + Texas law.
> Runs through a **Claude Desktop or Claude Code** subscription, **no Anthropic API key needed**.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![LangGraph](https://img.shields.io/badge/built_on-LangGraph-purple.svg)](https://github.com/langchain-ai/langgraph)
[![Tests](https://img.shields.io/badge/tests-273_passed-brightgreen.svg)](#)

> ⚠️ General information only — the legal/tax/regulatory content is not legal advice. Confirm with a licensed Texas attorney, CPA, customs broker, and the relevant certification labs.

---

## ✨ Who is it for?

A **division manager** at a Texas electronics company who owns hardware product development, operations, RMA, supply chain, and quality — and wants:

- 🏢 **5 specialist departments** of AI agents that mirror the real org (15 agents: EE/firmware/NPI, ops/inventory/fulfillment, RMA/repair/failure-analysis, buyer/ODM/logistics, QMS/certifications/supplier-quality)
- ⚖️ Decisions **based on a multi-angle debate** instead of one tired brain at 6pm
- 📄 Documents **grounded in US federal + Texas law** and hardware-industry practice (FCC Part 15, UL/IEC, PCI PTS/EMVCo, HTS/customs, Magnuson-Moss warranty) `[UNCERTAIN — verify specifics with attorney/labs]`
- 🧠 Every decision + document **stored in Obsidian + Git** — a single source of truth
- 💰 Runs through a single **Claude Desktop or Claude Code** subscription

### Real situations

| You face | Before | With the Division OS |
|---|---|---|
| An NPI pilot ships in 6 weeks | Chase engineering, the factory, and the lab by email; hope nothing was forgotten | Chat: "Pilot 500 PT-500 units by 06/30" → HW PD + Supply Chain + Quality + Operations debate → a gate plan with cert, spares, and IQC blockers caught up front |
| A component goes EOL | Panic-buy at broker prices | Chat: "Main MCU EOL'd, 30-week LTB" → option table (alternate via ECO, LTB quantity math, redesign) with cost and risk per path |
| Field returns spike on one lot | Anecdotes and finger-pointing | Chat: "PT-300 returns doubled in March" → RMA + Quality + HW PD → 8D with containment across factory/transit/field, rate-based evidence |
| A factory transfer to Mexico is proposed | Spreadsheet wars | Chat: "Compare moving the dock build to the Mexico CM" → landed-cost + tariff + tooling-duplication + transfer-risk analysis, with sign-off gates |

→ **You stay the manager. The departments do the staff work.**

---

## 🏗 Architecture

```
┌────────────────────────────────────────────────────────────────┐
│  Manager chats in Claude Desktop / Code                        │
│              ↓                                                  │
│  vn_run(brief) → Router classifies → Read the division Brain  │
│              ↓                                                  │
│  Detect a gap → Ask clarification (cites the Brain)           │
│              ↓                                                  │
│  vn_meeting → Live research (law, benchmarks, competitors)    │
│              ↓                                                  │
│  5 departments meet → Pro/Con debate → 3 perspectives         │
│              ↓                                                  │
│  Synthesizer + Translator (plain English) + Citation validator│
│              ↓                                                  │
│  vn_approve → Structured execution plan                        │
│              ↓                                                  │
│  vn_execute → Render .docx/.xlsx → 03-Outputs/                │
│              ↓                                                  │
│  Auto-commit to a private Git repo (Obsidian vault)           │
└────────────────────────────────────────────────────────────────┘
```

### The org (5 managers, 24 teams)

| Code                        | Department (Manager speaks)              | Teams                                                                                          |
| --------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `01-hardware-engineering`   | Hardware Engineering                     | ME, EE, FW/Embedded, System Architecture                                                       |
| `02-npi-program-management` | NPI & Program Management                 | Hardware PM, Certification, BOM/ECO/PLM, Launch Readiness, Sourcing & Buying, ODM Program Mgmt |
| `03-quality-reliability`    | Quality & Reliability *(debate skeptic)* | QA System, QC Inspection, Validation/Reliability, Firmware QA, Field Quality/RMA FA            |
| `04-mfg-supplier-quality`   | Manufacturing & Supplier Quality         | ODM Quality, Supplier Quality, Manufacturing Engineering, Factory Test/Yield                   |
| `05-service-operations`     | Service Operations                       | Repair, Fulfillment, Inventory, Deployment Support, Logistics                                  |

**How a meeting works (V2):** in round 1 every relevant team gives its manager a ≤150-word take; each manager synthesizes a department position (crediting teams, naming disagreements); the five managers then debate (Pro/Con + Growth/Cautious/Balanced) and the synthesizer writes the decision report for the VP. Team takes are preserved in `04-meeting-r1-perspectives.md` with `[[wikilinks]]`, so every position is traceable in Obsidian. Toggle with `meeting.intra_department_round` in `.vncoderc` (on by default; off = managers only, ~5× cheaper).

### Stack

- **Debate engine**: Python 3.11+ + LangGraph (adapted from TradingAgents, renamed neutral) + intra-department team round
- **Knowledge base**: 245 templates (81 division + 9 orchestrator + 155 generic in `_shared/`) + 5 manager-led departments (29 agents)
- **Storage**: Obsidian Markdown + private Git (one vault per division)
- **LLM**: MCP sampling via Claude Desktop / Claude Code (subscription) — NO Anthropic API key needed
- **Search**: Tavily (free tier 1000 req/month) for law/benchmarks/web

---

## 🚀 Quick Start

### 1. Install

```powershell
# Clone the repo
git clone https://github.com/<owner>/<repo>.git
cd <repo>

# Create a venv
python -m venv .venv
.venv\Scripts\activate     # Windows
# source .venv/bin/activate  # macOS/Linux

# Install
pip install -e .
```

### 2. Install the MCP server

Choose one of two clients depending on what you use:

**A) Claude Desktop** (GUI app)

```powershell
vn-os install-mcp
# Fully restart Claude Desktop (Quit from the taskbar → reopen)
# Click the "</> Code" tab at the top right
```

**B) Claude Code** (CLI / terminal)

```bash
bash adapters/claude-code/install.sh
# Automatically: installs the `vn-business-os` skill + registers the MCP in ~/.claude.json
```

Or manually:
```powershell
vn-os install-mcp --target claude-code
```

> 💡 On Windows with Claude Code: run `install.sh` via Git Bash or WSL. Or use the manual command above.
> See [`adapters/claude-code/README.md`](adapters/claude-code/README.md) for details.

### 3. Create a vault for your division

In a Claude Desktop / Claude Code chat:
```
Set up a vault for my hardware division at the path F:/work/division-vault.
My TAVILY_API_KEY: tvly-xxx (get a free one at tavily.com).
```

Claude automatically calls the MCP tool `vn_onboard` to create the vault scaffold + save the key to `<vault>/.env` (gitignored).

### 4. Re-install the MCP with the env injected

```powershell
# Claude Desktop
vn-os install-mcp --vault "F:/work/division-vault"
# Restart Claude Desktop again

# Claude Code
vn-os install-mcp --vault "F:/work/division-vault" --target claude-code
# Restart the Claude Code session
```

### 5. Fill in the Brain (one time)

Open `<vault>/00-Brain/` in Obsidian and fill in:
- `strategy.md` — vision, target customers, yearly goals (units, return rate, OTD)
- `products.md` — device catalog + price + margin
- `budget.md` — yearly budget + department allocation
- `headcount.md` — which departments are active, expertise gaps
- `laws.md` — certifications held/required (FCC, UL, PCI/EMVCo), customs notes
- `state.md` — division stage, fleet size, current quarter numbers

### 6. Run your first task

In a Claude Desktop / Claude Code chat:
```
We need to pilot 500 units of the new terminal with our top customer by 06/30.
Reference the budget and check the certification status.
```

The system will:
1. Classify the task → COMPLEX (3-5 departments debate)
2. Read the Brain → detect gaps (cert renewal timing? spares plan?)
3. Ask you 3-5 clarifying questions (each citing the Brain)
4. Research applicable law/benchmarks live
5. Run pro/con + 3 perspectives (Growth/Cautious/Balanced)
6. Generate `07-decision-report.md` (you approve)
7. Generate `08-execution-plan.md` + render `.docx/.xlsx`

---

## 📦 Packs

The pack mechanism (industry/role overlays) is supported but **no packs ship by default** — the 5 division departments are the core. See [`packs/README.md`](packs/README.md) and [`docs/how-to-create-pack.md`](docs/how-to-create-pack.md) to build one.

---

## 📜 6 RULES (immutable)

| # | Rule | Implementation |
|---|---|---|
| 1 | **Brain-first** | Don't ask the manager before reading the Brain |
| 2 | **Domain-neutral** | The engine doesn't leak trading/finance jargon |
| 3 | **Single source of truth** | The Obsidian vault is canonical |
| 4 | **Manager-friendly language** | Translator pipeline (3 modes) |
| 5 | **Live research with citations** | Tools gracefully skip + citation validator |
| 6 | **BYOT** | Division custom > pack > default templates |

---

## 🛠 Configuration

Edit `<vault>/.vncoderc`:

```yaml
vault_path: F:/work/division-vault
packs: []
version: "0.1.0"

# Translator scope (P1.6)
# off | final_only (default) | all_intermediate
translator_mode: final_only

meeting:
  max_debate_rounds: 2
  max_perspective_rounds: 1
  use_checkpointer: false        # P1.4 opt-in crash recovery
  intra_department_round: true   # V2: teams brief their manager before managers debate

llm:
  primary: claude-sonnet-4-6
```

---

## 🧪 Tests

```bash
python -m pytest tests/ -q
# 273 passed, 4 skipped
```

---

## 📚 Documentation

- [`docs/getting-started.md`](docs/getting-started.md) — detailed install + onboarding
- [`docs/install-claude-code.md`](docs/install-claude-code.md) — **step-by-step Claude Code install + interaction script**
- [`docs/user-guide.md`](docs/user-guide.md) — the 5-stage flow + examples
- [`docs/configuration.md`](docs/configuration.md) — `.vncoderc`, packs, BYOT
- [`docs/troubleshooting.md`](docs/troubleshooting.md) — common errors
- [`docs/architecture.md`](docs/architecture.md) — architecture + RULES + extensibility
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contributing code

---

## 🤝 Contributing

PRs welcome. Especially needed:
- More division templates (test plans, control plans, customs SOPs)
- Glossary growth: hardware/supply-chain terms
- Test coverage: real-LLM E2E

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📄 Author & License

**Author:** Brian H. Doan — VP, Hardware Development, Quality & Supply Chain. The division specialization, the 5-department/29-agent architecture, and the division templates are his work.

**Apache License 2.0** — © 2026 Brian H. Doan

See [LICENSE](LICENSE) for the full text and [NOTICE](NOTICE) for detailed attribution.

Apache 2.0 allows commercial use + modification + redistribution, while **protecting the "VN Business OS" name/logo from being used by forks to advertise other products** (Section 6) and ensuring forks must **clearly state the changes** they made.

**Credits (detailed in [NOTICE](NOTICE)):**
- 192 US business templates in `templates-us/` adapted from `business-builder.plugin` (28 division-mapped + 9 orchestrator + 155 in `_shared/`); the 53 hardware-division templates are original work by Brian H. Doan
- Debate engine pattern adapted from [TradingAgents](https://github.com/TauricResearch/TradingAgents) (Apache 2.0)
- Role definitions reference from [agency-agents](https://github.com/msitarzewski/agency-agents)
