# P-SVC-07: Excess & Obsolete (E&O) Disposition Report

#### Description
The periodic E&O review — aging stock identified, root-caused, and dispositioned while options still exist. Obsolescence is cheapest the day it's created (usually by an ECO or EOL decision); this report catches it then, not at the year-end write-off.

#### Information to collect (ask the user before generating)
1. Stock scopes? (finished goods, components, spares pools, RMA/refurb stock, consigned at factory)
2. Aging thresholds? (e.g. no movement 90/180/365 days)
3. Recent ECOs/EOLs that created obsolescence? (from change control)
4. Disposition options available? (use-as-is in builds, rework to current rev, sell-down, return-to-vendor, donate/scrap)
5. Write-down authority levels?

#### Suggested template
Structure (.xlsx):
- **Sheet "E&O List"**: part/SKU, location, qty, value, last movement, aging bucket,
  cause (ECO-#### / EOL / demand change / over-buy / refurb overflow)
- **Sheet "Dispositions"**: per item — options with recovery value and cost
  (rework cost vs. current-rev value; RTV terms; sell-down price), recommendation,
  approver per authority level
- **Sheet "Root causes"**: Pareto of causes — over-buys go back to sourcing policy,
  ECO-created E&O checks whether disposition happened at ECO time (it should have)
- **Sheet "Trend"**: E&O value by quarter — the metric that proves the process works
- **Handoffs**: ECO-time disposition gaps (bom-eco-plm), buy-policy findings (sourcing-buyer), write-down summary (VP/finance)

Confirm the structure before generating.

#### File-generation prompt
```
Create an E&O Disposition Report workbook (.xlsx).

CONTEXT:
- Scopes: [stock types] — Aging thresholds: [days] — Recent ECOs/EOLs: [list]
- Authority levels: [$ bands]

FORMAT (.xlsx):
- "E&O List" with cause codes; "Dispositions" with option economics and approvers
- "Root causes" Pareto with policy feedback; "Trend" by quarter; handoff list

RULES: every item has a cause code; ECO-caused E&O that skipped ECO-time
disposition is flagged as a change-control finding; recommendations show the
recovery math, not just "scrap".
```

---
✍️ Author: Brian H. Doan
