# P-PPL-13: Candidate Evaluation Scorecard

#### Description
A post-interview candidate evaluation — scoring against weighted criteria to reach an objective Go/No-Go decision. Used per interviewer and aggregated across the panel.

> EEO note: score on job-related criteria only; a consistent, documented scorecard reduces bias and supports defensible hiring decisions (Title VII / ADA / ADEA).

#### Information to collect (ask the user before generating)
1. How many evaluation criteria? (usually 8-12)
2. Weight per criterion? (e.g. Experience 25%, Culture fit 20%, Skills 20%...)
3. Scale: 1-5 or 1-10?
4. How many interviewers evaluate? (need an individual form + a summary form)
5. Decision: majority vote or consensus?

#### Suggested template
Structure:
- **Individual Scorecard**: one form per interviewer — criteria × score × notes
- **Panel Summary**: aggregate of all interviewers — compared on one table
- **Decision Framework**: score thresholds → Hire / Maybe / No Hire
- **Comparison View**: Candidate A vs. B vs. C — side by side

Confirm the structure before generating.

#### File-generation prompt
```
Create a Candidate Evaluation Scorecard.

CONTEXT:
- Company: [Name] — # criteria: [8-12]
- Weights: [e.g. Experience 25% | Skills 20% | Culture 20% | Communication 15% | Problem Solving 10% | Motivation 10%]
- Scale: [1-5 / 1-10]
- # interviewers: [number]
- Decision: [Majority / Consensus]

FORMAT:
- Individual form: table Criterion | Weight | Score 1-5 | Evidence/Notes
- Rubric per criterion: Score 1 (description) → 3 (description) → 5 (description)
- Weighted score: clear formula — Sum(Weight × Score) = Total
- Panel summary: table Criterion | Interviewer 1 | 2 | 3 | Average | Weighted
- Decision thresholds: ≥[X] Strongly Hire 🟢 | ≥[Y] Hire 🟡 | ≥[Z] Maybe 🟠 | <[Z] No Hire 🔴
- Comparison matrix: 3 candidates × 12 criteria — highlight the top scorer per criterion

TONE: Objective, quantitative, bias-free.
LENGTH: 2-3 pages.
```

---
✍️ Author: Brian H. Doan
