# P-PPL-02: Standard Job Description Template

#### Description
A standardized job-description (JD) template for EVERY role in the business. Ensures a consistent format, complete information, and easy recruiting and evaluation.

> EEO note: keep JD requirements bona-fide and job-related; avoid criteria that could screen out protected groups without job justification (Title VII / ADA / ADEA). [verify with an attorney for sensitive roles]

#### Information to collect (ask the user before generating)
1. Do you have a competency framework?
2. Should the JD link to a pay band?
3. Format: Markdown / Word / Google Doc?

#### Suggested template
Structure — JD sections:
- **Header**: title, department, level, reports to, direct reports
- **Position purpose**: 2-3 sentences on why the role exists
- **Key responsibilities**: 5-8 bullets, ordered by importance
- **Key KPIs**: 3-5 measurable KPIs
- **Requirements**: education, experience, hard skills, soft skills, certifications
- **Core competencies**: per the competency framework (if any)
- **Working conditions**: hours, location, travel, remote
- **Compensation**: pay range, benefits highlights
- **Career path**: the next role(s) for advancement

Confirm the structure before generating.

#### File-generation prompt
```
Create a Standard Job Description Template.

CONTEXT:
- Company: [Name] — Competency framework: [Yes/No]
- Link to pay band: [Yes/No]
- Format: [Markdown / Word / GDoc]

FORMAT:
- One-page template — fill fields [___]
- Header table: Title | Dept | Level | Reports to | Manages | Date
- Responsibilities: numbered list + % time on each
- KPIs: table KPI | Target | Measurement | Frequency
- Requirements: split Must-have vs. Nice-to-have
- Competencies: table Competency | Level Required (Basic/Intermediate/Advanced/Expert)
- Fill guide: 1 page — tips for writing an effective, EEO-compliant JD

TONE: Professional HR, clear, attractive to candidates.
LENGTH: 2 pages (template + guide).
```

---
✍️ Author: Brian H. Doan
