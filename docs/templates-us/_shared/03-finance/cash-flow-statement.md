# P-FIN-18: Cash Flow Statement

#### Description
A Cash Flow Statement template under **US GAAP** — analyzing the three cash flows: operating, investing, and financing activities. Supports both the direct and indirect methods. General information only — not accounting advice.

#### Information to collect (ask the user before generating)
1. Method? (Direct / Indirect — most companies use indirect)
2. Accounting basis? (US GAAP accrual / cash basis)
3. Any large investing activity? (buy/sell fixed assets, equity investments)
4. Any financing activity? (borrow/repay debt, issue stock, pay dividends/distributions)

#### Suggested template
Structure:
- **Part I** — Operating cash flow: Net income → adjustments (depreciation, reserves, interest...) → changes in working capital → net cash from operations
- **Part II** — Investing cash flow: buy/sell fixed assets, investments, lending
- **Part III** — Financing cash flow: borrow/repay debt, issue stock, dividends/distributions
- **Summary** — Net Cash Flow = I + II + III → Beginning cash + Net = Ending cash
- **Analysis** — Free Cash Flow, Cash Conversion Ratio

Confirm the structure before generating.

#### File-generation prompt
```
Create a Cash Flow Statement template.

CONTEXT:
- Company: [Name] — Method: [Direct / Indirect]
- Basis: [US GAAP accrual / cash]
- Investing activity: [Yes/No] — Detail: [describe]
- Financing activity: [Yes/No] — Detail: [describe]

FORMAT:
- Cash-flow template (GAAP)
- 3 clear sections: Operating | Investing | Financing
- Reconciliation: Beginning cash + Net Cash = Ending cash (= Balance Sheet)
- Analysis: Free Cash Flow = CFO - CapEx
- Cash Conversion: NI → CFO → Ratio → Interpretation
- Chart data: 3 cash flows × 12 months, stacked bar

TONE: Formal finance.
LENGTH: 3-5 pages.

NOTE: General information, not accounting advice.
```

---
✍️ Author: Brian H. Doan
