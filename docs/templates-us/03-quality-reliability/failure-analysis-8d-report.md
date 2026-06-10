# P-RMA-02: Failure Analysis 8D Report

#### Description
An eight-disciplines (8D) problem-solving report for a recurring product failure mode — team, problem definition, containment, root cause, corrective actions, and verified closure. The standard vehicle for turning failure trends into permanent fixes.

#### Information to collect (ask the user before generating)
1. Failure mode and affected product(s)/revision(s)?
2. Scale: how many units affected vs. installed population (rate, not count)?
3. Where seen: factory test, IQC, field returns, deployment failures?
4. Suspected domain: design / component / process / firmware / damage?
5. Containment already in place?

#### Suggested template
Structure:
- **D1 Team**: cross-functional (RMA, engineering, quality, supplier if relevant)
- **D2 Problem**: what/where/when/how-many — with rates per cohort (lot,
  revision, firmware, site), evidence attached
- **D3 Containment**: full pipeline — factory WIP, in transit, dock stock,
  field population; effectivity dates
- **D4 Root cause**: mechanism proven with evidence (not correlation);
  escape analysis — why didn't existing controls catch it
- **D5/D6 Corrective actions**: chosen fix + implementation (ECO ref, supplier
  SCAR ref, firmware release ref), effectivity
- **D7 Prevention**: systemic change (design rule, test added, control plan)
- **D8 Closure**: verification data (before/after rate), sign-off

Confirm the structure before generating.

#### File-generation prompt
```
Create an 8D Failure Analysis Report.

CONTEXT:
- Failure mode: [description] — Products: [models/revisions]
- Rate: [returns ÷ population, by cohort] — Seen at: [factory/field/IQC]
- Containment status: [current state]

FORMAT:
- D1-D8 sections as above; rates not counts in D2
- D4 must include escape analysis
- D8 requires before/after rate data — no closure without verification
- Cross-references: ECO #, SCAR #, firmware release as applicable

TONE: evidence-first, no speculation presented as fact. LENGTH: 3-5 pages.
```

---
✍️ Author: Brian H. Doan
