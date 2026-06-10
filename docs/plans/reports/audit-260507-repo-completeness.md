# Repo Audit — Completeness vs Plans

**Audited:** 2026-05-07
**Auditor:** code-reviewer (Staff Engineer mode)
**Scope:** core/, departments/, packs/, adapters/, tests/, plans/

---

## Executive Summary

**Overall status:** **Has Gaps — runs but multiple shipping promises broken**

Tests pass (146/147), MCP server boots, end-to-end mocked test of debate works. But several user-facing features advertised in plans + skill.md are **stubbed or silently broken**:

### Top 3 critical issues
1. **Search functionality is wired but un-credentialed** — 4 of 6 tools (web_search, vn_law_search, vn_local_regulation, competitor_research) require `TAVILY_API_KEY` env var. `onboard_vault()` never asks for it. `install_mcp.py` never injects it into `claude_desktop_config.json -> env`. Live research will fail in real Claude Desktop runs the moment ToolRouter chooses any Tavily-backed tool. Crash mode: `tavily.TavilyClient(api_key="")` raises auth error → ResearchPhase swallows into `error` field per query → meeting continues with empty findings, RULE 5 violated silently.
2. **`vn_approve` and `vn_execute` are stubs** — `flow_controller.approve_decision()` writes a "(TODO Phase 6)" placeholder; `flow_controller.execute()` writes a `README.md` saying "(TODO Phase 6: render .docx/.xlsx via DocWriter)". DocWriter + TemplateResolver fully implemented in `core/obsidian/` but **never wired**. Phase 5 + 6 deliverable "DN-VN .docx/.xlsx output" does not exist. `skill.md` Step 7 advertises an action that doesn't run.
3. **Meeting reads departments from REPO not VAULT** — `flow_controller.run_meeting:167` hard-codes `Path(__file__).parent.parent.parent / "departments"`. Custom packs/BYOT departments installed under `<vault>/01-Departments/` are NEVER loaded as participants. RULE 6 (BYOT) broken at meeting layer. `PackLoader` class defined but imported nowhere in production flow.

### Top 3 strengths
1. **Engine debate solid** — Pro/Con + 3 perspective debators + Synthesizer + LangGraph state machine implement TradingAgents pattern correctly with full neutral renaming. Domain leakage test (`test_domain_neutral.py`) enforced.
2. **Brain layer clean** — `BrainReader` + `GapAnalyzer` + `QuestionGenerator` + `Clarifier` chain works end-to-end with citations, idempotent, well-tested (~30 tests).
3. **MCP sampling architecture sound** — `MCPSamplingProvider` correctly splits system role into `system_prompt` kwarg (recent fix), handles async/sync coroutines, falls back gracefully for mocks. 8 MCP tools registered.

---

## Phase-by-Phase Coverage

### Phase 1 Foundation: **PARTIAL**
- Implemented: pyproject, README, vault-template, BrainReader/Schema/GapAnalyzer/Memory, 12 dept stubs + agents, 191 templates vendored.
- Missing: Plan promised **13 dept core**; only **12 dirs** (`01-governance`..`12-growth`) — no 13th department exists. Plan footnote claims "13" repeatedly; routing prompt also says "13".
- Bugs: none in this layer.

### Phase 2 Debate Engine: **DONE**
- Implemented: MeetingState, conditional_logic, checkpointer (sqlite saver), Pro/Con/Perspective debators, Synthesizer, MeetingGraph (LangGraph). Neutral rename enforced + tested.
- Missing: nothing material.
- Bug: `meeting_graph.py:173` calls `MeetingGraph(checkpointer=False)` — disables persistent state across vn_meeting invocations. Comment says "to avoid SQLite issues" but no follow-up issue. Resume after a crash mid-meeting impossible.

