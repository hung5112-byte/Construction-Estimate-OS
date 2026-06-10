### PROMPT 10: Training ROI Report

#### Description
A report measuring the effectiveness of training investment — consolidating costs, benefits (tangible & intangible), calculating ROI, and recommending improvements. Uses the Phillips ROI Methodology (extending Kirkpatrick to Level 5). Helps the CEO/CFO see training as an investment, not a cost.

#### Information to collect (ask the user before generating)
1. Report for a specific program or the whole year?
2. Total training cost? (trainer, venue, materials, lost productivity, travel, technology)
3. Measurable benefits: revenue increase / cost reduction / lower turnover / higher productivity?
4. Any baseline data (before training)?
5. Isolation method: control group / trend analysis / expert estimation?
6. Report audience: CEO/CFO / HR Director / Board?

#### Suggested template
Structure:
- **Executive Summary** — ROI headline, key findings, recommendations
- **Part 1** — Program overview: description, objectives, participants
- **Part 2** — Cost analysis: all fully-loaded costs
- **Part 3** — Benefits analysis: tangible & intangible benefits
- **Part 4** — ROI calculation: formula, isolation, conversion to monetary value
- **Part 5** — Kirkpatrick results: L1-L4 summary
- **Part 6** — Intangible benefits: not monetized but valuable
- **Part 7** — Recommendations: improve, scale, or discontinue
- **Appendix**: detailed calculations, data sources, methodology notes

Confirm the structure before generating.

#### File-generation prompt
```
Create a Training ROI Report.

CONTEXT:
- Company: [Name] — Report for: [specific program / annual roll-up]
- Total training cost: [amount]
- Measurable benefits: [revenue / cost / turnover / productivity]
- Baseline data: [Yes/No]
- Isolation method: [control group / trend / expert estimate]
- Audience: [CEO / CFO / HR Director / Board]

FORMAT:
- Executive summary: 1 page — ROI %, BCR, key findings, top 3 recommendations
- Cost analysis: fully-loaded cost table (USD)
  - Direct: Trainer fees | Materials | Venue | Technology | Certification
  - Indirect: Participant time (salary × hours) | Manager time | Travel | Admin
  - Total cost per participant = Total / # participants
- Benefits analysis:
  - Tangible: table Benefit | Measurement | Before | After | Change | Monetary value | Confidence %
  - Isolation: method used per benefit — attribution % to training
  - Annualized: project benefits over 12 months
- ROI calculation:
  - BCR (Benefit-Cost Ratio) = Total Benefits / Total Costs
  - ROI % = (Net Benefits / Total Costs) × 100%
  - Payback period = Total Costs / Monthly benefit
  - Show the calculation step-by-step
- Kirkpatrick summary: table Level | Metric | Result | Target | Status
  - L1: Satisfaction | L2: Knowledge gain % | L3: Application rate % | L4: Business impact
- Intangible benefits: list — engagement, morale, teamwork, innovation, employer brand
- Sensitivity analysis: table Scenario | Assumption change | Impact on ROI — Best / Base / Worst
- Recommendations:
  - Scale: high-ROI programs → expand
  - Improve: low L3 programs → add follow-up coaching
  - Discontinue: negative-ROI programs → replace or redesign
- Trend: year-over-year training investment vs. ROI
- Benchmark: industry-average training spend per employee, ROI benchmarks

TONE: Executive, data-driven, clear conclusion — training = investment.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
