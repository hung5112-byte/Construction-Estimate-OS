# PROMPT 12: OKR Template (Objectives & Key Results)

#### Description
A quarterly OKR system — cascading from Company → Department → Individual. Each Objective has 3-5 measurable Key Results. Includes a scoring guide and review template.

#### Information to collect (ask the user before generating)
1. OKRs for which level? (Company / Department / Individual / all)
2. Which quarter? (Q1/Q2/Q3/Q4, which year)
3. Company-level objectives? (list 3-5)
4. Which departments need OKRs? (list)
5. Used OKRs before? (need training materials included?)
6. Scoring system: 0-1.0 (Google style) / % / RAG?

#### Suggested template
Structure:
- **OKR Primer** — a 1-page quick guide: what OKRs are, rules, common mistakes
- **Company OKRs** — 3-5 Objectives, each with 3-5 KRs
- **Department OKRs** — per dept, aligned to Company OKRs
- **Individual OKRs** — a blank template for individuals
- **Scoring Guide** — 0.0-0.3 (Red), 0.4-0.6 (Yellow), 0.7-1.0 (Green)
- **Weekly Check-in Template** — KR | Target | Current | Confidence (🟢🟡🔴) | Blockers
- **Quarterly Review Template** — score + learnings + next-quarter adjustments
- **OKR Calendar** — timeline: Set (week 1) → Check-in (weekly) → Score (week 12) → Reflect (week 13)

Confirm the structure before generating.

#### File-generation prompt
```
Create an OKR Template.

CONTEXT:
- Company: [Name] — OKR level: [Company / Department / Individual / All]
- Quarter: [Q_/20__]
- Company objectives: [list 3-5]
- Departments: [list]
- OKR maturity: [first time / experienced]
- Scoring: [0-1.0 / % / RAG]

FORMAT:
- OKR Primer: 1 page, visual, rules of thumb
- OKR Sheet: O | KR1 | KR2 | KR3 | Score | Owner
- Cascade view: Company → Dept → Individual alignment map
- Confidence meter: weekly template with traffic light
- Quarterly retrospective: What worked | What didn't | Adjust for next Q
- Common mistakes: top 10 OKR mistakes + how to avoid them

TONE: Goal-setting — ambitious, measurable, inspiring.
LENGTH: 5-8 pages (including templates).
```

---
✍️ Author: Brian H. Doan
