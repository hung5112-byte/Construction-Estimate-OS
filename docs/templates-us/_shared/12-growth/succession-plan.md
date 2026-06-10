### PROMPT 11: Succession Plan

#### Description
A succession plan for key positions — especially CEO/Founder. Identifies potential successors, development gaps, transition timeline, and necessary governance changes. Ensures the business keeps running even if a key person leaves.

#### Information to collect (ask the user before generating)
1. Which positions need a succession plan? (CEO, C-suite, key technical roles)
2. Internal candidates? Readiness level?
3. Succession timeline? (emergency / planned 1-3 years / planned 5+ years)
4. Governance: what's the Board's role in succession?
5. Is the founder willing to mentor/transition?
6. Key-person risk: if the CEO leaves suddenly, what happens?

#### Suggested template
Structure:
- **Part 1** — Philosophy: why succession planning, link to sustainability
- **Part 2** — Key position mapping: critical roles, criticality rating, vacancy risk
- **Part 3** — Successor identification: per position — 2-3 candidates, readiness (Ready Now / 1-2 years / 3+ years)
- **Part 4** — Development plans: per successor — gap analysis, development actions, timeline
- **Part 5** — Emergency succession: interim plan if a key person leaves suddenly
- **Part 6** — Transition process: phased handover — shadow → co-lead → lead → full transition
- **Part 7** — Governance changes: board role, advisory period, founder emeritus
- **Part 8** — Communication plan: when and how to communicate succession
- **Appendix**: successor-assessment matrix, individual development plan template, transition checklist

Confirm the structure before generating.

#### File-generation prompt
```
Create a Succession Plan.

CONTEXT:
- Company: [Name] — Key positions: [list]
- Internal candidates: [Yes/No] — Readiness: [describe]
- Timeline: [emergency / 1-3 years / 5+ years]
- Board role: [active / advisory / none]
- Key-person risk: [assessment]

FORMAT:
- Key position map: Position | Incumbent | Criticality (1-5) | Vacancy risk (H/M/L) | Impact if vacant
- 9-box grid data: per candidate — Performance (L/M/H) × Potential (L/M/H) → placement
- Successor slate: Position | Successor 1 (Ready Now) | Successor 2 (1-2 yr) | Successor 3 (3+ yr) | External option
- Readiness assessment: Candidate | Competency | Current level | Required level | Gap | Development action
- Emergency plan: Position | Interim successor | First 30 days | First 90 days | Permanent solution
- Transition timeline: Phase | Duration | Activities | Milestones | Support needed
  - Phase 1: Shadow (3-6 months) | Phase 2: Co-lead (3-6 months) | Phase 3: Lead with support (6 months) | Phase 4: Independent
- Communication plan: Stakeholder | Message | Timing | Channel | Speaker
- Governance transition: current structure | transition structure | final structure

TONE: Sensitive, strategic, forward-thinking — don't cause alarm.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
