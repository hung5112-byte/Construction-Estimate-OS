# P-HWE-04: Tolerance Stack Analysis

#### Description
A tolerance stack-up record for a critical mechanical interface — the math that predicts whether parts will assemble at production volumes, before the tool is cut. Assembly yield is decided here, not at the line.

#### Information to collect (ask the user before generating)
1. Which interface/chain? (e.g. display-to-bezel gap, connector engagement, gasket compression)
2. The dimension chain (parts and dimensions involved)?
3. Method preference? (worst-case for safety-critical; RSS for cosmetic)
4. Functional requirement? (min/max gap, engagement, compression %)
5. Known supplier process capability for the parts? [ask manufacturing engineering]

#### Suggested template
Structure:
- **Requirement**: the functional condition with min/max limits
- **Chain table**: part, dimension, nominal, tolerance, contribution direction
- **Stack result**: worst-case and RSS totals vs. requirement; predicted Cpk if capability data exists
- **Verdict**: PASS / MARGINAL (action) / FAIL (redesign or tolerance renegotiation)
- **Actions**: tolerance changes, datum changes, supplier capability requests
- **Handoffs**: drawing updates (ME), supplier capability confirmation (supplier quality), fixture implications (manufacturing engineering)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Tolerance Stack Analysis document.

CONTEXT:
- Interface: [description] — Requirement: [min/max condition]
- Chain: [part/dimension list with tolerances] — Method: [worst-case/RSS]

FORMAT:
- Requirement statement; chain table with directions
- Worst-case + RSS results vs. requirement; capability note if data exists
- Verdict with actions; handoff list

RULES: cosmetic chains may use RSS; anything affecting sealing, safety, or
connector engagement uses worst-case; every FAIL carries a redesign action.
```

---
✍️ Author: Brian H. Doan
