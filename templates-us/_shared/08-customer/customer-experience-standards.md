### PROMPT 01: Customer Experience Standards

#### Description
An overview document defining the company's customer-experience standards — service-level standards, interaction guidelines, quality benchmarks, CX principles. The "constitution" for every customer interaction, ensuring consistency no matter who serves the customer (E-Myth: systems-dependent).

#### Information to collect (ask the user before generating)
1. B2B or B2C? Average number of customers?
2. Main customer touchpoints? (hotline, email, chat, in person, app)
3. Current response time? Desired?
4. Do you measure NPS/CSAT? Results?
5. Customers' biggest pain point when interacting with you?
6. How many CS staff? A dedicated CS Manager?

#### Suggested template
Structure:
- **CX Vision & Principles**: 5-7 core principles (e.g. "First response < 2 hours", "First-contact resolution > 80%")
- **Service Level Standards**: SLA per channel — response time, resolution, escalation
- **Interaction Guidelines**: tone, language, do/don't when communicating with customers
- **Quality Benchmarks**: CX KPIs — NPS target, CSAT target, FCR, churn rate
- **Customer Journey Map**: stages + standards at each touchpoint
- **SERVQUAL Dimensions**: Tangibles, Reliability, Responsiveness, Assurance, Empathy — how to measure

Confirm the structure before generating.

#### File-generation prompt
```
Create Customer Experience Standards.

CONTEXT:
- Company: [Name] — B2B/B2C: [type] — # customers: [number]
- Touchpoints: [hotline / email / chat / in person / app]
- Current response time: [hours/min] — Target: [hours/min]
- Current NPS: [score / not measured] — CSAT: [% / not measured]
- CS team: [number] — CS Manager: [Yes/No]
- Customer pain points: [describe]

FORMAT:
- CX Principles: 5-7 principles — each with a title + 1-2 sentence description + metric
- SLA matrix: Channel | Response time | Resolution time | Escalation trigger | Business hours
- Interaction playbook: Situation | Say this | Don't say | Example
- KPI dashboard: KPI | Target | Measurement | Frequency | Owner | Current
- Customer journey: Mermaid — Awareness → Purchase → Onboarding → Usage → Renewal → Advocacy
- SERVQUAL scorecard: 5 dimensions × 3-5 sub-criteria × rating scale

TONE: Customer-centric, inspirational yet actionable.
LENGTH: 8-12 pages.
```

---
✍️ Author: Brian H. Doan
