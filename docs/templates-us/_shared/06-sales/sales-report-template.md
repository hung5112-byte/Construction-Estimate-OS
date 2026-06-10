### PROMPT 14: Sales Report Template

#### Description
A sales report template at 3 cadences (daily/weekly/monthly) — tracking performance by rep, product, and channel, and comparing to target. Includes variance analysis and action items.

#### Information to collect (ask the user before generating)
1. Which cadences? (daily / weekly / monthly / all)
2. KPIs to track? (revenue, deals, conversion, activities, pipeline...)
3. Break down by what? (per rep / per product / per channel / per region)
4. Compare against what? (vs. target / vs. prior period / vs. prior year)
5. Who receives it? (Sales Manager / Director / CEO)
6. Format? (Excel / Dashboard / Email / Markdown)

#### Suggested template
Structure:
- **Daily Flash Report**: today's revenue | # deals closed | pipeline movement | top activities
- **Weekly Report**: revenue WTD | deals W/L | pipeline changes | rep ranking | actions next week
- **Monthly Report**: revenue MTD | vs. target | vs. prior | breakdown per rep/product/channel | variance analysis | next-month forecast
- **KPI Dashboard**: visual summary — cards + charts + tables
- **Variance Analysis**: top 5 positive + negative variances + root cause + actions
- **Rep Leaderboard**: ranking by revenue, deals, activities
- **Product Performance**: revenue + margin per product/service

Confirm the structure before generating.

#### File-generation prompt
```
Create a Sales Report Template.

CONTEXT:
- Company: [Name] — Team size: [# reps]
- Cadence: [daily / weekly / monthly / all]
- KPIs: [list]
- Breakdown: [rep / product / channel / region]
- Comparison: [target / prior / prior year]
- Audience: [Sales Manager / Director / CEO]

FORMAT:
- Daily flash: 1 compact table — Revenue | Deals | Pipeline | Activities — 5-min read
- Weekly: 1 page — Revenue WTD vs. Target | Win/Loss | Pipeline Δ | Rep ranking | Actions
- Monthly: 2-3 pages — Revenue MTD | vs. Target | vs. Prior | Breakdown tables | Top 5 variances | Forecast
- KPI cards: Revenue | # Deals | Win Rate | Avg Deal | Pipeline | Activities — Actual | Target | Δ | Status (USD)
- Rep leaderboard: Rank | Rep | Revenue | % Quota | Deals | Win Rate | Activity Score
- Product table: Product | Revenue | Units | Margin % | vs. Target | Trend
- Variance analysis: KPI | Actual | Target | Var $ | Var % | Root Cause | Action

TONE: Data-driven, concise, executive-friendly.
LENGTH: Daily 1 page | Weekly 1-2 pages | Monthly 2-3 pages.
```

---
✍️ Author: Brian H. Doan
