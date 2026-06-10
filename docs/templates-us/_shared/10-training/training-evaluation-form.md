### PROMPT 07: Training Evaluation Form

#### Description
A set of training-evaluation forms using the 4-level Kirkpatrick model — Level 1: Reaction (were learners satisfied?), Level 2: Learning (what did they learn?), Level 3: Behavior (are they applying it?), Level 4: Results (business outcomes?). Each level has its own form and timing.

#### Information to collect (ask the user before generating)
1. Any training evaluation today? At what level? (satisfaction survey only / none)
2. To what level do you want to evaluate? (L1-L2 for most / L3-L4 for key programs)
3. Who distributes and collects the forms? (trainer / HR / LMS auto)
4. Format: paper / Google Forms / LMS / software?
5. Need to compare pre-test vs. post-test?
6. Will the manager assess behavior change?

#### Suggested template
Structure:
- **Part 1** — How to use: when to use each level, who fills, timeline
- **Part 2** — Level 1 — Reaction Form: satisfaction survey right after training
- **Part 3** — Level 2 — Learning Assessment: pre-test / post-test / knowledge check
- **Part 4** — Level 3 — Behavior Change Form: manager + self-assessment after 30-90 days
- **Part 5** — Level 4 — Results Measurement: business KPIs before vs. after training
- **Part 6** — Summary Dashboard: all 4 levels per program
- **Appendix**: scale reference, sample analysis report

Confirm the structure before generating.

#### File-generation prompt
```
Create a Training Evaluation Form.

CONTEXT:
- Company: [Name] — Current evaluation: [describe current level]
- Evaluate to level: [L1-L2 most / L3-L4 major programs]
- Format: [paper / digital / LMS]
- Manager participates: [Yes/No]
- Pre/Post test: [Yes/No]

FORMAT:
- Usage guide: table Level | Timing | Who fills | Who collects | Purpose
- Level 1 — Reaction Form (right after training):
  - Rating scale: 1-5 Likert — 8-12 questions
  - Categories: content relevance | trainer quality | materials | logistics | overall satisfaction
  - Open questions: "Most useful?" | "Needs improvement?" | "Suggestions?"
  - NPS question: "Would you recommend this course to a colleague? (0-10)"
- Level 2 — Learning Assessment:
  - Pre-test: 10 MCQ/True-False — measure baseline
  - Post-test: 10 equivalent questions — measure knowledge gain
  - Learning-gain formula: (Post - Pre) / (Max - Pre) × 100%
  - Practical assessment: rubric — Criteria | Excellent | Good | Needs Improvement | Not Demonstrated
- Level 3 — Behavior Change (30-90 days later):
  - Self-assessment: "I applied skill X..." — rating 1-5 + evidence/example
  - Manager assessment: "The employee demonstrated behavior X..." — rating 1-5 + observation
  - Application rate: % of skills applied / total learned
  - Barriers: "What prevented application?" — checklist + open
- Level 4 — Results (3-6 months later):
  - KPI tracking: Metric | Before training | After training | Change % | Attribution %
  - Business-impact examples: revenue, productivity, quality, customer satisfaction, employee retention
- Summary dashboard: Program | L1 Score | L2 Gain % | L3 Application % | L4 Impact | ROI estimate
- Trend analysis: Program × Quarter → score trends

TONE: Scientifically measured, easy to fill, actionable insights.
LENGTH: 5-8 pages.
```

---
✍️ Author: Brian H. Doan
