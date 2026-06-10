# P-FIN-19: Monthly Financial Dashboard

#### Description
A consolidated one-page financial dashboard — an executive summary for the Owner/Board. Includes KPI cards, trend charts, traffic-light indicators, and key highlights/actions.

#### Information to collect (ask the user before generating)
1. Top 8-10 financial KPIs to track? (e.g. Revenue, GP%, NI, Cashflow, AR/AP, DSO...)
2. Compare against what? (vs. Budget / vs. Prior Month / vs. Prior Year)
3. Format: 1-page PDF / live Google Sheets / Power BI / Markdown?
4. Who reads it? (Owner monthly / Board quarterly)
5. Need a commentary section, or just the numbers?

#### Suggested template
Structure:
- **Header** — Month/Year, Company, "FINANCIAL DASHBOARD"
- **KPI Cards** — 8-10 cards: Metric | Actual | Target | Variance | ↑↓ | 🟢🟡🔴
- **P&L Summary** — Mini P&L: Revenue → GP → EBITDA → NI (actual vs. budget)
- **Cashflow Summary** — Inflow | Outflow | Net | Balance → trend line
- **AR/AP Summary** — Total | Overdue | DSO | DPO
- **Top 3 Highlights** — the positives
- **Top 3 Concerns** — items to watch + action required
- **Next Month Outlook** — forecast / plan

Confirm the structure before generating.

#### File-generation prompt
```
Create a Monthly Financial Dashboard template.

CONTEXT:
- Company: [Name]
- KPIs: [list 8-10 KPIs]
- Comparison: [Budget / Prior / Both]
- Format: [1-page PDF / Sheets / Markdown]
- Audience: [Owner / Board]

FORMAT:
- A single page — compact, visual, scannable
- KPI cards: 2 rows × 4-5 columns — Metric | Value | vs. Target | Trend | Status light
- Mini P&L: 6 lines max — Revenue → COGS → GP → SG&A → EBITDA → NI
- Cash position: Balance + trend sparkline data
- AR/AP: pie-chart data (Current vs. Overdue)
- Traffic light: 🟢 On track | 🟡 Watch | 🔴 Action needed
- Commentary: max 3 bullet highlights + 3 bullet concerns
- Action items: Owner | Due date

TONE: Executive — concise, visual, action-oriented.
LENGTH: 1 page (+ 1 page of fill-in instructions).

CROSS-REFERENCE: This is the financial data dashboard. For the standard report format, see bb-reporting/Financial report and Monthly management report.
```

---
✍️ Author: Brian H. Doan
