# P-SCM-02: Shortage Escalation Plan

#### Description
A decision framework for component shortages — early-warning signals, a ranked option table (expedite / alternate / broker / redesign), authenticity controls for broker buys, and clear escalation levels with owners. Replaces panic with a playbook.

#### Information to collect (ask the user before generating)
1. Which parts are currently critical/sole-source?
2. Build plan at risk (line-down date if unresolved)?
3. Approved alternates documented in the BOM/AVL?
4. Broker policy — allowed at all? With what inspection?
5. Who can approve premium costs, and up to what amount?

#### Suggested template
Structure:
- **Early warning**: signals that trigger this plan (decommit, lead-time push,
  allocation notice, EOL announcement) and who watches them
- **Impact statement**: parts, builds affected, line-down date, customer impact
- **Option table**: per option — recovery date, cost delta, risk, decision owner
  (expedite at supplier / approved alternate via ECO / broker with authenticity
  testing / partial build / redesign)
- **Broker controls**: authorized brokers only, traceability docs, inspection/
  test protocol with Quality before stock release
- **Escalation levels**: L1 buyer (≤$X), L2 division manager (≤$Y), with
  time-boxes — a shortage older than N days auto-escalates
- **Post-mortem**: root cause of the shortage (planning, supplier, design) and
  the prevention action

Confirm the structure before generating.

#### File-generation prompt
```
Create a Shortage Escalation Plan.

CONTEXT:
- Critical parts: [list or "template"] — Line-down exposure: [date/build]
- Broker policy: [allowed with controls / not allowed]
- Approval limits: [L1 $X / L2 $Y]

FORMAT:
- Trigger list; impact-statement template
- Option table format (option, date, cost Δ, risk, owner)
- Broker authenticity-control checklist
- Escalation ladder with time-boxes; post-mortem template

TONE: decision-oriented. LENGTH: 2-3 pages.
```

---
✍️ Author: Brian H. Doan
