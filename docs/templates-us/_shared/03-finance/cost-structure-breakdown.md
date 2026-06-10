# P-FIN-05: Cost Structure Breakdown

#### Description
A document analyzing the company's cost structure in detail — classifying costs as fixed/variable, direct/indirect, and COGS/SG&A. The foundation for budgeting, pricing, and financial decisions.

#### Information to collect (ask the user before generating)
1. Industry & business model? (manufacturing / services / trading / SaaS)
2. Your largest current cost items?
3. Do you have a current P&L to analyze?
4. Need analysis by department / product / project?
5. Any seasonal / highly variable monthly costs?

#### Suggested template
Structure:
- **Part 1** — Cost-structure overview: pie-chart data, top 10 largest items
- **Part 2** — Classification: fixed vs. variable, direct vs. indirect
- **Part 3** — COGS (cost of goods sold): detail each component
- **Part 4** — SG&A (selling, general & administrative): detail
- **Part 5** — Cost by department: breakdown per department
- **Part 6** — Trend analysis: MoM, YoY, % of revenue
- **Part 7** — Optimization opportunities: identify costs that can be cut
- **Appendix**: detailed cost template, industry benchmark

Confirm the structure before generating.

#### File-generation prompt
```
Create a Cost Structure Breakdown.

CONTEXT:
- Company: [Name] — Model: [Manufacturing / Services / Trading / SaaS]
- Revenue: [amount/year] — # departments: [number]
- Largest items: [list top 5]
- Seasonality: [Yes/No]

FORMAT:
- Summary: overview table COGS | SG&A | Other → % of revenue
- Fixed vs. variable: table each item + classification + amount + % of total
- Pie-chart data: top 10 cost items
- Per-department: table Department | Headcount | Cost | % of total | Cost per head
- Trend template: 12 months × main cost lines
- Optimization matrix: cost item | cuttability | impact | priority

TONE: Analytical, data-driven, objective.
LENGTH: 5-8 pages.
```

---
✍️ Author: Brian H. Doan
