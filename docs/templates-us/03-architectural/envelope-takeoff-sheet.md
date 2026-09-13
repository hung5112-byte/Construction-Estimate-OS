# Envelope Takeoff Sheet

#### Description
Roofing, insulation, cladding, storefront/curtain wall, flashing and accessories by system from elevations, sections and the roof plan.

#### Information to collect (ask the Chief Estimator before generating)
1. Roof system, R-value, warranty from 07 sections?
2. Cladding systems per elevation?

#### Suggested template
Structure:
- **Roofing** — SQ · insulation by thickness · taper volume · penetrations · drains · coping LF
- **Walls** — system · SF (openings > 10 SF deducted) · flashing LF · sheet
- **Glazing** — storefront/curtain wall SF by elevation · entrance leaves · windows by mark
- **Questions**

Confirm the structure before generating.

#### File-generation prompt
```
Create the Envelope Takeoff Sheet for {{project_name}} (bid {{bid_date}}), Blackland Commercial Builders preconstruction.
Every quantity cites sheet id + revision; every price cites a cost-library row; every open question carries a cost exposure.
Output as a markdown document with the sections listed above; tables where the section is tabular.
```
