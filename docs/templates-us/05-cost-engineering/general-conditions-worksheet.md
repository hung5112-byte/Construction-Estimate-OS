# General Conditions Worksheet

#### Description
Duration-driven general conditions: staff by role and months, temporary facilities and controls, safety, testing, cleaning, equipment, permits.

#### Information to collect (ask the Chief Estimator before generating)
1. Contract duration and phasing from the bid form / 01 10 00?
2. Temporary facilities required by 01 50 00?

#### Suggested template
Structure:
- **Staffing** — role · months · burdened rate · total
- **Temporary facilities** — item · qty · months · rate · total
- **Other Division 01** — layout, testing, cleaning, closeout, permits
- **Sanity** — % of direct cost vs 8–15% band

Confirm the structure before generating.

#### File-generation prompt
```
Create the General Conditions Worksheet for {{project_name}} (bid {{bid_date}}), Blackland Commercial Builders preconstruction.
Every quantity cites sheet id + revision; every price cites a cost-library row; every open question carries a cost exposure.
Output as a markdown document with the sections listed above; tables where the section is tabular.
```
