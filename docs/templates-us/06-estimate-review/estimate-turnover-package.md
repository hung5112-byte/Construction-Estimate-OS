# Estimate Turnover Package

#### Description
What operations receives after award: the estimate with quantities and labor hours, sub quotes and validity, scope sheets, assumptions, exclusions, site notes and schedule basis.

#### Information to collect (ask the Chief Estimator before generating)
1. Award date and turnover meeting date?
2. Verbal commitments made to the owner?

#### Suggested template
Structure:
- **Estimate detail** — by division with quantities, unit costs, labor hours
- **Sub quotes and validity dates**
- **Scope sheets, allowances, exclusions, alternates accepted**
- **Site and schedule notes; open RFIs**
- **Contract document conflicts list**

Confirm the structure before generating.

#### File-generation prompt
```
Create the Estimate Turnover Package for {{project_name}} (bid {{bid_date}}), Blackland Commercial Builders preconstruction.
Every quantity cites sheet id + revision; every price cites a cost-library row; every open question carries a cost exposure.
Output as a markdown document with the sections listed above; tables where the section is tabular.
```
