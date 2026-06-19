# P1 Fixes Report — 2026-05-07

> **Status:** ✅ DONE. Tests **243 passed**, 1 skipped (+63 vs. P0). Commit `8868986`.

---

## 7 P1 bugs — Fixed

### P1.1 — PerspectivesCollector uses per-agent prompts

**Before:** 38 agent prompts were enriched (the CFO knows accounting, the head-chef knows food cost, ...) but `PerspectivesCollector` ignored them, still using the generic template `PERSPECTIVE_PROMPT.format(dept_name=...)` → the Phase 5 effort wasted.

**After:**
- Load `AgentDefinition` for `dept.default_speaker` via `AgentLoader`
- Lookup path: `<departments_root>/<dept>/agents/<default_speaker>.md` → `<vault>/01-Departments/<dept>/agents/<default_speaker>.md`
- Use `agent_def.system_prompt` (the body of the .md file) as the system message
- Graceful fallback: if the agent file is missing → use the generic template (doesn't break the flow)

**Tests:** 8 new tests (`test_perspectives_collector_enriched.py`)

---

### P1.2 — Reconcile "12 vs 13" departments

**Before:** the plan + router prompt + README said "13 core departments" but there were actually only 12 directories. Off by 1 → the LLM gets confused.

**After:**
- `plans/plan.md`: "13 core departments" → "12 core (+ pack-specific 13-XX)"
- `core/agents/registry.py` docstring updated
- Router prompt clarified: "01-..12-... + pack-specific 13-XX"

---

### P1.3 — MCPSamplingProvider retry + timeout

**Before:** when Anthropic returned 429 (subscription quota exhausted) or timed out → a single failure killed the whole `bd_meeting` flow. No retry.

**After:**
- `max_retries=3`, `timeout_seconds=120`, exponential backoff
- `_is_retryable()` recognizes: rate limit / 429 / timeout / connection / 503 / 502
- Non-retryable errors (e.g. `ValueError`) fail fast without retry

**Tests:** 3 new tests (rate-limit retry, non-retryable, max-retries giveup)

---

### P1.4 — LangGraph checkpointer opt-in

**Before:** `checkpointer=False` hardcoded in `flow_controller.py` with the comment "to avoid SQLite issues" — can't recover from a mid-meeting crash.

**After:**
- `meeting.use_checkpointer` config option (default `False` to keep old behavior)
- When the user enables `meeting.use_checkpointer: true` in `.vncoderc`:
  - Try to init `make_checkpointer()` (SqliteSaver)
  - If it fails (LangGraph version mismatch, SQLite locked, ...) → log a warning, fall back off
- **Note:** still needs deeper investigation to find the SQLite issue's root cause and turn it on by default. Opt-in is the safest for now.

---

### P1.6 — Translator scope via config

**Before:** the translator only applied to the final report. Clarification questions, perspective outputs, debate transcripts still used technical jargon → hard for the Department Head.

**After:**
- `translator_mode` config: `"off"` | `"final_only"` (default) | `"all_intermediate"`
- `"all_intermediate"`: wraps perspectives + pro/con outputs through the translator before appending to state
- Default stays `"final_only"` to keep old behavior — the Department Head opts in via `.vncoderc`
- Performance: `"all_intermediate"` increases LLM cost (each output → 1 translator call), so the user opts in deliberately

**Tests:** 12 new tests (`test_translator_mode_config.py`)

---

### P1.7 — GitSync logs instead of swallowing silently

**Before:** `try: GitSync.commit(...) except: pass` → the Department Head doesn't know why a Git commit failed (permission, no git, conflict, ...).

**After:**
- `FlowController._log_warning()` writes to `<vault>/.bd-business-os.log`
- Format: `[YYYY-MM-DD HH:MM:SS] WARN: Git commit failed (Stop 1): <error message>`
- The Department Head opens the log to see the exact reason

---

### P1.8 — Citation validator post-synthesizer

**Before:** the Synthesizer relied on the LLM to self-cite — no validation → it could fabricate figures/law with no source.

**After:** `core/orchestrator/citation_validator.py`
- Detects numeric claims (`%`, `USD`, `$`, `million`) without a `[source: ...]` marker
- Detects legal references (statute/code/regulation citations) without a cite
- Recognizes Brain file refs (`strategy.md`, `laws.md`, ...) as valid citations
- Common-knowledge phrases are exempted (e.g. "the holidays are a big spending season")
- Appends a `## ⚠️ Warning: claims missing a source` section to the decision report if any are found
- Idempotent: re-running doesn't append duplicates
- Wired into `flow_controller.run_meeting()` right after the Synthesizer writes `07-decision-report.md`
- The flag count appears in `FlowResult.message`

**Tests:** 40 new tests (`test_citation_validator.py`)

---

## Files changed

### Core
- `core/orchestrator/perspectives_collector.py` — full rewrite (vault_root param + AgentLoader integration)
- `core/orchestrator/flow_controller.py` — translator wrap + CitationValidator wire + `_log_warning` + checkpointer opt-in
- `core/orchestrator/citation_validator.py` — **NEW** (CitationValidator + CitationFlag + regex heuristics)
- `core/llm/providers.py` — retry + timeout
- `core/utils/config.py` — TranslatorMode + use_checkpointer fields
- `core/agents/registry.py` — docstring update
- `plans/plan.md` — "12 vs 13" reconcile

### Tests (+63 new)
- `tests/unit/test_perspectives_collector_enriched.py` — 8 tests
- `tests/unit/test_translator_mode_config.py` — 12 tests
- `tests/unit/test_citation_validator.py` — 40 tests
- `tests/unit/test_mcp_sampling_provider.py` — +3 tests (retry behavior)

---

## Tests

| | Before P1 | After P1 |
|---|---|---|
| Passed | 180 | **243** |
| Skipped | 1 | 1 |
| Net new | — | +63 |
| Regressions | — | 0 |

```
$ python -m pytest tests/ -q
243 passed, 1 skipped in 17.68s
```

---

## How to use the new options

### Translator mode (Department-Head-friendly language across the whole flow)

Edit `<vault>/.vncoderc` (or `~/.vncoderc`):

```yaml
translator_mode: all_intermediate
```

→ Every output (perspectives, debate, final report) is simplified to Department-Head-friendly language. LLM cost rises (~2-3x) but it's much easier to understand.

### Checkpointer (crash recovery)

```yaml
meeting:
  use_checkpointer: true
```

→ LangGraph saves the debate state to `~/.bd-business-os/checkpoints.db`. A mid-meeting crash → can resume (verify with your specific LangGraph version). If init fails, the plugin falls back off + logs.

### View log warnings

```powershell
Get-Content "F:\.../my-vault/.bd-business-os.log" -Tail 20
```

---

## Remaining — P2 (nice-to-have)

See `audit-260507-repo-completeness.md` section P2:
- Multi-turn `bd_onboard` via MCP elicitation
- Router JSON-mode
- `tool_cache.db` per-vault
- Real-LLM E2E test in CI
- PackLoader integration or removal
- Slug handling
- Brain context filter per agent
- MCP `tools_changed` notification

P2 is not blocking — the plugin is production-ready for beta testing with the current P0 + P1.

---

## Next steps for the user

1. **Restart Claude Desktop** to load the new MCP server
2. **(Optional) Enable translator mode all_intermediate:**
   - Edit `<vault>/.vncoderc`, add `translator_mode: all_intermediate`
3. **Test the full flow:**
   - Setup vault → bd_run → bd_resume → bd_meeting → bd_approve → bd_execute
   - Check whether `07-decision-report.md` has a "⚠️ Warning: claims missing a source" section
   - Check that `03-Outputs/<task>/*.docx` is rendered
4. **Report any bugs** — ready to keep fixing
