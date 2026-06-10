# P-MSQ-05: Process Control Plan

#### Description
The control plan for a production process at the ODM — every key station's characteristics, control method, reaction plan, and ownership. The document that makes "the line drifted" impossible to discover months late.

#### Information to collect (ask the user before generating)
1. Product/assembly and the site/line?
2. Process steps in scope? (SMT, reflow, assembly, test, packaging)
3. Critical-to-quality characteristics? (from FMEA, drawings, failure history)
4. Control methods available at the factory? (SPC, checklists, poka-yoke, sampling)
5. Reaction-plan authority? (who stops the line)

#### Suggested template
Structure:
- **Header**: product, BOM/process revision, site/line, plan owner (ours + factory's)
- **Control table**: step, station, characteristic (CTQ flag), spec/tolerance,
  control method (SPC chart / parameter check / fixture poka-yoke / sample insp.),
  frequency, sample size, who measures, record location
- **Reaction plans**: per characteristic — out-of-control action (contain WIP since
  last good check, notify, disposition), restart authority
- **Special processes**: anything not verifiable by later inspection (e.g. conformal
  coat, torque, solder profile) — flagged with tightened controls
- **Change linkage**: this plan's revision follows ECO cut-ins; unauthorized parameter
  changes are scorecard strikes
- **Verification**: periodic audit of plan-vs-floor (links to the audit checklist)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Process Control Plan.

CONTEXT:
- Product: [assembly] — Site/line: [factory] — Steps: [list]
- CTQs: [characteristics] — Factory capabilities: [SPC/poka-yoke/...]

FORMAT:
- Header with dual ownership; control table (step, characteristic, spec,
  method, frequency, n, owner, record)
- Reaction plans with containment-since-last-good rule and restart authority
- Special-process flags; ECO linkage clause; audit verification note

RULES: every CTQ has a reaction plan; special processes get tightened controls;
the plan revision is tied to the BOM/process revision.
```

---
✍️ Author: Brian H. Doan
