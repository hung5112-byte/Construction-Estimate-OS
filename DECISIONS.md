# Decisions + Rules — VN Business OS

> All decisions + principles locked in the brainstorming session 2026-05-05 → 2026-05-06.
>
> ⚠️ Note (06/09/2026): the 6 RULES remain in force. Department-specific decisions
> below predate the restructure into the 5 hardware-division departments
> (see `README.md`); read them as build history.

---

## 🎯 5 main decisions (locked with the CEO)

### Decision 1 — Setup approach
**A + B (Hybrid open-source repo)**
- Clone the repo → set up manually, **OR**
- Clone the repo → run the onboarding wizard (asks ~30 questions)

→ Public repo, supporting both tech-savvy devs and non-tech CEOs.

### Decision 2 — Department set
**A + B + D (Core + Industry packs + On-demand creator)**
- 13 core departments (per business-builder.plugin)
- Industry packs for specialized industries
- A "hire a new agent" mechanism at runtime when missing expertise is detected

### Decision 3 — MVP v1 scope
**C — Core 13 + 3 industry packs**
- F&B pack (eatery / cafe / restaurant)
- Retail pack (shop / e-commerce / D2C)
- Tech-SaaS pack (software startup)

→ After v1, expand packs: Real Estate, Healthcare, Education, Beauty, Auto, Construction.

### Decision 4 — Level of automation
**B — Semi-auto + Context-aware Clarification**
- Read the Brain BEFORE asking the CEO
- Ask about the right gap, with a Brain citation
- 2 stops: Stop 1 (decision report approval), Stop 2 (execution approval)

### Decision 5 — Storage
**B — Local + Git private**
- Obsidian vault local on the CEO's machine
- Auto-commit (NOT auto-push) to a private GitHub
- Standard `.gitignore` excludes sensitive files

### Decision 6 — Execution stack (bonus)
**D — Hybrid: Python+LangGraph + Obsidian + multi-tool adapters**
- Lift the debate engine from TradingAgents (rename neutral)
- Hand-code the Brain / Clarifier / Tools / Translator
- Multi-tool entry: Claude Code + Cowork (v1) → Codex + Antigravity (v2)

### Decision 7 — Test case v1 (bonus)
**B then A + C — A marketing campaign targeting $80k+ income customers**
- v1 ships only test case B (the full debate flow)
- v1.1 adds A (onboarding flow) + C (simple JD/contract)

### Decision 8 — Repo location (bonus, 2026-05-06)
**`<path>/One Person Company`**

---

## 🔒 6 immutable RULES (enforced in code)

### RULE 1 — Brain-first clarification
> Do NOT ask the CEO before reading the Brain. Every question MUST cite a Brain source (file:section).
> If the Brain is sufficient → don't ask, go straight to the router.

**Enforce:** `core/clarifier/question_generator.py` — `if not gaps: return []`.

### RULE 2 — Domain-neutral engine
> Code copied from TradingAgents MUST be fully renamed. Don't let trade/finance/market/ticker/Bull/Bear leak.

**Specific renames:**
- `trading_graph.py` → `meeting_graph.py`
- `Bull/Bear Researcher` → `Pro/Con Advocate`
- `risk_debators` → `perspective_debators` (growth / cautious / balanced)
- `Portfolio Manager` → `Decision Synthesizer`
- Remove `yfinance`, `Alpha Vantage`, `dataflows/`

**Enforce:** `scripts/dev/check-domain-neutral.sh` runs in CI.

### RULE 3 — Single source of truth (Obsidian)
> The Obsidian vault is the truth. SQLite is only a crash-recovery cache. Code does NOT store state in a third place.

### RULE 4 — CEO-friendly language
> Every output to the CEO MUST:
> 1. Be in plain English
> 2. Define a term on first use (e.g. `**ROAS** (revenue / ad spend ratio, e.g. spend $1k earn $4k → ROAS=4x)`)
> 3. Have a TL;DR at the top (3-5 lines a layperson reads in 30 seconds and understands)
> 4. Avoid jargon when a plain word exists (lead → interested customer, churn → customers leaving)

**Enforce:** `core/translator/pipeline.py` (jargon detector → simplifier → TL;DR).

### RULE 5 — Live research with citations
> An agent may search:
> - US/Texas law (statutes, codes, regulations) — `us_law_search`
> - Local regulations — `us_local_regulation`
> - Competitors — `competitor_research`
> - US industry benchmarks — `industry_benchmark`
> - General news — `web_search`
> - US tax (income, self-employment, sales-and-use, franchise) — `tax_calculator`
>
> MUST cite the source (URL + access date). Cache 24h.

**Enforce:** `core/tools/base_tool.py` — `ToolResult.sources: list[str]` + `retrieved_at`.

### RULE 6 — BYOT (Bring Your Own Templates)
> The company can bring its own templates into the vault. Priority order:
> 1. `vault/00-Templates-Custom/<dept>/` (company custom — highest)
> 2. `vault/01-Departments/<dept>/refs/` (pack templates)
> 3. `repo/templates-us/<dept>/` (192 defaults from bb-plugin — lowest)
>
> Supports: `.md`, `.docx`, `.xlsx`. PDF optional.

**Enforce:** `core/obsidian/template_resolver.py` — checks 3 paths in the correct order.

---

## 📊 Summary table

| # | Decision | Locked |
|---|---|---|
| 1 | Setup | A+B Hybrid (manual + wizard) |
| 2 | Departments | Core 13 + Packs + On-demand |
| 3 | MVP packs | F&B + Retail + Tech-SaaS |
| 4 | Auto level | Semi-auto + Brain-first clarification |
| 5 | Storage | Local + Git private |
| 6 | Stack | Python+LangGraph + Obsidian + multi-adapter |
| 7 | Test case | B (marketing campaign) for v1 |
| 8 | Location | `<path>/One Person Company` |

---

## ❓ Open questions (for the CEO to answer at impl time)

1. **Default LLM provider v1** — hardcode Claude Sonnet 4.6, or let the user choose at onboard?
2. **Web search API** — Tavily (free tier 1000/mo) or Serper ($1/1000)?
3. **Spell-check** — v1 or v1.1?
4. **BYOT with PDF + OCR right in v1?** — or only md/docx/xlsx?
5. **Auto-commit Git** — on by default or opt-in via config?
6. **Glossary auto-grow** — on by default or manual approve per term?
7. **CI cost with a real LLM** — use cassette/recording (VCR) or pure mock?
