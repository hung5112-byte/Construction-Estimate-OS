# P-MSQ-01: Supplier Qualification Report

#### Description
The qualification record for a new supplier or a new part at an existing supplier — capability assessment, audit result, FAI outcome, and an explicit approval scope. Qualification is an audit and an FAI, not a marketing deck; this report is the evidence.

#### Information to collect (ask the user before generating)
1. Supplier and the commodity/part(s) being qualified?
2. Why this supplier? (second source, cost, capability, region)
3. Audit performed? (on-site / remote / waived-with-justification)
4. FAI scope and results?
5. Approval scope requested? (specific parts, commodity family, volume cap during probation)

#### Suggested template
Structure:
- **Header**: supplier, site(s), commodity, requested scope, qualification owner
- **Business screen**: financial health note, capacity, region risk, certifications held (ISO 9001 etc. — certificate refs)
- **Audit summary**: date, auditor, scorecard result, findings with closure status
- **Process capability**: key processes, capability data (Cpk where available), special processes flagged
- **FAI**: part(s), result, deviations dispositioned
- **Counterfeit/traceability controls** (for distributors/brokers): protocol verified
- **Verdict**: APPROVED (scope + probation terms: tightened inspection for N lots) / CONDITIONAL / REJECTED
- **AVL action**: entry with scope; scorecard baseline started
- **Handoffs**: AVL update (bom-eco-plm), buying clearance (sourcing-buyer), IQC level (qc-inspection)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Supplier Qualification Report.

CONTEXT:
- Supplier: [name/site] — Commodity: [parts] — Reason: [second source/cost/...]
- Audit: [date/result] — FAI: [result] — Requested scope: [definition]

FORMAT:
- Header; business screen; audit summary with findings closure
- Capability data; FAI results; counterfeit-control check where applicable
- Verdict with probation terms; AVL action; handoff list

RULES: approval scope is explicit (parts, volumes, sites); probation means
tightened inspection with stated exit criteria; a waived audit states who
accepted the risk.
```

---
✍️ Author: Brian H. Doan
