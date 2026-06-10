### PROMPT 05: Quality Control SOP

#### Description
A quality-control process for products/services — from quality standards, inspection checklists, and handling defects/nonconformance, to tracking metrics. Applies to physical products and to services/software.

#### Information to collect (ask the user before generating)
1. Type of product needing QC? (physical / software / service)
2. Existing quality standards? (ISO, internal, industry)
3. Current inspection points? (incoming / in-process / final / post-delivery)
4. Current defect/return rate? Target?
5. Who is responsible for QC? (a dedicated team / each person self-checks)
6. A tracking tool? (spreadsheet / software / manual)

#### Suggested template
Structure:
- **Purpose & scope**
- **Quality standards**: table of criteria per product/service — criteria, spec, tolerance
- **Incoming QC**: inspect incoming materials/inputs
- **In-Process QC**: inspect during production/service delivery
- **Final QC**: inspect the finished product before delivery
- **Nonconformance Handling**: flowchart detect → record → analyze → correct → CAPA
- **Quality Metrics & Reporting**: KPIs to track quality
- **Appendix**: QC checklist template, nonconformance report form, CAPA form

Confirm the structure before generating.

#### File-generation prompt
```
Create a Quality Control SOP.

CONTEXT:
- Company: [Name] — Product type: [physical / software / service]
- Standards: [ISO / internal / industry]
- Current process: [incoming / in-process / final]
- Defect rate: [current %] — Target: [target %]
- QC team: [dedicated team / self-check / hybrid]

FORMAT:
- Quality standards: table Product | Criteria | Spec | Tolerance | Method
- QC flowchart: Mermaid — Incoming → In-Process → Final → Release
- Inspection checklist: a table per stage ☐ — Item | Criteria | Pass/Fail | Notes
- Nonconformance flow: Mermaid — Detect → Record → Analyze → Correct → CAPA → Close
- CAPA template: Issue | Root Cause (5 Whys / Fishbone) | Corrective Action | Preventive Action | Owner | Due
- Quality KPIs: Metric | Formula | Target | Frequency | Owner
  - Defect Rate, First Pass Yield, Customer Return Rate, CAPA Closure Rate
- Monthly QC report template: summary + trend + top issues + actions

TONE: ISO-style SOP, detailed, tightly controlled.
LENGTH: 6-10 pages.

CROSS-REFERENCE: This is the executable quality-control SOP. For the overall quality policy (commitment, ISO objectives), see bb-operations/Quality Policy.
```

---
✍️ Author: Brian H. Doan