### Phase 3 Orchestrator + Brain-first: **PARTIAL**
- Implemented: Router, GapAnalyzer integration, QuestionGenerator, ClarificationIO, FlowController (run/resume_after_clarification/run_meeting).
- Missing: `resume_after_clarification` returns `PAUSE_DECISION_REPORT` with message "Phase 4+5 will wire research + meeting" — meaning the **resume does not auto-trigger meeting**. Department Head/AI must explicitly call `vn_meeting`. Skill.md docs this correctly so functionally OK, but contradicts plan's "2-stop flow" idea (a 3rd manual step exists).
- Bug: `flow_controller.run` calls `Router(rules_path=classifier_rules.yaml)` — no error handling if YAML malformed.

### Phase 4 Tools + Translator: **PARTIAL — DEGRADED**
- Implemented: BaseTool, ToolCache, ToolRouter, 6 tools (web/law/local/competitor/benchmark/tax), Translator pipeline (Glossary + JargonDetector + Simplifier + TLDR), `terms_dictionary.yaml`.
- Missing/Broken:
  - **No API key plumbing** (see Search Audit below). 4 Tavily tools fail silently when key absent.
  - No fallback when Tavily import fails (e.g. user without `tavily` extra installed). `from tavily import TavilyClient` happens lazily inside `run()` per tool — ImportError propagates.
  - `industry_benchmark` data path hardcoded — no graceful behavior if `data/benchmarks-vn.yaml` missing.
- Bug: `tool_router.plan()` `re.search(r"\{.*\}", raw, re.DOTALL)` — first `{` to last `}` — works but if the LLM emits multiple JSON objects (e.g. example + answer), parses wrong block. No JSON-mode requested.

### Phase 5 Departments + Packs + BYOT: **PARTIAL**
- Implemented: 12 departments with agent .md prompts, 3 packs (fnb/retail/tech-saas), `DepartmentLoader`, `PackLoader`, `TemplateResolver`, `DocWriter`.
- Wired: Department prompts loaded for `name_vn` only — **enriched per-agent prompts not used in PerspectivesCollector** (uses generic `PERSPECTIVE_PROMPT` template instead).
- Missing/Broken:
  - `PackLoader` is dead code (no imports outside file).
  - `DocWriter` + `TemplateResolver` not wired into `flow_controller.execute()`.
  - BYOT meeting integration broken (departments_root hard-coded to repo).
  - Pack `adds_departments` like `13-kitchen` (fnb), `13-warehouse` (retail) installed to vault but `Router` prompt still hardcodes `13-XX` as placeholder, depending on LLM to pick correct codes from `active_departments` heuristic.

