# P-MSQ-07: Yield & Fallout Report

#### Description
The weekly/monthly yield truth per product and site — FPY by station, fallout Pareto, retest-rate watch, and the separation of real defects from test artifacts. Yield read as engineering data, not a scoreboard.

#### Information to collect (ask the user before generating)
1. Product(s)/site(s) and the reporting window?
2. Data source? (factory test logs, MES export)
3. FPY targets per station/overall?
4. Retest policy? (how many retries allowed before disposition)
5. Output format? (.xlsx recommended)

#### Suggested template
Structure (.xlsx):
- **Sheet "FPY"**: per station — units in, first-pass, FPY %, target, trend; overall rolled-throughput yield
- **Sheet "Pareto"**: failure code, count, % of fallout, suspected class (real defect / test artifact / unknown), linked action
- **Sheet "Retest"**: retest rate per station (the honesty metric — passes-on-retry-3 are findings), top retest codes
- **Sheet "Correlation"**: station-pair correlation checks (same units, same verdicts?), golden-unit run results
- **Sheet "Actions"**: top fallout drivers with owner (design → ee-team, process → manufacturing-engineering, fixture → factory-test-yield), due dates

Confirm the structure before generating.

#### File-generation prompt
```
Create a Yield & Fallout Report workbook (.xlsx).

CONTEXT:
- Product/site: [list] — Window: [week/month] — FPY targets: [per station]
- Retest policy: [n retries]

FORMAT (.xlsx):
- "FPY" per station + rolled-throughput; "Pareto" with defect-vs-artifact class
- "Retest" honesty sheet; "Correlation" station/golden-unit checks
- "Actions" with routed owners and dates

RULES: retest rate is reported beside FPY, always; every top-5 Pareto item has
an owner; artifact-suspected codes get a correlation check before being dismissed.
```

---
✍️ Author: Brian H. Doan
