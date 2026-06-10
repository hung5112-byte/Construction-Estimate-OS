# P-FIN-09: Break-Even Analysis

#### Description
A break-even (BEP) analysis for the company as a whole and for each product/service. Determines how much sales volume, and how many orders, are needed to cover all costs. Includes a sensitivity analysis for changes in price or cost.

#### Information to collect (ask the user before generating)
1. List of products/services + the selling price of each?
2. Variable cost per unit? (COGS, commissions, shipping...)
3. Total fixed cost per month?
4. Does any product cross-subsidize another?
5. Desired target margin?

#### Suggested template
Structure:
- **Overview** — company-wide BEP: break-even sales / month, / year
- **Per Product** — BEP by product: contribution margin, BEP units, BEP revenue
- **Sensitivity** — change price ±5%, ±10% → how much BEP changes
- **Margin of Safety** — gap between actual sales and BEP
- **Visualization** — chart data: total cost vs. revenue vs. BEP line
- **Recommendations** — which products to push, which to cut

Confirm the structure before generating.

#### File-generation prompt
```
Create a Break-Even Analysis.

CONTEXT:
- Company: [Name] — # products/services: [number]
- Main products: [Name | Price | Variable cost/unit | Contribution margin]
- Fixed cost: [amount/month] — Detail: [list top 5]
- Target margin: [%]

FORMAT:
- BEP Summary: table company-wide | per product → BEP units | BEP revenue | Contribution margin %
- Clear formula: BEP = Fixed Cost / (Price - Variable Cost per Unit)
- Sensitivity table: price ±5/10/15% × variable cost ±5/10/15% = BEP matrix
- Margin of Safety: Current Revenue | BEP Revenue | MoS % | Interpretation
- Chart data: X = Units, Y1 = Total Revenue, Y2 = Total Cost, intersection = BEP
- Product ranking: contribution margin desc → recommended push order

TONE: Analytical, data-driven, easy for non-finance readers.
LENGTH: 4-6 pages.
```

---
✍️ Author: Brian H. Doan
