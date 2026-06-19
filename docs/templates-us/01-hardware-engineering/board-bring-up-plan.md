# P-HWE-14: Board Bring-Up Plan (EE)

#### Description
A safe, ordered power-on and validation sequence for first articles of a new board — prevents smoke and isolates faults methodically.

#### Information to collect (ask the user before generating)
1. Board and revision; how many first articles?
2. Power architecture and expected rail voltages/sequence?
3. Programming/debug access (JTAG/SWD, bootloader)?
4. Known unknowns / first-use parts?
5. Instruments available (bench supply, scope, thermal cam)?

#### Suggested template
Structure:
- Pre-power inspection checklist (shorts, orientation, DNP)
- Current-limited power-on steps with expected rail readings
- Bring-up order: power -> clocks -> debug -> peripherals -> radios
- Per-step pass criteria + abort conditions
- Defect log + hand-back to layout/schematic if needed

Confirm the structure before generating.

#### File-generation prompt
```
Create a Board Bring-Up Plan (EE).

CONTEXT:
- Board: [name/rev] — Units: [n]
- Rails: [list + expected V] — Debug: [JTAG/SWD/UART]

FORMAT:
- Inspection checklist; staged power-on table (limit, expected, measured)
- Bring-up sequence with pass/abort criteria
- Defect log template

RULES: first power-on uses a current-limited supply with a stated trip threshold; each rail has an expected value and an abort condition before proceeding.
```

---
✍️ Author: Brian H. Doan
