# PROMPT 16: Crisis Management Plan

#### Description
A crisis playbook — for scenarios such as a PR crisis, product incident, data breach, litigation, natural disaster, or loss of a key person. Each scenario has its own protocol to ensure a fast, consistent response.

#### Information to collect (ask the user before generating)
1. Ever faced a crisis? (what type, how handled)
2. PR/communications in-house or outsourced?
3. Who is the Crisis Commander?
4. Do you have on-call legal counsel?
5. Main communication channels to manage during a crisis?
6. Which scenario worries you most? (e.g. product recall, data breach, negative viral, legal...)

> Note: a data-breach scenario may trigger legal notification requirements (e.g. Texas Business & Commerce Code ch. 521, plus any applicable federal/sector rules). Confirm specific obligations with a licensed Texas attorney. [verify — varies by data type and circumstances]

#### Suggested template
Structure:
- **Crisis Classification** — Level 1 (minor) → 2 (moderate) → 3 (severe) → 4 (existential)
- **Crisis Team** — roles & contacts: Commander, Spokesperson, Legal, Ops, HR, IT, Communications
- **Communication Cascade** — who calls whom, how fast, on which channel — a "First 60 minutes" protocol
- **Scenario Playbooks** — 6-8 scenarios, each with:
  - Trigger / indicators
  - Severity level
  - Immediate actions (first 1 hour)
  - Short-term actions (24-72 hours)
  - Communication templates (internal, customer, media, authorities)
  - Recovery steps
- **Holding Statements** — template statements to use before full information is in
- **Post-Crisis Review** — an After-Action Review (AAR) template

Confirm the structure before generating.

#### File-generation prompt
```
Create a Crisis Management Plan.

CONTEXT:
- Company: [Name] — Industry: [industry]
- Crisis history: [describe or "none"]
- PR: [in-house / agency: name]
- Crisis Commander: [title]
- Legal counsel: [Yes/No — name if any]
- Communication channels: [list: social media, website, press...]
- Scenarios of concern: [list top 3]

FORMAT:
- Crisis-level matrix: Level | Description | Authority | Response time | Communication scope
- Team contact card: Role | Name | Phone | Email | Backup
- "First 60 Minutes" checklist: 10 mandatory steps
- 6-8 scenario playbooks: 1-2 pages each
- Communication templates: internal memo, customer email, press statement, social-media post
- Holding-statement library: 5 generic statements ready to use
- AAR template: What happened | What went well | What went wrong | Improvements | Owner

TONE: Emergency protocol — clear, decisive, no ambiguity.
LENGTH: 15-20 pages.
```

---
✍️ Author: Brian H. Doan
