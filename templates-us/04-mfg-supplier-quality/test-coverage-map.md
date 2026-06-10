# P-MSQ-08: Test Coverage Map

#### Description
The map of what production test actually verifies — per functional block, which station catches what, and the explicit list of what nothing catches. Escapes live in the unmapped gaps; this document makes the gaps visible and owned.

#### Information to collect (ask the user before generating)
1. Product and the test stations in the flow? (ICT, FCT, RF cal, final functional, OQC sampling)
2. Functional blocks/features of the product?
3. Known field-failure modes to check coverage against?
4. DVT coverage available for comparison? (what's verified at design vs. production)
5. Output format? (.xlsx recommended)

#### Suggested template
Structure (.xlsx):
- **Sheet "Map"**: functional block / failure mode × station — covered (how: measurement vs. functional vs. indirect), partially, or NOT COVERED
- **Sheet "Gaps"**: every NOT COVERED row — field consequence if it escapes, detection alternative (IQC, OQC sample, field telemetry), accepted-risk owner if left open
- **Sheet "Field check"**: known field failure modes vs. the map — would today's test catch each one? (the most honest column in the workbook)
- **Sheet "Changes"**: coverage deltas from ECOs/test revisions, with dates

Confirm the structure before generating.

#### File-generation prompt
```
Create a Test Coverage Map workbook (.xlsx).

CONTEXT:
- Product: [model] — Stations: [flow] — Blocks: [functional list]
- Known field modes: [list]

FORMAT (.xlsx):
- "Map" matrix (block/mode × station, coverage type)
- "Gaps" with consequence + alternative + accepted-risk owner
- "Field check" (would we catch each known field mode today?)
- "Changes" log tied to ECO/test revisions

RULES: NOT COVERED rows always carry an owner (fix or accepted risk);
the field-check sheet is updated with every new field mode from the 8D flow.
```

---
✍️ Author: Brian H. Doan
