# Next Steps — After compact

> ⚠️ HISTORICAL (06/09/2026): this was the bootstrap guide for the original v1
> build sessions. The build is complete and the repo has been restructured into
> a 5-department hardware-division OS — see `README.md` and `MIGRATION_REPORT.md`.

> Guide for the next Claude Code session (after `/compact`).

---

## 🎯 Step 1 — Start a new session

Open a new Claude Code session in this folder:
```
<path>/One Person Company
```

Paste the startup prompt:

```
Read the following files in order to understand the context:
1. README.md          — project overview
2. DECISIONS.md       — 6 RULES + 8 locked decisions
3. SESSION-LOG.md     — the full brainstorming transcript
4. SPEC.md            — the complete design spec
5. docs/plans/plan.md      — overview of the 6 phases
   (the detailed per-phase plan files were removed 06/09/2026 — the build is complete)

Once done, use the skill superpowers:subagent-driven-development to implement Phase 1.
12 tasks in Phase 1 — spawn an implementer + 2 reviewers (spec + quality) per task.
Create the root repo RIGHT HERE in the current folder (do not create a vn-business-os subfolder).
```

---

## 🔑 Environment requirements

Before running, make sure you have:

```bash
# Python 3.11+
python --version

# API keys (export before running)
export ANTHROPIC_API_KEY=sk-ant-...     # required
export TAVILY_API_KEY=tvly-...           # for Phase 4 (tools)

# Git config (if not set)
git config --global user.name "<your name>"
git config --global user.email "your-email@example.com"
```

---

## 📋 Expected output after Phase 1

The structure after Phase 1 is done:

```
One Person Company/
├── pyproject.toml
├── README.md (exists — overwritten in Phase 1 Task 1)
├── LICENSE (MIT)
├── .gitignore
├── docs/core/
│   ├── __init__.py
│   ├── cli.py
│   ├── brain/
│   │   ├── schema.py
│   │   ├── reader.py
│   │   └── memory.py
│   ├── obsidian/
│   │   ├── frontmatter.py
│   │   └── vault.py
│   ├── agents/
│   │   └── department.py
│   ├── llm/
│   │   └── providers.py
│   └── utils/
│       └── config.py
├── docs/departments/                  # 12 dept folders
├── docs/templates-us/                 # 192 .md from bb-plugin (vendored)
├── docs/vault-template/               # Obsidian scaffold
├── docs/tests/
│   ├── unit/                     # ~10 test files
│   ├── integration/
│   │   └── test_phase01_smoke.py
│   └── fixtures/
│       └── demo-vault/
├── docs/scripts/
│   └── dev/
│       ├── vendor-bb-plugin.sh
│       └── create-dept-stubs.sh
├── docs/plans/                        # exists
├── DECISIONS.md                  # exists
├── SESSION-LOG.md                # exists
├── SPEC.md                       # exists
└── NEXT-STEPS.md                 # this file
```

Verify Phase 1:
```bash
pip install -e .
vn-os --version                    # 0.1.0
vn-os status --vault docs/tests/fixtures/demo-vault   # green checks
pytest docs/tests/integration/test_phase01_smoke.py -v
git tag | grep phase-01-complete
```

---

## ⚠️ Important notes for the next session

### 1. Vendor bb-plugin
Phase 1 Task 3 needs the `business-builder.plugin` file at:
```
<path>/business-builder.plugin
```
Or copy it into `One Person Company/` then run the script.

### 2. Keep Python files under 200 lines
Per the global development-rules.md. Each module focused on one responsibility.

### 3. Domain-neutral check (RULE 2)
After Phase 2 (lifting the engine from TradingAgents), EVERY commit must pass:
```bash
bash docs/scripts/dev/check-domain-neutral.sh
```

### 4. Language
- Agent system prompts: **plain English**
- Code comments: English
- Variable / function names: English (Python convention)
- Output to the CEO: **plain English + define terms + TL;DR (RULE 4)**

### 5. Test with a mock LLM
- CI uses a mock (no API cost)
- E2E real LLM gated by env `RUN_REAL_LLM=1`

---

## 🗺️ Overall roadmap

| Phase | Tasks | Estimate |
|:-:|:-:|---|
| 1 | 12 | After Phase 1 done → review → decide next |
| 2 | 8 | Debate engine (LangGraph) |
| 3 | 9 | Orchestrator + Brain-first clarification |
| 4 | 14 | Tools + Translator |
| 5 | 12 | Departments full + 3 packs + BYOT |
| 6 | 10 | Adapters + E2E + Onboard wizard |

After Phase 6 is done → tag `v0.1.0` → ship v1.

---

## 📞 Author & references

**CEO / Repo owner:** `your-email@example.com`

**Vendored content credit:**
- 192 templates in `docs/templates-us/` (originally authored in Vietnamese, localized to US English) from `references/business-builder.plugin`.
- The debate engine (LangGraph pattern) lifted from **TradingAgents** (TauricResearch).
- Role definitions referenced from **agency-agents** (msitarzewski).

---

## 🚦 TL;DR for the CEO

1. Everything is prepared; the detailed 65-task plan is in `docs/plans/`
2. The next session just needs to paste the startup prompt in Step 1
3. Phase 1 is ~1-2 hours of tool calls. Then review and decide next.
4. Do NOT violate the 6 RULES in `DECISIONS.md`.

Ready. Waiting for the CEO to `/compact` then paste the prompt.
