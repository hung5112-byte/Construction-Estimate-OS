# P-MSQ-02: Supplier / Factory Audit Checklist

#### Description
The on-site audit instrument for suppliers and ODM lines — process discipline, change control, traceability, and the floor-vs-paper gap. Audits the line, not the conference room: every section demands observed evidence.

#### Information to collect (ask the user before generating)
1. Audit target? (component supplier / ODM line / specific process)
2. Audit type? (qualification, surveillance, for-cause after an escape)
3. Sections in scope? (quality system, incoming control, process control, change control, traceability, ESD/MSL handling, test, packaging)
4. Prior findings to verify closed?
5. Auditor(s) and date?

#### Suggested template
Structure:
- **Header**: target, type, date, auditor, escort, areas walked
- **Section checklists** — each item scored (compliant / minor gap / major gap / not observed) with observed evidence:
  - Quality system: procedures match practice, records real-time (not backfilled)
  - Incoming control: their IQC on their suppliers, quarantine discipline
  - Process control: control plan at the station, parameters within spec, operator knowledge spot-check
  - Change control: last 3 changes — authorized? our notification required and given?
  - Traceability: pick a unit, trace back to lots/date codes in minutes, not days
  - ESD/MSL: grounding checks, MSL clocks honored, floor-life records
  - Test: fixtures calibrated, golden units controlled, retest discipline
  - Packaging/labeling: spec match, label data verification
- **For-cause focus** (if applicable): the escape path walked end-to-end
- **Findings + verdict**: per-section scores, overall, findings with owners/dates; closure on evidence

Confirm the structure before generating.

#### File-generation prompt
```
Create a Supplier/Factory Audit Checklist.

CONTEXT:
- Target: [supplier/line] — Type: [qual/surveillance/for-cause]
- Sections: [list] — Prior findings: [list]

FORMAT:
- Header; per-section checklist tables (item, score, observed evidence)
- Traceability drill instructions; change-control sample of last 3 changes
- Findings table with owners/dates; overall verdict

RULES: every score cites observed evidence (a record ID, a photo, a unit serial);
"not observed" is a score, not a pass; prior findings are re-verified on the floor.
```

---
✍️ Author: Brian H. Doan
