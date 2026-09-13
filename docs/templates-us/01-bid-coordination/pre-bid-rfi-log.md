# Pre-Bid RFI Log

#### Description
Log of questions to the architect during bidding with cost exposure, status and the addendum that answered each.

#### Information to collect (ask the Chief Estimator before generating)
1. RFI cutoff date and the architect's contact?
2. Which questions were already resolved from the set?

#### Suggested template
Structure:
- **Log table** — id · date · sheet/section · question · cost exposure · priority · status · answer/addendum
- **Assumptions carried** — open CRITICAL items and the written assumption for each
- **Resolved from the set** — question and where the answer was found

Confirm the structure before generating.

#### File-generation prompt
```
Create the Pre-Bid RFI Log for {{project_name}} (bid {{bid_date}}), Blackland Commercial Builders preconstruction.
Every quantity cites sheet id + revision; every price cites a cost-library row; every open question carries a cost exposure.
Output as a markdown document with the sections listed above; tables where the section is tabular.
```
