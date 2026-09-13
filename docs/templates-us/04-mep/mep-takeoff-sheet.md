# MEP Takeoff Sheet

#### Description
Equipment by tag, ductwork by weight, piping by size, fixtures each, gear by kVA, fixtures/devices each and low-voltage boundary, schedules first.

#### Information to collect (ask the Chief Estimator before generating)
1. Which MEP schedules exist (equipment, fixture, panel, one-line)?
2. Sprinkler designed or design-build; flow test available?

#### Suggested template
Structure:
- **HVAC** — tag · type · capacity · electrical · duct lb · piping LF · air devices · controls scope
- **Plumbing/FP** — fixtures each · pipe LF by system/size · equipment · heads by hazard
- **Electrical/LV** — service · gear · panels · feeders · fixtures · devices · conduit/wire LF · FA devices · LV boundary
- **Cross-trade ties** — units vs connections, panels vs feeders
- **Questions**

Confirm the structure before generating.

#### File-generation prompt
```
Create the MEP Takeoff Sheet for {{project_name}} (bid {{bid_date}}), Blackland Commercial Builders preconstruction.
Every quantity cites sheet id + revision; every price cites a cost-library row; every open question carries a cost exposure.
Output as a markdown document with the sections listed above; tables where the section is tabular.
```
