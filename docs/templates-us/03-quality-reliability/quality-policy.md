### PROMPT 16: Quality Policy (ISO-aligned)

#### Description
An overall quality policy — commitment, objectives, quality KPIs, PDCA, continuous improvement. Aligned with ISO 9001:2015 (usable immediately if the company wants to pursue ISO).

#### Information to collect (ask the user before generating)
1. Do you have ISO 9001 certification? (have it / want it / don't need it but want to align)
2. Main products/services needing quality control?
3. Current defect/complaint rate? (if you have data)
4. A dedicated QC/QA function? How many people?
5. Any quality KPIs already tracked?
6. Do customers require any special quality standards?
7. Current process for handling nonconforming products/services?

#### Suggested template
Structure:
- **Quality commitment**: a quality statement from the Department Head — one paragraph, poster-printed
- **Scope**: which products/services, departments, processes
- **Quality objectives**: SMART × 5-8 objectives per year
- **Quality KPIs**: table KPI | Target | How measured | Frequency | Owner
- **PDCA cycle**: Plan-Do-Check-Act for each main process
- **Customer feedback loop**: collect → analyze → improve → measure
- **Nonconformity handling**: detect → isolate → RCA → corrective → preventive
- **Management review**: frequency, agenda, expected outputs
- **Quality training**: a plan to raise QMS awareness

Confirm the structure before generating.

#### File-generation prompt
```
Create a Quality Policy.

CONTEXT:
- Company: [Name] — Industry: [industry]
- ISO 9001: [have it / want it / align only]
- Main products/services: [list]
- QC/QA team: [Yes/No] — Headcount: [number]
- Existing quality KPIs: [list]
- Current defect rate: [%]

FORMAT:
- Quality statement: one-paragraph commitment — poster-printed
- Quality objectives: SMART × 5-8 objectives
- KPIs: table KPI | Target | Measurement | Frequency | Owner
- PDCA cycle: diagram + guidance for each process
- Customer feedback loop: flowchart — collect → analyze → improve → measure
- Nonconformity handling: process + RCA
- Management review: frequency, agenda, output
- Basis: ISO 9001:2015 clauses 5.2, 6.2

TONE: ISO-aligned, professional, committed.
LENGTH: 5-8 pages.

CROSS-REFERENCE: This is the quality policy (commitment, objectives, KPIs). For the executable quality-control SOP, see bb-product-tech/Quality Control SOP.
```

---
✍️ Author: Brian H. Doan
