# Interiors Takeoff Sheet

#### Description
Partitions by type, ceilings by RCP type, flooring/base/wall finishes by room and paint by substrate, tied to the finish schedule.

#### Information to collect (ask the Chief Estimator before generating)
1. Partition types and heights?
2. Finish schedule available?

#### Suggested template
Structure:
- **Partitions** — type · LF · height · SF per side · sheet
- **Ceilings** — type · SF · height · sheet
- **Finishes by room** — room · floor · base · walls · ceiling · SF
- **Openings** — door mark · type · rating · hardware set · frame
- **Questions**

Confirm the structure before generating.

#### File-generation prompt
```
Create the Interiors Takeoff Sheet for {{project_name}} (bid {{bid_date}}), Blackland Commercial Builders preconstruction.
Every quantity cites sheet id + revision; every price cites a cost-library row; every open question carries a cost exposure.
Output as a markdown document with the sections listed above; tables where the section is tabular.
```
