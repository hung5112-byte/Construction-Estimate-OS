# PROMPT 08: Competitive Landscape

#### Description
A detailed competitive landscape — comparing the company with 3-5 main competitors across many criteria: product, price, distribution channels, marketing, technology, people, market share. Identifies positioning and market gaps.

#### Information to collect (ask the user before generating)
1. 3-5 main competitors to compare? (name + website)
2. Most important comparison criteria? (price / quality / speed / technology / service)
3. Any concrete data on competitors? (revenue, market share, headcount)
4. The company's current USP vs. competitors?
5. The white space the company is targeting?
6. Include indirect competitors?

#### Suggested template
Structure:
- **Executive Summary** — top 3 competitive insights
- **Competitor Profiles** — half a page each: overview, products, strengths, weaknesses, recent moves
- **Comparison Matrix** — table: criteria (rows) × competitors (columns), scored or descriptive
- **Positioning Map** — 2D plot: Axis 1 (e.g. price) × Axis 2 (e.g. quality) — data points for the company + competitors
- **Feature Comparison** — detailed table: Feature | Us ✅❌ | Competitor A ✅❌ | ...
- **SWOT per Competitor** — a mini SWOT for each competitor
- **White Space Analysis** — gaps nobody is serving
- **Battlecard** — a 1-page summary for the sales team: "When competing against X, say..."

Confirm the structure before generating.

#### File-generation prompt
```
Create a Competitive Landscape Analysis.

CONTEXT:
- Company: [Name] — Current positioning: [describe]
- Competitors: [Name 1 - website] | [Name 2 - website] | [Name 3 - website]
- Comparison criteria: [list 8-12 criteria]
- Competitor data: [source: public / estimated / industry report]
- Company USP: [describe]
- White space target: [describe]

FORMAT:
- Competitor profiles: half a page each
- Comparison matrix: criteria × competitors, using ⭐ (1-5) or ✅/⚠️/❌
- Positioning map: 2D data (Axis 1: [___], Axis 2: [___]) + coordinates per player
- Feature comparison: binary ✅/❌ for 20-30 features
- Battlecards: 1 page per competitor → "They say... We say..."
- White space: underserved needs × competitor coverage matrix

TONE: Intelligence report — objective, data-driven, actionable.
LENGTH: 8-12 pages.
```

---
✍️ Author: Brian H. Doan
