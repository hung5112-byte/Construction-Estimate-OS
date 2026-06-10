# PROMPT 02: Scope Assessment

#### Description
An SOP for analyzing the Intake Questionnaire results to determine: what maturity level the company is at, which tier to prioritize, which sub-skills to run first, and which to skip or customize.

#### Information to collect (ask the user before generating)
1. Do you have your own maturity model, or use the standard?
2. Which criteria decide priority order? (urgency / impact / effort / cost)
3. Any case where a sub-skill should be skipped entirely? (e.g. a one-person company doesn't need HR)
4. Who assesses the scope? (AI automatically / coach review / both)

#### Suggested template
Structure:
- **Purpose & scope** — when to use, who uses it
- **Input** — the completed Intake Questionnaire
- **Step 1: Score maturity** — 9 dimensions × 0-5 scale, reference `maturity-scoring.md`
- **Step 2: Determine priority tier** — a decision tree based on score + company goals
- **Step 3: Customize the skill list** — a table of 12 skills × (Run/Skip/Customize) + reason
- **Step 4: Estimate timeline** — a formula for time based on scope
- **Output** — Scope Document (1-page summary) + Execution Plan

Confirm the structure before generating.

#### File-generation prompt
```
Create a "Scope Assessment" SOP for the Business Packaging system.

CONTEXT:
- This is step 2 in the Orchestrator flow: after Intake, before creating folders and calling sub-skills
- Maturity model: [your own / standard] — 9 dimensions: Strategy, Finance, Marketing, Sales, Operations, People, Technology, Governance, Training
- Scale: 0 (nothing yet) → 5 (world-class, automated)
- Priority criteria: [urgency/impact/effort/cost]
- 12 sub-skills: governance, strategy, finance, people, operations, sales, marketing, customer, product-tech, training, reporting, growth

FORMAT:
- Standard SOP: Purpose → Scope → Glossary → Step-by-step process → Flowchart (mermaid) → Output template
- A clear decision tree: IF score < X THEN prioritize Y
- Mapping table: Maturity Score → Recommended Action per skill

TONE: Standards-based, clear, easy to follow for both AI and coach.
LENGTH: 3-5 pages.
```

---
✍️ Author: Brian H. Doan
