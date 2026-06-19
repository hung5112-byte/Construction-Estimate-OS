# P-HWE-09: Schematic Review Checklist (EE)

#### Description
A discipline-specific gate for an electrical schematic before layout — catches power, reset, decoupling, protection, and net-naming issues while they are cheap to fix.

#### Information to collect (ask the user before generating)
1. Product/board and schematic revision under review?
2. Functional blocks present (power, MCU, radios, payment, I/O)?
3. Any new or risky parts (sole-source, first-use, high-power)?
4. Target standards in scope (FCC Part 15, UL/IEC 62368-1, PCI PTS)?
5. Reviewers and required sign-offs?

#### Suggested template
Structure:
- Scope: board, revision, blocks reviewed
- Checklist by area: power tree + sequencing, decoupling, reset/boot straps, protection (ESD/OVP/reverse), unused pins, test points, net naming/ERC clean
- Findings table: item, severity (block/major/minor), owner, action
- Open questions to other teams (FW boot, MSQ test access)
- Exit decision: go to layout / rework first

Confirm the structure before generating.

#### File-generation prompt
```
Create a Schematic Review Checklist (EE).

CONTEXT:
- Board: [name/rev] — Blocks: [list]
- Risky parts: [list] — Standards: [list]

FORMAT:
- Checklist grouped by area with pass/fail/NA + note
- Findings table (item, severity, owner, due)
- Sign-off block; explicit go/no-go to layout

RULES: every BLOCK-severity item must be closed or waived in writing before layout starts; ERC must be clean (zero unacknowledged errors).
```

---
✍️ Author: Brian H. Doan
