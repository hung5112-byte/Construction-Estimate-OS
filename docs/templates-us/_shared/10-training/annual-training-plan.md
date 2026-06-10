### PROMPT 03: Annual Training Plan

#### Description
A full-year training plan — consolidated from the TNA, company strategy, compliance requirements, and budget. Includes a detailed schedule, budget allocation, trainer assignments, KPIs, and a 12-month training calendar.

#### Information to collect (ask the user before generating)
1. Total annual training budget? Allocated by department or by type?
2. Annual mandatory training? (OSHA safety, compliance, industry certifications/CE)
3. Internal trainers? How many?
4. Preferred delivery method? (classroom / e-learning / on-the-job / blended)
5. Current training KPIs? (training hours/employee, completion rate, satisfaction score)
6. A learning management system (LMS)?

#### Suggested template
Structure:
- **Part 1** — Executive summary: annual training goals, strategy link, total budget
- **Part 2** — Training objectives: training OKRs/KPIs for the year
- **Part 3** — Training calendar: 12 months × programs × audience × trainer
- **Part 4** — Budget breakdown: by training type, by department, by quarter
- **Part 5** — Trainer pool: internal & external — expertise, availability
- **Part 6** — Delivery methods: % split across classroom / e-learning / OJT / coaching
- **Part 7** — Evaluation plan: which Kirkpatrick level for each program
- **Part 8** — Risk & contingency: risks (budget cut, trainer unavailable) + plan B
- **Appendix**: training-calendar template, budget-tracking template

Confirm the structure before generating.

#### File-generation prompt
```
Create an Annual Training Plan.

CONTEXT:
- Company: [Name] — Headcount: [number] — Year: [year]
- Budget: [total] — Allocation: [by department / by type]
- Mandatory training: [list: OSHA safety, compliance, ...]
- Internal trainers: [number] — External: [yes/no]
- LMS: [name / none]
- Methods: [classroom / e-learning / blended / OJT]

FORMAT:
- Executive summary: 1 page — goals, budget, key programs, KPIs
- Training OKRs: table Objective | Key Result | Target | Measurement
- Calendar: 12 months × Program | Target group | # Participants | Duration | Trainer | Method | Budget | Status (USD)
- Budget breakdown:
  - By category: Mandatory | Technical | Soft skills | Leadership | Total → % allocation
  - By quarter: Q1 | Q2 | Q3 | Q4 | Total → Planned vs. Actual
  - By department: Dept | Headcount | Budget | Per capita | Programs
- Trainer pool: Name | Expertise | Internal/External | Rate | Availability | Rating
- Method mix: pie-chart data — Classroom % | E-learning % | OJT % | Coaching % | Self-study %
- Evaluation plan: Program | Kirkpatrick Level | Method | Timing | Owner
- KPI dashboard: Metric | Target | Q1 | Q2 | Q3 | Q4 | YTD
  - Training hours/employee, completion rate, satisfaction score, budget utilization, skill-gap closure %
- Risk register: Risk | Impact | Probability | Mitigation | Owner

TONE: Detailed plan, actionable, trackable quarterly.
LENGTH: 8-12 pages.
```

---
✍️ Author: Brian H. Doan
