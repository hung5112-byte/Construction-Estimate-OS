# P-PPL-03: Key Position Job Descriptions

#### Description
Four detailed JDs for the most common key roles in a small business: Sales Director, Marketing Manager, Controller (Head of Accounting), and Sales Representative. Customize by industry and company size.

#### Information to collect (ask the user before generating)
1. The company's industry? (affects technical requirements)
2. Current size? (a JD for a 10-person company differs from a 100-person one)
3. Expected pay for each role? (to write the compensation section)
4. Which role is the most urgent to hire?
5. Add/remove any roles?

#### Suggested template
Each JD follows the standard format in PROMPT 02, fully detailed:
- **Sales Director**: lead the sales team, sales strategy, revenue targets, channel development
- **Marketing Manager**: brand, digital marketing, content, marketing budget, campaign ROI
- **Controller (Head of Accounting)**: accounting system, financial statements, taxes, audit, compliance
- **Sales Representative**: consultative selling, customer care, hit targets, reporting

Confirm the structure before generating.

#### File-generation prompt
```
Create JDs for 4 key positions.

CONTEXT:
- Company: [Name] — Industry: [industry] — Size: [headcount]
- Pay: Sales Director [range] | Marketing Mgr [range] | Controller [range] | Sales Rep [range]
- Urgent role: [role name]
- Changes/additions: [list if any]

FORMAT:
- 4 separate JDs, 1.5-2 pages each
- Standard format: Header → Purpose → Responsibilities (8-10 bullets) → KPIs (5) → Requirements → Competencies → Compensation
- Customize by industry: e.g. Sales in SaaS differs from Sales in CPG
- Specific, measurable KPIs: e.g. "Hit 100% of the quarterly revenue target" rather than "sell well"
- Responsibilities ordered by % time: 40% Selling | 20% Managing | 20% Planning | 20% Reporting

TONE: Professional, attractive — both an internal document and a recruiting tool.
LENGTH: 6-8 pages (4 JDs × 1.5-2 pages).
```

---
✍️ Author: Brian H. Doan
