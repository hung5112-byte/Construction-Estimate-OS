# MIGRATION REPORT — Generic One-Person-Company OS → Hardware Division OS

**Author/Operator:** Brian H. Doan — VP, Hardware Development, Quality & Supply Chain
**Date:** 06/09/2026 (V1 division restructure + V2 VP-org restructure, same day)
**Scope:** Audit → fix → restructure of the repo into an AI operating system for a
**hardware engineering & supply chain division** of a Texas electronics company,
managed by one person. Legal grounding stays US federal + Texas (IRS, Texas
franchise tax, Texas Secretary of State); no Vietnamese legal references remain.
**Backup:** the pre-migration tree is preserved at `C:\One Person Company\OPC_English`.
**Verification:** 273 tests passed / 4 skipped / 0 failed; `ruff check docs/core/ docs/tests/`
fully clean (first time); all YAML parses.

> Prior history: this repo was originally a Vietnamese one-person-company AI OS,
> translated to English and re-grounded to US/Texas law in an earlier session.
> That session's records are archived at
> `docs/plans/reports/migration-260609-vn-to-us-localization-{report,audit}.md`.

---

## 1. What was broken (found in the audit, fixed before restructuring)

| # | Defect | Fix |
|---|---|---|
| 1 | **Phantom Brain references** — all 33 agent prompts told agents to read/cite Brain files that don't exist (`operations.md`, `finance.md`, `sales.md`, `marketing.md`, `people.md`, `customers.md`, `market.md`, `product.md`); `BaseAgent._filter_brain` silently dropped the unknown refs, so agents ran with less context than promised and were coached to fabricate citations | All agent frontmatter + prompt bodies remapped to the 8 real Brain sections (`strategy/products/budget/headcount/laws/decisions-log/state/glossary`); 42 files fixed |
| 2 | **Vault config never loaded** — `FlowController` called `load_config()` with no path, so `<vault>/.vncoderc` (written by onboarding, documented as the config) was ignored; only `~/.vncoderc` was ever read | `FlowController` now loads `<vault>/.vncoderc` first with home fallback |
| 3 | **Citation validator checked phantom filenames** — its Brain-file whitelist contained `finance/operations/marketing/hr/tech` and missed `budget/headcount/state/decisions-log`, so reports citing real Brain files were falsely flagged | Both regexes rebuilt on the real 8 sections |
| 4 | **Dead pack feature** — `extends_departments`/`add_agents` was parsed but never applied, and all 17 agents it referenced had no files | Dead blocks removed from pack configs; documented as not-applied in `docs/how-to-create-pack.md` |
| 5 | **Permanently failing test** — `test_phase_tags_present` ran `git tag` in a repo with no git history | Skips cleanly when `.git` is absent |
| 6 | **Doc/code contradictions** — CLAUDE.md claimed an LLM priority (MCP→Anthropic→Google→OpenAI) the code doesn't implement (actual: DeepSeek→Anthropic→MCP sampling), a tool-registration location that was an empty file, wrong config filenames (`config.yaml` vs `department.yaml`), stale test counts; skill docs said 7 MCP tools while the server registers 9 | All corrected |
| 7 | **Translation artifacts** — `pyproject.toml` still described "Vietnamese One-Person Companies… VN-compliant docs"; a Vietnamese word in a core docstring; translator notes referencing Vietnam leaked into 2 agent prompts and 12 templates; a "translated" dev report still mostly Vietnamese; a test query targeting Vietnam | All cleaned/translated; 11 fully Vietnamese dev build-log files deleted (user-approved; preserved in backup) |
| 8 | **CI would fail** — the workflow ran a deleted test file; the lint step had 86 pre-existing errors (2 were real `F821` undefined-name bugs) | Workflow updated; lint now fully green |
| 9 | Minor: CLI version 0.1.0 vs package 0.2.0; committed `__pycache__` bytecode; broken pointers to deleted files | Fixed/removed/annotated |

## 2. What was restructured

**V1 (intermediate, same day):** 12 generic departments + 3 industry packs → 5
flat division departments (15 agents). Superseded within hours by V2 below; the
V1 structure exists only in the backup.

**V2 (current) — the VP org layout: 5 manager-led departments, 29 agents (5 managers + 24 teams):**

| Department | Manager (default speaker) | Teams |
|---|---|---|
| `01-hardware-engineering` | hw-engineering-manager | me-team, ee-team, fw-embedded-team, system-architecture |
| `02-npi-program-management` | npi-pm-manager | hardware-pm, certification, bom-eco-plm, launch-readiness, sourcing-buyer, odm-program-mgmt |
| `03-quality-reliability` *(debate: con)* | quality-manager | qa-system, qc-inspection, validation-reliability, firmware-qa, field-quality-rma-fa |
| `04-mfg-supplier-quality` | msq-manager | odm-quality, supplier-quality, manufacturing-engineering, factory-test-yield |
| `05-service-operations` | service-ops-manager | repair, fulfillment, inventory, deployment-support, logistics |

Supply-chain functions were placed per the VP's decision: sourcing/buying and ODM
program management under NPI & Program Management; logistics under Service
Operations.

