# Sheet Register

#### Description
Document-control log of every drawing sheet with number, title, discipline, scale, revision, date, addenda and vector/scanned status; the scale gate lives here.

#### Information to collect (ask the Chief Estimator before generating)
1. Which addenda have been received and when?
2. Is the cover-sheet index available?

#### Suggested template
Structure:
- **Register table** — sheet · title · discipline · type · scale · rev · date · size · vector
- **Completeness** — index vs package: missing, extra, duplicates, superseded
- **Gates** — sheets without a parsable scale; scanned sheets
- **Addenda log** — number, date, sheets and sections affected

Confirm the structure before generating.

#### File-generation prompt
```
Create the Sheet Register for {{project_name}} (bid {{bid_date}}), Blackland Commercial Builders preconstruction.
Every quantity cites sheet id + revision; every price cites a cost-library row; every open question carries a cost exposure.
Output as a markdown document with the sections listed above; tables where the section is tabular.
```
