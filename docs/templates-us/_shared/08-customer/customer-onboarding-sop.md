### PROMPT 02: Customer Onboarding SOP

#### Description
An onboarding process for new customers — from signing the contract/buying to the customer reaching "first value" and stable usage. The onboarding phase determines most of long-term retention.

#### Information to collect (ask the user before generating)
1. Main product/service to onboard? Complexity?
2. Average onboarding time? (1 day / 1 week / 1 month)
3. How does the Sales → CS handoff happen?
4. Does the customer need training? Online or in person?
5. "First value" — when does the customer get their first result? What signals it?
6. Churn rate in the first 90 days?

#### Suggested template
Structure:
- **Step 1** — Welcome: welcome email, introduce the assigned CS, onboarding timeline
- **Step 2** — Setup: account setup, configuration, initial settings
- **Step 3** — Training: usage guidance, docs, video
- **Step 4** — First Value: help the customer reach their first result
- **Step 5** — Check-in: call/meet check-ins on Day 7, Day 14, Day 30
- **Step 6** — Stabilize: move to regular care

Confirm the structure before generating.

#### File-generation prompt
```
Create a Customer Onboarding SOP.

CONTEXT:
- Company: [Name] — Product/service: [name] — Complexity: [low/med/high]
- Onboarding time: [days/weeks/months]
- Sales → CS handoff: [current process]
- Training: [online / in person / self-serve] — Duration: [hours]
- First-value milestone: [describe]
- 90-day churn: [%]

FORMAT:
- 6-step flowchart: Mermaid — Welcome → Setup → Training → First Value → Check-in → Stabilize
- Timeline: Gantt-style — Day 0 → Day 7 → Day 14 → Day 30 → Day 60 → Day 90
- Welcome email template: Subject + body + CTA
- Handoff checklist: 10 items Sales must transfer to CS
- Check-in script: 3 scripts for Day 7, 14, 30 — questions + action
- Success criteria: Milestone | Metric | Target | Check method
- Risk signals: 5-7 signs of impending churn during onboarding + action

TONE: Warm, supportive, proactive.
LENGTH: 6-8 pages.
```

---
✍️ Author: Brian H. Doan
