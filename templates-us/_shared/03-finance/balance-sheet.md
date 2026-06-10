# P-FIN-17: Balance Sheet

#### Description
A balance-sheet template under **US GAAP**. Analyzes the structure of assets and liabilities/equity and the change across periods. General information only — not accounting advice.

#### Information to collect (ask the user before generating)
1. Accounting basis? (US GAAP accrual / cash basis)
2. Which period to compare? (period end vs. beginning of year / prior period end)
3. Any large fixed assets? (real estate, machinery, vehicles)
4. Any long-term debt? (bank loans, notes)
5. Frequency? (quarterly / annual)

#### Suggested template
Structure:
- **Balance Sheet** — standard GAAP format
- **Assets**: current (cash, receivables, inventory, other) + non-current (PP&E, investments, other)
- **Liabilities & Equity**: liabilities (current + long-term) + owner's/stockholders' equity
- **Composition analysis**: % of each line / total assets
- **Change analysis**: compare 2 periods, explain large changes
- **Key ratios**: current ratio, quick ratio, D/E, ROE, ROA

Confirm the structure before generating.

#### File-generation prompt
```
Create a Balance Sheet template.

CONTEXT:
- Company: [Name] — Basis: [US GAAP accrual / cash]
- Comparison: [beginning of year / prior period]
- Fixed assets: [Yes/No] — Large items: [list]
- Debt: [Yes/No] — Detail: [current / long-term]

FORMAT:
- Balance-sheet template (GAAP) — 2 columns (period end | beginning of year)
- Composition: a % column for each line / total
- Change: $ change | % change | commentary
- Ratio cards: current ratio | quick ratio | D/E | ROE | ROA + benchmark
- Chart data: asset-structure pie + liabilities/equity-structure pie
- Working-capital analysis: CA - CL = NWC, trend

TONE: Formal finance.
LENGTH: 3-5 pages.

NOTE: General information, not accounting advice.
```

---
✍️ Author: Brian H. Doan
