# User Guide — Hardware Division OS

Day-to-day usage after onboarding. See [Getting Started](getting-started.md) first if you haven't installed.

---

## Flow overview

```
                    ┌─ Stage 1 ─┐         ┌─ Stage 2 ─┐
Department Head chat brief ────→│  bd_run   │────────→│ bd_resume │
                    └───────────┘         └───────────┘
                          │                     │
                          ↓                     ↓
                    Create task folder   Read clarification
                    Classify + Brain     answers, continue
                    Generate clarification

                    ┌─ Stage 3 ─┐         ┌─ Stage 4 ─┐         ┌─ Stage 5 ─┐
                    │ bd_meeting│────────→│ bd_approve│────────→│ bd_execute│
                    └───────────┘         └───────────┘         └───────────┘
                          │                     │                     │
                          ↓                     ↓                     ↓
                    Research + meeting   Generate execution     Render .docx/
                    debate + cite        plan structured        .xlsx outputs
                    validator
                          │
                       STOP 1                  STOP 2
                  (Department Head approves report)  (Department Head approves execute)
```

**2 stops requiring Department Head intervention:**
- **STOP 1:** after `bd_meeting` — read `07-decision-report.md`, OK → call `bd_approve`
- **STOP 2:** after `bd_approve` — read `08-execution-plan.md`, OK → call `bd_execute`

The Department Head can edit both files before moving to the next stage.

---

## Files in each task

```
<vault>/02-Tasks/<task-slug>/
├── 00-brief.md                  # The Department Head's original brief
├── 01-routing.md                # Classification + participating departments
├── 02-context.md                # Brain dump used
├── 03-clarification.md          # Department Head questions (Stage 1)
├── 03-clarification-answered.md # Normalized answers (Stage 2)
├── 03b-research-findings.md     # Live research output (Stage 3)
├── 04-meeting-r1-perspectives.md
├── 05-meeting-debate.md         # Pro/Con transcript
├── 06-meeting-synthesis.md
├── 07-decision-report.md        # ★ STOP 1 — Department Head reads + approves
├── 08-execution-plan.md         # ★ STOP 2 — Department Head reads + approves
└── 09-execution-summary.md      # After Stage 5

<vault>/03-Outputs/<task-slug>/
└── <template-name>.docx/.xlsx   # The actual rendered documents
```

---

## Real examples

### SIMPLE task: Draft an RMA intake SOP

```
I need an RMA intake SOP for the repair bench. Returns arrive by UPS,
serialized devices, target turnaround 10 business days.
```

The plugin:
- Classifies as **SIMPLE** → 1-2 departments (`05-service-operations`, `03-quality-reliability`)
- Brain check: RMA department active? Turnaround target on file? → OK
- Skips clarification (enough info)
- Skips the meeting (SIMPLE)
- Generates the SOP from the `05-service-operations/rma-process-sop` template → `.docx`
- ~2 minutes, ~$0.10 LLM cost

### COMPLEX task: NPI pilot deployment

```
Pilot 500 units of the new terminal with our top retail customer.
Budget $20,000, ship before 06/30.
```

The plugin:
- Classifies as **COMPLEX** → 5 departments debate
- Brain check → gaps found (certification renewal timing? spares plan for the pilot?)
- 4 clarification questions (cert letter status, spares strategy, wave plan, ...)
- Research: hardware return-rate benchmarks, applicable certification rules
- Meeting of 5 departments × 3 perspectives × 2 rounds → 30+ messages
- Decision report ~1500 words + citation warnings if anything is missing
- Execution plan with tasks per department + templates
- Render: field-deployment-checklist.docx, rma-process-sop.docx, ...
- ~10-15 minutes, ~$0.80-1.20 LLM cost

### STRATEGIC task: Transfer a build to the Mexico CM

```
Evaluate moving the charging-dock build from the China ODM to the Mexico CM
in Q4. Tariff exposure is the driver. Get sourcing + quality + ops input.
```

The plugin:
- Classifies as **STRATEGIC** → all departments + manager approval mid-way
- More thorough clarification (10+ questions)
- Research: current tariff rates `[verify with broker]`, transfer-time benchmarks, dual-tooling costs
- Multi-round meeting
- Strict STOP 1 + STOP 2
- ~25-30 minutes, ~$1.5-2.0 LLM cost

---

## Tools used only when needed

### `bd_draft` — fast path for doc boilerplate
Drafts one document in a single LLM call (~10-30s), WITHOUT the debate engine.

**Use case:** employment agreement, JD, work rules, receipt, simple SOP, meeting invite...
```
Draft an employment offer for an accounting assistant at cafe ABC, $45k/year, 2-month introductory period.
```
Output: `<vault>/02-Tasks/<ts>-draft-<slug>/draft.md`

**Do NOT use** for strategic decisions / anything with significant legal risk → use `bd_run` + `bd_meeting`.

### `bd_status`
Inspect the vault state — Brain summary + active departments + tasks + tool availability.
```
bd_status vault F:\work\xyz-vault
```

### `bd_upgrade`
After pulling a plugin update, refresh an existing vault:
```
Upgrade vault F:\work\xyz-vault
```
- Refreshes agent .md prompts
- Injects new Brain aliases
- Does NOT touch Brain content / Tasks / Outputs (Department Head data)

### `bd_onboard`
Create a new vault (see [Getting Started](getting-started.md)).

---

## Tips for running effectively

### 1. The Brain must be complete
The plugin is Brain-first → an empty Brain = very long clarification. Spend 30 minutes filling in the Brain up front, then maintain it weekly.

### 2. Translate mode
- `final_only` (default): fast, low cost, the Department Head sees an easy-to-read decision report
- `all_intermediate`: 2-3x slower but every output (perspectives, debate) is Department-Head-friendly. Enable if the Department Head has no CTO/CMO to help read.

Edit `<vault>/.bd-os.yaml`:
```yaml
translator_mode: all_intermediate
```

### 3. Re-run a task
The plugin is idempotent: if a task fails midway, call the corresponding MCP tool again — the old task folder is resumed.

### 4. Edit the decision report before approving
The Department Head opens `07-decision-report.md`, edits, saves → `bd_approve` reads the edited version.

### 5. Citation warnings
If `07-decision-report.md` has a `## ⚠️ Warning: claims missing a source` section → review those claims before approving. They may be LLM hallucinations.

### 6. Tools skipped → enable the key
If `bd_status` reports `tools_skipped: [web_search, ...]` → the flow still runs but the decision report relies entirely on the Brain + LLM common knowledge. Enable TAVILY_API_KEY to search real US law/competitors.

---

## Next

- [Configuration](configuration.md) — tune `.bd-os.yaml`
- [Troubleshooting](troubleshooting.md) — debug when something breaks
- [How to create a pack](how-to-create-pack.md) — add a new industry pack
