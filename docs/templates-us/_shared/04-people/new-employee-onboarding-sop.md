# P-PPL-15: New Employee Onboarding SOP

#### Description
An end-to-end onboarding process for a new hire — from before the start date (pre-boarding), through Day 1, Week 1, and the first month. Ensures the new hire ramps quickly and becomes productive early.

> US new-hire paperwork note: complete **Form I-9** (employment eligibility, 8 U.S.C. §1324a) within the federal deadline, collect **Form W-4** (federal withholding) and direct-deposit info, and provide required notices. Texas has no state income tax, so there's no state withholding form. [verify current forms]

#### Information to collect (ask the user before generating)
1. Before the start date: what does IT prepare? (email, laptop, access) How long?
2. Day 1: who greets them? Office tour? Welcome kit? Training?
3. A buddy/mentor program?
4. Length of the introductory period? (1 / 2 / 3 months)
5. Who owns onboarding? (HR / Manager / Buddy)
6. A shared orientation session for a batch of new hires?

#### Suggested template
Structure:
- **Pre-boarding (T-7 to T-1)**: IT setup, email/access, workspace, welcome email, pre-read materials, new-hire paperwork (I-9, W-4, direct deposit)
- **Day 1**: greeting → office tour → meet the team → IT handover → employee handbook → lunch with manager → complete I-9/W-4
- **Week 1**: product/process training → meet stakeholders → assign buddy → first task
- **Month 1**: weekly check-ins → deeper training → individual OKR/KPI → 30-day feedback
- **RACI**: HR | Manager | Buddy | IT | Admin — per task

Confirm the structure before generating.

#### File-generation prompt
```
Create a New Employee Onboarding SOP.

CONTEXT:
- Company: [Name] — Buddy program: [Yes/No]
- IT setup time: [days]
- Introductory period: [1 / 2 / 3 months]
- Batch orientation: [Yes/No]
- Owners: HR [___] | Manager [___] | Buddy [___]

FORMAT:
- Timeline visual: Pre-boarding → Day 1 → Week 1 → Month 1 — Mermaid/Gantt
- Pre-boarding checklist: 10-12 items ☐ + Owner + Deadline (T-7 to T-1), incl. I-9/W-4/direct deposit
- Day 1 schedule: Time × Activity × Owner × Location
- Week 1 plan: Day × Topic × Trainer × Output
- RACI per phase: Task | HR | Manager | Buddy | IT | Admin
- Welcome email template: sent T-3 — team intro, address, parking, dress code
- 30-day feedback form: 10 questions for the new hire + 5 for the manager

TONE: Welcoming, organized — the new hire should feel "this company is professional."
LENGTH: 5-7 pages.
```

---
✍️ Author: Brian H. Doan
