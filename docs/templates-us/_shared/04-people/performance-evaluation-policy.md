# P-PPL-20: Performance Evaluation Policy

#### Description
A performance-evaluation policy — defining frequency, method, rating scale, the link to pay/promotion, and the appeal process. The foundation for KPIs, 360 reviews, and the whole performance-management system.

> US note: consistent, documented performance reviews help support fair pay decisions and defend at-will personnel decisions against discrimination claims. Apply ratings consistently across employees. [verify with an attorney]

#### Information to collect (ask the user before generating)
1. Frequency? (quarterly / semi-annual / annual)
2. Method: MBO / OKR / KPI / BSC / mixed?
3. Rating scale: 1-5 (Outstanding → Poor) or A-E?
4. Pay link: how much does the rating affect a raise (%)?
5. Promotion link: how many good cycles to move up a level?
6. An appeal process for review results?

#### Suggested template
Structure:
- **Part 1** — Purpose: improve performance, develop people, basis for pay/promotion
- **Part 2** — Scope: who it applies to, from when (after the introductory period)
- **Part 3** — Method: MBO/OKR/KPI/BSC — when to use which
- **Part 4** — Cycle & timeline: evaluation calendar, deadlines per step
- **Part 5** — Rating scale: scale + detailed description per level
- **Part 6** — Process: self-assessment → manager assessment → calibration → feedback → sign-off
- **Part 7** — Comp linkage: rating → raise %, bonus, promotion
- **Part 8** — Appeal mechanism: process to contest a result
- **Appendix**: evaluation calendar, rating-distribution guideline

Confirm the structure before generating.

#### File-generation prompt
```
Create a Performance Evaluation Policy.

CONTEXT:
- Company: [Name] — Headcount: [number]
- Frequency: [Quarterly / Semi-annual / Annual]
- Method: [MBO / OKR / KPI / BSC / Mixed]
- Scale: [1-5 / A-E]
- Pay link: [describe]
- Promotion link: [describe]
- Appeal: [Yes/No]

FORMAT:
- Rating scale: table Score | Label | Description | expected % of employees (bell-curve guide)
- Process flowchart: Mermaid — Set goals → Mid-review → Self-assess → Manager assess → Calibrate → Feedback → Sign-off
- Calendar: 12-month timeline × evaluation milestones
- Comp linkage matrix: Rating | raise % | bonus multiplier | promotion eligible
- Calibration guide: forced distribution vs. absolute scale — pros/cons
- Appeal flowchart: employee contests → HR review → committee → final decision
- FAQ: 10 common questions
- Note: document consistently; apply ratings uniformly

TONE: Fair, transparent, developmental — not punitive.
LENGTH: 6-8 pages.
```

---
✍️ Author: Brian H. Doan
