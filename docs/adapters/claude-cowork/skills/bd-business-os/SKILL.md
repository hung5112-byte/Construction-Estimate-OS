---
name: bd-business-os
description: AI agent OS for a Texas hardware engineering & supply chain division. Use the MCP tools (bd_run, bd_meeting, bd_approve, bd_execute, bd_draft, bd_status, bd_resume, bd_onboard, bd_upgrade) to coordinate the 5 division departments (Hardware Engineering; NPI & Program Management; Quality & Reliability; Manufacturing & Supplier Quality; Service Operations) that debate and produce reports + .docx/.xlsx documents aligned with US federal + Texas law. Activate when the user asks about NPI/product launches, BOMs/ECOs, RMA/returns, sourcing/ODM/logistics, quality/certifications, inventory/deployments, SOPs, or any division documentation.
---

# Hardware Division OS — Claude Skill

> AI Operating System for a hardware engineering & supply chain division.
> The manager chats naturally → the 5 departments (AI agents) debate → documents are generated.

This skill uses **9 MCP tools** from the `bd-business-os` server. All LLM thinking runs through the **Claude Desktop / Code subscription** (no ANTHROPIC_API_KEY needed).

## When to activate

The user types things like these → trigger the skill:
- "Plan the NPI pilot / product launch ..."
- "Draft an ECO / RMA SOP / deployment checklist ..."
- "Handle this component shortage / EOL ..."
- "Compare ODM sites / landed cost ..."
- "Investigate the return-rate spike ..."
- "Track our certifications (PCI/EMVCo/FCC/UL) ..."
- "Set up my division vault"
- "Systematize a process"

## One-time install (the manager does this)

```bash
pip install bd-business-os         # or pipx install
bd-os install-mcp                  # auto-edits claude_desktop_config.json
# Restart Claude Desktop
```

After this, the `bd-business-os` MCP server is always available in Claude Desktop. This skill activates automatically when needed.

## 9 MCP Tools

| Tool | When to use |
|---|---|
| `bd_status(vault)` | Verify the vault exists + read the Brain summary |
| `bd_onboard(vault)` | Create a new vault scaffold (first time) |
| `bd_run(brief, vault)` | Stage 1: brief → router → gap → clarification |
| `bd_resume(task_folder)` | Stage 2: resume after the manager answers clarification |
| `bd_meeting(task_folder, departments)` | Stage 3: research + meeting → 07-decision-report.md |
| `bd_approve(task_folder)` | Stage 4: the manager approves → 08-execution-plan.md |
| `bd_execute(task_folder)` | Stage 5: render .docx/.xlsx into 03-Outputs/ |
| `bd_draft(brief, vault, doc_type)` | Fast path: one LLM call for boilerplate (agreement, JD, policy) — no meeting |
| `bd_upgrade(vault)` | Refresh an existing vault with updated prompts + aliases (does not touch Brain content) |

## Standard workflow

### Step 0: Detect vault + Brain
When the manager mentions a division task, read the CWD or ask for the vault path. Call `bd_status(vault)`:

```
✓ vault exists, ICP="mid-size US retailers", products=3, depts=["01-hardware-engineering","02-npi-program-management",...]
```

If the vault has no Brain → call `bd_onboard(vault)` to create the scaffold, and guide the manager to fill in 00-Brain/.

### Step 1: Run the task
```
bd_run(brief="Pilot 500 units of the new terminal with our top customer", vault="~/my-vault")
→ {"stage": "PAUSE_CLARIFICATION", "task_folder": "~/my-vault/02-Tasks/<ts>-pilot-deployment/"}
```

### Step 2: Read clarification + ask the manager
Read `<task_folder>/03-clarification.md` (markdown with checkboxes). Format the questions for the manager in plain English, with Brain citations.

The manager answers → edit the file (tick `[x]` on a choice) via the filesystem MCP or text editing.

### Step 3: Resume after the manager answers
```
bd_resume(task_folder="...")
→ {"stage": "PAUSE_DECISION_REPORT", ...}
```

