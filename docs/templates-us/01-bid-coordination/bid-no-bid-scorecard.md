# Bid/No-Bid Scorecard

#### Description
Weighted go/no-go score for a bid invitation per 00-Brain/bid-policy.md, completed within 48 hours of the ITB.

#### Information to collect (ask the Chief Estimator before generating)
1. Owner and payment history?
2. Building type, size, location, delivery method?
3. Estimating bandwidth and PM/superintendent availability on the bid date?
4. Number of competing GCs and any incumbent?

#### Suggested template
Structure:
- **Project profile** — owner, type, GSF, delivery, bid date, RFI cutoff
- **Scorecard** — five weighted factors scored 1–5 with rationale
- **Decision** — pursue / judgment call / decline, signed by
- **Conditions** — what must be true to bid

Confirm the structure before generating.

#### File-generation prompt
```
Create the Bid/No-Bid Scorecard for {{project_name}} (bid {{bid_date}}), Blackland Commercial Builders preconstruction.
Every quantity cites sheet id + revision; every price cites a cost-library row; every open question carries a cost exposure.
Output as a markdown document with the sections listed above; tables where the section is tabular.
```
