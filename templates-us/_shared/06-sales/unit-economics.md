### PROMPT 04: Unit Economics

#### Description
A detailed unit-economics analysis — measuring business efficiency at the unit level: customer acquisition cost (CAC), lifetime value (LTV), payback period, and margin per channel. The basis for marketing/sales investment decisions.

#### Information to collect (ask the user before generating)
1. Average revenue per customer/order? (ARPU / average order value)
2. Repeat-purchase frequency? Return-customer rate?
3. Average marketing + sales cost to acquire one customer?
4. Average time from lead → customer?
5. Current churn / retention rate?
6. Cost breakdown by channel? (online ads, content, events, sales team)

#### Suggested template
Structure:
- **Executive Summary** — key metrics: CAC, LTV, LTV/CAC ratio, payback period
- **Part 1** — Customer Acquisition Cost (CAC): total + per-channel breakdown
- **Part 2** — Lifetime Value (LTV): calculation, assumptions, sensitivity
- **Part 3** — LTV/CAC ratio: benchmark (>3x healthy), trend, per segment
- **Part 4** — Payback period: months to recover CAC, per channel
- **Part 5** — Contribution margin per channel: revenue - variable cost per channel
- **Part 6** — Cohort analysis: retention curve, revenue per cohort
- **Part 7** — Recommendations: which channels to scale, optimize, cut
- **Appendix**: calculation methodology, data sources, benchmark references

Confirm the structure before generating.

#### File-generation prompt
```
Create a Unit Economics Report.

CONTEXT:
- Company: [Name] — Model: [B2B / B2C / SaaS / E-commerce]
- ARPU/AOV: [amount/month or /order]
- Purchase frequency: [times/year] — Retention: [%]
- M+S cost: [amount/month] — New customers/month: [number]
- Conversion rate: [%] — Sales cycle: [days]
- Channels: [list + cost per channel]

FORMAT:
- Summary dashboard: 6 KPI cards — CAC | LTV | LTV/CAC | Payback | ARPU | Churn (USD)
- CAC breakdown: table Channel | Spend | Leads | Customers | CAC | % Total
- LTV calculation: ARPU × Avg Lifespan × Gross Margin — sensitivity ±10/20%
- LTV/CAC per segment: table Segment | LTV | CAC | Ratio | Verdict (Healthy/Watch/Cut)
- Payback period: table Channel | CAC | Monthly Revenue | Payback Months
- Cohort table: Month 0-12 × cohort → Retention % + Revenue
- Recommendation matrix: Channel | LTV/CAC | Action (Scale/Optimize/Cut) | Priority

TONE: Analytical, data-driven, investment-decision-oriented.
LENGTH: 5-8 pages.
```

---
✍️ Author: Brian H. Doan
