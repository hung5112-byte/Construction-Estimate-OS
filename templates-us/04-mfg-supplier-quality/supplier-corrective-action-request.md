# P-QC-02: Supplier Corrective Action Request (SCAR)

#### Description
The formal corrective-action request sent to a supplier or factory after a quality escape — defect definition, containment expectations, root-cause requirements (including escape analysis), and verified closure criteria. Standardizes how suppliers are required to respond.

#### Information to collect (ask the user before generating)
1. Supplier/factory and the affected part/assembly?
2. Defect description and detection point? (IQC, factory test, field/RMA)
3. Quantities: rejected lot size, suspect population (other lots, field)?
4. Required response times? (containment 24-48h, root cause 14 days, etc.)
5. Prior SCAR history with this supplier for similar defects?

#### Suggested template
Structure:
- **Header**: SCAR #, supplier, part, date, severity, response deadlines
- **Defect definition**: what/where found, photos, rejected qty, lot/date codes,
  spec violated (drawing/criteria reference)
- **Containment (supplier)**: sort/screen WIP, in-transit, our dock and field
  exposure — with quantities certified clean and effectivity marking
- **Root cause (supplier)**: process root cause AND escape root cause (why their
  controls missed it) — both required for acceptance
- **Corrective actions**: process change with effectivity date/lot, control-plan
  update, evidence required
- **Verification & closure (us)**: acceptance criteria — N clean lots / re-audit /
  DPPM threshold over M weeks; recurrence rule (repeat defect reopens at
  higher severity)

Confirm the structure before generating.

#### File-generation prompt
```
Create a SCAR form/document.

CONTEXT:
- Supplier: [name] — Part: [P/N] — Detection: [IQC/factory/field]
- Rejected: [qty/lots] — Deadlines: [containment X h, RCA Y days]

FORMAT:
- Header block; defect definition with evidence fields
- Containment section covering full pipeline with quantities
- Root-cause section requiring process + escape causes
- Corrective-action table (action, effectivity, evidence)
- Closure criteria + recurrence clause; signature blocks both parties

TONE: firm, factual, partnership-with-accountability. LENGTH: 2 pages.
```

---
✍️ Author: Brian H. Doan
