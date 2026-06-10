# P0 Fix Report — 2026-05-07

> **Answer for the user:** Checked the whole repo + fixed 7 P0 bugs. Tests: 180 pass. Commit `a3a7638`.

---

## Issues the user reported — verified

### ❌ "Vault setup doesn't ask for a Tavily/Brave API key"
**CORRECT.** The old `core/onboard.py` had no place to enter an API key. The `.vncoderc` schema had no key field. The CLI wizard `scripts/onboard.py` only asked about packs + BYOT.

→ **Fixed:**
- New `onboard_vault(api_keys={...})` param
- CLI wizard asks for `TAVILY_API_KEY` + `ANTHROPIC_API_KEY` (password input)
- MCP tool `vn_onboard` gains 4 params: `tavily_api_key`, `anthropic_api_key`, `google_api_key`, `openai_api_key`
- Saved to `<vault>/.env` (auto-adds `.env` to `.gitignore`)

### ❌ "Search functionality doesn't work"
**PARTIALLY CORRECT:**
- Search WAS wired into `vn_meeting` (calls `ResearchPhase.run()` before the meeting)
- BUT the 4 Tavily tools (web/law/local/competitor) hit auth errors without a key → caught silently → the meeting continued with empty findings → a silent RULE 5 violation
- The 2 tools that need no key (`industry_benchmark`, `tax_calculator`) still worked

→ **Fixed:**
- The 4 Tavily tools now have an `is_available()` check
- When the key is missing: return `ToolResult(data={"skipped": True}, notes="Missing TAVILY_API_KEY...")` instead of crashing
- ToolRouter only plans tools that have credentials (no wasted LLM tokens)
- `vn_status` reports `tools_live` + `tools_skipped` so the Department Head knows up front

---

## 15 bugs found in the audit (see `audit-260507-repo-completeness.md`)

### P0 (7 bugs) — FIXED in this commit

| # | File | Bug | Fix |
|---|---|---|---|
| 1 | `flow_controller.py:167` | `departments_root` pointed at the REPO instead of the vault → BYOT meeting broken | Changed to `vault.root / "01-Departments"` |
| 2 | `flow_controller.py:approve_decision` | Stub "(TODO Phase 6)" | Real LLM-generated execution plan with tasks/risks/KPIs/templates table |
| 3 | `flow_controller.py:execute` | Stub README placeholder | Parse template table → TemplateResolver → DocWriter renders .docx/.xlsx → saved to `03-Outputs/` |
| 4 | 4 Tavily tools | Crash when key missing, silent failure | `is_available()` + `skipped_result()` graceful |
| 5 | `core/onboard.py` | Never asked for API keys | New `api_keys` param + save to `<vault>/.env` |
| 6 | `core/install_mcp.py` | Did not inject env into mcpServers | `--vault` flag reads `<vault>/.env` → injects `env: {TAVILY_API_KEY: ...}` |
| 7 | `tool_router.py` | Planned tools without credentials | `available_tools` filter |

### P1 (5 bugs) — Pending a later phase

- `PerspectivesCollector` ignores per-agent enriched prompts (still uses the generic template)
- 12 dept dirs but the plan/router prompt said "13 core" — off-by-one
- `MCPSamplingProvider` has no retry/timeout on rate limit
- LangGraph `checkpointer=False` hardcoded → a mid-meeting crash is unrecoverable
- `GitSync` swallows exceptions silently

### P2 (3 bugs) — Polish later

- Multi-turn `vn_onboard` via MCP elicitation
- Router JSON mode for deterministic parsing
- `tool_cache.db` per-vault (currently `~/.vn-business-os/`)

---

## Files changed (38 files, +11,148 lines)

