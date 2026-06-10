# PROMPT 01: Intake Questionnaire

#### Description
A structured questionnaire to gather all the information needed from the business owner before packaging begins. This is the most important step — "garbage in, garbage out." Split into 5 question groups, from basic to in-depth.

#### Information to collect (ask the user before generating)
1. What format for the questionnaire? (Google Form / Markdown checklist / PDF form / interactive prompt)
2. The company's specific industry? (to customize industry-specific questions)
3. Who will fill it out? (owner directly / an assistant / a team?)
4. Desired level of detail? (Quick scan ~20 questions / Standard ~50 / Deep dive ~100)

#### Suggested template
5 question groups:
- **Group 1 — Basic info** (10-15 questions): company name, industry, founding year, revenue, headcount, location, legal entity
- **Group 2 — Stage of development** (8-10 questions): current stage (startup/growth/mature), 1-3-5 year goals, raised capital yet, plans to chain/franchise
- **Group 3 — Current structure** (10-15 questions): is there an org chart, how many departments, which processes are standardized, tools in use (CRM, ERP, accounting...)
- **Group 4 — Priorities & pain points** (8-10 questions): top 3 problems, areas to prioritize, budget & timeline
- **Group 5 — Industry specifics** (5-10 questions): industry regulations, special licenses, seasonal patterns, industry-specific staffing

Format: Markdown with checkboxes, each question with a hint/example. Confirm the structure before generating.

#### File-generation prompt
```
Create an Intake Questionnaire for the Business Packaging project.

CONTEXT:
- Purpose: gather enough information for the AI + business coach to define the packaging scope and customize 200+ documents for the specific company
- Respondent: [Owner / Assistant] — industry [industry]
- Level: [Quick/Standard/Deep dive]

FORMAT:
- Markdown with checkbox [ ] for each question
- Each question has: main question → hint/example (italic) → answer field
- 5 clear groups, continuously numbered
- Define specialized terms on first use
- End of each group: a free-text "Additional notes" field

TONE: Professional yet friendly, easy for a non-specialist owner to understand.
LENGTH: [20/50/100] questions depending on the chosen level.

OUTPUT: a complete markdown file, ready to send to the owner to fill in.
```

---
✍️ Author: Brian H. Doan
