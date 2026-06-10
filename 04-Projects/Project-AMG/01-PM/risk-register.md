---
type: project-doc
project: AMG
section: pm
tags: [demo, synthetic, risk]
last_updated: 06/10/2026
---
# Project AMG — Risk Register

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Score = Probability (1-5) × Impact (1-5)

| ID | Risk | P | I | Score | Owner | Mitigation | Status |
|---|---|---|---|---|---|---|---|
| R-01 | PCI PTS v6.2 pre-assessment (07/06) finds hardware change → PVT slips 4–6 wks | 2 | 5 | 🔴 10 | Rachel Adeyemi | NovaPay SP-30 pre-certified module; tamper mesh review done by Atlas 05/28; design frozen around secure boundary | Open — review 07/10 |
| R-02 | ISS-014 antenna rework parts late for DVT build 06/22 (arrive 06/16, 3-day buffer) | 2 | 4 | 🟡 8 | Elena Rodriguez | Air freight, dual connector vendors quoted; fallback = build 40 units without trim, rework later | Open — tracking daily |
| R-03 | Veltron battery recurrence; DynaCell 2nd source not qualified by PVT | 2 | 4 | 🟡 8 | James Park | DynaCell qual lot at cell CT 06/30; 100% lot X-ray at BrightPath incoming until PVT | Open |
| R-04 | eMMC allocation Q4 (ISS-030) — coverage only through ramp month 2 | 3 | 3 | 🟡 9 | Linda Gomez | SanDisk iNAND second source EE-qual in DVT; broker buy pre-approved up to $30k premium | Open |
| R-05 | EMC formal fail (ISS-025 pre-scan margin 1.2 dB over) | 2 | 4 | 🟡 8 | David Chen | Shield can + ferrite cut into DVT; pre-scan #2 booked 07/14 at lab before formal | Open |
| R-06 | DVT FPY < 85% blocks PRT sample flow | 2 | 3 | 🟢 6 | Omar Haddad | EVT pareto fixes in test plan: touch cal v2, Wi-Fi golden-unit cal → [[factory-yield-evt]] | Open |
| R-07 | BrightPath Tet shutdown (2 wks, Feb 2027) inside ramp month 3 | 4 | 2 | 🟡 8 | Kevin Tran | Pre-build +6k units in Jan 2027; safety stock at Fort Worth DC | Planned |
| R-08 | Dock AMG-D10 tooling (T0 06/30) slips — printer mech tolerance stack | 3 | 2 | 🟢 6 | Janet Liu | Dock is launch-decoupled; tablet ships standalone wave 1 if needed | Open |
| R-09 | Single RF engineer (bus factor) during antenna campaign | 2 | 3 | 🟢 6 | Brian H. Doan | Contract RF consultant on retainer from 07/01; cross-train Marcus | Mitigating |
| R-10 | Field trial (Sept) surfaces UX/reliability issue too late for PVT | 2 | 4 | 🟡 8 | Sarah Whitfield | 3-site alpha with 24 EVT units already running since 05/26 — early signal | Mitigating |

## Retired risks
| ID | Risk | Outcome |
|---|---|---|
| R-00a | ODM EMV line capability unproven | Closed 03/10 — BrightPath line audit passed, 2 findings minor → [[01-Departments/04-mfg-supplier-quality/index\|MSQ]] |
| R-00b | Display GFF lamination yield at 13.3" | Closed 05/02 — supplier yield 96.5% at EVT, OK |
