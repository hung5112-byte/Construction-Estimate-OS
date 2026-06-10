# PROMPT 09: Decision Authority Matrix (RACI)

#### Description
A RACI matrix (Responsible-Accountable-Consulted-Informed) for all important company decisions. Defines who does the work, who is accountable, who is consulted, and who is informed — for each decision type.

#### Information to collect (ask the user before generating)
1. Current org chart? (management levels)
2. List of common important decisions? (e.g. hiring, spending, signing contracts, new product launch...)
3. Any current authority problems? (e.g. CEO bottleneck, unclear who decides)
4. Group by area or by decision level?

#### Suggested template
Structure:
- **How to read**: what R/A/C/I mean, the rule "each row has exactly one A"
- **Matrix by area**: a table per area (Finance, People, Sales, Operations, Marketing...)
- **Each table**: Decision | Board | CEO | CFO | HR Lead | Sales Lead | Ops Lead | Manager | Staff
- **Escalation rules**: when a decision must escalate
- **Conflict resolution**: when two people both claim "A" for one decision

Confirm the structure before generating.

#### File-generation prompt
```
Create a Decision Authority Matrix (RACI).

CONTEXT:
- Org structure: [describe or link the org chart]
- Management levels: [number] — Titles: [list]
- Current pain points: [e.g. the CEO must approve everything]
- Grouping: [by area / by level / both]

FORMAT:
- Legend: R=Responsible (does the work), A=Accountable (owns the outcome), C=Consulted, I=Informed
- Matrix per domain: 6-8 tables (Finance, People, Sales, Marketing, Operations, IT, Legal, Strategy)
- Each table: 8-15 decisions × 6-8 roles
- Each cell: R / A / C / I / — (not involved)
- Rule: highlight if a row lacks an A, or a column has too many A's (bottleneck)
- Summary: a workload-per-role table

TONE: Structured, analytical.
LENGTH: 8-12 pages.
```

---
✍️ Author: Brian H. Doan
