# P-RMA-03: Refurbishment Standard

#### Description
The standard that defines when a returned device may be refurbished and what "refurbished" means — cosmetic grading, functional test requirements, data sanitization, re-provisioning, and labeling. Protects both the brand and the customer.

#### Information to collect (ask the user before generating)
1. Product families eligible for refurbishment?
2. Cosmetic grades used? (e.g. A: like-new / B: light wear / C: parts-only)
3. Refurbished units sold, redeployed, or used as warranty replacements?
4. Data/keys on devices? (storage to wipe, certificates/keys to re-inject)
5. Warranty offered on refurbished units?

#### Suggested template
Structure:
- **Eligibility**: which returns qualify (failure class, age, revision currency —
  units below minimum revision get updated or scrapped)
- **Cosmetic grading**: photo-anchored criteria per grade, gradeable surfaces
- **Functional standard**: full production test pass required — same criteria as
  new, including provisioning/firmware to current released version
- **Data sanitization**: wipe/reset procedure, key/certificate handling for
  secure devices [verify scheme rules for payment devices — re-keying may be
  restricted]
- **Identity**: refurb labeling, serial retention, refurb count tracking
- **Release**: QC check, packaging standard, stock category (refurb ≠ new)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Refurbishment Standard document.

CONTEXT:
- Products: [families] — Grades: [A/B/C definitions]
- Use of refurbs: [sale/redeploy/warranty] — Refurb warranty: [terms]
- Secure/payment device: [yes/no]

FORMAT:
- Eligibility rules table; cosmetic grading rubric (per surface, per grade)
- Functional test requirement (= production criteria + current firmware)
- Data sanitization & key-handling procedure
- Labeling/serialization rules; stock category rules
- QC release checklist

TONE: standard/spec language. LENGTH: 2-3 pages.
```

---
✍️ Author: Brian H. Doan
