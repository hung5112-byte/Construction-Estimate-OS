# P-HWE-33: Connector & Pinout Specification (EE)

#### Description
A definitive pinout and connector spec for board-to-board, dock, and external connectors — prevents reversed pins, wrong mating, and costly respins.

#### Information to collect (ask the user before generating)
1. Which connectors (board-to-board, dock pogo, USB-C, FPC)?
2. Mating part numbers and orientation/keying?
3. Pin assignments: signal, direction, level, current?
4. Power pins + current limits + sequencing?
5. Hot-plug/hot-swap requirements?

#### Suggested template
Structure:
- Connector list: ref, part, mate, keying/orientation
- Pinout table per connector: pin, net, direction, level, max current
- Power/ground pins + sequencing + inrush
- Hot-plug/ESD considerations
- Cross-check vs. ICD + schematic

Confirm the structure before generating.

#### File-generation prompt
```
Create a Connector & Pinout Specification (EE).

CONTEXT:
- Connectors: [list] — Mates: [PNs] — Hot-swap: [y/n]
- Power pins: [rails/current]

FORMAT:
- Per-connector pinout table (pin, net, dir, level, I-max)
- Keying/orientation notes; power sequencing
- Consistency check vs. ICD/schematic

RULES: pin direction and voltage level are mandatory per pin; keying/orientation must prevent reverse-mate; verify against the schematic and any ICD.
```

---
✍️ Author: Brian H. Doan
