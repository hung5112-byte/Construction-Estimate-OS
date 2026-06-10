# Installing Hardware Division OS on Claude Code

> Detailed guide — install the plugin on **Claude Code** (CLI / terminal), not Claude Desktop.

## 0. Requirements

| Requirement | Notes |
|---|---|
| **Claude Code** installed + logged in | Pro or Max subscription (Free rate limit is too low) |
| **Python 3.11+** | Check: `python --version` |
| **Git** | To clone the repo + auto-commit the vault |
| **Windows users**: Git Bash or WSL | To run the `install.sh` script. Otherwise use the alternative commands below. |
| **Tavily API key** (free) | Get it at https://tavily.com — free tier 1000 req/month |

---

## 1. Clone the repo + install the Python package

```bash
# Clone locally
git clone https://github.com/andyluu98/vn-one-person-company.git
cd vn-one-person-company

# Create a virtual env (recommended)
python -m venv .venv
.venv\Scripts\activate          # Windows PowerShell
# source .venv/bin/activate     # macOS/Linux/Git Bash

# Install the package
pip install -e .
```

Verify:
```bash
vn-os --help
# → prints the command list: install-mcp, ...
```

---

## 2. Install the skill + register the MCP server into Claude Code

### Option A — Auto script (Linux/macOS/Git Bash)

```bash
bash docs/adapters/claude-code/install.sh
```

The script does 2 things:
1. Copies `skill.md` → `~/.claude/skills/vn-business-os/SKILL.md`
2. Runs `vn-os install-mcp --target claude-code` → adds a `vn-business-os` entry to `~/.claude.json`

### Option B — Manual (Windows PowerShell, no Git Bash)

```powershell
# 1: Create the skill folder
mkdir "$env:USERPROFILE\.claude\skills\vn-business-os" -Force

# 2: Copy the skill file
Copy-Item adapters\claude-code\skill.md "$env:USERPROFILE\.claude\skills\vn-business-os\SKILL.md"

# 3: Register the MCP server
vn-os install-mcp --target claude-code
```

### Verify the install

```bash
# Check the skill was copied
ls ~/.claude/skills/vn-business-os/SKILL.md     # Linux/macOS
dir "$env:USERPROFILE\.claude\skills\vn-business-os\SKILL.md"   # Windows

# Check the MCP was registered
cat ~/.claude.json | grep -A 3 "vn-business-os"
```

You should see an entry like:
```json
"vn-business-os": {
  "command": "vn-os-mcp"
}
```

### Restart Claude Code

Close the current terminal + open a new one. Claude Code reads `~/.claude.json` at session start.

---

## 3. First-time use — create a vault for your company

Open Claude Code in any folder (the vault can live elsewhere):

```bash
claude
```

In the chat session, type:

```
Set up a Hardware Division vault for my division.
- Vault path: F:/work/division-vault
- Tavily API key: tvly-xxxxxxxxxxxxxxxx
```

**Claude will:**
1. Detect the `vn-business-os` skill is active (because of the keyword "Set up a ... vault")
2. Call the MCP tool `vn_onboard(vault="F:/work/division-vault")`
3. The tool creates the scaffold:
   ```
   F:/work/division-vault/
   ├── 00-Brain/          ← the manager fills these in
   │   ├── strategy.md
   │   ├── products.md
   │   ├── budget.md
   │   ├── headcount.md
   │   └── state.md
   ├── 01-Departments/    ← the 5 division departments (managers + teams)
   ├── 02-Tasks/          ← one folder per task
   ├── 03-Outputs/        ← generated .docx/.xlsx
   ├── .vncoderc          ← config
   └── .env               ← TAVILY_API_KEY (gitignored)
   ```
4. Then asks: *"The vault is created. Want me to walk you through filling in the Brain now?"*

**After the vault has a Tavily key**, run the inject-env command again:

```bash
vn-os install-mcp --target claude-code --vault "F:/work/division-vault"
```

This reads `<vault>/.env` and injects it into the MCP server entry in `~/.claude.json` → the search tools have credentials available and won't skip silently. **Restart Claude Code once more.**

---

## 4. Fill in the Brain (once, ~30 min)

Open `<vault>/00-Brain/` in an editor (VSCode, Obsidian, nano, ...). Fill in the 5 files:

| File | Content |
|---|---|
| `strategy.md` | Vision, target customers, annual goals (units, return rate, OTD) |
| `products.md` | Device catalog + price + margin |
| `budget.md` | Annual budget + department allocation |
| `headcount.md` | Which departments are active, skill gaps |
| `state.md` | Division stage, fleet size, quarterly numbers |

The scaffold files include templates — just fill them in.

---

## 5. Run your first task

In the Claude Code chat:

```
Pilot 500 units of the PayTerm 500 with our top retail customer.
Budget $20,000, ship before 06/30.
Vault: F:/work/division-vault
```