### Code
- `core/utils/config.py` — `load_vault_env`, `save_vault_env`, `apply_vault_env_to_os`
- `core/tools/base_tool.py` — `is_available()` + `skipped_result()` helpers
- `core/tools/{web_search,vn_law_search,vn_local_regulation,competitor_research}.py` — graceful skip
- `core/tools/tool_router.py` — filter by available_tools
- `core/orchestrator/research_phase.py` — `list_available_tools` / `list_skipped_tools`
- `core/orchestrator/flow_controller.py` — departments_root + approve_decision + execute (real impl)
- `core/orchestrator/execution_planner.py` — NEW (LLM generates 08-execution-plan.md)
- `core/orchestrator/document_executor.py` — NEW (DocWriter + TemplateResolver wired)
- `core/onboard.py` — api_keys param
- `core/mcp_server.py` — vn_onboard 4 key params, vn_status tool availability, _make_fc auto-loads env
- `core/install_mcp.py` — vault_path env injection
- `core/cli.py` — install-mcp --vault flag
- `scripts/onboard.py` — interactive API key prompts (password input)

### Tests (+34 new)
- `tests/unit/test_env_and_tool_skip.py` — 11 tests
- `tests/unit/test_execution_planner.py` — 9 tests
- `tests/unit/test_document_executor.py` — 9 tests
- `tests/unit/test_install_mcp.py` — 2 new (env injection)
- `tests/e2e/test_b_campaign_high_income.py` — 4 new + mock updates

---

## Usage (updated)

### Set up a new vault (via Claude Desktop)
```
In chat: "Set up a vault for company XYZ at the path F:/.../my-company.
Install the F&B pack. My Tavily API key is: tvly-xxx"
```
→ Claude calls `vn_onboard(vault=..., packs=["fnb"], tavily_api_key="tvly-xxx")`
→ The key is saved to `<vault>/.env`, and `.gitignore` excludes the file

### After onboarding, inject env into the MCP server
**Important step:** after saving the key, re-install MCP so Claude Desktop launches with the env:
```bash
vn-os install-mcp --vault "F:/.../my-company"
```
→ Reads `<vault>/.env` → injects `env: {TAVILY_API_KEY: ...}` into `claude_desktop_config.json`
→ Restart Claude Desktop

### Verify
In chat: "vn_status vault F:/.../my-company"
→ Returns `tools_live: [web_search, vn_law_search, ...]` (when the key exists)
→ Or `tools_skipped: [{name: web_search, reason: Missing TAVILY_API_KEY}]` when missing

---

## Tests

**Before:** 146 passed + 1 skipped
**After:** 180 passed + 1 skipped (+34 new, 0 regressions)

```
$ python -m pytest tests/ -q
180 passed, 1 skipped in 14.33s
```

---

## RULES Compliance Matrix (updated after the fix)

| RULE | Before | After |
|---|---|---|
| 1. Brain-first | ✓ | ✓ |
| 2. Domain-neutral | ✓ | ✓ |
| 3. Single source of truth | Partial | ✓ (departments from the vault) |
| 4. Department-Head-friendly language | Partial | Partial (P1.6) |
| 5. Live research with citations | **DEGRADED** | ✓ (graceful skip + status report) |
| 6. BYOT | **BROKEN** | ✓ (meeting + execute both respect the vault) |

---

## Next steps for the user

1. **Restart Claude Desktop** to load the new MCP server (8 tools with fixes)
2. **Test a new vault setup** with the syntax: "Set up a vault... my TAVILY key is..."
3. **Re-install MCP with --vault** for env injection:
   ```
   vn-os install-mcp --vault "F:/path/to/vault"
   ```
4. **Verify with vn_status** to see how many `tools_live` there are

## Pending (P1 + P2 — next phase)

See the "Priority Fix List" section of `audit-260507-repo-completeness.md`. A phase-07 could clean up the rest:
- Per-agent prompts wired into PerspectivesCollector
- 13th-department resolution
- Retry/timeout in MCPSamplingProvider
- Re-enable the LangGraph checkpointer
- Multi-turn onboard via MCP elicitation
- Citation validator
