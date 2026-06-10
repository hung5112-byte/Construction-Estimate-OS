### PROMPT 13: CRM Setup Guide

#### Description
A guide to set up a CRM for the sales team — custom fields, pipeline stages, automation rules, dashboards, and data-hygiene rules. Ensures the CRM serves the standardized sales process and doesn't become a "data dumpster."

#### Information to collect (ask the user before generating)
1. CRM in use or planned? (HubSpot / Salesforce / Zoho / Pipedrive / Custom)
2. Expected # users? Roles? (Admin, Manager, Rep)
3. Pipeline stages defined?
4. Custom fields needed beyond the defaults? (industry, source, deal type...)
5. What automation? (auto-assign lead, follow-up reminder, stage notification)
6. Dashboards needed: for rep, for manager, for Department Head?
7. Integrations needed: email, phone, website, chat, marketing tools?

#### Suggested template
Structure:
- **Part 1** — CRM strategy: usage goals, adoption metrics, governance
- **Part 2** — Contact & company fields: required fields, custom fields, field types, picklist values
- **Part 3** — Pipeline setup: stages, probability, required fields per stage, exit criteria
- **Part 4** — Automation rules: lead assignment, task creation, notifications, follow-up sequences
- **Part 5** — Dashboards: rep, manager, executive — KPIs per role
- **Part 6** — Data hygiene: naming conventions, dedup rules, update frequency, data owner
- **Part 7** — Integration map: email, phone, website, marketing, accounting
- **Part 8** — User management: roles, permissions, training plan
- **Appendix**: field reference table, automation flowcharts, dashboard mockups

Confirm the structure before generating.

#### File-generation prompt
```
Create a CRM Setup Guide.

CONTEXT:
- Company: [Name] — CRM: [software name]
- Users: [number] — Roles: [Admin / Manager / Rep]
- Pipeline stages: [list]
- Custom fields: [list]
- Automation: [list needs]
- Integration: [email / phone / website / marketing]

FORMAT:
- Field reference: table Field Name | Type | Required | Picklist Values | Description | Where to fill
- Pipeline config: table Stage | Probability | Required Fields | Exit Criteria | Auto-actions
- Automation rules: table Trigger | Condition | Action | Owner | Priority
- Dashboard specs per role:
  - Rep: My pipeline | My activities | My quota
  - Manager: Team pipeline | Forecast | Rep performance
  - Department Head: Revenue trend | Win rate | Pipeline health
- Data hygiene: table Rule | Check frequency | Responsible | Action if violation
- Integration map: Mermaid diagram — CRM ↔ Email ↔ Phone ↔ Website ↔ Marketing
- Training plan: table Week | Topic | Duration | Audience | Format

TONE: Technical guide — clear, step-by-step, screenshot-friendly.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
