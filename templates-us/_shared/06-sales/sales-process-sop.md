### PROMPT 05: Sales Process SOP

#### Description
A standardized process for the whole sales operation — from receiving a lead to closing the deal and handing off the customer. Ensures every rep sells the same proven way, reducing reliance on individuals.

#### Information to collect (ask the user before generating)
1. Main lead sources? (Marketing, referral, outbound, event, website)
2. Lead-qualification criteria? (BANT / MEDDIC / CHAMP / custom?)
3. How many steps in the current process? Describe?
4. Average time per step? Whole cycle?
5. Any handover between teams? (SDR → AE → AM → CS?)
6. Supporting tools? (CRM, email, phone, chat?)
7. Current step-to-step conversion rates?

#### Suggested template
Structure:
- **Purpose & scope**
- **Glossary**: Lead, MQL, SQL, Opportunity, Deal, Won, Lost
- **Process overview**: 7 steps — Lead → Qualify → Demo/Consult → Proposal → Negotiate → Close → Handover
- **Step detail**: objective, specific actions, output, exit criteria, timeline, tools
- **Qualification framework**: BANT or MEDDIC — applied checklist
- **Handover protocol**: SDR → AE, AE → AM, Sales → CS
- **Escalation rules**: when to bring in a manager/director
- **Tracking & reporting**: CRM stages, pipeline-review cadence
- **Appendix**: qualification checklist, stage criteria, handover template

Confirm the structure before generating.

#### File-generation prompt
```
Create a Sales Process SOP.

CONTEXT:
- Company: [Name] — Model: [B2B / B2C / SaaS / Services]
- Lead source: [Marketing / Referral / Outbound / Event / Website]
- Qualification: [BANT / MEDDIC / CHAMP / Custom]
- Current # steps: [number] — Sales cycle: [days]
- Team structure: [SDR + AE + AM / All-in-one]
- CRM: [software name]

FORMAT:
- Overall flowchart: Mermaid — 7 main steps + decision points
- Per-step detail: table Step | Objective | Actions | Output | Exit Criteria | Timeline | Owner
- Qualification checklist: BANT/MEDDIC — Criterion | Question | Met/Not | Score
- Conversion funnel: table Stage | Leads In | Converted | Rate | Avg Days | Bottleneck
- Handover template: info to transfer between roles
- Escalation matrix: Situation | Escalate to | Timeline | Expected action
- Weekly pipeline-review agenda: 5 fixed check items

TONE: Standard SOP — step-by-step, clear, actionable.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