→ See the [interaction walkthrough](#interaction-walkthrough-claude--user) below.

---

## Interaction walkthrough: Claude ↔ user

This is the **standard flow** the user will see. Show it to users first so they aren't surprised.

### Stage 1: Brief → Clarification

**User types:**
> Pilot 500 units of the PayTerm 500 with our top retail customer. Budget $20,000, ship before 06/30. Vault: F:/work/division-vault

**Claude (automatically):**
1. Calls `vn_status(vault="F:/work/division-vault")` → verifies the Brain
2. Calls `vn_run(brief, vault)` → the tool returns `{"stage": "PAUSE_CLARIFICATION", "task_folder": "F:/work/division-vault/02-Tasks/260530-2340-pilot-deployment/"}`
3. Reads `03-clarification.md` in the task folder
4. **Asks the user (in plain English, citing the Brain)**:

```
Per `00-Brain/laws.md`, the PT500 contactless certification renewal is due Q3.
Question 1: Is the certification valid through the pilot window?

   [a] Valid through pilot — letter on file
   [b] Renewal pending — get the lab's ETA in writing first

Question 2: Per `00-Brain/headcount.md`, no spares planning exists for pilots.
A 500-unit pilot typically carries a 3% spares pool. How do you want to cover it?

   [a] 3% spares pool onsite
   [b] Advance replacement from HQ

Do you choose (a) or (b) for question 1?
```

> **Important note**: per CLAUDE.md, Claude **asks only one question at a time**. After the user answers question 1 → Claude asks question 2.

**User:**
> Q1: a, Q2: a

**Claude:**
5. Ticks `[x]` in `03-clarification.md` for the user's choices
6. Calls `vn_resume(task_folder)` → continues to Stage 2

---

### Stage 2: Meeting (research + debate)

**Claude (auto, no user action needed):**

1. Reports: *"Starting a meeting of 5 departments: Hardware PD, Supply Chain, Quality, Operations, RMA. Takes about 5-8 minutes."*
2. Calls `vn_meeting(task_folder)` — the tool runs:
   - Research phase (Tavily searches certification rules, hardware benchmarks)
   - 3 perspectives in parallel (Growth / Cautious / Balanced)
   - 2-3 rounds of Pro/Con debate
   - Synthesizer consolidates
   - Generates `07-decision-report.md`
3. Reads the decision report, summarizes for the user:

```
✅ Meeting done. Summary of 07-decision-report.md:

TL;DR: GO with revisions — pilot in 2 waves, with 4 blockers before wave 1.

Recommendation: GO with revisions

BLOCKERS (do before wave 1 ships):
1. Certification validity letter on file for the PT500 [verify with the lab]
2. Build the 3% spares pool and stage it at the customer's site
3. Publish IQC criteria for the pilot lot at receiving
4. Finalize the field-deployment checklist with acceptance sign-off

KPI gates:
- Week 1: DOA < 1%
- Week 4: 100% site acceptance sign-offs

Question for the manager:
- Ship both waves from the Vietnam ODM, or stage wave 2 via the Texas warehouse?

Do you approve this plan? (approve / revise / reject)
```

---

### Stage 3: Approve → Execution plan

**User:**
> Approve, stage wave 2 via the Texas warehouse

**Claude:**
1. Calls `vn_approve(task_folder)`
2. The tool generates `08-execution-plan.md`
3. Reports: *"Plan approved. Generate the .docx/.xlsx files?"*

**User:**
> OK

---

### Stage 4: Execute → render files

**Claude:**
1. Calls `vn_execute(task_folder)`
2. The tool renders:
   - `field-deployment-checklist.docx` — site install + acceptance
   - `rma-process-sop.docx` — the pilot's returns lane
   - `incoming-inspection-plan.docx` — IQC criteria for the pilot lot
3. Auto-commits to the vault's private git repo
4. Reports: *"Done. Files are in `F:/work/division-vault/03-Outputs/260530-2340-pilot-deployment/`."*

**Total time**: 8-15 minutes. The user is at the keyboard ~5 minutes (answering clarification + approving).

---

## Troubleshooting

### Error: `vn-os: command not found`

The venv isn't activated, or you haven't run `pip install -e .`. Run:
```bash
.venv\Scripts\activate
pip install -e .
```

### Error: MCP server doesn't appear in Claude Code

1. Check `~/.claude.json` has a `vn-business-os` entry
2. Restart Claude Code (close the terminal, reopen)
3. Run `claude --mcp-debug` to see the log

### Error: search tools skip silently

The Tavily key isn't injected. Re-run:
```bash
vn-os install-mcp --target claude-code --vault "<path-to-vault>"
```
Then restart Claude Code.

### Error: rate limit (subscription quota exhausted)

- Pro plan ≈ 45 msg/5h → one COMPLEX task nearly hits the quota
- Suggestion: take a 1-2h break and retry, or upgrade to the Max plan (~225 msg/5h)
- Or enable **lite mode** in `.vncoderc`:
  ```yaml
  meeting:
    max_debate_rounds: 1
    max_perspective_rounds: 0
  ```
  → reduces to ~15 sampling calls/task

### Error: Vault not found

```
Set up a vault for company XYZ at path ... before running a task.
```
Or call `vn_onboard` directly via the MCP tool.

### Windows: `bash: command not found` when running `install.sh`

Use Option B (manual PowerShell) in section 2.

---

## Checklist for instructors

Before class, verify each student has:

- [ ] Installed Claude Code + logged into a Pro/Max subscription
- [ ] Installed Python 3.11+
- [ ] Installed Git (+ Git Bash on Windows)
- [ ] A Tavily API key (free tier)
- [ ] Cloned the repo + run `pip install -e .` successfully
- [ ] Run `vn-os --help` and seen the command list
- [ ] Run `install.sh` (or Option B) — verified `~/.claude.json` has a `vn-business-os` entry
- [ ] Restarted Claude Code
- [ ] Created a test vault + filled in a sample Brain (can use the bundled demo vault)
- [ ] Run one SIMPLE task to verify end-to-end (e.g. "Draft a JD for a software developer at $90k")

---

## See also

- [`docs/adapters/claude-code/README.md`](adapters/claude-code/README.md) — adapter overview
- [`docs/adapters/claude-code/skill.md`](adapters/claude-code/skill.md) — skill definition
- [`docs/user-guide.md`](user-guide.md) — the 5-stage flow in detail
- [`docs/troubleshooting.md`](troubleshooting.md) — common errors in general
- [`docs/architecture.md`](architecture.md) — architecture + RULES
