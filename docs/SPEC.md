# VN Business OS — Design Spec

**Date:** 2026-05-06
**Author:** Brainstorming session with the Department Head
**Status:** HISTORICAL — this is the original v1 design spec (generic 12-department
division OS). On 06/09/2026 the repo was specialized into a **5-department
hardware engineering & supply chain division OS** (Hardware Product Dev, Operations,
RMA, Supply Chain, Quality) — see `README.md` and `CLAUDE.md` for the current
architecture. Department/pack specifics below describe the v1 design, not the
shipped system.
**Slug:** `bd-business-os` (alias `vbos`)
**License:** MIT

---

## 1. Goal

Build an open-source repo that helps **any US small business / solo operator** run on a "division + AI agent team" model.

The Department Head assigns work via chat/CLI → the system reads the company's data → the departments (AI agents) debate → produce a consolidated report → the Department Head approves → it auto-generates a plan + documents (.docx/.xlsx).

Works for any industry (F&B, retail, tech, edu, healthcare...). Not a trading system.

## 2. Overall architecture (4 layers)

```
┌─────────────────────────────────────────────────────┐
│ LAYER 1 — ENTRY (Department Head chat)                          │
│ Adapters: Claude Code · Cowork · (v2: Codex/Antigrav)│
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ LAYER 2 — CORE (Python + LangGraph)                 │
│ Orchestrator · Brain · Clarifier · Translator       │
│ Meeting (Pro/Con debate) · Tools (research) · LLM   │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ LAYER 3 — STATE                                     │
│ SQLite (LangGraph checkpoint)  +  Obsidian (Git)    │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ LAYER 4 — OUTPUT                                    │
│ Markdown reports · .docx/.xlsx · Decisions log      │
└─────────────────────────────────────────────────────┘
```

## 3. Locked architecture decisions

| # | Decision |
|---|---|
| Approach | Hybrid (Approach C): lift the debate engine from TradingAgents + hand-code the rest |
| Stack | Python + LangGraph + SQLite + Obsidian Markdown + Git private |
| Storage | Company self-hosts: local + private Git repo (Github/Gitea) |
| Setup | Hybrid: clone manually or wizard onboarding |
| Departments | 13 core (from business-builder.plugin) + industry packs + on-demand creator |
| MVP packs v1 | F&B + Retail + Tech-SaaS |
| Auto level | Semi-auto (2 stops) + context-aware clarification |
| Test case v1 | B — a marketing campaign targeting $80k+ income customers |
| Multi-LLM | Default Claude Sonnet 4.6, fallback Gemini/GPT/Qwen/Ollama |
| Tools | Web search, US law search, competitor research, industry benchmark, tax calc |

## 4. The six immutable principles

| # | Rule | Description |
|---|---|---|
| 1 | Brain-first clarification | Don't ask the Department Head before reading the Brain. Every question must cite a Brain source. |
| 2 | Domain-neutral engine | Code copied from TradingAgents must be fully renamed — no trade/finance leak. |
| 3 | Single source of truth | The Obsidian vault is the truth. SQLite is only a recovery cache. |
| 4 | Department-Head-friendly language | Plain English, define terms, include a TL;DR. |
| 5 | Live research with citations | Search law/competitors/benchmarks as needed. MUST cite the source. |
| 6 | BYOT (Bring Your Own Templates) | The company can bring its own templates → prefer custom > default. |

## 5. Repo structure

```
bd-business-os/
├── docs/core/                              # Python engine
│   ├── orchestrator/                  # router, flow_controller
│   ├── brain/                         # reader, gap_analyzer, memory
│   ├── clarifier/                     # question_generator (Brain-first)
│   ├── translator/                    # glossary, jargon, simplifier, TL;DR (RULE 4)
│   ├── meeting/                       # debate engine (reused TradingAgents)
│   ├── agents/                        # base_agent, department, registry, creator
│   ├── obsidian/                      # vault I/O, doc_writer, template_resolver
│   ├── tools/                         # web_search, us_law, competitor, benchmark, tax (RULE 5)
│   ├── llm/                           # multi-provider abstraction
│   └── cli.py
├── docs/departments/                       # 13 core departments (YAML + agent .md)
├── docs/packs/                             # F&B, Retail, Tech-SaaS
├── docs/templates-us/                      # 191 templates from bb-plugin (vendored)
├── docs/vault-template/                    # Obsidian scaffold for onboard
├── docs/adapters/                          # claude-code, claude-cowork, codex, antigravity
├── docs/scripts/                           # install.sh, onboard.py
├── docs/tests/                             # unit, integration, e2e, fixtures
└── docs/                              # getting-started, architecture, how-to-create-pack
```

