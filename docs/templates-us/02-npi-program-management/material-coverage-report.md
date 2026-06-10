# P-NPI-05: Material Coverage Report

#### Description
The buyer's coverage truth against the build plan — what's on order, confirmed, at risk, and short, with recovery options costed. The report that prevents "we found out at the line" line-downs.

#### Information to collect (ask the user before generating)
1. Which builds/plan horizon? (next build, rolling 13 weeks, quarter)
2. BOM revision(s) the coverage is computed against?
3. Data sources? (open-PO report, factory clear-to-build, MRP)
4. Risk thresholds? (e.g. unconfirmed within lead time = at-risk)
5. Output format? (.xlsx recommended)

#### Suggested template
Structure (.xlsx):
- **Sheet "Coverage"**: part, qty required (per build plan), on-hand (ours + consigned at factory), on-order, confirmed date vs. need date, gap, status (covered / at-risk / short)
- **Sheet "Shorts"**: the action list — part, build affected, line-down date, recovery options (expedite / alternate w/ ECO ref / broker w/ authenticity protocol / partial build) with cost and date each, decision owner
- **Sheet "Confirmations"**: supplier promise performance (confirmed vs. delivered history) — repeat offenders flagged
- **Sheet "Assumptions"**: BOM revision, plan version, data as-of dates

Confirm the structure before generating.

#### File-generation prompt
```
Create a Material Coverage Report workbook (.xlsx).

CONTEXT:
- Plan horizon: [builds/weeks] — BOM rev(s): [X] — As-of: [date]
- Risk thresholds: [definition]

FORMAT (.xlsx):
- "Coverage" sheet with gap/status per part
- "Shorts" sheet as an option table with costs, dates, decision owners
- "Confirmations" supplier promise-performance sheet
- "Assumptions" sheet with data vintages

RULES: every short carries at least two recovery options with costs;
unconfirmed POs inside lead time are at-risk by definition, not judgment.
```

---
✍️ Author: Brian H. Doan
