# PROMPT 10: Risk Management Policy

#### Description
A comprehensive framework to identify, assess, treat, and monitor risk at the company level. Based on ISO 31000:2018, customized for a US small business.

#### Information to collect (ask the user before generating)
1. Industry & size? (defines the risk profile)
2. Any serious incidents before? (e.g. data loss, litigation, production failure)
3. Is there a dedicated risk-management function?
4. Risk appetite: is the company risk-averse or risk-taking?
5. Need a risk-register template included?

#### Suggested template
Structure:
- **Part 1** — Purpose, scope, leadership commitment
- **Part 2** — Terms & definitions (per ISO 31000)
- **Part 3** — Risk-management framework: identify → analyze → evaluate → treat → monitor
- **Part 4** — Risk categories: strategic / financial / operational / compliance / reputational / technology
- **Part 5** — Risk matrix: likelihood (1-5) × impact (1-5) = risk score
- **Part 6** — Treatment strategies: avoid / mitigate / transfer / accept
- **Part 7** — Roles & responsibilities
- **Part 8** — Reporting & periodic review
- **Appendix**: risk register template, heat-map template

Confirm the structure before generating.

#### File-generation prompt
```
Create a Risk Management Policy.

CONTEXT:
- Company: [Name] — Industry: [industry] — Size: [headcount, revenue]
- Incidents experienced: [list or "none"]
- Risk-management function: [Yes/No]
- Risk appetite: [Conservative / Moderate / Aggressive]
- Reference standard: ISO 31000:2018

FORMAT:
- Clear sections with a table of contents
- 5×5 risk matrix: likelihood × impact, color-coded (Green/Yellow/Orange/Red)
- Risk categories: 6 types with concrete examples for the industry
- Treatment strategies: table: risk | strategy | action | owner | timeline | KRI
- Risk register template: # | description | type | L | I | score | strategy | owner | status
- Reporting workflow: flowchart for a newly identified risk

TONE: Professional, ISO-aligned, practical.
LENGTH: 10-15 pages.
```

---
✍️ Author: Brian H. Doan
