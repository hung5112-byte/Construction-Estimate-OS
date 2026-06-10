# P-RMA-01: RMA Process SOP

#### Description
The end-to-end returns process for electronic devices — authorization, intake, diagnosis, disposition (repair / refurbish / replace / scrap), and closure with SLAs. Keeps returns flowing and failure data trustworthy.

#### Information to collect (ask the user before generating)
1. Who can request an RMA, and what info is required to authorize?
2. Published warranty terms per product family?
3. Turnaround SLA commitment? (e.g. 10 business days door-to-door)
4. Advance replacement offered? For which customers?
5. Disposition economics: repair-cost ceiling vs. replacement cost?

#### Suggested template
Structure:
- **Authorization**: RMA request data (serial, symptom, site), warranty check,
  RMA number issue, return shipping instructions (battery/DG rules if applicable)
- **Intake**: receipt into RMA-quarantine stock, condition photos, queue entry
- **Diagnosis**: structured triage, failure classification (taxonomy enforced:
  hardware / firmware / damage / misuse / no-fault-found)
- **Disposition matrix**: in/out of warranty × failure class → repair / refurbish /
  replace / scrap / return-to-vendor, with cost ceilings
- **Closure**: outbound shipment or credit, customer notification, records updated
- **SLAs & KPIs**: turnaround by step, repair yield, backlog aging, cost per RMA
- **Data handoff**: weekly failure classifications to the failure analyst

Confirm the structure before generating.

#### File-generation prompt
```
Create an RMA Process SOP.

CONTEXT:
- Products: [families] — Warranty: [terms per family]
- SLA: [X days] — Advance replacement: [yes/no, criteria]
- Repair cost ceiling: [% of replacement cost]

FORMAT:
- Five-stage process (authorize → intake → diagnose → disposition → close)
  with numbered steps and owners
- Failure-classification taxonomy table (with definitions)
- Disposition matrix (warranty status × failure class → action)
- SLA/KPI table with targets; weekly failure-data handoff step

TONE: procedural. LENGTH: 3-4 pages.
```

---
✍️ Author: Brian H. Doan
