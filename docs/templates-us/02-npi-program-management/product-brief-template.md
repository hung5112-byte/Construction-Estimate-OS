### PROMPT 04: Product Brief Template

#### Description
A standard template to describe a new product/feature before development starts. The brief aligns Product, Dev, Design, and Marketing — so everyone understands "what we're building, for whom, and why."

#### Information to collect (ask the user before generating)
1. Brief for what? (a brand-new product / a new feature / an improvement to an existing product)
2. Who writes the brief? (PM / Founder / which team?)
3. Who reads and approves it?
4. Include a technical spec in the brief, or keep it separate?
5. Desired level of detail? (1 page / 3-5 pages)

#### Suggested template
Structure:
- **Header** — product/feature name, author, date, status (Draft/Review/Approved)
- **Problem Statement** — what problem? Who has it? How big is the impact?
- **Target Customer** — persona, segment, jobs-to-be-done
- **Proposed Solution** — high-level description, key features, differentiators
- **Success Metrics** — KPIs for success: adoption, revenue, NPS
- **Scope** — in scope / out of scope / future considerations
- **Competitive Landscape** — how do competitors solve this?
- **Go-to-Market** — pricing direction, channel, messaging (high-level)
- **Timeline & Resources** — effort estimate, team needed, milestones
- **Risks & Assumptions** — assumptions to validate, main risks
- **Approval** — sign-off section

Confirm the structure before generating.

#### File-generation prompt
```
Create a Product Brief Template.

CONTEXT:
- Company: [Name] — Brief type: [New product / Feature / Improvement]
- Author: [PM / Founder / Team]
- Approver: [title]
- Technical spec: [Included / Separate]
- Length: [1 page / 3-5 pages]

FORMAT:
- 1 fillable template — each section has a [placeholder] + short guidance
- Problem: framework — [Who] has problem [what] when [situation] leading to [consequence]
- Solution: feature list as a table — Feature | Description | Priority (P0/P1/P2)
- Metrics: table KPI | Definition | Target | Measurement method
- Scope: 2 columns — ✅ In Scope | ❌ Out of Scope
- Timeline: Milestone | Date | Owner | Dependencies
- Risk register: Risk | Probability | Impact | Mitigation
- Approval: Role | Name | Date | Signature | Comments

TONE: Structured, concise, actionable — easy to fill, easy to read.
LENGTH: 3-5 pages.
```

---
✍️ Author: Brian H. Doan
