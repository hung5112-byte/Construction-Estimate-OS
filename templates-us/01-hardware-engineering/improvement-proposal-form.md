### PROMPT 12: Improvement Proposal Form

#### Description
A template for any employee to propose an improvement idea — problem description, root cause, proposed solution, expected impact, and required resources. The form must be simple and easy to fill so it doesn't discourage proposals.

#### Information to collect (ask the user before generating)
1. What is the form filled on? (paper / Google Forms / Notion / internal software)
2. Level of detail: simple (1 page) or detailed (2-3 pages)?
3. Include a root-cause section?
4. Who reviews the form? Review timeline?
5. A category/classification for improvements?

#### Suggested template
Structure:
- **Header** — proposal title, proposer, department, date, ID
- **Part 1** — Current problem: description, frequency, impact
- **Part 2** — Root cause: root-cause analysis (5 Whys / Fishbone)
- **Part 3** — Proposed solution: description, how to implement
- **Part 4** — Expected impact: time/cost savings, quality improvement
- **Part 5** — Resources needed: budget, people, time, tools
- **Part 6** — Evaluation (reviewer fills): score, priority, decision, feedback
- **Footer** — approval chain

Confirm the structure before generating.

#### File-generation prompt
```
Create an Improvement Proposal Form.

CONTEXT:
- Company: [Name] — Format: [paper / digital / hybrid]
- Detail: [simple 1 page / detailed 2-3 pages]
- Root cause: [Yes/No]
- Reviewer: [title] — Review timeline: [X days]

FORMAT:
- 1 fillable template — max 2 pages
- Header: Proposal ID [IMP-YYYY-NNN] | Proposer | Department | Date
- Problem: [___] + hint "Describe the problem in 2-3 sentences"
- Root cause: a simple 5 Whys (Why 1 → Why 2 → ... → Root Cause)
- Solution: [___] + hint "Describe the solution step-by-step"
- Impact: table — Metric | Before | After (expected) | Improvement %
- Resources: Budget [___] | People [___] | Time [___] | Tools [___]
- Reviewer section: Impact score (1-5) | Effort score (1-5) | Priority | Decision (Approve/Defer/Reject) | Comments
- Approval: Reviewer signature + Date + Manager signature + Date

TONE: Simple, encouraging, easy to fill — anyone can use it.
LENGTH: 1-2 pages.
```

---
✍️ Author: Brian H. Doan
