# P-HWE-20: Mechanical Material Selection Record (ME)

#### Description
A decision record for housing/structural materials — balancing strength, cost, moldability, flammability, chemical resistance (sanitizer!), and regulatory needs.

#### Information to collect (ask the user before generating)
1. Part(s) and function (housing, bezel, button, gasket)?
2. Candidate materials (PC, PC/ABS, TPU, etc.)?
3. Environmental exposure (sanitizer chemicals, UV, temperature)?
4. Flammability/regulatory needs (UL 94, food-contact)?
5. Cost and moldability constraints?

#### Suggested template
Structure:
- Requirements: mechanical, chemical, thermal, regulatory
- Candidate comparison table: properties vs. requirement, cost, moldability
- Chemical-resistance assessment (cleaning agents in use)
- Flammability/regulatory status (UL 94 rating, RoHS/REACH)
- Decision + approved alternates; supply note

Confirm the structure before generating.

#### File-generation prompt
```
Create a Mechanical Material Selection Record (ME).

CONTEXT:
- Parts: [list] — Candidates: [PC/PC-ABS/TPU/...]
- Exposure: [sanitizer/UV/temp] — Regs: [UL94/food-contact]

FORMAT:
- Requirements list; candidate comparison table
- Chemical-resistance + flammability assessment
- Decision with alternates + supply note

RULES: chemical resistance must be assessed against the actual cleaning agents used in the field; cite UL 94 / regulatory ratings [verify with supplier datasheet].
```

---
✍️ Author: Brian H. Doan
