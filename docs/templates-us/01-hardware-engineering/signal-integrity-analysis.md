# P-HWE-12: Signal Integrity Analysis (EE)

#### Description
An SI assessment for the board's critical buses — impedance, length matching, crosstalk, and termination — to avoid intermittent, hard-to-debug field failures.

#### Information to collect (ask the user before generating)
1. Which buses/interfaces (USB 2.0/3.x, MIPI, DDR, Ethernet, SD)?
2. Edge rates and clock frequencies?
3. Stackup and target impedances (single-ended/differential)?
4. Connector/cable transitions and lengths?
5. Available tooling (sim, TDR, eye-diagram capability)?

#### Suggested template
Structure:
- Interface inventory + spec (Z0, skew, jitter budgets)
- Topology + termination strategy per net class
- Length-match and crosstalk budget vs. spec
- Risk areas: vias, connectors, stubs, return-path gaps
- Verification plan: sim and/or measured eye/TDR

Confirm the structure before generating.

#### File-generation prompt
```
Create a Signal Integrity Analysis (EE).

CONTEXT:
- Interfaces: [USB/MIPI/DDR/...] — Stackup: [...]
- Lengths/connectors: [...] — Tooling: [sim/TDR/scope]

FORMAT:
- Per-interface spec + budget table
- Topology/termination notes; risk list
- Verification plan with pass criteria (eye mask, jitter)

RULES: each interface states its governing spec and the eye/jitter pass criteria; unverifiable claims flagged [verify by sim/measurement].
```

---
✍️ Author: Brian H. Doan