**V2 engine change — intra-department debate round** (`meeting.intra_department_round`,
default true): in round 1 every team agent gives a ≤150-word take, then the
manager synthesizes the department perspective (crediting teams, naming
disagreements), then the managers debate (Pro/Con + Growth/Cautious/Balanced) and
the synthesizer reports to the VP. Team takes land in
`04-meeting-r1-perspectives.md` under per-team `[[wikilink]]` headings. Cost:
~29 round-1 LLM calls for a 5-department meeting (vs. 5 with the flag off).
Implemented in `docs/core/orchestrator/perspectives_collector.py`,
`docs/core/meeting/debate_state.py` (`team_inputs` channel),
`docs/core/utils/config.py`, `docs/core/orchestrator/flow_controller.py`.

**V2 wikilink/memory upgrades** (`docs/core/wikilinks.py`): department hubs render an
org chart (Manager ⭐ + teams) and a "Works with" section from `depends_on` with
display names; team agents' auto-appended Links blocks include a `Manager:` link;
agent prompt bodies cross-reference peers with `[[wikilinks]]` ("Works with"
sections) — the Obsidian graph now shows the org structure and its handoffs, and
agents see the same names the router can dispatch to.

**V2 template re-home + byline removal:** the 43 division templates were
redistributed to the new departments (1 / 11 / 9 / 6 / 16); the
`📋/✍️/🔗 MODORO` byline block was removed from all 183 vendored templates at the
VP's direction — third-party attribution is maintained in `NOTICE`.

**Other restructuring:**
- **Router/classifier** rebuilt for division semantics (SIMPLE: SOPs/ECOs/RMA letters; COMPLEX: NPI/shortage/capacity plans; STRATEGIC: new ODM, factory transfer, certification programs, EOL)
- **Templates** (`docs/templates-us/`, 207 total): 28 relevant templates moved into the 5 dept folders, **15 new original division templates** authored (BOM, ECO, DVT report, receiving/IQC SOP, cycle-count program, deployment checklist, RMA SOP, 8D, refurb standard, ODM SOP, shortage plan, landed-cost model, certification tracker, SCAR, IQC plan), 155 generic business templates **parked in `_shared/`** (BYOT source material), 9 `_orchestrator` meta-templates kept (storage-rules rewritten for the division)
- **Packs**: the 3 industry packs (fnb/retail/tech-saas) deleted; the pack *mechanism* kept and documented (`docs/packs/README.md`)
- **Vault template**: Brain prefills now hardware-division (laws.md: FCC Part 15, UL/IEC, PCI PTS/EMVCo, HTS/customs, lithium-battery transport, Magnuson-Moss; glossary: NPI/BOM/ECO/ODM/RMA/AQL/SCAR/8D; headcount/budget/state examples use the 5 departments)
- **Benchmark tool**: `hardware_electronics` segment added (return rate, FPY, OTD, turns, RMA turnaround, ocean transit) — all `[UNCERTAIN]`-flagged
- **Fixtures/tests**: fixture vaults retargeted to a hardware company ("VoltEdge Devices", `hardwareco-vault`); the flagship e2e is now an NPI pilot-deployment scenario; 25+ test files updated
- **Docs**: README rewritten; CLAUDE.md updated; all 8 `docs/` guides re-exampled; both adapter skills re-triggered on NPI/RMA/ODM/certification language; SPEC/ROADMAP/DECISIONS/START-HERE/NEXT-STEPS marked HISTORICAL with supersession notes; prior migration records archived to `docs/plans/reports/`
- **Hazard removal**: 5 dev scripts that would regenerate the old 12-department layout now exit with deprecation notices

**Deliberately kept:** the `vn_*` MCP tool names, `vn-business-os` server name,
`vn-os` CLI, and `vn-one-person-company` package slug (installed API contract —
user decision); the `name_vn`/`aliases_vn` YAML keys (schema compatibility, English
values); the MODORO author credit in vendored templates (license attribution per
`NOTICE`); the unused `google-genai`/`openai` dependencies (user decision);
core code's "CEO" terminology for the human principal (= the division manager;
noted in CLAUDE.md).

## 3. Open questions for the manager

1. **Reinstall the adapters** — the Claude Cowork plugin installed on this machine still carries the old Vietnamese skill description. Rebuild (`bash docs/adapters/claude-cowork/build-plugin.sh`) and reinstall, and re-run `vn-os install-mcp` so Claude Desktop picks up the updated skill text.
2. **Benchmarks and rate figures** — every figure in `benchmarks-us.yaml` and the tariff/AQL/yield ranges in agent prompts/templates is illustrative and `[UNCERTAIN]`-flagged. Replace with your division's real numbers (and your broker's current tariff rates) as you fill the Brain.
3. **Certification scope per product** — the Quality department's prompts cover PCI PTS/EMVCo/FCC/UL generically; the per-product required set should be captured in `laws.md` and the certification-tracker template once real products are loaded.
4. **`README-USER.md`** — the long non-coder guide was patched (departments, packs, examples, status checks) but its narrative walkthroughs still carry some generic-business flavor; a full rewrite is cosmetic and was deprioritized.
5. **Brain schema depth** — the Brain has 8 fixed sections. If you later want first-class supplier/fleet sections (beyond `products.md`/`state.md` free text), that's a `docs/core/brain/schema.py` + reader change; deferred to keep the architecture untouched.

---

*General information only — the legal/tax/regulatory content is not legal advice.
Confirm specifics with a licensed Texas attorney, CPA, customs broker, and the
relevant certification labs.*
