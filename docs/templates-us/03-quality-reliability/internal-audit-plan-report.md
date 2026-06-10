# P-QR-02: Internal Audit Plan & Report

#### Description
The internal audit program — annual schedule by process area, and the per-audit report with findings that close on evidence. Audits exist to find the gap between the QMS on paper and the work as done; this template audits reality, not the conference room.

#### Information to collect (ask the user before generating)
1. Planning an annual schedule, or reporting one audit?
2. Process areas in scope? (design control, change control, inspection, RMA, factory oversight, supplier management, document control)
3. Standard/criteria audited against? (internal QMS, ISO 9001 clauses, customer requirements)
4. Auditor(s) — independence from the audited area?
5. Prior findings still open in this area?

#### Suggested template
Structure (plan):
- **Schedule table**: area, criteria, auditor, planned month, prior-findings status, risk-based frequency justification
Structure (report):
- **Header**: audit ID, area, criteria, auditor, date, people interviewed
- **Method**: documents sampled, records pulled, floor observation (work-as-done vs. work-as-written)
- **Findings table**: ID, classification (major NC / minor NC / observation), requirement, evidence, statement
- **Strengths**: what works (auditing isn't only fault-finding)
- **Actions**: per finding — owner, CAPA reference for majors, due date
- **Closure rule**: findings close on evidence (re-audit or record check), not on promises

Confirm the structure before generating.

#### File-generation prompt
```
Create an Internal Audit [Plan/Report].

CONTEXT:
- Mode: [annual plan / single audit report] — Area(s): [list]
- Criteria: [QMS sections / ISO clauses] — Auditor: [name, independent of area]

FORMAT:
- Plan: risk-based schedule table with prior-findings column
- Report: header, method (incl. floor observation), findings table with
  classification + evidence, strengths, actions with CAPA refs, closure rule

RULES: every major NC opens a CAPA; evidence is quoted (record IDs), not
paraphrased; the auditor is independent of the audited area.
```

---
✍️ Author: Brian H. Doan
