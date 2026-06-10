# P-NPI-08: Tooling & NRE Register

#### Description
The register of every tool and fixture the company's production depends on — ownership, location, condition, and the duplication lead time that defines business continuity. If the answer to "could we build elsewhere?" takes more than a minute, this register is missing.

#### Information to collect (ask the user before generating)
1. Sites and products in scope?
2. Tool types to track? (injection molds, stamping dies, test fixtures, assembly jigs, golden units)
3. Ownership documentation status? (MSA clauses, invoices) [ownership/IP terms — verify with attorney]
4. Known condition data? (shot counts, maintenance records)
5. Output format? (.xlsx recommended)

#### Suggested template
Structure (.xlsx):
- **Sheet "Register"**: tool ID, description, product(s), type, site/location, owner
  (us / factory / shared — with document reference), cost (NRE), build date,
  rated life (shots/cycles), current usage, condition, last maintenance
- **Sheet "Continuity"**: per critical tool — duplication lead time, duplication cost,
  drawings/CAD in our possession? (yes/no — no = action), single-point-of-failure flag
- **Sheet "Actions"**: missing ownership docs, missing drawings, tools near end-of-life,
  duplication decisions due
- **Review cadence**: quarterly with the site-risk assessment

Confirm the structure before generating.

#### File-generation prompt
```
Create a Tooling & NRE Register workbook (.xlsx).

CONTEXT:
- Sites: [list] — Products: [list] — Tool types: [list]
- Ownership doc status: [summary]

FORMAT (.xlsx):
- "Register" sheet (ID, product, type, site, owner + doc ref, cost, life, condition)
- "Continuity" sheet (duplication lead time/cost, drawings-in-hand flag, SPOF flag)
- "Actions" sheet; quarterly review note

RULES: every tool has an owner with a document reference, or an action to get one;
every critical tool has a duplication lead time; "drawings not in our possession"
is always an action item.
```

---
✍️ Author: Brian H. Doan
