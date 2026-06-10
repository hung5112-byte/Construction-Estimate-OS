# P-PPL-16: Employee Handbook

#### Description
An "all-in-one" handbook for new and current employees. Summarizes everything they need to know: company intro, culture, policies, processes, benefits, contacts. References the source files instead of copying full content. General information only — not legal advice; have an employment attorney review (especially the at-will and EEO sections).

#### Information to collect (ask the user before generating)
1. A welcome letter from the Department Head? (personal touch)
2. Company intro: history, mission, vision, values already in 02-Strategy?
3. Desired tone: formal / friendly / startup-vibe?
4. Need a polished digital (PDF) version, or is Markdown enough?
5. Update frequency: annual / on change?

#### Suggested template
Structure:
- **Department Head welcome**: 1 page — a personalized welcome letter
- **About the company**: history, VMV, core values, products, team (summary)
- **Culture**: culture code summary, rituals, norms
- **At-will & acknowledgment**: a clear at-will statement and that the handbook is NOT an employment contract (Texas at-will default)
- **EEO statement**: equal employment opportunity & anti-harassment (Title VII / EEOC; Texas Labor Code ch. 21)
- **Policies**: summary + link to source file — pay, benefits, leave/PTO, remote, confidentiality
- **Processes**: summary + link — requests, reimbursement, reporting, purchasing
- **Benefits**: highlight top benefits — a 1-page summary table
- **FAQ**: 20 common new-hire questions
- **Contacts**: HR, IT, Admin, direct manager

Confirm the structure before generating.

#### File-generation prompt
```
Create an Employee Handbook.

CONTEXT:
- Company: [Name] — Department Head letter: [Yes/No]
- Tone: [Formal / Friendly / Startup-vibe]
- VMV + Core Values: [summary or link to 02-Strategy]
- Format: [Markdown / PDF]
- Authority: at-will employment (Texas); Title VII / EEOC + Texas Labor Code ch. 21 (EEO/anti-harassment); FLSA; Texas Payday Law

FORMAT:
- Table of contents: clear, clickable (if digital)
- Department Head letter: 1 page — personal, inspiring
- About the company: 2-3 pages — history timeline, VMV, team-photo placeholder
- At-will + EEO: a clear statement near the front
- Culture: 2 pages — values in behaviors, dos/don'ts
- Policy summaries: 3-5 pages — half a page each + "Details: [link to source file]"
- Process summaries: 2-3 pages — simple flowchart + link
- Benefits highlight: 1-page table — top 10 benefits
- FAQ: 2 pages — 20 questions + short answers
- Directory: 1 page — Dept | Contact | Email | Phone

TONE: Handbook — easy to read, friendly, one employees WANT to read.
LENGTH: 20-30 pages.

NOTE: General information, not legal advice. Have a licensed Texas employment attorney review the at-will, EEO, and policy sections.
```

---
✍️ Author: Brian H. Doan
