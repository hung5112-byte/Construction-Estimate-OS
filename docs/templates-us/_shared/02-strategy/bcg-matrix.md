# PROMPT 13: BCG Matrix

#### Description
Classify products/services/SBUs on the BCG Matrix: Stars, Cash Cows, Question Marks, Dogs. Based on two axes: market growth rate and relative market share. Supports invest/exit decisions.

#### Information to collect (ask the user before generating)
1. List of products/services/SBUs to classify?
2. Revenue per product? Growth rate?
3. Estimated market share vs. the largest competitor?
4. Market growth rate of each segment?
5. Current investment per product?

#### Suggested template
Structure:
- **BCG Matrix Plot** — 2×2, data points for each product (bubble size = revenue)
- **Product Cards** — per product: Quadrant | Revenue | Growth | Market Share | Recommendation
- **Strategy per Quadrant** — Stars (Invest), Cash Cows (Harvest), Question Marks (Invest/Divest decision), Dogs (Divest/Niche)
- **Portfolio Balance** — revenue & investment allocation by quadrant
- **Action Plan** — per product: Invest more / Maintain / Reduce / Exit + Timeline

Confirm the structure before generating.

#### File-generation prompt
```
Create a BCG Matrix Analysis.

CONTEXT:
- Company: [Name]
- Products/SBUs: [List: Name | Revenue | Growth % | Market Share vs #1 competitor]
- Market growth rate benchmark: [industry = %]
- Market share benchmark: [relative to largest competitor]

FORMAT:
- Matrix data: Product | Revenue | Growth Rate | Relative Market Share | Quadrant
- Visual description: 2×2 plot with bubble-chart data
- Product analysis: half a page per product — why it's in this quadrant + evidence + recommendation
- Portfolio balance: pie-chart data — % revenue in Stars/Cash Cows/QM/Dogs
- Investment reallocation: From → To table
- 12-month action plan per product

TONE: Strategic portfolio management — decisive, data-driven.
LENGTH: 4-6 pages.
```

---
✍️ Author: Brian H. Doan