LoC est.: ~4800 lines of Python core + ~150-200 YAML/MD config files + ~1000 lines of test.

## 6. Company vault structure

```
~/<company>-vault/
├── 00-Brain/                          # the AI must read this before any work
│   ├── strategy.md                    # vision, ICP, annual goals
│   ├── products.md                    # current products + price + margin
│   ├── budget.md                      # quarterly budget + remaining
│   ├── headcount.md                   # which departments, which agents active
│   ├── laws.md                        # business, labor, accounting, advertising law
│   ├── decisions-log.md               # append-only decisions
│   ├── state.md                       # stage, current KPIs
│   └── glossary.md                    # auto-grown from outputs
├── 00-Templates-Custom/               # 🆕 RULE 6: company brings its own templates
├── 01-Departments/                    # cloned from /departments + pack
├── 02-Tasks/                          # the Department Head drops a brief here
│   └── YYYY-MM-DD-<slug>/
│       ├── 00-brief.md
│       ├── 01-routing.md
│       ├── 02-context.md
│       ├── 03-clarification.md
│       ├── 03b-research-findings.md   # 🆕 RULE 5
│       ├── 04-meeting-r1-perspectives.md
│       ├── 05-meeting-r2-debate.md
│       ├── 06-meeting-r3-perspectives.md
│       ├── 07-decision-report.md      # Department Head approves here (Stop 1)
│       └── 08-execution-plan.md       # Department Head approves execute (Stop 2)
├── 03-Outputs/                        # official docx/xlsx (10 standard bb-plugin folders)
└── 99-Archive/
```

## 7. Data flow (Test case B)

```
Department Head brief
   ↓
Brain reader   → load 7 files in 00-Brain/
   ↓
Router         → SIMPLE/COMPLEX/STRATEGIC + dept list
   ↓
Gap analyzer   → compare brief vs Brain
   ↓
Clarifier      → ask the Department Head (Brain-first, with citations) — only if something's missing
   ↓
🆕 Research    → tools run in parallel (law + competitors + benchmark)
   ↓
Meeting R1     → each department speaks (parallel)
   ↓
Meeting R2     → Pro Advocate vs Con Advocate (2-3 turns)
   ↓
Meeting R3     → Perspective Debators (Growth/Cautious/Balanced)
   ↓
Synthesizer    → 07-decision-report.md
   ↓
=== STOP 1: Department Head approves the report ===
   ↓
Execution Dispatcher → 08-execution-plan.md
   ↓
=== STOP 2: Department Head approves execute ===
   ↓
Doc Writer     → generate .docx/.xlsx into 03-Outputs/
Memory         → append to decisions-log.md
Git sync       → auto-commit
```

Timing: 15-25 min per COMPLEX task. Department Head at the keyboard ~10 min.
Cost: ~$0.5-1.5/task (Claude Sonnet 4.6).

## 8. Department + Agent definition

### Department (`docs/departments/<code>/department.yaml`)
```yaml
code: "07-marketing"
name_vn: "Marketing & Brand"
tier: 3
agents: [brand-manager, content-creator, ads-specialist, seo-specialist]
default_speaker: brand-manager
routing_rules: [keyword-based agent selection]
refs_folder: refs/
depends_on: ["02-strategy", "08-customer", "03-finance"]
debate_role: { default: pro, override: { cost_cutting: con } }
```

### Agent (`docs/departments/<code>/agents/<id>.md`)
```yaml
---
id: ads-specialist
name_vn: "Advertising Specialist"
department: 07-marketing
expertise: [...]
required_refs: [...]
required_tools: [us_law_search, industry_benchmark]
deliverables: [...]
llm_override: { model: claude-sonnet-4-6, temperature: 0.3 }
---
[System prompt in English]
```

