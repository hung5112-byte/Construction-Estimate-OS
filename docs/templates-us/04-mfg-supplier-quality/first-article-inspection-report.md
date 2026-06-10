# P-MSQ-04: First Article Inspection (FAI) Report

#### Description
The FAI record proving a supplier or process change produces conforming parts before production use — full dimensional/functional verification against the drawing, with every characteristic accounted for. No first production use without a dispositioned FAI.

#### Information to collect (ask the user before generating)
1. Trigger? (new supplier, new tool, tool repair, process move, drawing revision, 2-year lapse)
2. Part and drawing revision?
3. Sample size and selection? (typically 1-5 from a production-intent run)
4. Characteristics list source? (ballooned drawing, CTQ list)
5. Functional/material tests required beyond dimensions? (material certs, plating, RoHS)

#### Suggested template
Structure:
- **Header**: part, drawing rev, supplier/site/tool ID, trigger, FAI ID, date
- **Characteristic table**: balloon #, characteristic, nominal + tolerance, measurement
  method/instrument, actual (per sample), pass/fail
- **Material/process verification**: material certs, finish/plating reports, compliance
  declarations (RoHS/REACH refs) [verify documentation authenticity]
- **Functional test**: per applicable spec, results
- **Nonconformances**: each with disposition — fix-and-re-FAI / deviation (approver named, expiry) / reject
- **Verdict**: APPROVED for production / CONDITIONAL (deviation scope) / REJECTED
- **Handoffs**: AVL/PLM status update, IQC level for first lots, scorecard entry

Confirm the structure before generating.

#### File-generation prompt
```
Create a First Article Inspection Report.

CONTEXT:
- Part: [P/N, drawing rev] — Supplier/tool: [site/tool ID] — Trigger: [reason]
- Samples: [n] — Extra verifications: [material/finish/compliance]

FORMAT:
- Header; full characteristic table (balloon, nominal/tol, method, actuals, P/F)
- Material/process verification section; functional results
- Nonconformance dispositions; verdict; handoff list

RULES: every drawing characteristic appears — no sampling of the drawing;
deviations carry a named approver and an expiry; rejected FAIs block production use.
```

---
✍️ Author: Brian H. Doan
