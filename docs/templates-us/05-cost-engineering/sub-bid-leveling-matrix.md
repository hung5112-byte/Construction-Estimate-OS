# Sub-Bid Leveling Matrix

#### Description
Scope matrix per trade with each bidder's inclusions, exclusions, plugs with provenance, leveled totals, outlier flags and the recommended bidder.

#### Information to collect (ask the Chief Estimator before generating)
1. Quotes received per trade with addenda acknowledged?
2. Scope sheet per trade?

#### Suggested template
Structure:
- **Matrix** — scope item · bidder A/B/C · plug source
- **Leveled totals and outliers**
- **Recommendation** — lowest responsible bidder and what to clarify in writing
- **Gaps/overlaps across packages**

Confirm the structure before generating.

#### File-generation prompt
```
Create the Sub-Bid Leveling Matrix for {{project_name}} (bid {{bid_date}}), Blackland Commercial Builders preconstruction.
Every quantity cites sheet id + revision; every price cites a cost-library row; every open question carries a cost exposure.
Output as a markdown document with the sections listed above; tables where the section is tabular.
```
