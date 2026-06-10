### PROMPT 02: Pricing Strategy

#### Description
A comprehensive pricing strategy — defining your price position in the market, the pricing method, the discount structure, and the price-change process. Unlike the Pricing Policy (the internal policy in Finance), this focuses on competitive strategy and go-to-market.

#### Information to collect (ask the user before generating)
1. Desired price position? (Premium / Mid-range / Value / Low-cost)
2. Current price structure? (one-time / subscription / usage-based / hybrid)
3. Current average price? Where vs. competitors?
4. Current discount policy? (volume, loyalty, seasonal, early payment)
5. Who can discount? Up to what %?
6. Price-change frequency? Change triggers?
7. Any loss-leader / freemium product?

#### Suggested template
Structure:
- **Part 1** — Pricing objective: maximize revenue / market share / profit margin / penetration
- **Part 2** — Price positioning: perceptual map vs. competitors, value-price matrix
- **Part 3** — Pricing method: cost-plus / value-based / competitive / dynamic — when to use which
- **Part 4** — Price architecture: tiers, bundles, add-ons, upsell/cross-sell pricing
- **Part 5** — Discount framework: discount table by type, approval levels, guardrails
- **Part 6** — Competitive pricing: price-comparison matrix, response playbook
- **Part 7** — Price review & adjustment: triggers, process, communication plan
- **Appendix**: price-list template, discount calculator, competitive price tracker

Confirm the structure before generating.

#### File-generation prompt
```
Create a Pricing Strategy.

CONTEXT:
- Company: [Name] — Industry: [industry] — # products/services: [number]
- Price position: [Premium / Mid / Value / Low-cost]
- Price structure: [one-time / subscription / usage-based / hybrid]
- Average price: [amount] — vs. competitors: [higher / on par / lower by X%]
- Current discounts: [volume / loyalty / seasonal / early payment]
- Discount authority: [title] — Max: [%]
- Loss-leader/Freemium: [Yes/No] — [describe]

FORMAT:
- Price positioning map: 2x2 matrix (Value vs. Price) — plot company + competitors
- Price architecture: table Tier | Features | Price | Target segment | Margin % (USD)
- Discount framework: table Discount type | Conditions | % | Approval | Guardrail
- Competitive comparison: table Product | Our Price | Competitor A | B | C | Positioning
- Price waterfall: List Price → Discount → Net Price → COGS → Margin (Mermaid/table)
- Decision tree: when to raise/lower/hold price — flowchart
- Review calendar: quarterly trigger checklist

TONE: Strategic, data-driven, competitive.
LENGTH: 6-10 pages.

CROSS-REFERENCE: This is the competitive pricing strategy. For the internal pricing policy (cost, margin floors, approval workflow), see bb-finance/Pricing Policy.
```

---
✍️ Author: Brian H. Doan
