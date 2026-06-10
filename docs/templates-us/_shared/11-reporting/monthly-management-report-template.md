### PROMPT 03: Monthly Management Report Template

#### Description
A monthly management report for the leadership team — a one-page executive summary of company-wide performance plus department detail. Includes a KPI scorecard, financial highlights, operational metrics, key wins, issues, and action items.

#### Information to collect (ask the user before generating)
1. Who reads the monthly report? (CEO / leadership team / department heads)
2. Submission deadline? (which day each month)
3. Top KPIs for page 1? (revenue, profit, cash flow, NPS...)
4. Compare vs. Budget / vs. prior month / vs. prior year?
5. A narrative section (commentary), or just numbers?
6. Report tool? (Excel / PowerPoint / BI dashboard / document)

#### Suggested template
Structure:
- **Page 1** — Executive summary: KPI scorecard, traffic-light status, key headlines
- **Page 2** — Financial overview: P&L summary, revenue trend, expense breakdown, cash position
- **Page 3** — Sales & Marketing: pipeline, conversion, revenue by channel, campaign results
- **Page 4** — Operations: productivity, quality, SLA, incidents
- **Page 5** — People: headcount, turnover, hiring, engagement
- **Page 6** — Key Wins / Issues / Action Items: RAID log (Risks, Actions, Issues, Decisions)
- **Appendix**: detailed data tables, variance explanations

Confirm the structure before generating.

#### File-generation prompt
```
Create a Monthly Management Report Template.

CONTEXT:
- Company: [Name] — Audience: [CEO / leadership team / department heads]
- Deadline: [day X each month]
- Top KPIs: [list 8-12 page-1 KPIs]
- Comparison: [vs Budget / vs Prior month / vs YoY]
- Narrative: [Yes/No]
- Tool: [Excel / PPT / BI / document]

FORMAT:
- Page 1 — Executive Dashboard:
  - Company scorecard: 8-12 KPIs — KPI | Actual | Target | Variance | Trend (↑↓→) | Status (🟢🟡🔴)
  - Headlines: 3 key wins + 3 key concerns — 1 sentence each
  - CEO commentary: 3-5 sentences summarizing the month
- Page 2 — Financial:
  - P&L summary: Revenue | COGS | Gross Profit | OPEX | EBITDA | Net Profit — Actual vs. Budget vs. Prior (USD)
  - Revenue waterfall: Prior month → New sales + Upsell − Churn = Current month
  - Cash position: Opening | Inflows | Outflows | Closing | Runway (months)
  - Top 5 expense variances: Line item | Budget | Actual | Variance | Explanation
- Page 3 — Sales & Marketing:
  - Pipeline: Stage | # Deals | Value | Conversion % | Avg deal size
  - Revenue by channel/product: table + trend chart
  - Marketing: Leads | MQLs | SQLs | CAC | Campaign ROI
- Page 4 — Operations:
  - Productivity: Output / FTE | Utilization % | Cycle time
  - Quality: Defect rate | First pass yield | Customer complaints
  - SLA: Service | Target | Actual | Breaches
- Page 5 — People:
  - Headcount: Plan vs. Actual | New hires | Leavers | Turnover %
  - Open positions: Role | Days open | Status
  - Engagement pulse: Score | Trend
- Page 6 — RAID:
  - Risks: Risk | Impact | Probability | Mitigation | Owner
  - Actions: Action | Owner | Due | Status
  - Issues: Issue | Impact | Resolution | Owner
  - Decisions needed: Decision | Context | Options | Recommendation

TONE: Executive, visual, 1 page per section, no fluff.
LENGTH: 6-8 pages.
```

---
✍️ Author: Brian H. Doan
