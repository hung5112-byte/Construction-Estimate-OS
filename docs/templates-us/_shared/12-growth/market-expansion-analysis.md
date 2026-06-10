### PROMPT 08: Market Expansion Analysis

#### Description
A detailed analysis of a market-expansion opportunity — assessing market attractiveness, entry strategy, localization requirements, competitive landscape, and financial projections for a new market (geographic or segment).

#### Information to collect (ask the user before generating)
1. Target market? (city/state / country / new segment)
2. Reason to expand? (market pull / strategy / investor requirement)
3. Entry mode? (direct / franchise / JV / partnership / acquisition)
4. Available data? (market research, competitor intel, customer feedback from the target market)
5. Expansion budget? Timeline?
6. Biggest risk? (regulatory, cultural, competitive, operational)

#### Suggested template
Structure:
- **Executive Summary** — go/no-go recommendation + key findings
- **Market Assessment** — size, growth, trends, demographics, purchasing power
- **Competitive Landscape** — existing players, market share, positioning, barriers
- **Customer Analysis** — target segments, needs, willingness to pay, localization needs
- **Entry Strategy Options** — compare 3-4 modes: direct vs. franchise vs. JV vs. partnership
- **Localization Requirements** — product, pricing, marketing, legal, cultural adaptations
- **Financial Projections** — investment required, revenue forecast, break-even timeline, ROI
- **Risk Assessment** — risk matrix + mitigation strategies
- **Implementation Roadmap** — Phase 1-3 with milestones, timeline, resources
- **Recommendation** — ranked options with rationale

Confirm the structure before generating.

#### File-generation prompt
```
Create a Market Expansion Analysis.

CONTEXT:
- Company: [Name] — Target market: [market]
- Reason: [market pull / strategy / investor]
- Entry modes considered: [direct / franchise / JV / partnership]
- Budget: [range] — Timeline: [target launch]
- Key risks: [list]

FORMAT:
- Market scorecard: Criteria | Weight | Score (1-5) | Weighted → total attractiveness score
  - Market size, growth rate, competition intensity, regulatory ease, cultural fit, infrastructure
- Competitive map: Player | Market share | Strengths | Weaknesses | Positioning
- Entry-mode comparison: Mode | Investment | Risk | Control | Speed | Scalability → recommendation
- Localization matrix: Element | Current | Required change | Cost | Timeline
- Financial projection: Year 1-3 — Revenue | Costs | Cumulative Investment | Break-even month | 3-year ROI (USD)
- Risk matrix: Risk | Probability | Impact | Mitigation | Owner | Residual risk
- Roadmap: Gantt-style — Phase 1 (Research) | Phase 2 (Setup) | Phase 3 (Launch) | Phase 4 (Scale)
- Decision framework: table Go criteria ☐ — must meet X of Y to proceed

TONE: Strategic, analytical, decision-supporting.
LENGTH: 8-12 pages.
```

---
✍️ Author: Brian H. Doan
