# P-SCM-01: ODM/CM Management SOP

#### Description
The operating system for managing overseas manufacturing partners (China / Vietnam / Mexico) — meeting cadence, scorecards, build commitments, tooling control, and escalation paths. Makes factory performance visible and commitments contractual rather than verbal.

#### Information to collect (ask the user before generating)
1. Which factories/sites, and which products at each?
2. Current cadence? (weekly ops call, quarterly business review?)
3. Tooling: who owns what, and is it documented?
4. Build commitment process today — written or verbal?
5. Known pain points? (slips, quality, communication)

#### Suggested template
Structure:
- **Governance cadence**: weekly ops call (schedule, shortages, quality, actions),
  monthly scorecard review, quarterly business review (capacity, cost, roadmap)
- **Build commitments**: rolling plan with frozen window, written commit per
  build, change-request rules inside the frozen window
- **Scorecard**: output vs. commit, yield, OTD, quality (DPPM with SQE),
  responsiveness — with thresholds that trigger escalation
- **Tooling & NRE register**: ownership, location, condition, duplication lead
  time for critical tools [verify MSA tooling/IP clauses with an attorney]
- **Escalation path**: named contacts both sides, time-boxed levels
- **Site risk**: region exposure review (tariffs, labor, logistics) per quarter

Confirm the structure before generating.

#### File-generation prompt
```
Create an ODM/CM Management SOP.

CONTEXT:
- Factories: [site/country → products] — Cadence today: [state]
- Tooling register exists: [yes/no] — Pain points: [list]

FORMAT:
- Governance cadence table (meeting, frequency, agenda, attendees, output)
- Build-commit procedure with frozen-window rules
- Scorecard definition with metrics, targets, escalation thresholds
- Tooling/NRE register format; escalation ladder; quarterly risk review

TONE: operational, partnership-minded but contractual. LENGTH: 3-4 pages.
```

---
✍️ Author: Brian H. Doan