### Phase 6 Adapters + E2E + Onboard: **PARTIAL**
- Implemented: `scripts/onboard.py` (CLI wizard), `core/onboard.py` (lib), `adapters/claude-code/skill.md`, `adapters/claude-cowork/`, MCP install/uninstall, E2E `test_b_campaign_high_income.py` (mocked LLM).
- Missing/Broken:
  - Wizard does NOT prompt for **any** API keys (Anthropic, Tavily, Google, OpenAI). User must manually `export TAVILY_API_KEY=...` AFTER onboard.
  - When MCP server launched by Claude Desktop, it inherits Claude Desktop process env — typically empty for these keys. Result: subscription-based LLM works (via MCP sampling), but tools requiring Tavily silently 401.
  - `claude-cowork` adapter has shell scripts but no integration test.
  - `test_real_llm.py` exists but skipped/optional (no proof real LLM run passes E2E in CI).
  - `vn_approve` and `vn_execute` stubs (see Critical issue #2) → E2E test only verifies up to `07-decision-report.md`; "produces .docx/.xlsx" acceptance criterion in `plan.md` Definition of Done not validated.

---

## Search/Research Audit (CRITICAL — addresses user concern)

### Tools available
6 registered in `core/orchestrator/research_phase.py:TOOL_REGISTRY`:
- `web_search` — Tavily
- `vn_law_search` — Tavily restricted to thuvienphapluat.vn etc.
- `vn_local_regulation` — Tavily restricted to chinhphu.vn etc.
- `competitor_research` — Tavily
- `industry_benchmark` — local YAML curated data (no API key)
- `tax_calculator` — pure Python compute (no API key)

### API key plumbing
- All 4 Tavily tools: `os.getenv("TAVILY_API_KEY", "")` (default empty string).
- `core/utils/config.py:Config` has NO field for API keys; `.vncoderc` contains only `vault_path`, `packs`, `version`.
- `core/onboard.py:onboard_vault` — never prompts, never writes API key anywhere.
- `scripts/onboard.py` interactive wizard — only prompts pack codes + BYOT path, **not API keys**.
- `core/install_mcp.py:install` — writes `mcpServers[name] = {command, args}` only; **does NOT set `env: {...}`**, so MCP server inherits Claude Desktop process env (typically lacks TAVILY_API_KEY on Windows/macOS unless user set it system-wide before launch).
- README.md tells user to `export TAVILY_API_KEY=...` but this is shell-scoped — Claude Desktop GUI launch ignores shell rc on macOS/Windows.

### Actually called in flow? — Trace
1. Department Head calls `vn_run(brief, vault)` → `FlowController.run()`. **Does NOT call ResearchPhase**. Only Router + GapAnalyzer + QuestionGenerator. Returns `PAUSE_CLARIFICATION` or `PAUSE_DECISION_REPORT`.
2. Department Head answers → `vn_resume(task_folder)` → `resume_after_clarification()`. **Does NOT call ResearchPhase either**. Just normalizes answers and returns `PAUSE_DECISION_REPORT`.
3. Department Head/AI calls `vn_meeting(task_folder)` → `run_meeting()` — THIS calls `ResearchPhase.run()` (line 159-164) BEFORE building meeting graph.
4. Inside ResearchPhase: `tool_router.plan(brief, brain_summary)` asks LLM which tools to run → `TOOL_REGISTRY[name]()` instantiates → `tool.run(query)`.
5. Each Tavily tool: `from tavily import TavilyClient` + `TavilyClient(api_key="")` → on `client.search(...)` → 401 / network error → caught by ResearchPhase try/except → recorded as `{"query": q, "error": str(e)}` in findings.
6. Synthesizer reads `state["research_findings"]` and stringifies first 3000 chars — but if every entry is `{"error": ...}`, the report has no real research, RULE 5 silently violated. Department Head sees decision report citing only Brain + LLM "common knowledge".

**Conclusion:** Search IS in the flow, but only when `vn_meeting` runs, AND only succeeds for `industry_benchmark`/`tax_calculator` without API key.

User's observation #2 (flow goes straight into meeting without research) — **partially correct**:
- Research happens in `vn_meeting`, not as separate stage. So if AI calls `vn_meeting` immediately after clarification, research runs.
- BUT if AI in Claude Desktop bypasses `vn_meeting` (writes the decision itself, ignoring the MCP tool flow), no research at all. The skill.md is clear that vn_meeting must be called, but enforcement depends on AI obedience.
- Also: if Tavily key missing, even when `vn_meeting` runs, all web research fails silently.

### Onboard prompts for keys?
**NO.** The CLI wizard only asks pack selection + BYOT path. The MCP `vn_onboard` tool exposes only `vault` and `packs` parameters. The `.vncoderc` schema has no `api_keys` section.

### Issues
- No graceful degradation: tools should detect missing key and return `ToolResult(data={"skipped": "no API key"}, sources=[], notes="Set TAVILY_API_KEY")` instead of crashing into Tavily client.
- ToolRouter prompt does not know which tools are credentialed; will plan tools that will fail.
- No way for Department Head to provide key without editing shell rc / claude_desktop_config.json by hand.
- `vn_status` doesn't report tool availability — can't tell Department Head upfront "live research disabled, only benchmark+tax work".

### Recommendations
1. **Add API key step to onboard** — both CLI wizard and MCP `vn_onboard` should accept optional `tavily_api_key` arg, save to `<vault>/.env` (gitignored) or `~/.vn-business-os/keys.yaml`.
2. **Tools must check key + skip gracefully** — `if not self.api_key: return ToolResult(data={"skipped": True}, sources=[], notes="Missing TAVILY_API_KEY")`. ToolRouter should also be made aware via a method like `available_tools()` that filters by credential presence.
3. **`install_mcp.py` should support env injection** — read keys from `~/.vn-business-os/keys.yaml` and write `env: {TAVILY_API_KEY: ...}` into mcpServers entry so Claude Desktop launches MCP with proper env.
4. **`vn_status` should report tool availability** — return `{"tools_live": [...], "tools_skipped": [{"name":..., "reason":...}], ...}`.
5. **Skill.md should include preflight** — instruct AI to call `vn_status` before `vn_meeting`, warn Department Head if `tools_skipped` includes critical ones for the task domain (e.g. legal advice without `vn_law_search`).

---

## Onboarding Audit

### What `core/onboard.py` does
1. Copy `vault-template/` → `<vault>`
2. Copy 12 core depts → `<vault>/01-Departments/`
3. Install selected packs (adds 13-XX departments + brain-template overrides)
4. Optional BYOT import (keyword classifier into department subfolders)
5. Git init (best-effort)
6. Generate wikilinks (Brain hub, Dept hubs, agent cross-links)
7. Save `.vncoderc` with `{vault_path, packs, version: "0.1.0"}`

### What it does NOT do
- Not prompt for company name, industry (used only as pack code), Department Head name, fiscal year start, etc.
- Not prompt for or save **any API key** (Anthropic, Tavily, Google, OpenAI).
- Not validate vault writability before copying.
- Not check `vault-template/` integrity (e.g. all expected `00-Brain/*.md` present).
- Not set up `.gitignore` rules for sensitive files (the template has `.gitignore` but never patched with company-specific exclusions).
- Not initialize the Brain content from Department Head answers — Brain `.md` files left as placeholder template, Department Head must edit manually after.

### MCP `vn_onboard` issues
- Synchronous file ops in MCP request thread — `shutil.copytree` of 191 templates can take seconds. Comment in code says "fixes Claude Desktop timeout issue" via no-subprocess approach, but actual file IO blocking is unaddressed.
- No `elicitation` support for follow-up Department Head questions during onboard (e.g. "Which industry?", "Already have templates?"). MCP elicitation protocol ignored — `vn_onboard` is one-shot.
- Returns `next_steps` text but no structured "needs_action" so AI can't drive multi-turn onboard.

### Recommendations
- Add API key step (see Search Audit recs).
- Run `shutil.copytree` in `asyncio.to_thread` if elicited from async MCP context.
- Add `vn_onboard_step1`, `vn_onboard_step2` tools for multi-turn wizard, OR use MCP elicitation (recent FastMCP supports it).
- `vn_status` should warn if Brain files still contain template placeholder text (e.g. `<fill in ICP>`).

---

## Agent / Flow Integrity

### Agent prompts
- 12 dept folders × multiple agent .md files each — frontmatter schema rich (`expertise`, `required_refs`, `required_tools`, `model_override`, `temperature`).
- `AgentLoader` parses correctly + tested.
- **BUT** `PerspectivesCollector` ignores per-agent prompts — uses generic template `PERSPECTIVE_PROMPT.format(dept_name=dept.name_vn)`. The rich agent prompts are never used in real meetings.
- `routing_rules.keywords → agent` in `department.yaml` also unused — there's no code path that picks specific agent within department based on brief.

### Multi-turn debate
- Pro/Con: state machine correctly alternates in `conditional_logic.next_pro_con_node` until `count >= max_debate_rounds` (default 2).
- Perspective: Growth → Cautious → Balanced cycle until `max_perspective_debate_rounds` (default 1).
- Both honor `state["judge_decision"]` for early exit but no code sets it — judge feature inert.

### Synthesizer
- Reads all perspectives + debates + research → invokes LLM with structured prompt.
- Output stuffed into `final_report` field. Translator pipeline applied (RULE 4) before writing `07-decision-report.md`.
- No source-citation enforcement check — synthesizer relies on LLM to cite, no post-validation.

### Brain context handling
- `BrainContext.model_dump()` shoved entirely into `state["brain_context"]` and yaml-dumped into every agent's system message — large for big DNs. No per-agent filtering.
- Brain summary used in ToolRouter sliced to 3000 chars; in Synthesizer also 3000. Reasonable but no logging when truncated.

---

## v2 MCP Audit

### 8 MCP tools status
| Tool | Status | Notes |
|---|---|---|
| `vn_run` | OK | calls FlowController.run; returns task_folder + stage |
| `vn_resume` | OK | reads checkboxes; doesn't trigger meeting |
| `vn_meeting` | OK with caveats | runs Research+Meeting; tool key issues + departments_root bug |
| `vn_approve` | **STUB** | writes "(TODO)" placeholder |
| `vn_execute` | **STUB** | writes README.md only |
| `vn_status` | OK | no LLM, returns Brain summary + tasks |
| `vn_onboard` | OK | sync file copy, blocks request thread; no API key prompt |
| `vn_upgrade` | OK | refresh agent prompts + dept yaml + Brain aliases |

### Sampling provider
- Just got `system role` fix (commit d4c9a33) — `_split_system` correctly extracts system content.
- `_run_sync(coro)` uses ThreadPoolExecutor + `asyncio.run` when called inside running loop — works but spawns thread per call (perf cost, ~50ms each).
- `_extract_text` handles both `TextContent` object and dict shapes — robust.
- No retry on rate limit (Anthropic 429 from MCP host's subscription quota) — single failed call kills whole flow.
- No timeout — long sampling can hang indefinitely.

### Real Claude Desktop bugs (potential, not yet observed)
- `vn_meeting` runs `ThreadPoolExecutor` for parallel research + parallel perspectives. Inside `MCPSamplingProvider.complete`, sync→async bridging spawns threads per call. With 5 perspectives + N research queries running concurrently, easy to oversubscribe MCP host's sampling rate limit. No backpressure.
- LangGraph state checkpointer hardcoded to disabled (`checkpointer=False`). Crash mid-meeting → all progress lost. No way to resume.

### Tests
- `test_mcp_sampling_provider.py` — unit tests with mocks
- `test_mcp_server_tools.py` integration with FastMCP test harness
- `test_mcp_server_e2e.py` end-to-end via stdio transport
- `test_real_llm.py` — gated by env var (real Anthropic key) — likely not run in CI

---

## Six RULES Compliance Matrix

| RULE | Status | Evidence | Gap |
|---|---|---|---|
| 1. Brain-first | ENFORCED | `flow_controller.run` reads Brain → GapAnalyzer → only THEN clarification | None |
| 2. Domain-neutral | ENFORCED | `test_domain_neutral.py` checks no Bull/Bear/trade/portfolio in outputs; debate state uses `pro_history`/`con_history`/`growth_history` etc. | None |
| 3. Single source of truth | PARTIAL | Obsidian vault is canonical, all writes go through ObsidianVault. BUT meeting reads dept defs from REPO not VAULT — divergence possible after upgrade. | Fix departments_root to vault path |
| 4. Department-Head-friendly language | PARTIAL | TranslatorPipeline applied to final report. BUT clarification questions, perspectives, debate transcripts — none simplified, all surface to Department Head if AI shows them | Apply translator to clarification UI text + perspective summaries |
| 5. Live research with citations | **DEGRADED** | ResearchPhase + ToolRouter wired, sources field on every ToolResult — but Tavily tools silently fail without API key. Synthesizer relies on LLM to cite, no validation | API key plumbing + skip-gracefully + cite validator |
| 6. BYOT | **BROKEN at meeting layer** | onboard imports BYOT files into `00-Templates-Custom/`, but template_resolver never loaded by execute() (which is stubbed). Meeting also bypasses vault depts. | Fix departments_root + wire template_resolver into execute |

---

## Critical Bugs Found

1. **`core/orchestrator/flow_controller.py:167`** — `departments_root = Path(__file__).parent.parent.parent / "departments"`. Hardcoded repo path; ignores `<vault>/01-Departments/`. Custom packs/BYOT depts not in meeting.
2. **`core/orchestrator/flow_controller.py:241-252`** — `approve_decision()` writes "(TODO Phase 6)" stub. Plan promises real execution-plan generation.
3. **`core/orchestrator/flow_controller.py:254-267`** — `execute()` writes README placeholder. DocWriter never invoked.
4. **`core/tools/web_search.py:14` (and 3 sibling tools)** — `os.getenv("TAVILY_API_KEY", "")` defaults to empty string. `TavilyClient(api_key="")` constructor or first `client.search` call raises auth error. Caught by ResearchPhase try/except and silently turned into `{"error": ...}` per query. RULE 5 violated invisibly.
5. **`core/onboard.py:onboard_vault`** — accepts no API key parameters. `.vncoderc` schema has no key fields. Department Head has no in-flow way to provide credentials.
6. **`core/install_mcp.py:install`** — does not write `env: {...}` into mcpServers entry. MCP server launched by Claude Desktop inherits empty env on Windows/macOS GUI launch.
7. **`core/orchestrator/perspectives_collector.py:54`** — uses generic `PERSPECTIVE_PROMPT`, ignores per-agent enriched prompts loaded by `AgentLoader`. Phase 5 enrichment effort not effective at runtime.
8. **`core/agents/pack_loader.py:29`** — `PackLoader` class defined, never imported elsewhere. Dead code or missing wiring.
9. **`core/meeting/meeting_graph.py:173` (referenced from flow_controller)** — `checkpointer=False` hardcoded with comment "to avoid SQLite issues". Crash mid-meeting unrecoverable.
10. **`core/orchestrator/flow_controller.py:202-207`** — `GitSync.commit` called with `try/except: pass`. Silently swallows all errors including config errors, permission errors, no-git-installed errors. Department Head never told commit failed.
11. **`departments/`** — only 12 directories. Plan + router prompt say "13 core". Missing one or naming off-by-one.
12. **`core/orchestrator/flow_controller.py:63`** — `Router(self.llm, rules_path=rules_path)` if `classifier_rules.yaml` malformed, will crash before user-friendly error. No defensive load.
13. **`core/orchestrator/research_phase.py:39`** — `tool_cls()` instantiated with no args. Tools that need province (vn_local_regulation) cannot receive it from ToolRouter plan because ToolCall TypedDict only has `tool` + `queries`. Province must be encoded inside query string.
14. **`core/translator/pipeline.py:apply`** — applies simplifier+TLDR but no try/except. If Simplifier LLM call fails, decision report write also fails.
15. **`core/llm/providers.py:MCPSamplingProvider.complete`** — no retry on rate limit, no timeout. Single 429 from Anthropic kills the entire vn_meeting flow.

---

## Priority Fix List

### P0 (must fix — features broken or silently violating advertised behavior)
- **P0.1** Wire `DocWriter` + `TemplateResolver` into `flow_controller.execute()`. Generate real .docx/.xlsx from `08-execution-plan.md` and templates. Phase 5/6 acceptance.
- **P0.2** Implement `flow_controller.approve_decision()` properly — generate execution plan via LLM + structured spec, not stub.
- **P0.3** Fix `flow_controller.run_meeting:167` — `departments_root` should be `<vault>/01-Departments/` (with fallback to repo for missing dept). Restores RULE 6 BYOT for meetings.
- **P0.4** Tools must skip gracefully when `TAVILY_API_KEY` empty: return `ToolResult(data={"skipped": True}, notes="No TAVILY_API_KEY — set in vault/.env")` instead of crashing into TavilyClient.
- **P0.5** ToolRouter: filter plan to only credentialed tools. Add `available_tools()` introspection.
- **P0.6** Onboard: prompt for API keys (CLI wizard + MCP `vn_onboard` add `api_keys` param). Save to `<vault>/.env` (in `.gitignore`) + load via `python-dotenv` at FlowController init.
- **P0.7** `install_mcp.py` inject `env: {TAVILY_API_KEY: ..., ANTHROPIC_API_KEY?: ...}` from `<vault>/.env` or `~/.vn-business-os/keys.yaml` into mcpServers entry.

### P1 (should fix — correctness + UX)
- **P1.1** Wire per-agent enriched prompts in `PerspectivesCollector` — load AgentDefinition for `dept.default_speaker` and use that system_prompt instead of generic template.
- **P1.2** Add 13th core department or fix all references ("12 phòng core" everywhere — README, plan, router prompt, skill.md).
- **P1.3** Add retry-with-backoff + timeout to `MCPSamplingProvider.complete` — handle 429/timeout gracefully.
- **P1.4** Re-enable LangGraph checkpointer (root cause the SQLite issue, fix it). Resume mid-meeting after crash.
- **P1.5** `vn_status` should report `tools_live` / `tools_skipped` based on credential presence.
- **P1.6** Apply translator to perspectives + debate transcripts before showing to Department Head (currently only synthesizer output simplified — round summaries shown raw).
- **P1.7** Drop swallowing `GitSync` exceptions silently — log to a `<vault>/.vn-business-os.log` so Department Head can see why commits aren't happening.
- **P1.8** Add citation validator post-Synthesizer — flag claims without `[source: ...]` markers.

### P2 (nice to fix)
- **P2.1** Multi-turn `vn_onboard` via MCP elicitation for industry/Department Head/keys/BYOT.
- **P2.2** `Router` JSON-mode where supported — eliminate brittle regex.
- **P2.3** `tool_cache.db` per-vault not per-user (currently `~/.vn-business-os/`); else cache poisoning between companies.
- **P2.4** Real-LLM E2E test in CI (gated by env, but actually runs).
- **P2.5** PackLoader integration or removal — dead code is a smell.
- **P2.6** `flow_controller._slugify` allows leading/trailing dashes from non-ASCII (Vietnamese accents) → "task" fallback. Use `unicodedata.normalize` for proper Vietnamese-safe slugs.
- **P2.7** Brain context filtering per agent (today every agent sees full Brain dump → token waste with large DNs).
- **P2.8** Add MCP `tools_changed` notification on `vn_onboard` so Claude Desktop refreshes tool list.

---

## Unresolved Questions

1. Was the 13-department count an early plan revision (e.g. "11-reporting + 12-growth + a 13th merged into another"), or genuine missing department? Which one? `agency-agents` reference vs `business-builder.plugin` source — count differs between the two.
2. Is the user expectation "search runs automatically before meeting" — i.e. should `vn_resume` also call ResearchPhase, not just `vn_meeting`? Plans phrase it as "research then meeting" as one stage; current code separates them under `vn_meeting`. UX intent unclear.
3. Should API keys live per-vault (`<vault>/.env`) or global (`~/.vn-business-os/keys.yaml`)? Per-vault feels right for multi-DN consultants but more friction; global is simpler.
4. `MCPSamplingProvider` rate-limit strategy — should plugin auto-degrade to "lite mode" (1 round debate) when subscription near quota, or just fail loudly?
5. Why is `checkpointer=False` hardcoded? What was the original SQLite issue? Need to investigate before re-enabling.
6. `install_mcp` writes absolute path of `sys.executable` into config — breaks if user uses pyenv/venv that gets removed. Should we instead write `python -m core.mcp_server` and rely on PATH?

---

**Status:** DONE_WITH_CONCERNS
**Summary:** Repo is internally consistent and tests pass, but several Phase 5/6 deliverables are stubs (vn_approve, vn_execute, doc rendering) and the live-research feature has critical credential plumbing gaps that match user-reported behavior. RULE 5 + RULE 6 compromised at runtime.
**Concerns/Blockers:** P0 fixes required before claiming v0.2 production-ready. Recommend new phase-07-credentials-and-execution to close gaps before broader release.
