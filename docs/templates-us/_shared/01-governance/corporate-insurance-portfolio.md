# PROMPT 17: Corporate Insurance Portfolio

#### Description
A consolidated registry of all insurance the company has or needs. Covers: property, liability, workers' comp, business interruption, cyber, D&O. Helps manage the insurance portfolio centrally. General information only — not insurance or legal advice; confirm with a licensed Texas insurance agent/attorney.

#### Information to collect (ask the user before generating)
1. What insurance is currently in place? (list)
2. Industry & main assets? (defines risks to insure)
3. Headcount? (affects workers' comp / EPLI)
4. Annual insurance budget?
5. Any international operations? (may need international coverage)

#### Suggested template
Structure:
- **Portfolio table**: # | Coverage type | Carrier | Policy # | Coverage limit | Premium/year | Effective date | Expiration | Status
- **Grouping**: required / recommended / optional
- **Gap analysis**: uninsured risks
- **Renewal calendar**: 12-month timeline
- **Cost summary**: total premium, YoY comparison
- **Claim history**: claims log

Confirm the structure before generating.

#### File-generation prompt
```
Create a Corporate Insurance Portfolio.

CONTEXT:
- Company: [Name] — Industry: [industry] — Headcount: [number] — Main assets: [list]
- Current coverage: [list]
- Budget: [amount/year]
- International: [Yes/No]

FORMAT:
- Portfolio table: full columns as in the template
- Common US small-business coverages: General Liability, Commercial Property, Workers' Compensation,
  Professional Liability (E&O), Cyber liability, Directors & Officers (D&O), Business Interruption,
  Commercial Auto (if vehicles), Employment Practices Liability (EPLI)
- NOTE: Texas is the only state where workers' compensation is generally OPTIONAL for most private
  employers; a "non-subscriber" must report to the TDI/TWC and gives up certain tort defenses
  [UNCERTAIN — verify with a licensed Texas agent/attorney]
- Recommended-by-industry mapping table: industry → recommended coverages
- Gap analysis: risk | current coverage | gap | recommended | est. premium
- Renewal calendar: Gantt-style or by month
- Total cost of insurance: pie-chart data

TONE: Managerial, practical.
LENGTH: 4-6 pages.

NOTE: General information, not insurance/legal advice.
```

---
✍️ Author: Brian H. Doan
