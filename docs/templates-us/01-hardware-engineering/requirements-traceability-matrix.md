# P-HWE-30: Requirements Traceability Matrix (RTM)

#### Description
A single matrix linking each requirement to its design element, verification activity, and result — proves nothing was dropped between spec, design, and test.

#### Information to collect (ask the user before generating)
1. Source requirements set (SRS/ICD)?
2. Design artifacts to link (schematic, mechanical, firmware modules)?
3. Verification artifacts (DVP&R, test reports)?
4. Coverage gaps you already suspect?
5. Baseline/version this RTM tracks?

#### Suggested template
Structure:
- Columns: req ID -> design element(s) -> verification activity -> result/status
- Coverage summary: % requirements designed + verified
- Gaps: requirements with no design or no verification
- Orphans: design/tests with no parent requirement
- Baseline + change note

Confirm the structure before generating.

#### File-generation prompt
```
Create a Requirements Traceability Matrix (RTM).

CONTEXT:
- Requirements: [SRS/ICD ref] — Design artifacts: [...] — Verification: [DVP&R]
- Baseline: [version]

FORMAT:
- RTM table (req, design, verification, status)
- Coverage % summary; gaps + orphans lists

RULES: flag any requirement with no linked design OR no verification as a gap; flag design/tests with no parent requirement as orphans — both block baseline sign-off.
```

---
✍️ Author: Brian H. Doan