### Pack (`docs/packs/<name>/pack.yaml`)
```yaml
name: F&B Pack
adds_departments: [13-kitchen, 14-food-safety]
extends_departments:
  - target: 05-operations
    add_agents: [inventory-manager-fnb]
brain_template: brain-template/
compliance_refs: ["FDA Food Code + Texas DSHS food permit", "OSHA / local fire code"]
```

### On-demand agent creation
When the gap_analyzer detects missing expertise → propose to the Department Head → if approved → `creator.py` generates the agent definition file + commits to Git → persists permanently.

## 9. Industry Packs v1

### F&B (Eatery / Cafe / Restaurant)
- New departments: 13-kitchen, 14-food-safety (~9 agents)
- Extends: operations (inventory, vendor), customer (service-quality), sales (revenue mgr), finance (cogs tracker)
- Brain: table turnover, food cost %, labor cost %
- Compliance: FDA Food Code + Texas DSHS food permit; OSHA / local fire code

### Retail (Shop / E-commerce)
- New departments: 13-warehouse, 14-logistics (~12 agents)
- Extends: sales (marketplace, livestream), marketing (creative, affiliate), customer (online, returns), product-tech (ecommerce platform, pixel)
- Brain: GMV, AOV, return rate %, DOH
- Tools: integrate Amazon/Shopify/Etsy/TikTok Shop concepts

### Tech-SaaS (Software startup)
- New departments: 13-engineering, 14-product-design, 15-data (~22 agents)
- Extends from agency-agents engineering/, product/, design/
- Brain: MRR/ARR, DAU/MAU, churn, LTV/CAC, runway

Total v1: ~73 ready-to-use agents.

## 10. Department-Head-friendly language (RULE 4)

### Module `docs/core/translator/`
- `glossary.py` — load/save vault/00-Brain/glossary.md
- `jargon_detector.py` — detect jargon
- `simplifier.py` — rewrite complex → simple
- `tldr_generator.py` — generate the TL;DR
- `terms_dictionary.yaml` — US terms + examples + US benchmarks

### Standard output format
```markdown
## 📌 Bottom line (30-second read)
- [3-5 lines a layperson understands]

## Details
[content]

**Term X** (simple explanation, a concrete example for this company)
```

### Pipeline
```
Agent raw output → JargonDetector → Simplifier → TLDRGenerator → Department Head
```

## 11. Live research (RULE 5)

### Module `docs/core/tools/`
| Tool | Source | When to use |
|---|---|---|
| `web_search` | Tavily/Serper/Brave | General research |
| `us_law_search` | irs.gov, uscode.house.gov, statutes.capitol.texas.gov | Compliance check |
| `us_local_regulation` | texas.gov, comptroller.texas.gov, sos.state.tx.us | Local regulations |
| `competitor_research` | Public web info | Competitive analysis |
| `industry_benchmark` | Curated YAML + scrape | US industry KPIs |
| `tax_calculator` | Pure code | Income, self-employment, sales-and-use, franchise tax |

### Research Phase (new — runs before Meeting R1)
The ToolRouter scans the brief + Brain → decides what research is needed → runs in parallel → caches 24h → injects into MeetingState.

### Citation required
Every claim in the report must have a citation: URL + access date. Example: `[cite: irs.gov/.../self-employment-tax, retrieved 2026-05-06]`.

## 12. BYOT — Bring Your Own Templates (RULE 6)

### Priority order
1. `vault/00-Templates-Custom/<dept>/` — company brings its own
2. `vault/01-Departments/<dept>/refs/` — pack templates copied into the vault
3. `repo/docs/templates-us/<dept>/` — 191 default templates from bb-plugin (vendored)

### Supported formats
`.md`, `.docx`, `.xlsx`. PDF optional (needs OCR).

### Onboarding wizard
Asks whether the company already has templates → if so → import + LLM classification + generate `_index.md` mapping.

## 13. Multi-tool adapters

| Tool | Format | v1 | v2 |
|---|---|:-:|:-:|
| Claude Code | `.md` skill | ✅ | |
| Claude Cowork | `.claude-plugin` | ✅ | |
| Codex | system prompt | | ✅ |
| Antigravity | `SKILL.md` | | ✅ |

