# Emergency Component Inspection Checklist — Broker / Spot-Buy Parts

> ⚠️ SYNTHETIC DEMO TEMPLATE — Lone Star Interactive Systems (LSI). General information only; not legal advice.
> Task: {{task_id}}
> Scope: 100% inspection of open-market (broker) purchased components before release to production stock.

## 1. Document Control
- Part number / description: ______________________ (e.g., eMMC 64 GB, Kioxia)
- Broker / vendor: ______________________
- PO number: ______________________ · Lot/date codes: ______________________
- Quantity received: ________ · Inspector: ________ · Date: ________

## 2. Documentation Review (all must pass)
- [ ] Certificate of Conformance present and matches PO
- [ ] Traceability statement: original manufacturer, date code, country of origin
- [ ] No mixed date codes within a single reel/tray unless declared
- [ ] Moisture Sensitivity Level (MSL) bag intact, humidity indicator card within spec
- [ ] ESD packaging compliant (shielded bag, no regrind trays)

## 3. Visual Inspection (sample: 100% external, AQL 0.65 detailed)
- [ ] Package markings match manufacturer specification (font, layout, logo)
- [ ] No evidence of remarking: surface texture uniform, no sanding/blacktop residue
- [ ] Solder balls/pads: no oxidation, no coplanarity defects, no rework flux
- [ ] No scratches, chips, or mold damage on package body
- [ ] Reel/tray labels consistent with date codes on parts

## 4. Electrical / Authenticity Verification
- [ ] Decapsulation or X-ray on sample (n = 3 per lot): die markings match manufacturer
- [ ] Read manufacturer ID + device ID registers (n = 5): match datasheet values
- [ ] Functional test on golden test board (n = 5): boot, read/write, wear-leveling registers
- [ ] Solderability test per J-STD-002 (n = 3) if date code > 2 years old

## 5. Disposition
| Result | Action |
|---|---|
| All sections pass | Release to production stock with "broker-verified" label |
| Documentation fail | Quarantine — escalate to SQE within 24 h |
| Any authenticity fail | Reject entire lot, supplier complaint, report to GIDEP/ERAI as applicable |

## 6. Sign-off
- IQC inspector: ______________ Date: ______
- SQE approval: ______________ Date: ______
- Quality manager (lot release): ______________ Date: ______

*Context: {{brief}}*
