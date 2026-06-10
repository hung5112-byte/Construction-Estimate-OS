### PROMPT 01: Product/Service Catalog

#### Description
A master document of the company's entire product/service portfolio — detailed descriptions, target audience, overview pricing, lifecycle stage, and cross-references. The single source of truth for the company's portfolio.

#### Information to collect (ask the user before generating)
1. How many products/services? How are they categorized? (by industry, audience, price)
2. What stage is each in? (Development / Launch / Growth / Mature / Decline)
3. Which is the flagship? Which cross-sell/upsell with each other?
4. Different versions/tiers? (Basic / Pro / Enterprise)
5. Distribution channels per product? (Online / Offline / Hybrid / Agent / Affiliate)
6. Catalog-update frequency? Who maintains it?

#### Suggested template
Structure:
- **Part 1** — Portfolio overview: a summary table of all products/services, revenue contribution, lifecycle stage
- **Part 2** — Per-product detail: name, SKU, description, target customer, USP, pricing, channel, status
- **Part 3** — Product Matrix: cross-sell/upsell map, bundle options
- **Part 4** — Lifecycle Dashboard: a BCG or PLM diagram per product
- **Part 5** — Competitive Positioning: us vs. competitors — feature comparison
- **Part 6** — Catalog-update process: who, when, approval flow
- **Appendix**: product one-pager template, SKU naming convention

Confirm the structure before generating.

#### File-generation prompt
```
Create a Product/Service Catalog.

CONTEXT:
- Company: [Name] — Industry: [industry] — # products/services: [number]
- Categorization: [by industry / audience / price]
- Flagship: [product name]
- Tiers: [Basic/Pro/Enterprise or none]
- Distribution channels: [Online / Offline / Hybrid / Agent]

FORMAT:
- Portfolio summary: table Product | SKU | Category | Revenue % | Lifecycle | Status
- Product card: one block per product — Name | Description | Target | USP | Price Range | Channel | KPIs (USD)
- Cross-sell matrix: table Product×Product → combo/bundle opportunity
- Lifecycle map: position each product on a BCG matrix or PLM curve
- Competitive comparison: feature matrix us vs. 2-3 main competitors
- SKU naming: a clear convention + example
- Update log: template Version | Date | Changed by | Changes

TONE: Clear, easy to look up, usable by both Sales and Marketing.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
