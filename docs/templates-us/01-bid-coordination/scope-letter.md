# Scope Letter and Qualifications

#### Description
The inclusions, exclusions, alternates, unit prices and clarifications that accompany the bid form.

#### Information to collect (ask the Chief Estimator before generating)
1. Bid form alternates and unit prices as listed in 01 23 00 / 01 22 00?
2. Owner allowances to carry verbatim?

#### Suggested template
Structure:
- **Inclusions** — by division
- **Exclusions and qualifications** — from the master list, customized
- **Allowances, alternates, unit prices** — verbatim from the bid form
- **Assumptions** — from the RFI log
- **Bid validity and schedule basis**

Confirm the structure before generating.

#### File-generation prompt
```
Create the Scope Letter and Qualifications for {{project_name}} (bid {{bid_date}}), Blackland Commercial Builders preconstruction.
Every quantity cites sheet id + revision; every price cites a cost-library row; every open question carries a cost exposure.
Output as a markdown document with the sections listed above; tables where the section is tabular.
```