### Step 4: Run the meeting (debate engine)
```
bd_meeting(task_folder="...")
→ Stage 3 runs: research phase + perspectives in parallel + Pro/Con debate (2-3 rounds) + Growth/Cautious/Balanced debate + Synthesizer
→ Creates 03b-research-findings.md, 04-meeting-r1-perspectives.md, 05-meeting-r2-debate.md, 06-meeting-r3-perspectives.md, 07-decision-report.md
→ {"stage": "PAUSE_DECISION_REPORT"}
```

### Step 5: Read the decision report + summarize for the manager
Read `<task_folder>/07-decision-report.md`. The report has:
- TL;DR (first 3-5 lines)
- Recommendation (GO / GO with revisions / NO-GO)
- BLOCKERS (to do before launch)
- KPI gates
- Decisions the manager must make

Summarize for the manager in plain English, and ask: approve / revise / reject.

### Step 6: Approve → execution plan
```
bd_approve(task_folder="...")
→ Creates 08-execution-plan.md (Stop 2)
```

### Step 7: Execute → generate files
```
bd_execute(task_folder="...")
→ Renders .docx/.xlsx into <vault>/03-Outputs/<task_name>/
```

## Onboard a new vault (first-time setup)

When the manager has no vault or says "set up my division":

1. Ask the manager: division name, vault path
2. Call `bd_onboard(vault="~/bd-os/<slug>")`
3. Guide the manager to open `<vault>/00-Brain/` and fill in:
   - `strategy.md` — vision, target customers, yearly goals
   - `products.md` — device catalog, price, margin
   - `budget.md` — budget by department
   - `headcount.md` — active departments
   - `state.md` — fleet size, current KPIs
4. After filling it in, call `bd_status(vault)` to verify.

## Important

### Use plain English
- ALWAYS communicate with the manager in plain English
- Define an industry term the first time it appears
- Keep it manager-friendly: short, with a TL;DR, no heavy jargon

### Cite sources
- ALWAYS cite the Obsidian file when quoting information (e.g. "per `00-Brain/strategy.md`")
- Do NOT make up content — only summarize the output of the MCP tools

### Error handling
- MCP tool error → tell the manager + suggest a fix:
  - Vault not found → run `bd_onboard()` first
  - Brain incomplete → guide the manager to fill it in
  - Subscription rate limit → wait + retry, or use lite mode (1 debate round)

### Subscription quota
- 1 COMPLEX task ≈ 30-40 sampling calls
- Pro plan ≈ 45 msg/5h → 1 task is close to the quota
- Max plan ≈ 225 msg/5h → 6-7 tasks/5h
- If the manager runs many tasks in a row and hits a limit → suggest spacing them out or upgrading

### File-based state
- All task progress is saved in `<vault>/02-Tasks/<task-folder>/`
- You can stop mid-session and resume later with `bd_resume(task_folder)` or `bd_meeting(task_folder)`

## Sample workflow

Manager: "Pilot 500 PayTerm 500 units with our top customer, $20k budget"

```
1. bd_status("~/division-vault") → ✓ Brain loaded
2. bd_run(brief, vault) → PAUSE_CLARIFICATION, task_folder=...
3. Read 03-clarification.md → 2 questions (cert validity, spares strategy)
4. Show the manager the 2 questions, get answers
5. Edit 03-clarification.md (tick [x])
6. bd_resume(task_folder) → PAUSE_DECISION_REPORT
7. bd_meeting(task_folder) → all 5 departments debate, 07-decision-report.md ready
8. Read the decision report, summarize for the manager (TL;DR + recommendation + blockers)
9. Manager: "Approve this plan"
10. bd_approve(task_folder) → 08-execution-plan.md
11. bd_execute(task_folder) → .docx/.xlsx into 03-Outputs/
12. Show the manager the link to the outputs folder.
```

Total: ~8-15 minutes for a COMPLEX task. The manager spends ~5 minutes (answering clarification + approving the report).

---

## Credits

- Author: **Brian H. Doan** — all agents, the division architecture, and the division templates
- 192 US business templates in `templates-us/` adapted from `business-builder.plugin`
- Engine debate pattern adapted from [TradingAgents](https://github.com/TauricResearch/TradingAgents)
- Role definitions reference from [agency-agents](https://github.com/msitarzewski/agency-agents)
