# PROMPT 17: Business Continuity Plan — BCP

#### Description
A plan to keep the business running through a major incident: loss of the office, loss of IT systems, loss of a key person, natural disaster, pandemic. Focus: Recovery Time Objective (RTO), Recovery Point Objective (RPO), workaround procedures.

#### Information to collect (ask the user before generating)
1. Business-critical processes? (top 5 processes that cannot stop)
2. Critical IT systems? (website, CRM, email, ERP, payments...)
3. Backup site / remote-work capability?
4. Recovery targets: how much downtime is acceptable? (RTO)
5. Data backup: frequency, location, recovery tested?
6. Key-person dependencies: who, if absent, would paralyze operations?

#### Suggested template
Structure:
- **Business Impact Analysis (BIA)** — table: process × impact if down × RTO/RPO
- **Critical Function Recovery** — per function: primary site → backup site → manual workaround
- **IT Disaster Recovery** — system × RTO × RPO × backup method × recovery steps
- **People Continuity** — key person × backup person × cross-training status × succession plan
- **Communication Plan** — notify employees, customers, partners when BCP is activated
- **BCP Activation Protocol** — who decides to activate, trigger criteria, escalation
- **Testing Schedule** — tabletop exercise, walkthrough, full test — annual calendar

Confirm the structure before generating.

#### File-generation prompt
```
Create a Business Continuity Plan (BCP).

CONTEXT:
- Company: [Name] — Industry: [industry] — Headcount: [number]
- Critical processes: [list top 5]
- IT systems: [list critical systems]
- Remote work: [Yes/No] — Capability: [%]
- Acceptable RTO: [hours/days]
- Data backup: [method / frequency / location]
- Key-person risks: [list]

FORMAT:
- BIA table: Process | Owner | Impact if down 1h/1d/1w | RTO | RPO | Priority
- Recovery procedures: per critical function, step-by-step
- IT DR plan: System | RTO | RPO | Backup | Recovery Steps | Last Tested
- People matrix: Role | Primary | Backup | Cross-training | Succession
- Communication tree: flowchart — who notifies whom
- Activation checklist: 15-step protocol
- Test schedule: Type | Frequency | Last Done | Next Due | Owner

TONE: Operational resilience — thorough, practical, testable.
LENGTH: 12-18 pages.
```

---
✍️ Author: Brian H. Doan
