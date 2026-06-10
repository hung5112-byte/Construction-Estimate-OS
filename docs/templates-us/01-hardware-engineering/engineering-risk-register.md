# P-HWE-08: Engineering Risk Register

#### Description
The Hardware Engineering manager's owned risk list — technical risks across ME/EE/FW/architecture, ranked by launch and field impact, each with a mitigation and a verification. The honest companion to every schedule commitment.

#### Information to collect (ask the user before generating)
1. Scope? (one program or the whole portfolio)
2. Current top concerns from each team? (ME/EE/FW/SysArch)
3. Review cadence? (weekly with NPI, monthly with the VP)
4. Threshold for escalation to the VP?

#### Suggested template
Structure:
- **Register table**: ID, risk statement (condition → consequence), source team,
  probability (H/M/L), impact (launch slip / field failure / cost), exposure rank,
  mitigation, verification (the test/review that retires it), owner, status, review date
- **Top-5 view**: the risks the manager actively works, with this week's movement
- **Retired risks**: what closed and what evidence retired it (keeps the register honest)
- **Escalations**: risks above the VP threshold with the decision being requested

Confirm the structure before generating.

#### File-generation prompt
```
Create an Engineering Risk Register.

CONTEXT:
- Scope: [program/portfolio] — Inputs: [team concerns]
- Cadence: [weekly/monthly] — VP escalation threshold: [definition]

FORMAT:
- Register table (ID, condition→consequence, team, P, I, rank, mitigation,
  verification, owner, status, review date)
- Top-5 worked list; retired-risks section with evidence
- Escalation section framed as decisions requested

RULES: every risk is a condition→consequence sentence, not a topic; every
mitigation has a verification that can retire the risk; ranks force ordering —
no ties in the top 5.
```

---
✍️ Author: Brian H. Doan
