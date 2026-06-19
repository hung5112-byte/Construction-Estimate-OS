# P-HWE-15: Worst-Case Circuit Analysis (EE)

#### Description
A WCCA with component derating — verifies critical circuits still meet spec at the limits of tolerance, temperature, and aging, especially for payment and power paths.

#### Information to collect (ask the user before generating)
1. Which circuits are critical (power path, payment, reset, sensing)?
2. Tolerance/temperature/aging ranges to apply?
3. Derating policy in force (e.g. caps 80%V, resistors 60%P)?
4. Operating temperature extremes?
5. Safety/cert-relevant nets (PCI, isolation)?

#### Suggested template
Structure:
- Circuit list + the parameter that must hold (e.g. Vout, timing, current)
- WCCA method per circuit: min/max stack of tolerances + temp + aging
- Derating table: part, stress (V/I/P/T), rating, % used vs. policy
- Results: pass margin or violation
- Actions for violations (part change, redesign, waiver)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Worst-Case Circuit Analysis (EE).

CONTEXT:
- Circuits: [list] — Temp range: [°C] — Derating policy: [...]
- Cert-relevant nets: [PCI/isolation/...]

FORMAT:
- Per-circuit WCCA with min/max derivation
- Derating table with %-used vs. policy and pass/fail
- Violation actions list

RULES: state the derating policy used; any part exceeding policy is a violation requiring an action or written waiver; aging assumptions cited [verify].
```

---
✍️ Author: Brian H. Doan