Pattern: 1 core Python + many thin adapters calling the CLI via the Bash tool.

## 14. Error handling

| Layer | Type | Action |
|---|---|---|
| A | LLM (timeout/rate/filter) | Retry x3 → failover provider → reframe |
| B | Tool (API down) | Cache fallback → mark UNVERIFIED |
| C | State recovery | LangGraph checkpoint → `bd-os resume <task>` |
| D | Validation | Pause + ask the Department Head to add info |
| E | User input | Spell check + intent confirm |

## 15. Testing strategy

```
docs/tests/
├── unit/        ~70%  (router, brain, gap, clarifier, translator, tools)
├── integration/ ~20%  (meeting graph, BYOT, research phase)
├── e2e/         🎯    (test_b campaign, test_a onboard, test_c simple JD)
└── fixtures/    (techco-vault, fnb-vault, retail-vault demo data)
```

### Test case B — acceptance criteria (key items)
- task_class == COMPLEX
- ≥ 5 departments convened
- ≥ 3 research findings (law + competitor + benchmark)
- All clarifications have a citation (RULE 1)
- The decision report has a TL;DR + jargon defined (RULE 4)
- The decision report has law citations + competitor data (RULE 5)
- 2 output files (.docx + .xlsx) in the right folder
- < 100k tokens, < $2/task, < 25 min

## 16. Roadmap v1 (~6 weeks FT-equivalent)

| Week | Phase | Output |
|------|-------|--------|
| 1 | Foundation | Repo skeleton + Brain + 13 departments + vendor 191 templates |
| 2 | Engine extraction | meeting_graph from TradingAgents → rename neutral + checkpoint |
| 3 | Orchestrator + Brain-first | Router + Gap + Clarifier + Flow controller (2 stops) |
| 4 | Tools + Translator | 6 tools + glossary + simplifier + TL;DR + research phase |
| 5 | Departments + Pack + BYOT | 13 departments full agents + 3 packs + template resolver + doc writer |
| 6 | Adapter + E2E + Onboard | Claude Code/Cowork adapter + wizard + test B pass |

v1.1: test A (onboard) + C (simple JD), Codex/Antigravity stubs.
v2: auto-loop cron, web UI, multi-company, new packs (Real Estate, Healthcare, Edu).

## 17. Risks

| Risk | P | I | Mitigation |
|---|:-:|:-:|---|
| LangGraph version churn | M | H | Pin version, isolate in meeting/ |
| LLM cost overrun | H | M | Token counter + budget guard |
| Tool API down | M | M | Cache 24h + UNVERIFIED mode |
| LLM output quality | L | H | Default Claude Sonnet 4.6, A/B test |
| Unusual BYOT format | M | L | Support 3 standard formats |
| Vault corruption | L | H | Git auto-commit |
| Onboard too long | M | H | Max 30 questions, skip optional |
| Multi-pack conflict | M | L | Merge logic + combo tests |
| Maintainer bandwidth | H | M | Good docs + contribution guide |

## 18. Definition of Done v1

- [ ] Public repo, complete English README
- [ ] `pip install -e .` works on Win/Mac/Linux
- [ ] Wizard generates a valid vault
- [ ] Test case B runs E2E < 25 min, < $2
- [ ] 13 core departments have real agents
- [ ] 3 packs pass their own tests
- [ ] BYOT demo works
- [ ] 6 RULES enforced in code
- [ ] Claude Code + Cowork adapter E2E
- [ ] `getting-started.md` for a non-tech Department Head

## 19. Open questions

1. Default LLM provider v1 — Claude Sonnet 4.6, or let the user choose at onboard?
2. Web search API: Tavily (free tier 1000/mo) or Serper ($1/1000)? Which default?
3. Need a grammar/style check in v1, or v1.1?
4. Does BYOT support PDF + OCR in v1 (needs an extra library), or only md/docx/xlsx?
5. Auto-commit Git: on by default or opt-in via config?
6. Brain glossary auto-grow: on by default or manual approve per term?
7. Test cost with a real LLM in CI: use cassette/recording (like VCR) or pure mock?
