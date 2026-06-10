# v2 Roadmap — VN Business OS

> Status: **To implement after using v1 in the real world ≥ 2-4 weeks**
> Created: 2026-05-06
> Owner: your-email@example.com

---

## Context

v1 (shipped `phase-06-complete` + tag `v0.1.0`) breaks 4 core limitations:

| v1 limitation | v2 solution |
|---|---|
| Must run the CLI manually per task | Auto-loop cron |
| Output is only markdown in Obsidian | Web UI dashboard |
| 1 install = 1 company | Multi-company context switching |
| 3 industries (F&B, Retail, Tech-SaaS) | 6 new industry packs |

**Principle:** don't build v2 right away. Use v1 ≥ 2-4 weeks → measure pain points → prioritize features by what the Department Head misses most.

---

## Feature 1 — Auto-loop Cron

**Problem:** the Department Head has to remember to type `vn-os run --brief ...` every time a periodic report is due.

**Solution:** a cron schedule in `vault/cron.yaml`, a daemon reads + runs tasks automatically.

### Design

```yaml
# vault/cron.yaml
- schedule: "0 9 * * MON"      # Every Monday morning
  brief: "Weekly report — revenue, churn, gap vs KPI"
  auto_approve: true            # SIMPLE → no Department Head approval needed
  notify: ["email:ceo@company.com"]   # if there's a CRITICAL gap

- schedule: "0 9 1 * *"        # 1st of each month
  brief: "Assess runway + propose next month's budget"
  auto_approve: false           # STRATEGIC → Department Head must approve

- schedule: "0 8 * * *"        # Every morning at 8
  brief: "Check for newly enacted laws affecting the business"
  auto_approve: true
```

### New modules
- `core/scheduler/cron_runner.py` — Read cron.yaml, dispatch tasks via FlowController
- `core/scheduler/notifier.py` — Email/Slack notification when a task finishes or needs Department Head approval
- CLI: `vn-os daemon start|stop|status`

### Effort
~3-5 days

---

## Feature 2 — Web UI Dashboard

**Problem:** a non-tech Department Head has to learn CLI commands. Editing markdown in Obsidian isn't for everyone.

**Solution:** a web app running locally (`vn-os ui`) that shows a UI instead of the CLI.

### Proposed tabs

| Tab | Feature |
|---|---|
| **Tasks** | List running + finished tasks, click to view the decision report |
| **Brain** | Edit `00-Brain/*.md` via a form (no Obsidian needed) |
| **Approve** | View clarification + tick checkboxes in the UI, no markdown editing |
| **Outputs** | Download .docx/.xlsx, preview |
| **Insights** | KPI dashboard auto-generated from the Brain (MRR chart, runway gauge, food cost trend) |
| **Settings** | API keys, installed packs, cron schedule |

### Proposed stack
- **Backend**: FastAPI (wrap the FlowController API)
- **Frontend**: Vanilla HTML + HTMX or React (simple, few dependencies)
- **Auth**: local-only HTTP basic, not exposed to the internet
- CLI: `vn-os ui --port 8765`

### Effort
~10-15 days (backend API + 6 tabs + design)

---

## Feature 3 — Multi-company Support

**Problem:** 1 vault = 1 company. A Department Head holding 3 companies (eatery + online shop + SaaS) installs it 3 times.

**Solution:** one install manages multiple vaults, with context switching.

### New CLI

```bash
vn-os company add joes-diner --vault ~/vaults/diner --pack fnb
vn-os company add fashion-shop --vault ~/vaults/shop --pack retail
vn-os company add techco --vault ~/vaults/techco --pack tech-saas

vn-os company list
# - joes-diner    (F&B)   ~/vaults/diner
# - fashion-shop  (retail) ~/vaults/shop
# - techco        (saas)   ~/vaults/techco

vn-os company switch joes-diner
vn-os run --brief "Calculate May food cost"
# → auto-loads the diner's Brain + agents

vn-os company switch techco
vn-os run --brief "Analyze Q2 churn"
# → loads the SaaS Brain
```

### New modules
- `core/multi_company/registry.py` — `~/.vn-business-os/companies.yaml` stores the company list
- Modify `core/cli.py` — wrap every command with context auto-resolution

### Use cases
- A Department Head holding multiple companies
- An agency consulting for multiple clients
- A mentor advising multiple startups
- A family office managing multiple businesses

### Effort
~5-7 days

---

## Feature 4 — New packs (6 industries)

**Problem:** v1 only has 3 packs. Many common industries aren't covered.

### Proposed packs

