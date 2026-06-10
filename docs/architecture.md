# Architecture

> Technical architecture + 6 RULES + extensibility points. Audience: developers + tech-aware Department Heads.

## 4 layers

```
Layer 1 — ENTRY (Department Head chat)
  Adapters: Claude Code, Cowork, Codex (v2), Antigravity (v2)

Layer 2 — CORE (Python + LangGraph)
  Orchestrator (Router, FlowController) - docs/core/orchestrator/
  Brain (Reader, Schema, GapAnalyzer, Memory) - docs/core/brain/
  Clarifier (QuestionGenerator, ClarificationIO) - docs/core/clarifier/
  Translator (Glossary, Jargon, Simplifier, TLDR) - docs/core/translator/
  Meeting (debate_state, conditional_logic, synthesizer, meeting_graph) - docs/core/meeting/
  Agents (BaseAgent, Pro/Con, Perspective, Department, Registry) - docs/core/agents/
  Tools (web_search, us_law, competitor, benchmark, tax) - docs/core/tools/
  LLM (multi-provider abstraction) - docs/core/llm/

Layer 3 — STATE
  SQLite (LangGraph checkpoint) — crash recovery only
  Obsidian vault (private Git) — single source of truth (RULE 3)

Layer 4 — OUTPUT
  Markdown reports in 02-Tasks/
  .docx/.xlsx in 03-Outputs/
  Append-only decisions log
```

## Standard data flow

```
Department Head brief
  → Brain reader (load 00-Brain/*.md)
  → Router (classify SIMPLE/COMPLEX/STRATEGIC + select departments)
  → Gap analyzer (compare brief vs Brain, RULE 1)
  → Clarifier (ask the Department Head, with Brain citations) — STOP if needed
  → Research phase (tools in parallel, RULE 5)
  → Meeting R1 (perspectives — each department in parallel)
  → Meeting R2 (Pro vs Con, 2-3 rounds)
  → Meeting R3 (Growth/Cautious/Balanced)
  → Synthesizer (decision report, RULE 4)
  → Department Head approves (Stop 1)
  → Execution dispatcher (plan)
  → Department Head approves (Stop 2)
  → DocWriter (.docx/.xlsx into 03-Outputs/)
  → Memory append + Git auto-commit
```

## 6 RULES enforced in code

| Rule | Module | Enforce point |
|---|---|---|
| 1 — Brain-first | docs/core/clarifier/question_generator.py | `if not gaps: return []` |
| 2 — Domain-neutral | docs/scripts/dev/check-domain-neutral.sh | CI fails if it finds bull/bear/trader/ticker |
| 3 — Single source of truth | docs/core/obsidian/vault.py | All I/O through ObsidianVault |
| 4 — Department-Head-friendly language | docs/core/translator/pipeline.py | jargon detector + simplifier + TL;DR |
| 5 — Live research with citations | docs/core/tools/base_tool.py | ToolResult.sources + retrieved_at required |
| 6 — BYOT | docs/core/obsidian/template_resolver.py | Custom > pack > default order |

## Stack

- Python 3.11+
- LangGraph 0.2+ (state graph + checkpointer)
- Pydantic v2 (schema validation)
- Obsidian Markdown (vault format)
- SQLite (checkpoint + tool cache)
- python-docx + openpyxl (output rendering)
- Tavily API (web search + US law/local regulation)
- **MCP Sampling** via the Claude Desktop subscription (default — NO API key needed)
- Anthropic SDK (fallback if running outside MCP)
- Optional: Google Gemini, OpenAI fallbacks

## v0.2.0 architecture: MCP Sampling

```
┌─ Claude Desktop GUI ───────────────────────────┐
│  Department Head chats with Claude Sonnet                  │
│       ↓                                         │
│  Claude calls the MCP tool vn_meeting           │
│       ↓                                         │
│  ┌─ MCP Server (vn-business-os) ─────────────┐ │
│  │  FlowController.run_meeting()             │ │
│  │       ↓                                    │ │
│  │  llm.complete(messages)                    │ │
│  │       ↓                                    │ │
│  │  MCPSamplingProvider                       │ │
│  │       ↓                                    │ │
│  │  ctx.session.create_message(...)  ─────┐  │ │
│  └────────────────────────────────────────┼──┘ │
│                                            ↓    │
│  The sampling request returns to Claude   │    │
│  Claude generates a response              │    │
│  Response back to the MCP server  ←───────┘    │
└─────────────────────────────────────────────────┘
```

→ The plugin runs inside the Claude Desktop session; each LLM call routes through the user's subscription. No Anthropic API key needed.

## Cost budget

| Component | Per COMPLEX task |
|---|---|
| Router classify | ~$0.01 |
| Gap analysis | ~$0.05 |
| Question gen | ~$0.02 |
| Tool calls (3 tools) | ~$0.10 |
| Perspectives (5 departments × 1 turn) | ~$0.30 |
| Pro/Con debate (2 rounds × 2 = 4 turns) | ~$0.40 |
| Perspective debate (3 voices × 1 round) | ~$0.30 |
| Synthesizer | ~$0.20 |
| Translator (simplify + TL;DR) | ~$0.10 |
| **Total** | **~$1.50/task** |
| Limit | <$2.00/task |
