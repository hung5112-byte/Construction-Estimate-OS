# P-NPI-06: Supplier Negotiation Brief

#### Description
The prep sheet for a supplier or ODM negotiation — our position, their position, the walk-away line, and the total-landed-cost math. Negotiations are won in preparation; this is the preparation.

#### Information to collect (ask the user before generating)
1. Supplier and what's being negotiated? (price, MOQ, lead time, NCNR terms, capacity commitment, MSA renewal)
2. Our volumes and forecast confidence?
3. Their leverage vs. ours? (alternatives qualified? switching cost? their dependence on us)
4. Current terms and the target?
5. Who attends and who decides?

#### Suggested template
Structure:
- **Objective**: what we must get, what we'd like to get, what we'll trade
- **Position table**: term (price/MOQ/LT/payment/NCNR/capacity), current, target, walk-away
- **Total landed cost view**: unit price is not the number — show freight, duty, MOQ carrying cost per option [inputs from logistics]
- **Leverage analysis**: our alternatives (qualified? time-to-switch?), their alternatives, deadlines on both sides
- **Their likely asks** and our prepared responses
- **Concession ladder**: what we give first, what never
- **Decision rights**: who can agree to what in the room; escalation line to the VP
- **Follow-up**: terms go into the PO/MSA in writing [contract terms — verify with attorney]

Confirm the structure before generating.

#### File-generation prompt
```
Create a Supplier Negotiation Brief.

CONTEXT:
- Supplier: [name] — Subject: [terms at stake] — Volumes: [units/yr]
- Current vs. target: [summary] — Attendees/decider: [names]

FORMAT:
- Objective tiering; position table with walk-away column
- Landed-cost comparison; leverage analysis; anticipated asks + responses
- Concession ladder; decision-rights note; written-follow-up rule

RULES: every position has a walk-away; the landed-cost view accompanies any
price discussion; nothing agreed verbally is real until written.
```

---
✍️ Author: Brian H. Doan
