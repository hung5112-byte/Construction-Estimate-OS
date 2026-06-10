### PROMPT 04: Financial Reporting Package

#### Description
A complete financial reporting package — Income Statement (P&L), Balance Sheet, Cash Flow Statement, and variance analysis. Standard format under **US GAAP** (IFRS if applicable), for internal management and compliance.

#### Information to collect (ask the user before generating)
1. Accounting standard? (US GAAP / IFRS / both)
2. Reporting period? (monthly / quarterly / annual)
3. A consolidated report (multiple entities)?
4. Compare: vs. Budget / vs. prior period / vs. YoY?
5. Accounting software? (QuickBooks / NetSuite / Xero / manual)
6. Audience: CFO / leadership / CPA/auditor / investors / bank?

#### Suggested template
Structure:
- **Part 1** — Management commentary: financial-situation summary, key highlights
- **Part 2** — Income Statement (P&L): Revenue → COGS → Gross Profit → OPEX → EBITDA → Net Income
- **Part 3** — Balance Sheet: Assets | Liabilities | Equity — snapshot
- **Part 4** — Cash Flow Statement: Operating | Investing | Financing — indirect method
- **Part 5** — Variance analysis: Budget vs. Actual — top variances explained
- **Part 6** — Financial ratios: profitability, liquidity, leverage, efficiency
- **Part 7** — Forecast update: revised forecast based on actual performance
- **Appendix**: detailed schedules, notes to financial statements

Confirm the structure before generating.

#### File-generation prompt
```
Create a Financial Reporting Package.

CONTEXT:
- Company: [Name] — Standard: [US GAAP / IFRS]
- Reporting period: [month / quarter / year]
- Consolidated: [Yes/No] — # entities: [number]
- Comparison: [vs Budget / vs Prior / vs YoY]
- Accounting software: [name]
- Audience: [CFO / leadership / CPA / investors]

FORMAT:
- Management commentary: 1 page — revenue trend, profitability, cash position, outlook, risks
- Income Statement: standard US GAAP format
  - Revenue (by product/segment) | COGS | Gross Profit | Gross Margin %
  - OPEX (by category: Personnel, Marketing, Admin, R&D, Depreciation)
  - EBITDA | EBIT | Interest | Tax | Net Income | Net Margin %
  - Columns: Actual MTD | Budget MTD | Variance | Actual YTD | Budget YTD | Prior YTD (USD)
- Balance Sheet:
  - Current Assets: Cash | AR | Inventory | Prepaid
  - Non-current Assets: PP&E | Intangible | Investments
  - Current Liabilities: AP | Accrued | Short-term debt | Taxes payable
  - Non-current Liabilities: Long-term debt | Provisions
  - Equity: Capital | Retained earnings | Current-year profit
  - Columns: Current period | Prior period | Change | Change %
- Cash Flow Statement (indirect):
  - Operating: Net income ± adjustments ± working-capital changes = Operating CF
  - Investing: Capex | Asset sales | Investments = Investing CF
  - Financing: Debt | Equity | Distributions = Financing CF
  - Net change + Opening = Closing cash
- Variance analysis: Top 10 variances — Line item | Budget | Actual | Variance | % | Root cause | Action
- Financial-ratios dashboard:
  - Profitability: Gross margin | Net margin | ROE | ROA | ROIC
  - Liquidity: Current ratio | Quick ratio | Cash conversion cycle
  - Leverage: Debt/Equity | Interest coverage | Debt-service coverage
  - Efficiency: AR days | AP days | Inventory turns | Revenue per employee
  - Table: Ratio | Current | Target | Industry avg | Trend
- Forecast update: revised full-year estimate — Revenue | EBITDA | Net Income | Cash — vs. original budget

TONE: Financial, precise, audit-ready.
LENGTH: 8-12 pages.

CROSS-REFERENCE: This is the financial-report format. For detailed data and dashboards, see bb-finance/Monthly Financial Dashboard.
```

---
✍️ Author: Brian H. Doan
