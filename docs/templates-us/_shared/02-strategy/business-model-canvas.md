# PROMPT 06: Business Model Canvas (BMC)

#### Description
A business model in Osterwalder's 9 blocks: Customer Segments, Value Propositions, Channels, Customer Relationships, Revenue Streams, Key Resources, Key Activities, Key Partnerships, Cost Structure. A one-page view of how the company creates, delivers, and captures value.

#### Information to collect (ask the user before generating)
1. How many main product/service lines? (each may need its own BMC)
2. Who are the main customers? (B2B/B2C/B2B2C, segments)
3. The core value the company delivers? (what problem does it solve?)
4. Current sales/distribution channels?
5. Revenue sources: sales, subscription, commission, licensing...?
6. Largest costs: payroll, COGS, marketing, technology...?
7. Current strategic partners?

#### Suggested template
Structure:
- **1-page Canvas** — the standard Osterwalder 9-block layout
- **Detail per block** — half to one page expanding each block:
  - Current state
  - Desired state
  - Gap & Actions
- **Revenue Model detail** — table: Revenue stream | % of total revenue | Pricing model | Unit economics
- **Cost Structure detail** — fixed vs. variable, % breakdown
- **Assumptions & Risks** — which assumptions need validating?

Confirm the structure before generating.

#### File-generation prompt
```
Create a Business Model Canvas (BMC).

CONTEXT:
- Company: [Name] — Industry: [industry]
- Products/services: [list main lines]
- Customers: [segments]
- Value proposition: [core value]
- Channels: [current channels]
- Revenue: [sources + share]
- Cost: [largest costs]
- Partners: [main partners]

FORMAT:
- 1-page canvas: 9-block table, 3-5 short bullets per block
- Deep-dive: 9 expanded sections, each with Current/Desired/Gap
- Revenue model: table stream × pricing × unit economics
- Key metrics per block: e.g. Customer Segments → TAM/SAM/SOM, Revenue → MRR/ARPU/LTV
- Validation checklist: which assumptions are validated? which need testing?

TONE: Strategic, concise, visual.
LENGTH: 5-8 pages (1 page canvas + 7 pages detail).
```

---
✍️ Author: Brian H. Doan
