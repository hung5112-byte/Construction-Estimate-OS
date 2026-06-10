# P-PPL-12: Structured Interview Question Bank

#### Description
A structured-interview question bank — so every candidate is asked the same set of questions and evaluated fairly. Split into general (culture fit), competency-based, and role-specific questions.

> EEO note: keep questions job-related. Avoid asking about protected characteristics — age, race, religion, national origin, disability, pregnancy, marital/family status, or genetic information (Title VII / ADA / ADEA / GINA; Texas Labor Code ch. 21). A structured, consistent process reduces bias and legal risk. [verify specifics with an attorney]

#### Information to collect (ask the user before generating)
1. The company's core values? (culture-fit questions revolve around values)
2. A competency framework? (the core competencies to assess)
3. Which roles need their own question set? (sales, marketing, accounting, IT...)
4. Interview style: Behavioral (STAR) / Situational / Case study?
5. Use a skills test as well?

#### Suggested template
Structure:
- **Part A** — General questions (10-15): culture fit, motivation, career goals, teamwork
- **Part B** — Competency questions (20): leadership, problem-solving, communication, adaptability, integrity
- **Part C** — Role-specific questions (10/role): sales, marketing, finance, tech
- **Part D** — Red flags & deal breakers: warning signs to watch for
- **Guide**: how to use the STAR method to evaluate answers

Confirm the structure before generating.

#### File-generation prompt
```
Create a Structured Interview Question Bank.

CONTEXT:
- Company: [Name] — Core values: [list]
- Competency framework: [Yes/No] — Core competencies: [list]
- Sample roles: [Sales / Marketing / Accounting / IT]
- Style: [Behavioral STAR / Situational / Mixed]

FORMAT:
- 3 groups: General (culture fit) | Competency | Role-specific
- Each question: question + what to listen for + 1-5 scale
- STAR guide: Situation → Task → Action → Result — how the interviewer should probe
- 30 general + 20 competency + 10 per sample role
- Red-flags checklist: 8-10 warning signs
- Rubric per question: 1 (Weak) → 3 (Meets) → 5 (Excellent) — specific descriptions
- Compliance reminder: keep questions job-related; avoid protected-characteristic topics

TONE: Professional HR, objective, helps the interviewer avoid bias.
LENGTH: 5-7 pages.
```

---
✍️ Author: Brian H. Doan
