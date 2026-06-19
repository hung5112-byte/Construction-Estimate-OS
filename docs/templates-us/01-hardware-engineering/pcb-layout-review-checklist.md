# P-HWE-10: PCB Layout Review Checklist (EE)

#### Description
A pre-fab review of the physical layout — stackup, power/ground, high-speed routing, RF keep-outs, thermal, DFM/DFT — before releasing Gerbers.

#### Information to collect (ask the user before generating)
1. Board, layer count, and stackup?
2. High-speed/RF nets present (USB, DDR, antenna, contactless)?
3. Thermal hot spots and copper-pour plan?
4. DFM/DFT constraints from the CM and test team?
5. Release target (proto / DVT / production)?

#### Suggested template
Structure:
- Stackup + impedance targets
- Power/ground integrity: plane splits, return paths, decoupling placement
- High-speed/RF: length match, reference continuity, antenna keep-out
- Thermal: copper, vias, component spacing for hot parts
- DFM/DFT: courtyards, fiducials, test-point coverage, panelization
- Findings table + go/no-go to fab

Confirm the structure before generating.

#### File-generation prompt
```
Create a PCB Layout Review Checklist (EE).

CONTEXT:
- Board: [name/rev] — Layers/stackup: [...]
- Critical nets: [USB-C/RF/contactless/...] — Build: [proto/DVT/prod]

FORMAT:
- Section per area with checklist + findings
- Test-point/DFT coverage summary
- Sign-off + go/no-go to release Gerbers

RULES: controlled-impedance nets must cite the target Z and reference plane; release blocked until DFT coverage on critical nets is stated.
```

---
✍️ Author: Brian H. Doan