| Pack | Specialized departments | US compliance |
|---|---|---|
| **Real Estate** | sales-broker, property-manager, mortgage-advisor | TREC (Texas Real Estate Commission); RESPA; TILA; Fair Housing Act |
| **Healthcare** | clinical-coordinator, medical-billing, privacy-officer | HIPAA; Texas Medical Board; Stark/Anti-Kickback; Texas DSHS |
| **Education** | curriculum-designer, academic-coordinator, parent-relations | FERPA; Texas Education Agency; Title IX (if applicable) |
| **Beauty/Spa** | service-master, retail-product-mgr, hygiene-spa | Texas Dept. of Licensing & Regulation (TDLR — cosmetology); FDA cosmetics labeling |
| **Auto** | service-advisor, parts-manager, warranty-officer | FTC Used Car Rule; Magnuson-Moss; Texas DMV; Texas DOT |
| **Construction** | project-manager-construction, safety-officer, qs-engineer | OSHA construction standards (29 CFR 1926); local building codes; Texas contractor rules |

> Compliance references are general information, not legal advice — confirm with a licensed Texas attorney.

### Pattern
Each pack ~5-10 files, copying templates from the existing F&B/Retail/Tech-SaaS:
- `pack.yaml`
- 1-3 dept folders
- 1-2 agent .md per dept
- `brain-template/strategy.md` (override industry KPIs)
- `compliance_refs:` list of laws

### Effort
~1-2 days/pack × 6 = ~10 days

---

## Feature 5 — Codex + Antigravity adapter (v1.1)

**Listed in v1.1 but not yet done:**

- `adapters/codex/system-prompt.md` — Codex CLI integration
- `adapters/antigravity/SKILL.md` — Antigravity adapter

### Effort
~2 days (same pattern as the Claude Code adapter)

---

## Feature 6 — Test case A + C (v1.1)

**Listed in v1.1 but not yet done:**

- **Test case A**: full onboarding flow (new Department Head → a ready-to-use vault)
- **Test case C**: SIMPLE task — draft a JD in < 2 minutes, no meeting

### Effort
~2-3 days

---

## Feature 7 — Grammar/style check (optional)

**Listed in the open questions:**

Integrate a grammar/style checker for outputs, so the Department Head doesn't receive reports with typos.

### Effort
~1 day

---

## Total effort + proposed order

| Phase | Feature | Effort | Priority reason |
|---|---|---|---|
| **v1.1** | Test case A + C, Codex adapter, grammar check | ~5-7 days | Finish the scope committed in v1 |
| **v2.0** | Web UI Dashboard | ~10-15 days | Biggest pain point for a non-tech Department Head |
| **v2.1** | Auto-loop cron | ~3-5 days | High value, easy to build |
| **v2.2** | Multi-company | ~5-7 days | Expands the customer segment (agency, holding) |
| **v2.3** | 6 new packs | ~10 days | Expands the industries served |

**Total v1.1 + v2:** ~33-44 days FT-equivalent.

---

## Decision framework — when to start v2?

After ≥ 2-4 weeks of real v1 use, note in `vault/00-Brain/decisions-log.md`:

| Pain point noted | → Prioritize feature |
|---|---|
| "Tired of typing CLI commands" | Web UI Dashboard |
| "Forgot to run the weekly report" | Auto-loop cron |
| "Want to use it for my other company" | Multi-company |
| "My industry isn't F&B/Retail/Tech" | New pack |
| "Output has typos" | Grammar check |
| "I use Codex instead of Claude" | Codex adapter |

---

## Anti-patterns — DON'T do

❌ **DON'T build v2 before using v1 in the real world ≥ 2 weeks.** Predicted pain points usually differ from real ones.

❌ **DON'T over-engineer the Web UI.** The goal is a non-tech Department Head being able to use it, not replicating Notion.

❌ **DON'T add packs before a real demo company uses them.** Each pack needs a real user to test the compliance refs.

❌ **DON'T break the v1 API while building v2.** Multi-company must be backward-compatible: the single-company flow still runs as before.

❌ **DON'T copy-paste v1 patterns without refactoring.** After 6 phases there may be duplicate code — clean it up before extending.

---

## Open questions for v2 (for the Department Head to answer at start)

1. **Web UI auth**: local-only or support internal multi-user?
2. **Cron daemon**: run as a Windows service / systemd, or a simple cron script?
3. **Multi-company config**: store per-company API keys or share global?
4. **Pack contribution**: open it to source contributors or build all in-house?
5. **Web UI tech stack**: HTMX (simple) or React (rich)? Depends on whether the Department Head has a frontend dev.
6. **Notification channels**: email only, or add Slack?
7. **Grammar check**: actually needed, or does the LLM already handle spelling well?

---

## Cross-reference

- **v1 SPEC**: `SPEC.md`
- **v1 phase plans**: removed 06/09/2026 (Vietnamese dev build-logs; build complete — see `plans/plan.md` for the summary)
- **v1 decisions**: `DECISIONS.md`
- **v1 ship status**: tag `v0.1.0`
