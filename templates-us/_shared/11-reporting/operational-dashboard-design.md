### PROMPT 05: Operational Dashboard Design

#### Description
A guide to design and build operational dashboards — from selecting metrics, layout design, and data sources, to refresh frequency and user access. Applies data-visualization best practices (Stephen Few, Edward Tufte). The dashboard is the real-time "control panel" for management.

#### Information to collect (ask the user before generating)
1. Dashboard for whom? (CEO / COO / department head / team)
2. Tool: Excel / Google Sheets / Power BI / Tableau / Looker / Metabase?
3. Key metrics to track real-time?
4. Data sources: ERP / CRM / spreadsheet / manual / API?
5. Refresh frequency: real-time / daily / weekly?
6. Need mobile access?

#### Suggested template
Structure:
- **Part 1** — Dashboard strategy: objectives, audience, tiered dashboards (strategic/tactical/operational)
- **Part 2** — Metrics selection: pick the right metrics — leading vs. lagging, actionable vs. vanity
- **Part 3** — Layout design: wireframe, visual hierarchy, F-pattern, above-the-fold
- **Part 4** — Visualization best practices: chart-type selection, color, labels, interactivity
- **Part 5** — Data architecture: sources, ETL, data model, refresh
- **Part 6** — Dashboard catalog: all dashboards, owner, audience, metrics
- **Part 7** — Governance: access control, maintenance, update process
- **Appendix**: wireframe templates, chart-selection guide, color palette

Confirm the structure before generating.

#### File-generation prompt
```
Create an Operational Dashboard Design Guide.

CONTEXT:
- Company: [Name] — Dashboard audience: [CEO / COO / department head / team]
- Tool: [Power BI / Tableau / Looker / Google Sheets / Excel]
- Data sources: [ERP / CRM / spreadsheet / API]
- Refresh: [real-time / daily / weekly]
- Mobile: [Yes/No]

FORMAT:
- Dashboard tiers: Strategic (CEO, monthly) → Tactical (Manager, weekly) → Operational (Team, daily)
- Metrics-selection framework: table Business question | Metric | Type (Leading/Lagging) | Source | Refresh | Actionability
- CEO dashboard wireframe: layout mockup — 4-6 KPI cards top + 2-3 trend charts + 1 table
- Department dashboard wireframe: 6-8 KPI cards + 4-6 charts + filters (date, segment, region)
- Chart-selection guide:
  - Comparison: bar chart | column chart
  - Trend over time: line chart | area chart
  - Composition: pie/donut (max 5 slices) | stacked bar
  - Distribution: histogram | box plot
  - Relationship: scatter plot | bubble chart
  - KPI status: traffic-light cards | gauge | bullet chart
- Design principles:
  - Visual hierarchy: most important = top-left, largest
  - Data-ink ratio: maximize data, minimize decoration (Tufte)
  - Color: max 5-7 colors, semantic (green=good, red=bad), colorblind-safe
  - Labels: direct labeling > legends, meaningful titles, units
  - Interactivity: drill-down | filters | tooltips | cross-filtering
- Data architecture: Mermaid — source systems → ETL/Pipeline → data warehouse → dashboard tool → users
- Dashboard catalog: table Dashboard name | Audience | Tier | Metrics | Data source | Refresh | Owner | URL
- Governance: access matrix (dashboard × role), review schedule, change-request process
- Performance: load-time targets, optimization tips, caching strategy

TONE: Technical + design-oriented, visual-first thinking.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
