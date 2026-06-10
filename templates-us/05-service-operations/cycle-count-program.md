# P-OPS-N2: Cycle Count Program

#### Description
An ABC-stratified cycle-count program that keeps inventory records matching the floor — count frequencies, variance investigation rules, and accuracy KPIs. Replaces disruptive wall-to-wall counts with continuous accuracy.

#### Information to collect (ask the user before generating)
1. SKU count and rough value distribution? (for ABC stratification)
2. Serialized, lot-controlled, or quantity-only items?
3. Current record accuracy, if known?
4. Who counts, and can counting be blind (no expected qty shown)?
5. Variance threshold that triggers investigation vs. simple adjustment?

#### Suggested template
Structure:
- **Stratification**: A items (top value/movers) counted monthly, B quarterly,
  C semi-annually — adjust to volume
- **Method**: blind counts, second count on variance, daily count list generation
- **Variance rules**: tolerance by class; above tolerance → root-cause
  investigation (process leak, not just adjustment), below → adjust + log
- **Special stocks**: RMA quarantine, consigned stock at ODM, demo/loaner pools
- **KPIs**: record accuracy % by class, variance value, root-cause Pareto
- **Governance**: who approves adjustments, monthly accuracy review

Confirm the structure before generating.

#### File-generation prompt
```
Create a Cycle Count Program document.

CONTEXT:
- Company: [name] — SKUs: [n] — Serialization: [yes/partial/no]
- Current accuracy: [% or unknown] — Counters: [roles]

FORMAT:
- ABC stratification table with count frequencies
- Daily count procedure (blind count, recount rule, cutoff handling)
- Variance investigation procedure with thresholds and root-cause log
- Coverage of special stocks (RMA, consigned at factory, demo units)
- KPI table (accuracy by class, variance $) with targets
- Adjustment approval matrix

TONE: procedural. LENGTH: 2-3 pages.
```

---
✍️ Author: Brian H. Doan
