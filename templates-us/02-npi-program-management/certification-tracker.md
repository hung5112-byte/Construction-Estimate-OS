# P-QC-01: Certification Tracker

#### Description
The certification matrix for every product — which approvals are required (PCI PTS, EMVCo, FCC, UL/safety, CE, others), which are held, expiration/renewal dates, and which pending ECOs could impact them. The single source of truth that prevents lapsed-cert stop-ships.

#### Information to collect (ask the user before generating)
1. Products and target markets? (markets drive the required set)
2. Payment functionality? (PCI PTS / EMVCo scope)
3. RF content? (FCC authorization path)
4. Currently held certificates with numbers and dates?
5. Pending design changes (ECOs) on certified products?

#### Suggested template
Structure (matrix: product × certification):
- **Required set per product**: certification, scheme/standard version, mandatory
  vs. customer-required, market
- **Status**: held (cert #, issue/expiry date, lab) / in progress (stage, ETA) /
  gap (risk, plan)
- **Renewal calendar**: next 12 months of expirations with lead-time-adjusted
  start dates [UNCERTAIN — scheme versions and renewal rules change; verify with
  the lab/scheme]
- **Change watch**: open ECOs against certified products with impact verdicts
- **Evidence index**: where each test report/approval letter lives

Confirm the structure before generating.

#### File-generation prompt
```
Create a Certification Tracker workbook (.xlsx).

CONTEXT:
- Products: [models + markets] — Payment scope: [PCI PTS/EMVCo or none]
- RF: [yes/no] — Held certs: [list with dates]

FORMAT (.xlsx):
- Sheet "Matrix": product × certification grid with status color coding
- Sheet "Detail": one row per certificate (scheme, version, number, lab,
  issue/expiry, evidence link)
- Sheet "Renewals": 12-month calendar with start-by dates
- Sheet "ECO watch": open changes vs. certified products with impact verdicts

RULES: every expiring mandatory cert within lead time is flagged RED;
every ECO row needs a written impact verdict before approval.
```

---
✍️ Author: Brian H. Doan
