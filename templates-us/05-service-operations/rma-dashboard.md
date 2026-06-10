# P-SVC-02: RMA Dashboard

#### Description
The weekly RMA operations picture — intake, backlog aging, turnaround vs. SLA, repair yield, and cost per unit. The operational twin of the field-quality report: that one asks *why* units fail; this one proves the loop runs on time.

#### Information to collect (ask the user before generating)
1. Reporting window and products in scope?
2. SLA commitments? (door-to-door days, per customer tier if applicable)
3. Data source? (RMA system export, bench logs)
4. Cost elements tracked? (labor, parts, freight, scrap)
5. Output format? (.xlsx recommended)

#### Suggested template
Structure (.xlsx):
- **Sheet "Flow"**: per week — RMAs authorized, received, completed, shipped back; WIP and backlog with aging buckets (0-5 / 6-10 / >10 days)
- **Sheet "SLA"**: turnaround distribution vs. commitment, % within SLA, the misses with causes (parts wait / diagnosis / capacity)
- **Sheet "Bench"**: repair yield (repaired vs. scrapped vs. NFF), throughput per tech-day, parts blockers
- **Sheet "Cost"**: cost per RMA (labor + parts + freight), warranty vs. billable split, scrap value
- **Sheet "Handoffs"**: classification completeness (feeds field-quality), parts demand to inventory, aging escalations

Confirm the structure before generating.

#### File-generation prompt
```
Create an RMA Dashboard workbook (.xlsx).

CONTEXT:
- Window: [weekly] — Products: [list] — SLA: [days, tiers]
- Cost elements: [list]

FORMAT (.xlsx):
- "Flow" with aging buckets; "SLA" distribution + miss causes
- "Bench" yield/throughput/blockers; "Cost" per-unit economics
- "Handoffs" (classification completeness %, parts demand, escalations)

RULES: backlog is shown in aging buckets, never one number; every SLA miss
carries a cause; "parts wait" misses generate a line to sourcing/inventory.
```

---
✍️ Author: Brian H. Doan
