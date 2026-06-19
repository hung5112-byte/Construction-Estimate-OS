# P-HWE-21: GD&T Drawing Review Checklist (ME)

#### Description
A review of a part/assembly drawing for correct GD&T, datums, and tolerancing — so the CM builds what engineering intended and inspection can actually measure it.

#### Information to collect (ask the user before generating)
1. Part/assembly and drawing revision?
2. Critical-to-function features and mating interfaces?
3. Datum scheme defined?
4. Inspection method available (CMM, gauges)?
5. Tolerance source (stack analysis, supplier capability)?

#### Suggested template
Structure:
- Drawing completeness: views, dims, notes, title block, units
- Datum reference frame: defined, functional, repeatable
- GD&T per feature: correct symbols, modifiers, tolerances
- Measurability: each callout inspectable with available method
- Critical features flagged + tie to tolerance stack

Confirm the structure before generating.

#### File-generation prompt
```
Create a GD&T Drawing Review Checklist (ME).

CONTEXT:
- Part: [name/rev] — Critical features: [list]
- Datums: [A/B/C] — Inspection: [CMM/gauge]

FORMAT:
- Checklist by area with pass/fail
- Per-feature GD&T review notes; measurability check
- Findings + sign-off

RULES: every critical-to-function feature must have a GD&T callout tied to a functional datum and an inspection method; unmeasurable callouts are findings.
```

---
✍️ Author: Brian H. Doan
