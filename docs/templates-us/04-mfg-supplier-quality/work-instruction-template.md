# P-MSQ-06: Work Instruction Template

#### Description
The standard format for operator work instructions at the factory — one action per step, photo-anchored, versioned, and operator-proof. A process that needs a hero operator is a defect generator; these instructions remove the need for heroes.

#### Information to collect (ask the user before generating)
1. Station/operation the instruction covers?
2. Product/assembly and revision?
3. Photos available, or to be staged at the line?
4. Language(s)? (site language + English reference)
5. Quality checkpoints embedded in the operation?

#### Suggested template
Structure:
- **Header block**: WI number + revision, station, product + revision, effective date,
  approved by (ours + factory), language
- **Safety/handling**: ESD, MSL, sharp/hot warnings — icons + one line each
- **Materials & tools table**: what must be at the station, with part numbers and torque/temp settings
- **Steps**: numbered, ONE action per step, photo per step (annotated arrows/circles),
  the defect each step prevents noted where useful
- **Quality checkpoints**: in-line checks with accept criteria (photo-anchored good/bad)
- **Nonconformance**: what the operator does on a bad unit (red bin + tag, never rework-in-place unless authorized)
- **Revision history**: change, ECO reference, date

Confirm the structure before generating.

#### File-generation prompt
```
Create a Work Instruction.

CONTEXT:
- Station: [operation] — Product: [assembly + rev] — Language(s): [list]
- Checkpoints: [in-line checks] — Settings: [torque/temp/etc.]

FORMAT:
- Header with dual approval; safety icons; materials & tools table
- Numbered steps (one action each, photo placeholder + annotation note per step)
- Quality checkpoints with good/bad photo anchors; nonconformance routing
- Revision history tied to ECO refs

RULES: one action per step, no compound steps; every checkpoint has visual
accept criteria; revisions only through change control.
```

---
✍️ Author: Brian H. Doan
