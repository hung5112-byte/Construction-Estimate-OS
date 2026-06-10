### PROMPT 02: Training Needs Assessment

#### Description
A survey and analysis of training needs at 3 levels: organizational, departmental, and individual. The TNA result is the main input for the Annual Training Plan. Based on a gap analysis between current and required competencies.

#### Information to collect (ask the user before generating)
1. Does the company have a competency framework? (from 04-People)
2. Needs data source: performance reviews / manager requests / employee survey / business strategy?
3. TNA frequency? (annual / semi-annual / per project)
4. Who fills the survey? (employee self-assessment / manager assessment / both)
5. Distinguish hard vs. soft skills?
6. Desired output: a consolidated report or a prioritized list?

#### Suggested template
Structure:
- **Part 1** — How to use: who fills it, when, how
- **Part 2** — Organizational needs: company strategy → capabilities to build
- **Part 3** — Departmental needs: department × skill → gap
- **Part 4** — Individual assessment: employee self-assessment + manager assessment
- **Part 5** — Gap analysis summary: the largest gaps needing training
- **Part 6** — Priority matrix: Impact × Urgency → training priority
- **Appendix**: reference competency list, manager guide

Confirm the structure before generating.

#### File-generation prompt
```
Create a Training Needs Assessment Form.

CONTEXT:
- Company: [Name] — Headcount: [number] — # departments: [number]
- Competency framework: [Yes/No] — Source: [04-People or self-built]
- Data source: [Performance review / Manager / Survey / Strategy]
- TNA frequency: [annual / semi-annual]
- Assessor: [self-assessment / manager / 360]

FORMAT:
- Organizational analysis: table Strategic Goal | Required Capability | Current Level (1-5) | Gap | Priority
- Departmental analysis: table Department | Skill | Required Level | Current Level | Gap | # Staff affected
- Individual assessment form:
  - Self-rating: Skill | Self-rating (1-5) | Want to develop? (Yes/No) | Notes
  - Manager rating: Skill | Rating (1-5) | Priority (H/M/L) | Recommended training
- Gap heatmap template: Department × Skill → color-coded (🟢 OK / 🟡 small gap / 🔴 large gap)
- Priority matrix: 2×2 — High Impact + Urgent = P1 | High Impact + Not Urgent = P2 | Low Impact + Urgent = P3 | Low = P4
- Summary report template: Top 10 gaps | Affected population | Recommended interventions | Budget estimate

TONE: Easy-to-fill survey, systematic analysis.
LENGTH: 4-6 pages.
```

---
✍️ Author: Brian H. Doan
