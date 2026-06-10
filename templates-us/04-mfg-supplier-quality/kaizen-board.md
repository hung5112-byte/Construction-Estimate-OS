### PROMPT 11: Kaizen Board (Continuous Improvement Board)

#### Description
A board to manage continuous-improvement ideas and projects in the Kaizen spirit — from proposal → evaluation → prioritization → implementation → measurement. Builds a culture of improvement at every level.

#### Information to collect (ask the user before generating)
1. Is there an improvement culture yet? (formal / informal / none)
2. Who can submit improvements? (all employees / managers only)
3. Any reward/recognition for adopted improvements?
4. Improvement-idea review frequency? (weekly / monthly)
5. Which area needs the most improvement? (process / product / cost / CX)

#### Suggested template
Structure:
- **Part 1** — Kaizen philosophy: why, principles, culture
- **Part 2** — Submission process: flowchart proposal → screening → evaluation → prioritization
- **Part 3** — Kaizen Board Layout: Backlog → In Review → Approved → In Progress → Completed → Measured
- **Part 4** — Evaluation criteria: Impact × Effort matrix (Quick Wins / Major Projects / Fill-ins / Hard Slogs)
- **Part 5** — Tracking & metrics: # submitted, % implemented, cost saved, time saved
- **Part 6** — Recognition program: how improvements are rewarded
- **Appendix**: Improvement Proposal Form (link PROMPT 12), Kaizen event template

Confirm the structure before generating.

#### File-generation prompt
```
Create a Kaizen Board.

CONTEXT:
- Company: [Name] — Improvement culture: [formal / informal / none]
- Who submits: [all employees / managers]
- Review: [frequency]
- Reward: [Yes/No] — [detail]
- Focus areas: [process / product / cost / CX]

FORMAT:
- Kaizen board layout: Mermaid / Kanban — 6-column swim lanes
- Submission flowchart: Mermaid — Idea → Form → Review → Prioritize → Implement → Measure
- Impact-Effort matrix: 2×2 grid — Quick Wins | Major Projects | Fill-ins | Thank but No
- Scoring template: Criteria | Weight | Score (1-5) → Priority
  - Impact on customer, impact on cost, effort, speed to implement, strategic alignment
- Metrics dashboard: KPIs — # submitted | # approved | # completed | Avg cycle time | Total savings
- Recognition program: Tier | Criteria | Reward | Examples
- Monthly Kaizen report template: summary + top 5 + metrics + next-month focus

TONE: Motivational + structured — encourage participation, with a clear process.
LENGTH: 5-8 pages.
```

---
✍️ Author: Brian H. Doan
