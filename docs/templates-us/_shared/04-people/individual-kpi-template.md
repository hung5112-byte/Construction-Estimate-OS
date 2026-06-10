# P-PPL-21: Individual KPI Template

#### Description
An individual KPI template using the Balanced Scorecard's 4 perspectives — helping employee and manager set, track, and evaluate KPIs quarterly/annually. Each KPI has a formula, target, weight, actual, and an auto-computed score.

#### Information to collect (ask the user before generating)
1. Framework: BSC 4 perspectives or simple KPIs?
2. KPIs per person: 5-8 (recommended) or more?
3. Full SMART format? (Specific, Measurable, Achievable, Relevant, Time-bound)
4. Weights: manager-set or employee-proposed?
5. Scoring: linear (80% of target = 80 points) or step (≥100% = A, 80-99% = B...)?
6. Linked to company OKRs?

#### Suggested template
Structure:
- **Header**: Employee | Title | Department | Review period | Manager
- **BSC 4 Perspectives**: Financial | Customer | Internal Process | Learning & Growth
- **Each KPI**: name | formula | unit | target | weight | actual | score
- **Total score**: weighted average → rating conversion
- **Comments**: employee self-comment + manager comment
- **Sign-off**: Employee + Manager + HR

Confirm the structure before generating.

#### File-generation prompt
```
Create an Individual KPI Template (BSC).

CONTEXT:
- Company: [Name]
- Framework: [BSC 4 perspectives / Simple KPI]
- # KPIs: [5-8]
- Scoring: [Linear / Step]
- Linked to OKR: [Yes/No]

FORMAT:
- 1-2 page template
- BSC layout: 4 quadrants — Financial | Customer | Internal Process | Learning
- Each KPI row: # | Perspective | KPI Name | Formula | Unit | Target | Weight% | Actual | Achievement% | Score
- Weight validation: sum = 100%
- Score formula: Achievement% × Weight = Weighted Score → sum all = Total
- Rating conversion: Total ≥90 = A (Outstanding) | 80-89 = B (Good) | 70-79 = C (Meets) | 60-69 = D (Below) | <60 = E (Poor)
- SMART checklist: each KPI self-checks the 5 SMART criteria ☐
- Example KPIs: 2-3 examples per perspective for Sales/Marketing/Operations

TONE: Performance management, analytical, easy to fill.
LENGTH: 2-3 pages.
```

---
✍️ Author: Brian H. Doan
