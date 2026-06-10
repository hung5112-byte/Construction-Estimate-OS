# P-QR-06: Early Warning Alert

#### Description
A short alert raised when a failure signal is detected but not yet conclusive — what was seen, the population at risk, and the immediate watch/containment proposal. Sent while the affected population is still small; waiting for statistical perfection while shipments continue is the anti-pattern this template kills.

#### Information to collect (ask the user before generating)
1. The signal? (bench cluster, fault-code spike, lot-correlated returns, deployment failures)
2. Counts and the cohort? (lot, HW rev, FW version, site)
3. Population at risk if the signal is real? (in field, in transit, in stock, in WIP)
4. Cheapest immediate check? (pull stock samples, query fleet logs, bench re-test)
5. Containment options if it firms up?

#### Suggested template
Structure:
- **Alert line**: one sentence — what's being seen, in what cohort, at what rate so far
- **Evidence**: counts, dates, classifications; honest confidence (this is a signal, not a conclusion)
- **Population at risk table**: field / transit / dock stock / factory WIP — counts per cohort
- **Immediate checks**: action, owner, due (hours/days, not weeks)
- **Pre-positioned containment**: what we'd do if it firms (hold lot X, pause wave 2, screen at dock) — decided now, triggered by the check results
- **Distribution**: quality manager, MSQ, engineering manager, VP — same day
- **Resolution**: escalates to an 8D, or stands down with the disproving evidence recorded

Confirm the structure before generating.

#### File-generation prompt
```
Create an Early Warning Alert.

CONTEXT:
- Signal: [description] — Cohort: [lot/rev/FW/site] — Counts: [n of population]
- At-risk: [field/transit/stock/WIP counts] — Checks available: [list]

FORMAT:
- One-line alert; evidence with stated confidence; at-risk table
- Immediate checks with owners and hour/day deadlines
- Pre-positioned containment with triggers; same-day distribution list
- Resolution rule (8D or stand-down with evidence)

RULES: hours/days deadlines only; containment is pre-decided with triggers;
stand-downs record the disproving evidence so the signal isn't re-found monthly.
```

---
✍️ Author: Brian H. Doan
