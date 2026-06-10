# PROMPT 07: Porter Five Forces

#### Description
An analysis of the five competitive forces per Michael Porter: (1) existing rivals, (2) potential entrants, (3) substitutes, (4) supplier power, (5) buyer power. Assesses the attractiveness and competitive intensity of the industry.

#### Information to collect (ask the user before generating)
1. The specific industry/segment being analyzed?
2. Main direct competitors? (3-5 names, estimated market share)
3. Barriers to entry? (capital, technology, licenses, brand...)
4. Any substitute products/services posing a threat?
5. Main suppliers? Dependent on 1-2 big ones?
6. Do customers have many alternatives? Switching cost high/low?

#### Suggested template
Structure:
- **Dashboard** — 5-forces radar-chart data (each force: 1-5 scale)
- **Force 1: Competitive Rivalry** — number of rivals, industry growth rate, differentiation, exit barriers
- **Force 2: Threat of New Entrants** — entry barriers, economies of scale, capital requirements
- **Force 3: Threat of Substitutes** — substitutes, switching cost, price-performance trade-off
- **Force 4: Bargaining Power of Suppliers** — supplier concentration, switching cost, backward integration
- **Force 5: Bargaining Power of Buyers** — buyer concentration, switching cost, market information
- **Implications** — a response strategy for each force
- **Overall Assessment** — is the industry attractive; compete/niche/exit?

Confirm the structure before generating.

#### File-generation prompt
```
Create a Porter Five Forces Analysis.

CONTEXT:
- Company: [Name] — Industry/Segment: [specific]
- Direct competitors: [name + estimated market share]
- Entry barriers: [list]
- Substitutes: [list]
- Main suppliers: [list + dependency level]
- Customer characteristics: [concentrated/dispersed, switching cost]

FORMAT:
- Radar-chart data: 5 forces × score 1-5 (1=Low pressure, 5=High pressure)
- Each force: 1 page — factor-analysis table: Factor | Evidence | Score (1-5)
- Overall industry-attractiveness score: average of 5 forces
- Strategic implications: table Force | Level | Our Response
- Comparison: two radars — industry average vs. our position

TONE: Analytical, academic-meets-practical.
LENGTH: 6-8 pages.
```

---
✍️ Author: Brian H. Doan
