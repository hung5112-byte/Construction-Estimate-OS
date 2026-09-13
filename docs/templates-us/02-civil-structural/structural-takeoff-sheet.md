# Structural Takeoff Sheet

#### Description
Concrete, masonry and steel quantities by element with schedule references, waste factors and sanity ratios.

#### Information to collect (ask the Chief Estimator before generating)
1. Concrete strengths, rebar grade, steel spec from S0 notes?
2. Geotech bearing, rock and groundwater findings?

#### Suggested template
Structure:
- **Concrete** — element · CY · SFCA · lb rebar · SF finish · sheet
- **Masonry** — wall type · SF · units · grout CY · reinforcing · sheet
- **Steel** — mark · section · length · qty · lb · tons · sheet
- **Sanity** — steel psf, rebar lb/CY, CY per SF
- **Questions**

Confirm the structure before generating.

#### File-generation prompt
```
Create the Structural Takeoff Sheet for {{project_name}} (bid {{bid_date}}), Blackland Commercial Builders preconstruction.
Every quantity cites sheet id + revision; every price cites a cost-library row; every open question carries a cost exposure.
Output as a markdown document with the sections listed above; tables where the section is tabular.
```
