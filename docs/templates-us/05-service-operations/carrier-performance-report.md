# P-SVC-03: Carrier Performance Report

#### Description
The quarterly scorecard for parcel and freight carriers — on-time performance, damage/loss, claim recovery, and cost per shipment by lane. The data that turns carrier selection from habit into a decision.

#### Information to collect (ask the user before generating)
1. Carriers and service levels in use? (parcel, LTL, international forwarders)
2. Lanes that matter? (factory→US, warehouse→customers, RMA returns)
3. Data sources? (shipment logs, claims records, invoices)
4. Targets? (on-time %, damage rate, claim recovery %)
5. Output format? (.xlsx recommended)

#### Suggested template
Structure (.xlsx):
- **Sheet "Scorecard"**: per carrier/service — shipments, on-time %, damage/loss rate,
  claims filed vs. recovered $, avg cost per shipment, invoice-accuracy spot-check
- **Sheet "Lanes"**: per lane — volume, transit-time distribution (promised vs. actual),
  cost trend, the carrier mix on that lane
- **Sheet "Claims"**: open claims log — shipment, value, evidence status, age, recovery
- **Sheet "Actions"**: underperformers with consequence (volume shift, rate renegotiation,
  removal from launch-critical lanes)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Carrier Performance Report workbook (.xlsx).

CONTEXT:
- Carriers: [list] — Lanes: [list] — Window: [quarter]
- Targets: [on-time %, damage rate, recovery %]

FORMAT (.xlsx):
- "Scorecard" per carrier; "Lanes" with promised-vs-actual transit
- "Claims" log with aging; "Actions" with consequences

RULES: damage claims require photo evidence at receipt (per the receiving SOP);
launch-critical lanes only use carriers above target; invoice spot-checks are
part of the score.
```

---
✍️ Author: Brian H. Doan
