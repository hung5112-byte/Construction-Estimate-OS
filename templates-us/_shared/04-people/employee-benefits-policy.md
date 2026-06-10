# P-PPL-07: Employee Benefits Policy

#### Description
A comprehensive benefits policy — covering the mandatory employer payroll obligations under US law and supplemental benefits (private health insurance, retirement match, stipends, wellness, team events...). A key retention tool alongside pay. General information only — not legal/tax advice; confirm with an attorney/CPA.

> US legal note (statutory payroll obligations and benefit mandates):
> - **Mandatory employer obligations**: Social Security + Medicare (FICA — employer 6.2% + 1.45%, 26 U.S.C. §3111), federal unemployment tax (FUTA, 26 U.S.C. §3301) and Texas state unemployment tax (SUTA, via the Texas Workforce Commission).
> - **Workers' compensation**: Texas is the **only state where workers' comp is generally optional** for private employers (Tex. Lab. Code §406.002) — but a non-subscriber must report and loses certain liability defenses [verify current rules with an attorney].
> - **Health insurance**: not required for small employers — the ACA employer mandate applies only to "applicable large employers" with 50+ full-time-equivalent employees (26 U.S.C. §4980H). A solo operator is typically below this threshold.
> - **Supplemental** (discretionary): health/dental/vision, 401(k) or IRA, life/disability, PTO, wellness, education stipend.

#### Information to collect (ask the user before generating)
1. Offer supplemental health insurance? (carrier, tier?)
2. Annual retreat/offsite? Budget?
3. Holiday/birthday perks: gift or cash? Amount?
4. Education/training support? (tuition, certifications, conferences)
5. Special perks: gym, meals, flexible hours?
6. Benefit tiers by level/tenure?

#### Suggested template
Structure:
- **Part 1** — Purpose: attract, retain, motivate
- **Part 2** — Mandatory employer obligations: FICA, FUTA/SUTA, workers' comp (Texas optional — disclose subscriber/non-subscriber status)
- **Part 3** — Supplemental insurance: health/dental/vision, life/disability — carrier, tier, coverage
- **Part 4** — Financial perks: meal/commuter/phone/housing stipends
- **Part 5** — Culture perks: retreats, team events, birthdays, gifts
- **Part 6** — Development perks: training, certifications, conferences, books
- **Part 7** — Benefits by level: level → additional perks
- **Appendix**: benefits summary table, market comparison

Confirm the structure before generating.

#### File-generation prompt
```
Create an Employee Benefits Policy.

CONTEXT:
- Company: [Name] — Industry: [industry] — Headcount: [number]
- Supplemental insurance: [Yes/No] — Carrier: [name] — Tier: [basic/premium]
- Retreat: [Yes/No] — Budget: [amount/person/year]
- Birthday/holiday: [amount]
- Training: [yes/no] — Budget: [amount/person/year]
- Special perks: [list]
- Authority: FICA (26 U.S.C. §3111); FUTA (26 U.S.C. §3301) + Texas SUTA (TWC); workers' comp (Tex. Lab. Code §406.002, optional in Texas); ACA employer mandate (26 U.S.C. §4980H, 50+ FTE only)

FORMAT:
- 1-page summary table: Benefit | Description | Value | Eligibility | Frequency
- Mandatory obligations: FICA/FUTA/SUTA + workers' comp subscriber status note
- Supplemental insurance: table Coverage | Limit | How to use | Claim process
- Benefits calendar: 12 months × event/benefit
- Per-level benefits: table Level | Base benefits | Additional benefits
- FAQ: 10 common questions

TONE: Friendly, positive — employees should see benefits as a perk, not a burden.
LENGTH: 5-7 pages.

NOTE: General information, not legal/tax advice. Confirm employer obligations (incl. Texas workers'-comp election) with an attorney/CPA.
```

---
✍️ Author: Brian H. Doan
