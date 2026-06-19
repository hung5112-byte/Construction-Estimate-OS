# P-HWE-32: ESD & Surge Protection Review (EE)

#### Description
A review of transient protection on all external-facing ports (USB-C, payment contacts, dock pins) — the difference between surviving a busy counter and a field RMA spike.

#### Information to collect (ask the user before generating)
1. External-facing ports and exposed contacts?
2. Protection devices in place (TVS, varistors, GDT)?
3. Immunity targets (IEC 61000-4-2 contact/air levels)?
4. Payment-contact and connector exposure?
5. Known field ESD failures?

#### Suggested template
Structure:
- Port inventory + exposure level
- Protection per port: device, clamp level, placement vs. connector
- Immunity targets per IEC 61000-4-2 (contact/air kV)
- Layout review: protection-first, short return, ground
- Coverage gaps + actions

Confirm the structure before generating.

#### File-generation prompt
```
Create a ESD & Surge Protection Review (EE).

CONTEXT:
- Ports: [USB-C/payment/dock] — Protection: [TVS/varistor]
- Targets: [±kV contact/air] — Field failures: [...]

FORMAT:
- Per-port protection table (device, level, placement)
- Immunity target mapping; layout notes
- Gap + action list

RULES: every external-facing port has a stated protection device and clamp level placed before downstream circuitry; cite IEC 61000-4-2 levels [verify with test].
```

---
✍️ Author: Brian H. Doan
