### PROMPT 02: Product Roadmap

#### Description
A product roadmap by quarter/year — milestones, new features, improvements, dependencies, and required resources. The roadmap aligns Product, Engineering, Sales, and Leadership.

#### Information to collect (ask the user before generating)
1. Roadmap horizon? (3 months / 6 months / 12 months / 3 years)
2. How many products/product lines need a roadmap?
3. Development methodology? (Agile/Scrum / Waterfall / Hybrid)
4. Who are the main stakeholders reading this roadmap?
5. Current product OKRs/KPIs? How do they link?
6. Major constraints? (budget, headcount, tech debt, market timing)

#### Suggested template
Structure:
- **Part 1** — Vision & strategy: product vision, strategic themes
- **Part 2** — Now / Next / Later: classify initiatives by timeline
- **Part 3** — Quarterly roadmap: Q1-Q4 × product lines × milestones
- **Part 4** — Feature backlog: prioritized list — MoSCoW or RICE scoring
- **Part 5** — Dependencies & risks: dependency map, risk register
- **Part 6** — Resource allocation: team × quarter × % allocation
- **Part 7** — Review & update cadence: review frequency, change process
- **Appendix**: initiative-scoring template, roadmap-communication template

Confirm the structure before generating.

#### File-generation prompt
```
Create a Product Roadmap.

CONTEXT:
- Company: [Name] — # product lines: [number]
- Horizon: [3/6/12 months / 3 years]
- Methodology: [Agile / Waterfall / Hybrid]
- Stakeholders: [Product, Engineering, Sales, Leadership]
- Constraints: [budget / headcount / tech debt / market]

FORMAT:
- Vision statement: a short paragraph — why & where
- Now/Next/Later: 3 swim lanes × initiatives
- Quarterly view: Gantt-style table — Q×Product×Milestone×Owner×Status
- Backlog scoring: Initiative | Impact (1-5) | Effort (1-5) | RICE Score | Priority
- Dependency map: Mermaid diagram — Initiative A → B → C
- Resource table: Team | Q1 | Q2 | Q3 | Q4 — % allocation
- Risk register: Risk | Probability | Impact | Mitigation
- Review cadence: monthly review + quarterly reprioritization

TONE: Strategic, visual, alignment-focused.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
