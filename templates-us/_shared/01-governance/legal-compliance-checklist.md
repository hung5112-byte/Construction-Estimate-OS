# PROMPT 06: Legal Compliance Checklist

#### Description
A periodic (monthly/quarterly/annual) checklist to review legal compliance. Covers: federal/Texas tax, payroll taxes, employment, fire/health permits, environmental, financial recordkeeping, and other legal obligations. General information only — not legal/tax advice.

#### Information to collect (ask the user before generating)
1. Industry? (each has its own compliance)
2. Headcount? (affects employment + payroll-tax obligations)
3. Any import/export or foreign-payment activity?
4. Ever been audited/penalized? (identify risk areas)
5. Who is responsible for the monthly check?

#### Suggested template
Structure:
- **By frequency**: Monthly | Quarterly | Annually | Event-driven
- **By area**: Tax (IRS / Texas Comptroller) | Payroll (FICA/FUTA/SUTA, TWC) | Fire/health permits | Environmental | Industry-specific | Financial records
- **Each item**: # | Obligation | Deadline | Agency | Owner | Status ☐ | Notes
- **Calendar view**: 12-month timeline, highlight deadlines
- **Penalty reference**: penalty if missed (as a deterrent) [UNCERTAIN — verify amounts with CPA/attorney]

Confirm the structure before generating.

#### File-generation prompt
```
Create a Legal Compliance Checklist — a periodic compliance checklist.

CONTEXT:
- Company: [Name] — Industry: [industry] — Headcount: [number]
- Import/export: [Yes/No] — Foreign payments: [Yes/No]
- Compliance owner: [title]
- Special risk areas: [list if any]

FORMAT:
- 4 tables by frequency: Monthly / Quarterly / Annually / Event-driven
- Each table: # | Obligation | Deadline | Agency (IRS / Comptroller / TWC / DSHS / local) | Owner | Done ☐ | Penalty if missed
- Calendar heatmap: 12 months × deadline intensity
- Traffic-light status: 🟢 Done | 🟡 Upcoming (<30 days) | 🔴 Overdue
- Summary: __/__ items done this month

TONE: Compliance — serious, risk-aware.
LENGTH: 5-8 pages.

NOTE: General information, not legal/tax advice. Confirm obligations with a licensed Texas CPA/attorney.
```

---
✍️ Author: Brian H. Doan
