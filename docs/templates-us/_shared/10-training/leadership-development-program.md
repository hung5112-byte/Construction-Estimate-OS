### PROMPT 05: Leadership Development Program

#### Description
A leadership-development program for management levels — from team lead/supervisor to middle management and senior leadership. Includes a leadership competency model, a development path by level, training methods (classroom, coaching, action learning, stretch assignments), a succession-planning link, and progress evaluation.

#### Information to collect (ask the user before generating)
1. How many management levels? (Team Lead / Manager / Director / C-level)
2. A leadership competency model? Which leadership competencies are critical?
3. A succession plan? Who is in the succession pipeline?
4. Biggest current leadership challenge? (delegation / communication / strategic thinking / people management)
5. Budget for leadership development? Program duration?
6. External executive coaching?

#### Suggested template
Structure:
- **Part 1** — Philosophy & vision: the company's leadership philosophy, leadership brand
- **Part 2** — Leadership Competency Model: 6-10 competencies, definitions, behavioral indicators per level
- **Part 3** — Program Tiers:
  - Tier 1 — Emerging Leaders (Individual Contributor → Team Lead)
  - Tier 2 — Middle Management (Team Lead → Department Manager)
  - Tier 3 — Senior Leadership (Manager → Director / C-level)
- **Part 4** — Curriculum: per tier — modules, duration, methods, assessment
- **Part 5** — Delivery methods: 70-20-10 mix — action learning, coaching, classroom
- **Part 6** — Assessment & progress: 360 feedback, development plans, milestones
- **Part 7** — Succession-planning link: connect to the succession pipeline
- **Part 8** — Budget & timeline
- **Appendix**: Individual Development Plan (IDP) template, 360 feedback template

Confirm the structure before generating.

#### File-generation prompt
```
Create a Leadership Development Program.

CONTEXT:
- Company: [Name] — # management levels: [number] — Total managers: [number]
- Competency model: [Yes/No] — Core competencies: [list]
- Succession plan: [Yes/No]
- Leadership challenge: [top 3]
- Budget: [total] — Duration: [X months/year]
- External coaching: [Yes/No]

FORMAT:
- Leadership competency model: table Competency | Definition | Level 1 (Team Lead) | Level 2 (Manager) | Level 3 (Director+) — behavioral indicators per level
- Program tiers overview: Mermaid flowchart — IC → Tier 1 → Tier 2 → Tier 3
- Tier curriculum: a table per tier — Module | Topic | Duration | Method | Assessment | Prerequisite
  - Tier 1: 6-8 modules (delegation, feedback, team dynamics, time management, basic finance, coaching skills)
  - Tier 2: 6-8 modules (strategic planning, change management, cross-functional leadership, talent development, P&L management)
  - Tier 3: 4-6 modules (vision & strategy, board communication, M&A, innovation leadership, executive presence)
- 70-20-10 mix per tier: Experience | Exposure | Education — specific activities for each
- Action learning projects: format — real business challenge | team | duration | sponsor | expected output
- Assessment framework: entry (360 + competency eval) → midpoint check → exit
- IDP template: Competency | Current Level | Target Level | Development actions | Timeline | Support needed | Progress
- Succession pipeline: Role | Current holder | Successor 1 | Readiness | Development gaps | Target ready date
- Program calendar: Month 1-12 × activities × tier
- KPIs: promotion readiness % | 360 score improvement | succession pipeline fill rate | retention of HiPos

TONE: Strategic, developmental, tied to business outcomes.
LENGTH: 8-12 pages.
```

---
✍️ Author: Brian H. Doan
