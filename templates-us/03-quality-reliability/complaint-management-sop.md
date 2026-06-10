### PROMPT 05: Complaint Management SOP

#### Description
A process to handle customer complaints — from intake, severity classification, root-cause investigation, resolution, customer response, and follow-up, to process improvement. Aligned with ISO 9001 Clause 10.2 — every complaint is an improvement opportunity.

#### Information to collect (ask the user before generating)
1. Intake channels? (hotline, email, chat, social media, in person)
2. Average complaints/month? Most common type?
3. Current resolution time? Target?
4. Who can authorize compensation/refunds? Limit?
5. A ticket/CRM tracking system?
6. Any serious escalated complaint before?

#### Suggested template
Structure:
- **Step 1** — Intake: log, confirm with customer, create ticket
- **Step 2** — Classify: severity (Critical/High/Medium/Low), category
- **Step 3** — Investigate: gather info, verify, root cause
- **Step 4** — Resolve: propose solution, approve, execute
- **Step 5** — Respond: inform the customer of the outcome, apologize if needed
- **Step 6** — Follow up: 3-7 days later, ensure the customer is satisfied
- **Step 7** — Improve: root-cause analysis, preventive action, update the SOP

Confirm the structure before generating.

#### File-generation prompt
```
Create a Complaint Management SOP.

CONTEXT:
- Company: [Name] — Intake channels: [hotline / email / chat / social / in person]
- Complaints/month: [number] — Common type: [describe]
- Current resolution time: [hours/days] — Target: [hours/days]
- Compensation authority: [who] — Limit: [USD]
- Ticket system: [name / none]

FORMAT:
- 7-step flowchart: Mermaid — Intake → Classify → Investigate → Resolve → Respond → Follow up → Improve
- Severity matrix: Level | Description | Example | Response time | Resolution time | Escalate to
- Response scripts: 4 scripts by severity — greeting + acknowledgment + time commitment
- Escalation path: Level 1 (Support Agent) → Level 2 (CS Team Lead) → Level 3 (CS Manager) → Level 4 (Owner)
- Root cause template: 5 Whys + Fishbone → corrective action → preventive action
- KPI tracking: Resolution time | FCR | Escalation rate | Repeat complaint rate | CSAT post-resolution
- Compensation matrix: Complaint type | Compensation level | Approver | Conditions (USD)

TONE: Empathetic, solution-oriented, process-driven.
LENGTH: 6-8 pages.
```

---
✍️ Author: Brian H. Doan
