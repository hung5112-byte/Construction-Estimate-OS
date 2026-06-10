# P-FIN-07: 12-Month Cash Flow Forecast

#### Description
A cash flow forecast for the next 12 months — detailing cash in (sales collections, receivables, borrowing...) and cash out (purchases, payroll, taxes, debt service...). Identifies the months that will be tight on cash and where you may need to borrow or delay spending.

#### Information to collect (ask the user before generating)
1. Current cash & bank balance?
2. Main revenue sources? (sales / projects / subscription / investment)
3. Collection cadence: daily / weekly / monthly? Any seasonality?
4. Large fixed monthly outflows? (payroll, rent, debt...)
5. Any large planned spend in the next 12 months? (asset purchase, investment, principal repayment)
6. Desired minimum cash reserve?

#### Suggested template
Structure:
- **Assumptions** — growth, collection rate, payment terms
- **Cash Inflow** — 12-month table: each source × each month
- **Cash Outflow** — 12-month table: each expense × each month
- **Net Cashflow** — Inflow - Outflow = net per month
- **Cumulative Balance** — running balance — highlight negative months
- **Sensitivity Analysis** — what-if: revenue down 10/20/30%
- **Action Plan** — for shortfall months: specific solutions

Confirm the structure before generating.

#### File-generation prompt
```
Create a 12-month cash flow forecast.

CONTEXT:
- Company: [Name] — Current balance: [amount]
- Revenue sources: [list + estimate/month]
- Fixed outflows: [list + amount/month]
- Large upcoming spend: [list + timing]
- Minimum reserve: [amount]
- Seasonality: [Yes/No] — [describe pattern]

FORMAT:
- Main table: 12 columns (months) × rows (each inflow/outflow line), in USD
- Color coding: surplus month 🟢 | shortfall month 🔴 | borderline 🟡
- Chart data: line chart — Inflow vs. Outflow vs. Balance
- Minimum-cash line: a horizontal line → alert when balance < minimum
- Sensitivity table: base case ±10%, ±20%, ±30%
- Action triggers: IF balance < [X] THEN [action]

TONE: Practical, action-oriented, clear warnings.
LENGTH: 4-6 pages.
```

---
✍️ Author: Brian H. Doan
