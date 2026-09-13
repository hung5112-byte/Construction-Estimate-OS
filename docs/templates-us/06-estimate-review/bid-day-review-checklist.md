# Bid-Day Review Checklist

#### Description
The 16-point gate run by a reviewer other than the lead estimator, 24 hours before the bid, with pass/fail per item and the verdict.

#### Information to collect (ask the Chief Estimator before generating)
1. Who is the lead estimator (excluded as reviewer)?
2. Bid form, addenda list and bond form available?

#### Suggested template
Structure:
- **Hard gates** — sheets claimed · provenance · coverage vs spec · arithmetic · units · $/SF band · CRITICAL RFIs · scale gate · confidence floor
- **Bid-day items** — sub bids real · exclusions reconciled · allowances verbatim · alternates labeled · unit prices consistent · GC duration current · markups per matrix · addenda acknowledged · bond and insurance current
- **Verdict** — APPROVE / REVISE with blockers, owners and conditions

Confirm the structure before generating.

#### File-generation prompt
```
Create the Bid-Day Review Checklist for {{project_name}} (bid {{bid_date}}), Blackland Commercial Builders preconstruction.
Every quantity cites sheet id + revision; every price cites a cost-library row; every open question carries a cost exposure.
Output as a markdown document with the sections listed above; tables where the section is tabular.
```
