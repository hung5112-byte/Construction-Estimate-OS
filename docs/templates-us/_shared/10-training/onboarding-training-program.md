### PROMPT 04: Onboarding Training Program

#### Description
A new-hire training process from day one through 90 days — orientation, culture intro, product/service training, role-specific skills, buddy system, evaluation checkpoints, and "pass the introductory period" criteria. Gets new hires productive as fast as possible.

#### Information to collect (ask the user before generating)
1. Length of the introductory period? (1 / 2 / 3 months)
2. Average time for a new hire to become productive? (weeks / months)
3. A buddy/mentor system? Who is the buddy?
4. What does current onboarding cover? (orientation / culture / product / tools / compliance)
5. A handover checklist from HR → Manager → Buddy?
6. Specific criteria to pass the introductory period? Who evaluates?

#### Suggested template
Structure:
- **Purpose & scope**
- **Pre-boarding** (before start): IT setup, welcome email, prep workspace
- **Day 1 — Welcome & Orientation**: intro, tour, IT setup, admin (incl. I-9/W-4)
- **Week 1 — Foundation**: company culture, product/service overview, tools & systems
- **Weeks 2-4 — Role Training**: job skills, shadowing, practice
- **Day 30 — Checkpoint 1**: progress review, two-way feedback
- **Month 2 — Deep Dive**: real project, mentoring, networking
- **Day 60 — Checkpoint 2**: performance review, adjust plan
- **Month 3 — Independence**: independent work, contribute to team goals
- **Day 90 — Final Review**: pass/fail (at-will), next development plan
- **Appendix**: onboarding checklist, buddy guide, evaluation forms

Confirm the structure before generating.

#### File-generation prompt
```
Create an Onboarding Training Program.

CONTEXT:
- Company: [Name] — Introductory period: [months]
- Current time-to-productivity: [X weeks/months] — Target: [Y]
- Buddy system: [Yes/No] — Who: [senior / peer / cross-team]
- Current training: [list content]
- Pass criteria: [describe]

FORMAT:
- Timeline overview: Mermaid Gantt — Pre-board | Day 1 | Week 1 | Week 2-4 | Day 30 | Month 2 | Day 60 | Month 3 | Day 90
- Pre-boarding checklist: ☐ IT setup | ☐ Email | ☐ Workspace | ☐ Welcome kit | ☐ Buddy assigned | ☐ Schedule shared
- Day 1 schedule: Time | Activity | Owner | Location | Materials (incl. I-9/W-4)
- Week 1 curriculum: Day | Topic | Duration | Trainer/Resource | Method | Assessment
- Week 2-4 plan: table — Skill | Training activity | Duration | Trainer | Output expected
- 30-60-90 milestones: table Milestone | Expected competency | Assessment method | Assessor | Pass criteria
- Buddy guide: role & responsibilities | meeting frequency | conversation starters | escalation path
- Evaluation forms:
  - Checkpoint 1 (Day 30): knowledge check + cultural fit + manager feedback
  - Checkpoint 2 (Day 60): performance metrics + peer feedback + self-assessment
  - Final review (Day 90): comprehensive assessment + go/no-go (at-will) + development plan
- RACI: Activity × Role (HR, Manager, Buddy, IT, New hire)
- KPIs: time-to-productivity | introductory-period pass rate | 90-day retention | new-hire satisfaction

TONE: Welcoming, structured, measurable.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
