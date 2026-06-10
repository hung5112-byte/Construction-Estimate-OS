### PROMPT 03: New Product Development SOP

#### Description
A standardized process from a new-product idea to market launch. Includes gates/checkpoints, go/no-go criteria, each function's role, and a standard timeline.

#### Information to collect (ask the user before generating)
1. Type of product developed? (software / physical / service / hybrid)
2. Average cycle time from idea to launch? (weeks / months)
3. Who can propose a new product? (PM only / all employees / leadership only)
4. Current approval process? (stage-gate or freestyle?)
5. MVP/Beta testing before full launch?
6. Typical new-product development budget?

#### Suggested template
Structure:
- **Purpose & scope**
- **Stage 1 — Ideation**: collect ideas, screening, feasibility check
- **Gate 1 — Concept Approval**: go/no-go criteria, who approves
- **Stage 2 — Research & Planning**: market research, technical feasibility, business case
- **Gate 2 — Business Case Approval**: ROI, resource commitment
- **Stage 3 — Development**: build/produce, prototype, internal testing
- **Gate 3 — Product Review**: QC, UAT, beta feedback
- **Stage 4 — Launch Prep**: GTM plan, training, pricing, collateral
- **Gate 4 — Launch Decision**: final go/no-go
- **Stage 5 — Launch & Review**: go-to-market, 30/60/90 review
- **Appendix**: stage-gate checklist, RACI per stage

Confirm the structure before generating.

#### File-generation prompt
```
Create a New Product Development SOP.

CONTEXT:
- Company: [Name] — Product type: [software / physical / service]
- Target cycle time: [X weeks/months]
- Who proposes: [PM / all employees / leadership]
- New-product budget: [range]
- MVP/Beta: [Yes/No]

FORMAT:
- Stage-Gate flowchart: Mermaid — 5 stages + 4 gates
- Each stage: Input | Activities | Output | Owner | Timeline
- Each gate: criteria checklist ☐ | decision maker | Go/Kill/Pivot
- RACI matrix: Stage × Role (PM, Dev, QC, Marketing, Sales, Finance, CEO)
- Timeline template: Gantt for one sample product
- Budget template: Stage | Cost items | Estimate | Actual | Variance (USD)
- KPI post-launch: Metric | Target | Actual | Review date

TONE: Standard SOP — clear, step-by-step, with control gates.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
