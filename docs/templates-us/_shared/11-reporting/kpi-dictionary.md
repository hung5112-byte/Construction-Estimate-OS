### PROMPT 02: KPI Dictionary

#### Description
A master document defining all KPIs in the company — by the Balanced Scorecard's 4 perspectives. Each KPI has: name, code, definition, formula, unit, data source, measurement frequency, target, owner, and dashboard link. The single source of truth for how performance is measured.

#### Information to collect (ask the user before generating)
1. Do you have a KPI list yet? How many KPIs?
2. Classify by: BSC 4 perspectives / department / process?
3. An OKR system? How do KPIs link to OKRs?
4. Data sources: manual / ERP / CRM / BI tool?
5. Top 5-10 most important KPIs (Department Head dashboard)?
6. Cascading KPIs (company → department → individual)?

#### Suggested template
Structure:
- **Part 1** — Overview: measurement philosophy, BSC framework, cascading model
- **Part 2** — Financial KPIs: Revenue, Profit, Cash flow, ROI, cost ratios
- **Part 3** — Customer KPIs: NPS, CSAT, Retention, CAC, CLV, Market share
- **Part 4** — Internal Process KPIs: productivity, quality, cycle time, SLA compliance
- **Part 5** — Learning & Growth KPIs: training hours, employee engagement, innovation rate
- **Part 6** — Department Head Scorecard: top 10-15 company-level KPIs
- **Part 7** — Cascading guide: company → department → individual
- **Part 8** — Review & update process: add/edit/retire a KPI
- **Appendix**: KPI card template, glossary of metrics terms

Confirm the structure before generating.

#### File-generation prompt
```
Create a KPI Dictionary.

CONTEXT:
- Company: [Name] — Industry: [industry] — # departments: [number]
- KPI framework: [BSC / OKR / department / hybrid]
- Estimated # KPIs: [number]
- Data sources: [manual / ERP / CRM / BI / spreadsheet]
- Department Head top KPIs: [list top 5-10]
- Cascading: [Yes/No]

FORMAT:
- KPI overview: summary table — BSC Perspective | # KPIs | Key metrics
- KPI Card (1 card per KPI):
  - KPI Name | KPI Code | BSC Perspective | Department
  - Definition: what it measures, why it matters
  - Formula: a clear formula + numeric example
  - Unit: %, USD, count, days, points
  - Data source: which system, table, field
  - Frequency: Daily / Weekly / Monthly / Quarterly
  - Target: Threshold 🔴 | Target 🟡 | Stretch 🟢
  - Owner: who is responsible
  - Dashboard: link or location on the dashboard
  - Related KPIs: related leading/lagging indicators
- Department Head Scorecard: 10-15 KPIs on one page — Perspective | KPI | Current | Target | Trend | Status
- Cascading example: 1 company KPI → 3 dept KPIs → 5 individual KPIs
- KPI lifecycle: Propose → Define → Validate → Implement → Review → Retire
- Glossary: 20-30 common metrics terms — Revenue vs. Billings vs. Collections, Gross vs. Net, Leading vs. Lagging

TONE: Reference document, precise, easy to look up.
LENGTH: 10-15 pages (depending on # KPIs).
```

---
✍️ Author: Brian H. Doan
