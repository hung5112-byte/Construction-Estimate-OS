# 🚦 START HERE — Bootstrap for a new Claude Code session

> ⚠️ HISTORICAL (06/09/2026): this was the bootstrap file for the original v1
> build sessions. The build is complete and the repo has been restructured into
> a 5-department hardware engineering & supply chain division OS — for current
> guidance start with `README.md`, `CLAUDE.md`, and `MIGRATION_REPORT.md`.

> **Read this file BEFORE doing anything.**
> This file is designed so a fresh Claude Code session (with NO context from the brainstorming session) can safely pick up the work.

---

## ⚡ Quick bootstrap (Department Head: copy-paste this prompt into a new session)

Copy the block below and paste it into Claude Code:

```
I HAVE A PROJECT THAT WAS ALREADY BRAINSTORMED AND PLANNED IN A PREVIOUS SESSION.

YOUR TASK:

Step 1 — Understand the context (do NOT skip):
1. Read START-HERE.md (this file) — overview
2. Read DECISIONS.md — 8 decisions + 6 immutable RULES
3. Read README.md — entry point
4. Read SPEC.md — full design spec
5. Read docs/plans/plan.md — overview of the 6 phases
   (the detailed per-phase plan files were removed 06/09/2026 — the build is complete; see SESSION-LOG.md for history)

Step 2 — Verify understanding (REQUIRED):
After reading, answer these 4 questions (briefly, 1-2 lines each):
A. What does this project build? (1 sentence)
B. What are the 6 RULES? (just list the names)
C. How many tasks in Phase 1? What's the first task?
D. What's the main tech stack?

Step 3 — Wait for my confirmation:
After answering the 4 questions, do NOTHING more. Wait until I say "OK, correct, continue" before starting implementation.

Step 4 — Implementation:
When I confirm, use the skill `superpowers:subagent-driven-development` to run Phase 1.
Create the root repo RIGHT HERE in the current folder (do NOT create a bd-business-os subfolder).

NOTE:
- I am the Department Head/owner (your-email@example.com)
- All code must follow the 6 RULES in DECISIONS.md
- All output to me must be in plain English + define terms + include a TL;DR (RULE 4)
```

---

## 📂 Folder map

```
Hardware Division OS/
├── START-HERE.md         ← THIS FILE (read first)
├── README.md             ← project overview + status
├── DECISIONS.md          ← 8 decisions + 6 RULES (VERY IMPORTANT)
├── SESSION-LOG.md        ← full transcript of the brainstorming session
├── SPEC.md               ← complete design spec
├── NEXT-STEPS.md         ← detailed step-by-step guide
└── docs/plans/
    └── plan.md                                      ← overview of the 6 phases
        (the detailed phase-0X files were removed 06/09/2026 — build complete)
```

---

## 🔑 4 most important facts (if a new Claude session reads only one section → read this one)

### 1. Who am I?
- **Department Head/Owner of the repo:** `your-email@example.com` (that's me, the person chatting)
- **`references/business-builder.plugin`:** the source zip — contains 192 templates (originally authored in Vietnamese, now localized to US English) vendored into `docs/templates-us/`

### 2. What is the project?
**Hardware Division OS** — an open-source AI agent OS for a US department head:
- Department Head chats a brief → AI agents (departments) debate → produce a report + `.docx/.xlsx` documents
- Aligned with US GAAP + the Texas Business Organizations Code (TBOC) + FLSA + IRS rules (general information, not legal/tax advice)
- Task classification: SIMPLE / COMPLEX / STRATEGIC
- Stack: Python + LangGraph + Obsidian + multi-tool entry (Claude Code/Cowork)

### 3. The 6 immutable RULES
1. **Brain-first clarification** — read the Brain (`vault/00-Brain/*.md`) BEFORE asking the Department Head; every question MUST cite the Brain
2. **Domain-neutral engine** — code lifted from TradingAgents MUST rename all Bull/Bear/trade/finance/ticker
3. **Single source of truth** — the Obsidian vault is the truth, SQLite is only a cache
4. **Department-Head-friendly language** — plain English, define terms, TL;DR at the top of reports
5. **Live research with citations** — search law/competitors/benchmarks, cite URL + date
6. **BYOT** — custom company templates > pack > default (192 templates from the bb-plugin)

### 4. The overall plan
- 6 phases, 65 tasks total, ~330 bite-sized steps
- Phase 1 ~12 tasks, ~1-2 hours of tool calls
- Approach: hybrid — lift the LangGraph engine from TradingAgents + hand-code Brain/Clarifier/Tools/Translator
- Test case v1: a marketing campaign targeting higher-income customers (5 departments meet, 3 debate rounds)

---

## ⚠️ Anti-patterns (so a new Claude session doesn't go wrong)

| ❌ DON'T | ✅ DO |
|---|---|
| Skip reading DECISIONS.md because "I think I know" | Read the 6 RULES carefully, be able to cite them |
| Create a `bd-business-os/` subfolder | Create directly in the CWD (`Hardware Division OS/`) |
| Make up numbers / US law | Search live via tools (RULE 5) |
| Output in another language or full jargon | Plain English + definitions + TL;DR (RULE 4) |
| Skip the 6-RULES check on each commit | Run `docs/scripts/dev/check-domain-neutral.sh` |
| Spawn 65 tasks in parallel | Sequential — implementer → spec reviewer → quality reviewer |
| Implement without following the plan | Read the phase file → stick to task # and step # |
| Ask the user before reading the Brain | Brain-first ALWAYS (RULE 1) |

---

## 🆘 If the new session seems confused

The Department Head can paste this again:

```
Hold on. Re-read START-HERE.md + DECISIONS.md from the top, especially the 6 RULES.
Then tell me what this project is + what the 6 RULES mean.
Do NOTHING else until I confirm.
```

Or a simpler reset:
```
You seem to have lost the context. /clear, then paste the bootstrap prompt from START-HERE.md again.
```

---

## 🎯 After Phase 1 is done

Verify checklist (Department Head runs):

```bash
cd "<path>/Hardware Division OS"

# 1. pip install
pip install -e .
# expect: Successfully installed bd-business-os-0.1.0

# 2. CLI works
bd-os --version
# expect: 0.1.0

# 3. Brain reader works
bd-os status --vault docs/tests/fixtures/demo-vault
# expect: green checks for Brain

# 4. Smoke test passes
pytest docs/tests/integration/test_phase01_smoke.py -v
# expect: 4 passed

# 5. Templates vendored
find templates-us -name "*.md" | wc -l
# expect: 192
```

If all 5 checks are ✅ → Phase 1 done, can continue to Phase 2.

---

## 📌 Credits note (when the repo is public)

Required credits in README/LICENSE/NOTICE:
- **192 templates** in `docs/templates-us/` adapted from `references/business-builder.plugin`
- **Engine debate pattern** adapted from [TradingAgents](https://github.com/TauricResearch/TradingAgents)
- **Role definitions reference** from [agency-agents](https://github.com/msitarzewski/agency-agents)

---

**Ready. Department Head: `/compact`, then paste the bootstrap prompt at the top of this file.**
