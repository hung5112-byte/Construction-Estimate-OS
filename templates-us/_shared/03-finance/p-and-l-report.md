# P-FIN-16: P&L Report (Income Statement / Profit & Loss)

#### Description
An Income Statement (P&L) template under **US GAAP**. Includes variance analysis (vs. prior period, vs. budget) and executive commentary. General information only — not accounting advice.

#### Information to collect (ask the user before generating)
1. Accounting basis? (US GAAP accrual / cash basis for a small business)
2. What to compare? (prior period / same period last year / budget / all)
3. Need a segment P&L? (by product / department / channel)
4. Frequency? (monthly / quarterly / annual)
5. Who reads this report? (Owner / Board / Bank / CPA)

#### Suggested template
Structure:
- **Executive Summary** — 3-5 lines highlighting revenue, profit, key variances
- **P&L Statement** — standard GAAP format: Revenue → COGS → Gross Profit → Operating Expenses → EBIT → Taxes → Net Income
- **Variance Analysis** — Actual vs. Budget | Actual vs. Prior | Actual vs. Prior Year
- **Segment P&L** — by product/department/channel (if needed)
- **Key Ratios** — gross margin, operating margin, net margin, revenue growth
- **Commentary** — explain the top 5 variances

Confirm the structure before generating.

#### File-generation prompt
```
Create a P&L (Income Statement) report template.

CONTEXT:
- Company: [Name] — Basis: [US GAAP accrual / cash]
- Comparison: [Prior period / Budget / Prior year / All]
- Segment: [Product / Department / Channel / None]
- Frequency: [Monthly / Quarterly / Annual]
- Audience: [Owner / Board / Bank / CPA]

FORMAT:
- Income-statement template (GAAP)
- Variance columns: Actual | Budget | Var $ | Var % | Prior | Var $ | Var %
- Ratio dashboard: 6 key KPIs + trend arrow ↑↓→
- Segment breakdown (if any): a mini P&L per segment
- Commentary template: Top 5 variances + Root cause + Action
- Chart data: Revenue & Profit trend, 12 months

TONE: Formal finance, suitable for a bank/CPA.
LENGTH: 4-6 pages.

NOTE: General information, not accounting advice.
```

---
✍️ Author: Brian H. Doan
