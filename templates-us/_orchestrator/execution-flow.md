# PROMPT 04: Execution Flow

#### Description
An SOP describing the execution flow in detail: the order the 12 sub-skills are called, the trigger condition for each skill, dependencies between skills, and how to handle a skill that fails or is skipped.

#### Information to collect (ask the user before generating)
1. Run sequentially, or in parallel where possible?
2. A checkpoint review between tiers? (e.g. stop after Tier 1 for the owner to approve)
3. When a skill fails, what's the behavior? (retry / skip / halt all)
4. Who approves each skill's output before moving to the next?
5. A time-box per skill? (e.g. max 2 hours per skill)

#### Suggested template
Structure:
- **Execution Modes** — full run / selective run / single skill
- **Dependency Map** — which skill depends on which (DAG diagram)
- **Trigger Conditions** — when a skill is activated
- **Checkpoint Gates** — stopping points to review & approve
- **Error Handling** — retry logic, fallback, escalation
- **Progress Tracking** — a status dashboard (% complete per skill)
- **Flowchart** — a Mermaid diagram of the whole flow

Confirm the structure before generating.

#### File-generation prompt
```
Create an "Execution Flow" SOP for the Business Packaging system.

CONTEXT:
- 12 sub-skills (01→12) called by the Orchestrator (00)
- 5 tiers: Foundation (01-02) → Machine (03-05) → Engine (06-08) → System (09-11) → Growth (12)
- Mode: [Sequential / Parallel where possible]
- Checkpoint: [Yes / No] — at [checkpoint location]
- Error handling: [retry/skip/halt]
- Approver: [Owner / Coach / Auto]

FORMAT:
- An overall flowchart in Mermaid
- Dependency matrix (12×12): skill X needs output from skill Y
- Trigger Conditions table: Skill | Pre-conditions | Input required | Output expected
- Error-handling decision tree
- Progress-tracking template (status table)
- Estimated timeline per skill & per tier

TONE: Technical, process-oriented, unambiguous.
LENGTH: 5-7 pages.
```

---
✍️ Author: Brian H. Doan
