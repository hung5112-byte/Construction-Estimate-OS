# P-FIN-04: Pricing Policy

#### Description
A policy defining the methods, process, and authority for pricing products/services. Covers pricing strategy, price structure, discount policy, and the price-change process.

#### Information to collect (ask the user before generating)
1. Main products/services? How many SKUs / service lines?
2. Current pricing method? (Cost-plus / Value-based / Competitor-based / Dynamic)
3. Price structure: retail / wholesale / OEM / project pricing?
4. Discount policy? (by volume / by customer type / by payment terms)
5. Price-review frequency? Who has authority to change prices?
6. Any seasonal / market-driven products?

#### Suggested template
Structure:
- **Part 1** — Pricing objectives: target margin, market position, penetration/skimming
- **Part 2** — Pricing methods: cost-plus, value-based, competitive — when to use which
- **Part 3** — Price structure: price-list structure, tier pricing, bundle pricing
- **Part 4** — Discount policy: a discount table by type
- **Part 5** — Price-approval process: new price, price change, special price
- **Part 6** — Channel pricing: reseller, OEM, affiliate, direct
- **Part 7** — Review & adjustment: frequency, triggers, process
- **Appendix**: price-list template, discount-approval form, margin calculator

Confirm the structure before generating.

#### File-generation prompt
```
Create a Pricing Policy.

CONTEXT:
- Company: [Name] — Industry: [industry] — # SKUs/services: [number]
- Current method: [Cost-plus / Value-based / Competitive / Dynamic]
- Price structure: [Retail / Wholesale / OEM / Project]
- Discounts: [volume / customer type / payment terms]
- Price review: [frequency] — Decision maker: [title]

FORMAT:
- Pricing framework: a diagram Cost → Markup → List Price → Discount → Net Price
- Discount table: Type | Volume from-to | % discount | Approval required
- Margin analysis: table Product | Cost | Price | Margin % | Min Price Floor
- Decision tree: flowchart for when to use Cost-plus vs. Value-based vs. Competitive
- Price-approval workflow: Mermaid flowchart
- Competitive-price tracking template

TONE: Strategic + practical, balancing margin and competitiveness.
LENGTH: 6-10 pages.

CROSS-REFERENCE: This is the internal pricing policy (cost, margin, approval). For the competitive go-to-market pricing strategy, see bb-sales/Pricing strategy.
```

---
✍️ Author: Brian H. Doan
