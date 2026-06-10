# P-NPI-02: Program Status Report

#### Description
The weekly one-page program truth for the VP — where the program actually is, the critical path, slips with recovery options, and decisions needed. Written so a reader who missed three weeks still understands the state in two minutes.

#### Information to collect (ask the user before generating)
1. Program/product and current phase?
2. Reporting cadence and audience? (VP weekly is the default)
3. Current critical path and its owner?
4. Changes since last report? (slips, recoveries, scope changes)
5. Decisions needed from the VP this week?

#### Suggested template
Structure:
- **Status line**: GREEN / YELLOW / RED + one sentence why (the color must match the content)
- **Phase & dates table**: phase, baseline date, current forecast, delta, trend arrow
- **Critical path**: the binding constraint, its owner, the date it must clear
- **Movement since last report**: what slipped/recovered and why (causes, not blame)
- **Top risks (max 5)**: from the risk register, with this week's change
- **Decisions needed**: framed as options with a recommendation, not open questions
- **Team lane notes** (one line each): engineering, certification, BOM/ECO, sourcing, factory, quality

Confirm the structure before generating.

#### File-generation prompt
```
Create a Program Status Report template/instance.

CONTEXT:
- Program: [product] — Phase: [current] — Audience: [VP weekly]
- Critical path: [constraint + owner] — Decisions needed: [list]

FORMAT:
- Status line with color + reason; dates table with deltas and trends
- Critical path block; movement section; top-5 risks; decisions-as-options
- One-line lane notes per team

RULES: the color matches the dates table (a RED date means a non-GREEN report);
every slip carries a recovery option; decisions are options + recommendation.
```

---
✍️ Author: Brian H. Doan
