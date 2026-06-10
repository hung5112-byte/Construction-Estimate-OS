# P-QR-05: Field Quality Monthly Report

#### Description
The monthly field-quality truth — return rates by cohort (not counts), failure Pareto, 8D portfolio status, and emerging-mode watch. The division's early-warning system, written so the VP sees trends before customers report them.

#### Information to collect (ask the user before generating)
1. Reporting month and fleet sizes per product (for rate math)?
2. Data sources? (RMA intake classifications, repair bench findings, deployment escalations)
3. Cohort dimensions tracked? (product, HW rev, FW version, production lot, site/customer)
4. Open 8Ds and their phases?
5. Target return rate from the Brain (`strategy.md`)?

#### Suggested template
Structure:
- **Headline table**: per product — installed fleet, returns, annualized rate, target, trend arrow
- **Cohort views**: rate by HW rev / FW version / lot / customer — only cohorts that deviate get commentary
- **Failure Pareto**: top modes with rates and month-over-month movement; taxonomy hygiene note (NFF re-bin status)
- **8D portfolio**: ID, mode, phase (D3 containment / D4 cause / D8 verify), age, owner — aging flagged
- **Emerging modes**: small-n signals under investigation (rate, population at risk, next checkpoint)
- **Decisions needed**: containment or stop-ship calls the VP must make
- **Data quality**: classification completeness % (the report is only as good as the taxonomy)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Field Quality Monthly Report.

CONTEXT:
- Month: [MM/YYYY] — Fleets: [product: n] — Target rate: [%]
- Open 8Ds: [list w/ phase] — Emerging signals: [list]

FORMAT:
- Headline rate table with targets and trends; deviating-cohort commentary
- Failure Pareto with movement; 8D portfolio table with aging
- Emerging-modes watch; decisions-needed section; data-quality line

RULES: rates always accompany counts; an 8D aging past its phase date is
flagged, not hidden; emerging modes state the population at risk.
```

---
✍️ Author: Brian H. Doan
