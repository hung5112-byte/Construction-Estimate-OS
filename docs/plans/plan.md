# VN Business OS — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an open-source AI agent OS for a US small business — the Department Head assigns work via chat, agents (departments) debate, and generate reports + .docx/.xlsx documents aligned with US federal + Texas law.

**Architecture:** Python + LangGraph (lift the debate engine from TradingAgents, rename neutral) + Obsidian vault (Markdown + Git private) + multi-tool adapters (Claude Code, Cowork). 4 layers: Entry / Core / State / Output. 6 immutable RULES (Brain-first, Domain-neutral, Single source of truth, Department-Head-friendly language, Live research, BYOT).

**Tech Stack:** Python 3.13, LangGraph 0.2+, LangChain core, Pydantic v2, SQLite, python-docx, openpyxl, PyYAML, Tavily/Serper API, Anthropic SDK (default), google-genai, openai SDK, pytest, ruff, mypy.

**Spec reference:** `docs/superpowers/specs/2026-05-06-vn-business-os-design.md`

---

## Phase Overview

> Historical note (06/09/2026): all 6 phases were completed and the detailed
> per-phase plan files (Vietnamese dev build-logs) were removed during the
> US-localization cleanup. This table is kept as a build-history summary.

| # | Phase | Goal | Status |
|---|---|---|:-:|
| 1 | Foundation | Repo skeleton + Brain layer + 12 dept stubs + vendor 191 templates | ✅ |
| 2 | Debate Engine | Lift meeting_graph from TradingAgents → neutral + checkpointer | ✅ |
| 3 | Orchestrator + Brain-first | Router + Gap analyzer + Clarifier + Flow controller (2 stops) | ✅ |
| 4 | Tools + Translator | 6 live-research tools + translator (jargon + TL;DR) | ✅ |
| 5 | Departments + Packs + BYOT | Full 13 departments + 3 packs + template resolver + doc writer | ✅ |
| 6 | Adapters + E2E + Onboard | Claude Code/Cowork adapter + wizard + test case B pass | ✅ |

## Six RULES (enforced in code)

1. 🔒 **Brain-first clarification** — don't ask the Department Head before reading the Brain
2. 🔒 **Domain-neutral engine** — no trade/finance leak
3. 🔒 **Single source of truth** — the Obsidian vault is the truth
4. 🔒 **Department-Head-friendly language** — plain English + define terms + TL;DR
5. 🔒 **Live research with citations** — search law/competitors/benchmarks, cite the source
6. 🔒 **BYOT (Bring Your Own Templates)** — company custom > pack > default

## Key Dependencies

- Phase 1 → blocks all
- Phase 2 → blocks Phase 3 (the meeting needs the checkpointer + state)
- Phase 3 → blocks Phase 4, 5 (the flow controller integrates everything)
- Phase 4 → blocks Phase 5 (departments use tools + translator)
- Phase 5 → blocks Phase 6 (the E2E test needs all departments)

## File Structure (to create)

See each phase for details. In short:
- `core/` — Python engine (~4800 LoC)
- `departments/` — 12 core departments (+ pack-specific 13-XX) (YAML + agent .md)
- `packs/` — 3 industry packs
- `templates-us/` — 191 templates vendored from bb-plugin
- `vault-template/` — Obsidian scaffold
- `adapters/` — Claude Code + Cowork
- `tests/` — unit + integration + e2e
- `docs/` — getting started + how-to-create-pack

## Definition of Done v1

- [ ] Public repo, complete English README
- [ ] `pip install -e .` works on Win/Mac/Linux
- [ ] Wizard generates a valid vault
- [ ] Test case B (a marketing campaign) runs E2E < 25 min, < $2
- [ ] 12 core departments (+ pack-specific 13-XX) have real agents
- [ ] 3 packs (F&B, Retail, Tech-SaaS) pass their own tests
- [ ] BYOT demo works
- [ ] 6 RULES enforced + tested
- [ ] Claude Code + Cowork adapter E2E
- [ ] `docs/getting-started.md` for a non-tech Department Head
