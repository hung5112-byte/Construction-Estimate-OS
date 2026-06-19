# v0.2.0 — MCP Sampling Architecture

> **Ship date:** 2026-05-06
> **Tag:** `v0.2.0` + `phase-07-mcp-sampling`
> **Goal:** Let bd-business-os run via a Claude Desktop / Code subscription, WITHOUT an ANTHROPIC_API_KEY

## Answer for the Department Head

To the question: "How do we keep 100% of v1 and only change the LLM-call mechanism to use the subscription?"

→ **MCP Sampling protocol**: the MCP server doesn't call the LLM itself; it requests the host (Claude Desktop) to create a completion. The host uses the user's subscription → Anthropic. The response comes back to the server.

## Changes: 4 new files, 0 core files edited

| File | Role |
|---|---|
| `core/llm/providers.py` (extend) | `MCPSamplingProvider` class — routes complete() via MCP `session.create_message()` |
| `core/mcp_server.py` (new) | FastMCP server exposing 7 tools: bd_run, bd_resume, bd_meeting, bd_approve, bd_execute, bd_status, bd_onboard |
| `core/install_mcp.py` (new) | Auto-edit Claude Desktop's `claude_desktop_config.json` (cross-platform: Win/Mac/Linux) |
| `adapters/claude-code/skill.md` (rewrite) | Skill file using the 7 MCP tools instead of the subprocess CLI |

## v1 code UNCHANGED

- `core/agents/` (BaseAgent, Department, Pro/Con, Perspective debators)
- `core/brain/` (Schema, Reader, Memory, GapAnalyzer)
- `core/clarifier/` (QuestionGenerator, ClarificationIO)
- `core/meeting/` (MeetingState, ConditionalLogic, Synthesizer, MeetingGraph with LangGraph)
- `core/obsidian/` (Vault, TemplateResolver, DocWriter, GitSync)
- `core/orchestrator/` (Router, FlowController, PerspectivesCollector, ResearchPhase)
- `core/tools/` (6 tools: web_search, us_law, competitor, benchmark, tax, local_reg)
- `core/translator/` (Glossary, JargonDetector, Simplifier, TLDR, Pipeline)
- `core/cli.py` (CLI mode with an API key still works — fallback)

→ **103 v1 tests still pass + 23 new tests = 126 tests passing.**

## How it works

```
User chats in English in Claude Desktop
  ↓
The `bd-business-os` skill activates
  ↓
Claude (subscription) calls the MCP tool: bd_run(brief, vault)
  ↓ via MCP protocol
core/mcp_server.py:bd_run handler
  ↓ instantiate
FlowController(vault_root, llm=MCPSamplingProvider(ctx.session))
  ↓ run pipeline (Router, GapAnalyzer, ...)
  ↓ when an LLM call is needed:
LLMProvider.complete(messages)  →  MCPSamplingProvider.complete()
  ↓ async session.create_message()
  ↓ via MCP protocol back to the host
Claude Desktop (subscription)
  ↓ thinks
  ↓ returns a response
back through the stack to FlowController
  ↓ continues the pipeline
  ↓ writes vault/02-Tasks/<ts>-<slug>/03-clarification.md
returns to the MCP tool
  ↓ result dict back to the Claude session
Claude shows the Department Head a summary in English
```

## Department Head one-time setup

```bash
pip install bd-business-os         # or pipx install bd-business-os
bd-os install-mcp                  # auto-edit claude_desktop_config.json
# Restart Claude Desktop
bash adapters/claude-code/install.sh    # install the skill (optional)
```

After that: chat naturally in English in Claude Desktop, the skill auto-activates.

## Caveats

1. **Subscription rate limit**: Pro ~45 msg/5h → 1 COMPLEX task/5h. Max ~225 msg/5h → 6-7 tasks/5h.
2. **Sampling support**: Claude Desktop ✅, Claude Code ✅, Claude.ai web ❌ (no MCP).
3. **Latency**: +1-2s/call vs. the direct API (one extra MCP hop).
4. **User approval**: Claude Desktop asks on each sampling by default. Click "Always allow" once.
5. **Model preference**: the server hints `claude-sonnet-4-6`; the host may return a different model.

## Effort

3-5 days FT-equivalent (done in one ~6-hour session).

## Tests breakdown

| File | Tests | Phase |
|---|---|---|
| test_mcp_sampling_provider.py | 5 | T1 |
| test_mcp_server_tools.py | 5 | T2 |
| test_install_mcp.py | 8 | T3 |
| test_mcp_server_e2e.py | 5 | T5 |

Total new in v0.2.0: **23 tests**.
Full suite: **126 passed + 1 skipped** (after T5).

## Resume / debug guide

If a later session hits an MCP error:

1. **Verify install**: `cat ~/.config/Claude/claude_desktop_config.json` (Mac/Linux) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows). Must have a `bd-business-os` entry.
2. **Test server start**: `bd-os-mcp` (or `python -m core.mcp_server`) — should listen on stdio.
3. **Re-install**: `bd-os install-mcp` (idempotent).
4. **Uninstall + clean**: `bd-os uninstall-mcp` → manually edit config → restart.

## Open questions

1. Multi-company active-vault detection: the skill currently takes an explicit `vault` arg; should it auto-detect from cwd?
2. Lite-mode rate limit: should it auto-fallback to `max_debate_rounds=1` when it detects a rate limit?
3. Browser/Web client: Claude.ai web has no MCP — any solution?

---

## Cross-reference

- v1 ship log: `plans/session-log-260506-implementation.md`
- v2 roadmap (cron, Web UI, multi-company): `plans/v2-roadmap.md`
- Current file: `plans/v2-mcp-sampling-260506.md`
