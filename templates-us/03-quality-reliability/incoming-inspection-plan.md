# P-QC-03: Incoming Inspection Plan (IQC)

#### Description
The AQL-based incoming-inspection plan — what gets inspected per commodity, sampling levels, accept/reject criteria, and the tightened/normal/skip-lot switching rules that reward capable suppliers. The dock-side filter that keeps escapes out of stock.

#### Information to collect (ask the user before generating)
1. Commodity groups received? (PCBAs, finished devices, mechanical, packaging, cables)
2. Criticality per group — what failure would hurt most downstream?
3. AQL levels in use or desired? (e.g. 0.65 critical / 1.0 major / 2.5 minor)
4. Supplier history available to seed skip-lot eligibility?
5. Inspection capacity (people, fixtures, test equipment) at the dock?

#### Suggested template
Structure:
- **Commodity plan table**: commodity → inspection type (visual / dimensional /
  functional / document check), AQL level, sampling per ANSI/ASQ Z1.4 practice
  [UNCERTAIN — AQL choices are product-risk decisions; set with the quality
  manager]
- **Criteria**: photo-anchored accept/reject criteria per defect class
  (critical / major / minor) — referencing IPC-A-610 class for PCBAs
- **Switching rules**: normal → tightened on rejection, normal → skip-lot after
  N consecutive accepted lots, skip-lot revoked on any reject or SCAR
- **Rejection flow**: quarantine, discrepancy report to Supply Chain same day,
  SCAR trigger threshold, disposition (RTV / sort / use-as-is with waiver)
- **Records & KPIs**: lot acceptance rate by supplier, DPPM trend, inspection
  cycle time

Confirm the structure before generating.

#### File-generation prompt
```
Create an Incoming Inspection Plan.

CONTEXT:
- Commodities: [groups] — AQL: [levels or "propose"]
- Supplier history: [available/none] — Capacity: [inspectors/equipment]

FORMAT:
- Commodity plan table (type, AQL, sample plan)
- Defect classification with accept/reject criteria per class
- Switching rules (tightened/normal/skip-lot) as a state table
- Rejection flow with same-day reporting and SCAR threshold
- KPI table (acceptance rate, DPPM, cycle time) with targets

TONE: inspection-floor usable. LENGTH: 3 pages.
```

---
✍️ Author: Brian H. Doan
