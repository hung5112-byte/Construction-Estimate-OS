# P-SVC-06: Customs Entry Audit Checklist

#### Description
The periodic self-audit of customs entries filed by the broker — classification, valuation, origin, and special-program claims spot-checked against source documents. Brokers file what they're given; the importer of record owns the penalties. [Customs rules change — verify findings with a licensed customs broker / trade counsel.]

#### Information to collect (ask the user before generating)
1. Audit window and entry volume? (e.g. quarterly, sample N entries or all)
2. Origins/lanes in scope? (China, Vietnam, Mexico inbound; RMA re-imports)
3. Special programs claimed? (USMCA, Section 301 exclusions, duty drawback, returned-goods provisions)
4. Document sources? (broker entry summaries/7501s, commercial invoices, our POs)
5. Prior findings to re-check?

#### Suggested template
Structure:
- **Sample table**: entry #, date, origin, product, value, duty paid
- **Per-entry checks**: HTS code matches our classification record [verify with broker];
  valuation matches the commercial invoice and PO (assists/tooling included where required);
  country of origin consistent with the build site; special-program claims documented
  (USMCA certs on file, exclusion numbers valid); RMA re-imports used the right provision
- **Findings table**: entry, issue, exposure estimate, corrective action
  (prior-disclosure consideration → trade counsel [verify]), broker feedback item
- **Systemic checks**: classification database current with new products/ECOs;
  broker SOP current; UN38.3/DG paperwork for battery shipments on file
- **Verdict & follow-up**: clean / findings with actions; next audit date

Confirm the structure before generating.

#### File-generation prompt
```
Create a Customs Entry Audit Checklist.

CONTEXT:
- Window: [quarter] — Sample: [n entries] — Origins: [lanes]
- Programs claimed: [USMCA/301 exclusions/drawback] — Prior findings: [list]

FORMAT:
- Sample table; per-entry check sections (classification, valuation, origin,
  programs, RMA re-imports); findings with exposure + actions
- Systemic checks; verdict + next audit date

RULES: findings with duty exposure go to the broker AND trade counsel
[verify before any disclosure decision]; the classification database is part
of every audit; battery DG paperwork is checked every cycle.
```

---
✍️ Author: Brian H. Doan
