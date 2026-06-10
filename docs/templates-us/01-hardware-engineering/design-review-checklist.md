# P-HWE-01: Design Review Checklist

#### Description
A gate checklist for schematic, layout, and mechanical design reviews — the record that a design was reviewed against criteria before money is spent on boards or tooling. Output of the review is a verdict plus an owned action list, not a discussion summary.

#### Information to collect (ask the user before generating)
1. Review type? (schematic / PCB layout / mechanical / combined)
2. Product and revision under review?
3. Which checklist sections apply? (power, signal integrity, EMC hygiene, DFM/DFT, thermal, mechanical fit, firmware hooks, certification impact)
4. Reviewers required? (EE, ME, FW, manufacturing engineering, certification)
5. Target build this review gates?

#### Suggested template
Structure:
- **Header**: product/revision, review type, date, reviewers present, gating build
- **Checklist sections** (tailored): each item = criterion, pass/fail/N/A, evidence link
  - Power: rails, sequencing, derating, brown-out behavior
  - Signal integrity: critical nets, stack-up, termination
  - EMC/ESD hygiene: returns, shielding, protection on connectors
  - DFM/DFT: test points, fiducials, panelization, connector access [review with manufacturing engineering]
  - Thermal: dissipation paths, hot spots, ambient assumptions
  - Mechanical: keep-outs, tolerance interfaces, fastening
  - Certification impact: change re-triggers? [written verdict from certification]
- **Findings table**: ID, severity (blocker/major/minor), owner, due date
- **Verdict**: APPROVED / APPROVED WITH ACTIONS (dated) / REJECTED
- **Sign-off**: reviewer signatures

Confirm the structure before generating.

#### File-generation prompt
```
Create a Design Review Checklist document.

CONTEXT:
- Product: [model] rev [X] — Review type: [schematic/layout/mech]
- Gating build: [EVT/DVT/PVT/production change]
- Sections in scope: [list]

FORMAT:
- Header block; per-section checklist tables (criterion, P/F/NA, evidence)
- Findings table with severity/owner/due
- Verdict block with explicit criteria; sign-off block

RULES: a review with open blockers cannot be APPROVED; every finding has an
owner and date; certification impact requires a written verdict, not "probably fine".
```

---
✍️ Author: Brian H. Doan
