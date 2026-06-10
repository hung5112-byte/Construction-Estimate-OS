# P-QR-07: Quality Metrics Dashboard

#### Description
The division's single quality picture — factory FPY and field return rate on one page, with escapes, COPQ, CAPA health, and audit status. Factory yield and field returns are one quality picture, never two; this dashboard enforces that.

#### Information to collect (ask the user before generating)
1. Products/sites in scope?
2. Metric sources? (factory test data, RMA classifications, IQC lot records, CAPA log)
3. Targets per metric? (FPY, return rate, escape DPPM, CAPA aging)
4. Cadence? (monthly to the VP recommended)
5. Output format? (.xlsx with a summary sheet recommended)

#### Suggested template
Structure (.xlsx):
- **Sheet "Summary"**: one page — per product: FPY (factory), OQC/dock escapes (DPPM),
  field return rate (annualized), COPQ $ (scrap + rework + RMA + expedites attributable
  to quality), each vs. target with trend sparkline description
- **Sheet "Factory"**: FPY by site/station, top fallout Pareto, retest-rate watch
- **Sheet "Field"**: return rates by cohort, top modes (links to the monthly field report)
- **Sheet "Systems"**: CAPA count by phase + aging, audit findings open/overdue,
  SCAR recurrence count, document-control health
- **Sheet "Definitions"**: each metric's formula and data source — so no two people compute it differently

Confirm the structure before generating.

#### File-generation prompt
```
Create a Quality Metrics Dashboard workbook (.xlsx).

CONTEXT:
- Products/sites: [list] — Targets: [FPY %, return %, DPPM, CAPA days]
- Sources: [systems] — Cadence: [monthly]

FORMAT (.xlsx):
- "Summary" one-pager (metric vs. target vs. trend per product)
- "Factory" (FPY/fallout/retest), "Field" (cohort rates/modes),
  "Systems" (CAPA/audit/SCAR health), "Definitions" (formula + source per metric)

RULES: every metric has a definition row; factory and field appear on the same
summary page; COPQ includes quality-attributable expedites, not just scrap.
```

---
✍️ Author: Brian H. Doan
