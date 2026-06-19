# P-HWE-27: Interface Control Document (ICD)

#### Description
A precise definition of an interface between subsystems/parties (e.g. main board <-> dock, device <-> payment host) so independent teams build to the same contract.

#### Information to collect (ask the user before generating)
1. Which interface and the two sides/owners?
2. Interface type (electrical, mechanical, protocol/data, RF)?
3. Signals/pins, levels, timing, or message formats?
4. Power and grounding across the interface?
5. Versioning/compatibility expectations?

#### Suggested template
Structure:
- Interface overview + the two owners
- Physical: connector, pinout, levels, mechanical mating
- Protocol/data: messages, fields, timing, error handling
- Power/ground + sequencing across the boundary
- Compatibility/versioning + change control

Confirm the structure before generating.

#### File-generation prompt
```
Create a Interface Control Document (ICD).

CONTEXT:
- Interface: [A <-> B] — Owners: [teams] — Type: [elec/mech/proto/RF]
- Connector/protocol: [...]

FORMAT:
- Pinout/connector table; signal levels + timing
- Protocol/message definitions (if applicable)
- Versioning + change-control note

RULES: the pinout/message contract must be unambiguous (levels, direction, timing); any change requires agreement from both owners (record in change control).
```

---
✍️ Author: Brian H. Doan
