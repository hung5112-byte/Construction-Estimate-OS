# P-FIN-20: Notes to Financial Statements

#### Description
A template for the Notes to the Financial Statements — explaining the accounting policies applied, the detail behind the numbers, and significant events. Prepared under **US GAAP (FASB)**. General information only — not accounting/tax advice; confirm with a licensed CPA.

#### Information to collect (ask the user before generating)
1. Accounting basis? (US GAAP accrual / cash basis for a small business)
2. Specific accounting policies? (e.g. depreciation method, inventory valuation, revenue recognition under ASC 606)
3. Any significant transactions this period? (merger, disposal, litigation, large commitments)
4. Any related-party transactions to disclose? (insiders, major owners)
5. Any subsequent events to disclose?

#### Suggested template
Structure:
- **Part I** — Company info: name, EIN, industry, capital, headcount
- **Part II** — Basis of accounting (US GAAP / cash basis)
- **Part III** — Significant accounting policies: foreign currency, inventory, fixed assets, revenue (ASC 606), expenses, taxes
- **Part IV** — Detail of financial-statement line items: each material line → detailed breakdown
- **Part V** — Related-party transactions
- **Part VI** — Commitments & contingencies
- **Part VII** — Subsequent events
- **Part VIII** — Additional info: segments, EPS, dividends/distributions

Confirm the structure before generating.

#### File-generation prompt
```
Create a Notes to Financial Statements template.

CONTEXT:
- Company: [Name] — EIN: [number] — Basis: [US GAAP accrual / cash basis]
- Specific policies: [list]
- Significant transactions: [list or "none"]
- Related parties: [Yes/No]
- Basis: US GAAP (FASB ASC); for smaller entities, an income-tax or cash basis may apply [verify with CPA]

FORMAT:
- Standard GAAP note format
- Clear parts, continuously numbered
- Accounting policies: each policy a short, clear paragraph
- Line-item detail: table Line item | Beginning | Additions | Reductions | Ending
- Related parties: table Name | Relationship | Transaction | Value | Balance
- Placeholder per part: [fill in company-specific info]
- Audit note: highlight material items

TONE: Standard accounting, formal, audit-ready.
LENGTH: 8-15 pages.

NOTE: General information, not accounting advice. Confirm with a licensed CPA.
```

---
✍️ Author: Brian H. Doan
