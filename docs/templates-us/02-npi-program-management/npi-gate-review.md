# P-NPI-01: NPI Gate Review (EVT/DVT/PVT)

#### Description
The formal gate-review record for an NPI phase transition — entry/exit criteria checked against evidence, open issues dispositioned, and an explicit verdict. Gates are criteria, not dates; this document is where that principle lives.

#### Information to collect (ask the user before generating)
1. Which gate? (EVT exit, DVT exit, PVT exit / ramp entry)
2. Product and build under review?
3. The agreed exit criteria for this phase? (or use the standard set)
4. Open issues list with severities?
5. Who must sign? (NPI PM, engineering, quality, MSQ for PVT)

#### Suggested template
Structure:
- **Header**: product, phase, build/lot, review date, attendees
- **Criteria table**: criterion, required evidence, status (met / not met / waived),
  evidence link — standard sets:
  - EVT exit: design functions, major risks characterized, DVT plan approved
  - DVT exit: spec verified at sample size, cert pre-scans pass, BOM stable, FAI plan ready
  - PVT exit / ramp: process verified at rate, FPY ≥ target, test correlated, cert granted [verify], packaging/label approved
- **Open issues**: ID, severity, disposition (blocks gate / conditional action with date / accepted risk with approver)
- **Verdict**: PASS / CONDITIONAL PASS (dated actions) / FAIL (recovery plan + re-review date)
- **Sign-off**: required signatures; waivers explicitly recorded with approver

Confirm the structure before generating.

#### File-generation prompt
```
Create an NPI Gate Review document.

CONTEXT:
- Product: [model] — Gate: [EVT/DVT/PVT exit] — Build: [lot]
- Criteria set: [standard/custom] — Open issues: [list w/ severity]

FORMAT:
- Header; criteria table with evidence links; open-issues disposition table
- Verdict block (criteria-based); sign-off with explicit waiver records

RULES: a gate with open blockers cannot PASS; every waiver names its approver;
CONDITIONAL means dated actions, not vibes.
```

---
✍️ Author: Brian H. Doan
