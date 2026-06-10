### PROMPT 12: Business Valuation Report

#### Description
A comprehensive business-valuation report — using 3+ methods, premium/discount analysis, and a valuation range. For fundraising, M&A, exit planning, or internal purposes (ESOP, shareholder buyout). General information only — a formal valuation requires a credentialed appraiser.

#### Information to collect (ask the user before generating)
1. Valuation purpose? (fundraising / M&A / internal / legal)
2. Financial statements for the last 3-5 years?
3. Revenue model & growth trajectory?
4. Comparable companies or recent transactions in the industry?
5. Significant IP, brand, or intangible assets?
6. Apply a control premium or minority discount?

#### Suggested template
Structure:
- **Executive Summary** — valuation range, methods, key findings
- **Company Overview** — history, business model, competitive position
- **Industry Analysis** — market size, trends, multiples
- **Financial Analysis** — historical performance, normalization adjustments, trends
- **Valuation — Method 1: DCF** — FCF projections, WACC, terminal value
- **Valuation — Method 2: Comparable Companies** — trading multiples analysis
- **Valuation — Method 3: Comparable Transactions** — M&A multiples
- **Valuation — Method 4 (optional): Asset-based** — adjusted book value
- **Premium & Discount Analysis** — control, marketability, key person
- **Valuation Summary** — weighted average, range, recommended fair value
- **Appendix**: detailed financials, comparable-company data, DCF model details, assumptions

Confirm the structure before generating.

#### File-generation prompt
```
Create a Business Valuation Report.

CONTEXT:
- Company: [Name] — Industry: [industry] — Purpose: [fundraising / M&A / internal]
- Revenue: [3 years] — Profit: [3 years] — Growth: [%] (USD)
- Comparables: [3-5 companies + multiples]
- Intangibles: [IP / Brand / Technology / other]
- Premium/Discount: [control / minority / marketability]

FORMAT:
- Executive summary: 1 page — Valuation range: [low] — [mid] — [high] + method weights
- Financial normalization: adjustments table — Item | Reported | Adjustment | Normalized | Reason
- DCF model: FCF projection 5 years | WACC components | Terminal value (growth/exit multiple) | Enterprise value | Equity value
- Comparable companies: Company | Revenue | EBITDA | Growth | EV/Revenue | EV/EBITDA | Implied value
- Comparable transactions: Transaction | Date | Revenue | Price | EV/Revenue | EV/EBITDA | Implied value
- Premium/Discount: Type | Basis | % Applied | Impact on value
- Football-field chart data: Method | Low | Mid | High → visual range comparison
- Sensitivity analysis: WACC (rows) × Terminal growth (columns) → valuation matrix
- Weighted conclusion: Method | Value | Weight | Weighted value → fair-value estimate

⚠️ NOTE: A formal/defensible valuation should be performed by a credentialed appraiser (e.g. ASA, NACVA CVA, or AICPA ABV). This template is for reference only.

TONE: Analytical, professional, valuation-grade.
LENGTH: 10-15 pages.
```

---
✍️ Author: Brian H. Doan
