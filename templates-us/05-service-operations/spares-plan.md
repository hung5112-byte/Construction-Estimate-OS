# P-SVC-01: Spares Plan

#### Description
The spares-pool sizing and placement plan for a fleet or deployment program — failure rate × repair turnaround × service level, with the cost trade-off stated. The plan that makes "do we have a spare?" a math answer instead of a scramble.

#### Information to collect (ask the user before generating)
1. Fleet/program covered? (product, installed base or deployment size)
2. Failure-rate input? (from field-quality data; if pilot, the assumption used)
3. Repair loop turnaround? (door-to-door days, including cross-border legs)
4. Service-level commitment? (e.g. replacement on-site within N days, 95% fill rate)
5. Placement options? (customer site, our warehouse, regional depot)

#### Suggested template
Structure:
- **Inputs table**: fleet size, annualized failure rate [source: field-quality data; verify quarterly], repair TAT, target service level — each with its source and as-of date
- **Pool math**: expected failures in one TAT window → pool size per service level (show the formula and a sensitivity row: rate ±50%)
- **Placement table**: location, units, replenishment trigger and lead time
- **Repair-loop linkage**: returns flow that refills the pool; minimum repair-bench throughput required
- **Cost view**: pool inventory $, carrying cost, vs. downtime/penalty cost it prevents
- **Triggers**: when to resize (fleet growth, rate change from monthly field report, TAT change)
- **Handoffs**: stock setup (inventory), staging (deployment-support), rate inputs (field-quality-rma-fa)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Spares Plan.

CONTEXT:
- Fleet: [product, n units] — Failure rate: [%/yr + source] — TAT: [days]
- Service level: [commitment] — Placement options: [list]

FORMAT:
- Inputs table with sources/dates; pool math with formula + sensitivity
- Placement table with replenishment rules; repair-loop throughput requirement
- Cost-vs-downtime view; resize triggers; handoff list

RULES: every input names its source and date; the sensitivity row is mandatory
(rates are estimates); the plan states the bench throughput it depends on.
```

---
✍️ Author: Brian H. Doan
