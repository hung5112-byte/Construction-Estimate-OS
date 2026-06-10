# P-HPD-01: Bill of Materials (BOM) Template

#### Description
A structured engineering/manufacturing BOM for an electronic device — part identification, sourcing, lifecycle, and cost columns that keep design and purchasing aligned. The BOM is the contract between Hardware PD and Supply Chain.

#### Information to collect (ask the user before generating)
1. Product and revision? (BOM is per assembly revision)
2. Single-level or multi-level (sub-assemblies)?
3. Cost columns needed? (target cost, quoted cost, extended cost)
4. Which approved alternates (AVL) exist per critical part?
5. Output format: .xlsx (recommended) or .docx?

#### Suggested template
Structure (one row per line item):
- **Identification**: item #, level, reference designators, internal P/N, description
- **Sourcing**: manufacturer, MPN, approved alternates (AVL), preferred supplier
- **Lifecycle**: status (Active / NRND / EOL), last-time-buy date if applicable
- **Quantity & cost**: qty per assembly, unit cost, extended cost, cost rollup row
- **Control**: BOM revision, ECO reference, date, approved-by
- **Flags**: long-lead (>X weeks), sole-source, MSL level, RoHS/compliance notes

Confirm the structure before generating.

#### File-generation prompt
```
Create a Bill of Materials workbook for [product] rev [X].

CONTEXT:
- Product: [name/model] — Assembly P/N: [number] — Revision: [rev]
- Levels: [single / multi-level]
- Currency: USD

FORMAT (.xlsx):
- Sheet "BOM": item, level, ref des, internal P/N, description, mfr, MPN,
  alternates, qty, unit cost, ext cost, lifecycle status, lead time, flags
- Sheet "Cost rollup": material cost subtotal by category + total
- Sheet "Risk": sole-source and EOL/NRND items with mitigation owner
- Header block: revision, ECO ref, date, prepared by, approved by

RULES: every critical part needs either an alternate or a documented risk owner.
```

---
✍️ Author: Brian H. Doan
