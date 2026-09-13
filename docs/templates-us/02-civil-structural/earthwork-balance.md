# Earthwork Balance

#### Description
Cut, fill, import/export in bank/loose/compacted cubic yards with the swell and shrink factors and the geotech citation.

#### Information to collect (ask the Chief Estimator before generating)
1. Grading plan and geotech report available?
2. Topsoil strip depth and select fill spec?

#### Suggested template
Structure:
- **Volumes** — cut BCY · fill CCY · factors · import/export
- **Utilities** — run · size · material · LF · depth range · structures
- **Paving** — section · SF · curbs LF
- **Assumptions and questions**

Confirm the structure before generating.

#### File-generation prompt
```
Create the Earthwork Balance for {{project_name}} (bid {{bid_date}}), Blackland Commercial Builders preconstruction.
Every quantity cites sheet id + revision; every price cites a cost-library row; every open question carries a cost exposure.
Output as a markdown document with the sections listed above; tables where the section is tabular.
```
