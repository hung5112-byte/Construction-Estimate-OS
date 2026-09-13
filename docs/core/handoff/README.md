# Multi-agent handoff slice

A working vertical slice: a finished bd-business-os decision flows through a
machine-readable **handoff contract** into downstream agents that **prepare**
(never send) a stakeholder email, a set of staged Jira issues, and a Slack
notification. A human approves; only then does anything leave the building.

This is the smallest piece of the larger Agentic Enterprise OS — see
`Agentic-Enterprise-OS-Architecture.docx` in the vault root for the full picture.

## Run it (no API keys, nothing is sent)

```bash
python docs/core/handoff/demo.py                       # uses the Cyber CY-80 task
python docs/core/handoff/demo.py "02-Tasks/<slug>"     # any finished task
```

Drafts are written to `03-Outputs/<slug>/handoff/`. Re-running is idempotent.

## What it shows (the 2-minute story)

| Step | What you say |
|------|--------------|
| 1 | "Our agents already debated this and produced a decision plus six documents." |
| 2 | "Here's the new piece — they emit a contract any other agent can act on. Notice it's classified *confidential*, so the reasoning ran on a **local model** — the data never left the building." |
| 3 | "A dispatcher routes it under policy. Three different agents pick up the work." |
| 4 | "It drafted the approval email, staged 11 Jira tickets with owners and due dates, and prepared the Slack note — but **sent nothing**. A human approves these each morning." |
| 5 | "And it's safe to re-run — no duplicate tickets. This is built to run unattended overnight." |

Close with: *"Today this prepares drafts. Wire the real Gmail / Jira / Slack
connectors and it acts for real — always behind human approval. That's the
foundation; everything else plugs into this same contract."*

## The pieces

| File | Role |
|------|------|
| `manifest.py` | Builds `handoff.json` from `08-execution-plan.md` (the **seam**) |
| `consumers.py` | The three draft-only agents + the intent→agent routing table |
| `dispatcher.py` | Routes intents, enforces draft-only policy, dedupes, writes the event log |
| `demo.py` | The narrated end-to-end runner |

## Why it's safe to demo live

- **Draft-only by policy.** The dispatcher refuses any manifest whose policy is not
  `draft_only`; consumers only ever write files.
- **No credentials, no network.** Pure standard library.
- **Idempotent.** A task is dispatched once; re-runs are skipped unless forced.
- **Auditable.** Every prepared action is one line in `handoff/dispatch.log`.

## What's next (production)

Replace the file-writing bodies of the three agents in `consumers.py` with real
MCP calls — Gmail `create_draft`, Atlassian create-issue, Slack post — keeping
the same function boundary and the same draft-only / human-approval gate.
