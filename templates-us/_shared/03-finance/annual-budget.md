# P-FIN-06: Annual Budget

#### Description
A consolidated annual budget — revenue and expense budgets by department, by quarter. Includes the process to build, approve, track variance, and revise the budget.

#### Information to collect (ask the user before generating)
1. Fiscal year? (calendar year or other?)
2. Budgeting method? (Top-down / Bottom-up / Zero-based)
3. How many departments / cost centers need their own budget?
4. Revenue budget too, or expense budget only?
5. Variance review frequency? (Monthly / Quarterly)
6. Build process: timeline from kickoff to owner/board approval?

#### Suggested template
Structure:
- **Part 1** — Budgeting guide: method, assumptions, timeline
- **Part 2** — Revenue Budget: by product/channel × 12 months
- **Part 3** — Consolidated Expense Budget: COGS + SG&A × 12 months
- **Part 4** — Departmental Budget: a detailed table per department
- **Part 5** — CapEx Budget: asset investments, projects
- **Part 6** — Budget Summary: projected P&L, key ratios
- **Part 7** — Variance Tracking: a Budget-vs-Actual tracking template
- **Part 8** — Approval process & mid-year revision
- **Appendix**: per-department budget template, assumption log

Confirm the structure before generating.

#### File-generation prompt
```
Create an Annual Budget.

CONTEXT:
- Company: [Name] — Fiscal year: [year]
- Method: [Top-down / Bottom-up / Zero-based]
- Number of cost centers: [number] — List: [list]
- Revenue budget: [Yes/No]
- Variance review: [Monthly / Quarterly]

FORMAT:
- Revenue budget: Product/Channel × Q1-Q2-Q3-Q4 × monthly breakdown
- Expense budget: Expense line × 12 months × department
- Departmental template: Budget line | Annual | Q1 | Q2 | Q3 | Q4 | Notes (USD)
- P&L budget: Revenue → COGS → Gross Profit → SG&A → EBITDA → Net Income
- Variance tracker: Budget | Actual | Variance $ | Variance % | Explanation
- Key-assumptions log: Assumption | Source | Sensitivity | Impact if wrong
- Approval workflow: flowchart + timeline (T-60 to T-0)

TONE: Financial, structured, easy to fill.
LENGTH: 8-12 pages (+ templates).
```

---
✍️ Author: Brian H. Doan
