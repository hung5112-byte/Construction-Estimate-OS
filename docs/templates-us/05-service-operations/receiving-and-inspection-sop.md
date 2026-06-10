# P-OPS-N1: Receiving & Inspection SOP

#### Description
The dock-to-stock process for inbound electronic products and components — receipt verification, IQC handoff, discrepancy reporting, and putaway. Targets a measurable dock-to-stock time without letting defects into stock.

#### Information to collect (ask the user before generating)
1. Inbound types? (finished goods from ODM, components, RMA returns, spares)
2. Is incoming inspection (IQC) done in-house, at a 3PL, or skip-lot per supplier?
3. Serialized receiving? (scan-level traceability)
4. Dock-to-stock target? (e.g. < 2 business days)
5. ESD / moisture-sensitive (MSL) handling areas available?

#### Suggested template
Structure:
- **Scope & roles**: receiving clerk, IQC (Quality), inventory controller
- **Receipt steps**: dock check (counts, damage, labels) → system receipt →
  IQC routing rules (what gets inspected vs. skip-lot) → putaway by storage class
  (ESD, MSL, battery)
- **Discrepancy handling**: short/over/damaged → report to Supply Chain same day,
  quarantine location, photo evidence
- **RMA returns lane**: returns received into RMA-quarantine stock, never mixed
  with sellable
- **KPIs**: dock-to-stock time, receiving accuracy, discrepancy rate by supplier
- **Records**: what is logged, where, retention

Confirm the structure before generating.

#### File-generation prompt
```
Create a Receiving & Inspection SOP.

CONTEXT:
- Company: [name] — Inbound: [FG/components/RMA/spares]
- IQC model: [in-house / 3PL / skip-lot rules] — Serialized: [yes/no]
- Dock-to-stock target: [X days]

FORMAT:
- Process flow (numbered steps + swimlane description)
- IQC routing table (commodity → inspection level)
- Discrepancy procedure with same-day reporting rule
- Separate RMA receiving lane
- KPI table with targets; records/retention table

TONE: instructional, unambiguous. LENGTH: 3-4 pages.
```

---
✍️ Author: Brian H. Doan
