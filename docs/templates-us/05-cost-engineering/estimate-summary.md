# Estimate Summary

#### Description
Division-level summary with labor, material, equipment, subcontract, totals, $/SF and % of total, plus general conditions and the markup stack.

#### Information to collect (ask the Chief Estimator before generating)
1. Cost library rows and plugs used?
2. Markup policy defaults or bid-specific rates?

#### Suggested template
Structure:
- **Summary table** — division · description · L · M · E · sub · total · $/SF · %
- **General conditions** — staffing and temporary facilities by duration
- **Markup stack** — contingency · escalation · insurance · bond · tax · fee with basis
- **Unpriced and plugged lines**
- **Sources**

Confirm the structure before generating.

#### File-generation prompt
```
Create the Estimate Summary for {{project_name}} (bid {{bid_date}}), Blackland Commercial Builders preconstruction.
Every quantity cites sheet id + revision; every price cites a cost-library row; every open question carries a cost exposure.
Output as a markdown document with the sections listed above; tables where the section is tabular.
```
