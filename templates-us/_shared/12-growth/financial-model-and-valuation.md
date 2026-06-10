### PROMPT 02: Financial Model & Valuation

#### Description
A 3-5 year financial model and business valuation — revenue model, P&L projection, cashflow projection, and 2-3 valuation methods (DCF, comparable companies, comparable transactions). The foundation for a pitch deck and investor negotiation.

#### Information to collect (ask the user before generating)
1. Revenue model? (subscription / transaction / project / hybrid)
2. Current unit economics? (CAC, LTV, ARPU, churn, payback period)
3. Financials for the last 2-3 years? (revenue, costs, profit, cash)
4. Growth assumptions? (realistic, per channel/product)
5. Headcount plan? (hiring roadmap, cost per hire)
6. Planned CapEx? (technology, infrastructure, expansion)
7. Comparable companies? (public or recent fundraises in the same space)

#### Suggested template
Structure:
- **Part 1** — Model assumptions: revenue drivers, cost drivers, macro assumptions
- **Part 2** — Revenue model: bottom-up build — customers × ARPU × retention → Revenue
- **Part 3** — P&L projection: 5-year monthly (Year 1) + quarterly (Year 2-3) + annual (Year 4-5)
- **Part 4** — Cashflow projection: operating, investing, financing → cash balance
- **Part 5** — Unit-economics dashboard: CAC, LTV, LTV/CAC, payback, gross margin
- **Part 6** — Scenario analysis: bull / base / bear cases
- **Part 7** — Valuation: DCF, comparable companies, comparable transactions
- **Part 8** — Sensitivity analysis: key variables × valuation impact
- **Appendix**: detailed assumptions log, historical financials, cap-table impact

Confirm the structure before generating.

#### File-generation prompt
```
Create a Financial Model & Valuation.

CONTEXT:
- Company: [Name] — Revenue model: [subscription/transaction/project]
- Current metrics: Revenue [___] | Growth [___]% | Gross Margin [___]% (USD)
- Unit economics: CAC [___] | LTV [___] | Churn [___]%
- Historical: [2-3 years revenue + costs]
- Headcount: Current [___] → Year 5 [___]
- Comparables: [3-5 companies + multiples]

FORMAT:
- Assumptions page: Driver | Year 1 | Y2 | Y3 | Y4 | Y5 | Source/Rationale
- Revenue build: customer segment × growth rate × ARPU × retention → revenue per segment → total
- P&L: Revenue → COGS → GP → SG&A (detail: S&M, G&A, R&D) → EBITDA → D&A → EBIT → Tax → NI
- Cashflow: CFO | CFI | CFF → Net → Balance
- Unit economics: table CAC | LTV | LTV/CAC | Payback | Gross Margin — per segment
- DCF: WACC calculation | FCF projection | Terminal value | Enterprise value | Equity value
- Comps table: Company | Revenue | Growth | Margin | EV/Revenue | EV/EBITDA
- Sensitivity: WACC × Growth rate → valuation matrix
- Scenario comparison: Metric | Bull | Base | Bear → valuation range

TONE: Financial, rigorous, investor-grade.
LENGTH: 8-12 pages (+ spreadsheet template description).
```

---
✍️ Author: Brian H. Doan
