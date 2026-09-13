# Basis of Estimate

#### Description
AACE 34R-05-style record of scope, class, method, data sources, benchmarks, assumptions and exclusions behind the estimate.

#### Information to collect (ask the Chief Estimator before generating)
1. Declared AACE class and accuracy band?
2. Cost data sources used and their dates?

#### Suggested template
Structure:
- **Scope and class** — building, GSF, delivery, class, accuracy band
- **Method** — takeoff approach by discipline, provenance rules, tools
- **Data sources** — cost library rows, published data, indices with dates
- **Benchmarks** — comparables and position
- **Assumptions and exclusions**
- **Review** — scorecard summary and conditions

Confirm the structure before generating.

#### File-generation prompt
```
Create the Basis of Estimate for {{project_name}} (bid {{bid_date}}), Blackland Commercial Builders preconstruction.
Every quantity cites sheet id + revision; every price cites a cost-library row; every open question carries a cost exposure.
Output as a markdown document with the sections listed above; tables where the section is tabular.
```
