# P-MSQ-03: Factory Quality Scorecard

#### Description
The monthly quality scorecard per ODM/CM site — OQC results, escapes to dock and field, audit health, and CAPA responsiveness, on a scale that triggers consequences. What gets scored gets managed; what gets escalated gets fixed.

#### Information to collect (ask the user before generating)
1. Site(s) and products built there?
2. Metric sources? (OQC records, our IQC results, field cohort data, audit findings, SCAR log)
3. Weights and thresholds? (e.g. escapes 40%, OQC 20%, audits 20%, responsiveness 20%; green/yellow/red bands)
4. Consequence ladder? (yellow = action plan; red = business review with odm-program-mgmt)
5. Output format? (.xlsx recommended)

#### Suggested template
Structure (.xlsx):
- **Sheet "Scorecard"**: per site/month — OQC lot acceptance %, escape DPPM at our dock,
  field return rate attributable to workmanship (cohort data), open audit findings + aging,
  SCAR on-time response %, unauthorized-change strikes — weighted score + band
- **Sheet "Trends"**: 12-month score and component trends per site
- **Sheet "Actions"**: yellow/red consequences — action plans with owners, business-review triggers
- **Sheet "Definitions"**: each metric's formula, source, and window

Confirm the structure before generating.

#### File-generation prompt
```
Create a Factory Quality Scorecard workbook (.xlsx).

CONTEXT:
- Sites: [list] — Products: [per site] — Weights/bands: [definition]
- Consequence ladder: [yellow/red actions]

FORMAT (.xlsx):
- "Scorecard" (metrics, weighted score, band per site/month)
- "Trends" (12-month), "Actions" (consequences with owners),
  "Definitions" (formula/source/window per metric)

RULES: unauthorized changes are an automatic strike regardless of outcome;
a red band always opens a business review; definitions prevent metric drift.
```

---
✍️ Author: Brian H. Doan
