# P-HWE-02: Component Selection Record

#### Description
A decision record for selecting a critical component — the electrical justification plus the supply-side reality (lifecycle, sources, lead time, cost). Prevents the classic failure: a technically perfect part that can't be bought next year.

#### Information to collect (ask the user before generating)
1. Component function and the candidate parts considered?
2. Why is it critical? (sole-source risk, long lead, cost driver, cert-relevant)
3. Lifecycle status of each candidate? (active / NRND / EOL) [verify with distributor data]
4. Alternates identified? Drop-in or requires layout/firmware change?
5. Volume and target cost?

#### Suggested template
Structure:
- **Requirement**: electrical/mechanical/firmware requirements the part must meet
- **Candidates table**: part, manufacturer, key specs vs. requirement, lifecycle,
  sources (count), lead time, MOQ, unit cost at volume
- **Supply assessment**: second source available? broker exposure? region risk
- **Decision**: selected part + why; alternates approved for the AVL (drop-in vs. ECO-required)
- **Risk & mitigation**: what breaks if this part disappears; exit plan
- **Handoffs**: AVL update (BOM/ECO/PLM), buy plan (sourcing), qualification need (supplier quality)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Component Selection Record.

CONTEXT:
- Function: [what the part does] — Product(s): [models]
- Candidates: [list] — Volume: [units/yr] — Target cost: [$]

FORMAT:
- Requirements list; candidates comparison table (specs, lifecycle, sources,
  lead time, MOQ, cost)
- Supply assessment paragraph; decision with approved alternates
- Risk/exit plan; handoff list (AVL, sourcing, qualification)

RULES: a sole-source selection must state the exit plan explicitly;
lifecycle status must carry a verification date [verify with distributor].
```

---
✍️ Author: Brian H. Doan
