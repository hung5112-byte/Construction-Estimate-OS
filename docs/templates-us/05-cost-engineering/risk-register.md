# Risk Register

#### Description
Bottom-up risk register with probability × impact per risk, expected value, contingency reconciliation and escalation basis.

#### Information to collect (ask the Chief Estimator before generating)
1. Declared estimate class?
2. Open CRITICAL RFIs and their exposure?

#### Suggested template
Structure:
- **Register** — risk · trade/phase · probability · impact · EMV · owner · response
- **Contingency reconciliation** — class default vs EMV, justification
- **Escalation** — index, value, date, mid-point
- **Draw authority**

Confirm the structure before generating.

#### File-generation prompt
```
Create the Risk Register for {{project_name}} (bid {{bid_date}}), Blackland Commercial Builders preconstruction.
Every quantity cites sheet id + revision; every price cites a cost-library row; every open question carries a cost exposure.
Output as a markdown document with the sections listed above; tables where the section is tabular.
```
