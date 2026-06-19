# P-HWE-28: Design Verification Plan & Report (DVP&R)

#### Description
The plan-and-report that maps every requirement to a verification activity and records the result — the evidence package for a design gate (DVT/PVT exit).

#### Information to collect (ask the user before generating)
1. Which requirements set / SRS is being verified?
2. Gate being targeted (DVT exit, PVT exit)?
3. Verification methods available (test, analysis, inspection, demo)?
4. Sample sizes and conditions?
5. Where results/evidence are stored?

#### Suggested template
Structure:
- Verification matrix: req ID -> method -> sample/condition -> acceptance
- Status/result column (pass/fail/open) + evidence link
- Deviations/waivers with rationale
- Open items blocking the gate
- Gate recommendation (pass/conditional/fail)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Design Verification Plan & Report (DVP&R).

CONTEXT:
- Requirements: [SRS ref] — Gate: [DVT/PVT exit]
- Methods: [test/analysis/inspection/demo] — Samples: [...]

FORMAT:
- DVP&R matrix (req, method, sample, acceptance, result, evidence)
- Deviations/waivers table
- Gate recommendation with open-items list

RULES: every requirement appears exactly once with a method and acceptance; a gate cannot be recommended 'pass' with open BLOCK items — only 'conditional' or 'fail'.
```

---
✍️ Author: Brian H. Doan
