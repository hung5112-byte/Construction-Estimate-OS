# PROMPT 14: Strategic Roadmap

#### Description
A development roadmap on a 1-3-5 year timeline. Combines milestones from every area: product, market, people, technology, finance. Gantt-like, easy to communicate to the whole team and investors.

#### Information to collect (ask the user before generating)
1. Horizon: 1 year / 3 years / 5 years? (or split into phases)
2. Key milestones identified? (e.g. launch a new product, enter a new market, raise capital, IPO...)
3. Dependencies between milestones?
4. Phasing: Foundation → Growth → Scale → Exit?
5. Roadmap as swimlanes (one lane per department) or a single timeline?
6. Any trigger milestones (condition-dependent rather than time-dependent)?

#### Suggested template
Structure:
- **Executive View** — 1 page, timeline with 5-7 key milestones, high-level
- **Detailed Roadmap** — swimlane view: Product | Market | People | Finance | Tech — milestones per lane
- **Phase Descriptions** — per phase: objectives + key activities + exit criteria + budget estimate
- **Dependencies Map** — milestone X must finish before Y starts
- **Risk & Contingency** — per phase: what could delay + contingency plan
- **Quarterly Breakdown** — detailed Q1-Q2-Q3-Q4 for the first year
- **Review Cadence** — how often to review: Monthly (tactical) + Quarterly (strategic) + Annual (vision)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Strategic Roadmap.

CONTEXT:
- Company: [Name] — Stage: [startup/growth/mature]
- Horizon: [1/3/5 years]
- Key milestones: [list with target dates]
- Dependencies: [milestone A → B → C]
- Phases: [e.g. Foundation Q1-Q2 → Growth Q3-Q4 → Scale Year 2]
- Format: [Swimlane / Timeline / Phase-based]

FORMAT:
- Executive 1-pager: timeline + 5-7 key milestones
- Swimlane roadmap: 5 lanes (Product, Market, People, Finance, Tech) × time
- Phase cards: Phase name | Duration | Objectives | Key Activities | Exit Criteria | Budget
- Milestone table: # | Milestone | Lane | Start | End | Dependencies | Owner | Status
- Dependencies: Mermaid Gantt or DAG diagram
- Year 1 quarterly detail: Q1-Q4 breakdown with monthly actions
- Review template: quarterly roadmap-review form

TONE: Visionary yet practical — ambitious milestones, realistic timelines.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
