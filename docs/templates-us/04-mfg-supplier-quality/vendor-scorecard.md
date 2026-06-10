### PROMPT 07: Vendor Scorecard

#### Description
A weighted vendor-evaluation sheet — Quality, Price, Delivery, Service, Financial. Used for the initial evaluation and re-evaluation.

#### Information to collect (ask the user before generating)
1. Criteria weights? (e.g. Quality 30% + Price 25% + Delivery 20% + Service 15% + Financial 10%)
2. Scale: 1-5 or 1-10?
3. Passing threshold: minimum score?
4. A detailed rubric describing each score level?

#### Suggested template
Structure:
- **Scorecard matrix**: 5 criteria groups × 3-5 sub-criteria × weight × score
- **Detailed rubric**: each sub-criterion × each score level = specific behavioral description
- **Weighted score calculator**: the formula for the total score
- **Rating scale**: ≥X Approved 🟢 | ≥Y Conditional 🟡 | <Y Rejected 🔴
- **Comparison view**: Vendor A vs. B vs. C on one table
- **Trend tracking**: this period's score vs. last → trend

Confirm the structure before generating.

#### File-generation prompt
```
Create a Vendor Scorecard.

CONTEXT:
- Company: [Name] — Weights: Quality [%] | Price [%] | Delivery [%] | Service [%] | Financial [%]
- Scale: [1-5 / 1-10]
- Passing threshold: [score]

FORMAT:
- Scorecard matrix: 5 criteria groups × 3-5 sub-criteria each × weight × score
- Rubric: each sub-criterion × each score level = specific description (e.g. Quality=5 "Zero defects in 6 months")
- Weighted score calculator: clear formula
- Rating scale: ≥[X] Approved 🟢 | ≥[Y] Conditional 🟡 | <[Y] Rejected 🔴
- Comparison view: Vendor A vs. B vs. C on one table
- Trend: this period's score vs. last

TONE: Objective, quantitative, structured.
LENGTH: 3-4 pages.

CROSS-REFERENCE: Links to the Vendor Evaluation SOP (P-OPS-06) and the AVL (P-OPS-08).
```

---
✍️ Author: Brian H. Doan
