---
type: project-doc
project: AMG
section: pm
tags: [demo, synthetic, minutes]
last_updated: 06/05/2026
---
# AMG Core Team — Weekly Minutes 06/05/2026

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Chair: Sarah Whitfield · 14 attendees (Kevin Tran + Omar Haddad via video from Bac Ninh)

## Program health: 🟢 Green — DVT build 06/22 on track, 17 days out

## Decisions made
1. **DVT build proceeds 06/22 even if ISS-014 rework parts slip past 06/16**: fallback approved — build first 40 units without metal trim, rework at line side when parts land. (Owner: Kevin Tran)
2. EQ notch FW workaround for ISS-027 speaker buzz approved for alpha-trial units only; mechanical fix remains the DVT closure path.
3. Field trial site list locked: 12 DFW-area restaurants (fictional list with ops team), install week of 09/08 using DVT units.

## Workstream updates
- **EE (David):** DVT PCB rev B released to fab 06/02, arrives BrightPath 06/13. Shield can + ferrite for ISS-025 included. Pre-scan #2 booked 07/14 at Pinnacle.
- **RF (Elena):** Antenna re-match validated on 3 hand-modified EVT units: 5 GHz throughput back to −2% vs reference. Rework kits (200×) ship 06/12 from connector vendor, ETA 06/16. ⚠️ 3-day buffer.
- **ME (Miguel/Janet):** T1 mod for ISS-023 rib verified with 10-shot sample — no sink marks. Dock T0 on 06/30 holds. Speaker foam gasket samples at BrightPath.
- **FW (Anna):** v0.9.0 cut for DVT: roam fix params (ISS-032), NovaPay retry logic. NovaPay v2.1.4 still promised 06/20 — escalation letter ready if it slips (ISS-028).
- **Quality (Rachel):** DVT PRT plan signed → [[prt-plan]]. Atlas pre-assessment docs submitted 06/03 (R-01). DVT FAI checklist agreed with BrightPath IQC.
- **SQE (James):** Veltron 8D at D6 — permanent fix (electrolyte line filter + lot CT sampling) audit scheduled 06/26 → [[capa-8d-AMG-26-004]]. DynaCell qual lot ships 06/30.
- **Sourcing (Linda):** eMMC: Kioxia confirmed allocation through Dec; SanDisk iNAND samples at EE. Broker quote on file (+$2.10/unit worst case) (ISS-030).
- **Ops/Service (Carlos):** Depot FRU list v2 drafted from EVT teardown — 5 FRUs, target < 12 min swap verified on 2. → [[rma-process-dashboard]]

## Actions (new)
| # | Action | Owner | Due |
|---|---|---|---|
| A-118 | Daily tracking on antenna rework kit shipment, escalate if no AWB by 06/12 EOD | Elena | 06/12 |
| A-119 | CCB pre-read for potential broker eMMC buy ($30k cap) | Linda | 06/18 |
| A-120 | Alpha trial week-3 data summary to core team | Anna | 06/12 |
| A-121 | DVT build readiness review (BRR) deck — line slot 06/22 | Kevin | 06/17 |
| A-122 | Confirm UL sample config matches DVT rev B (avoid retest) | Rachel | 06/13 |

## Next meeting: 06/12/2026 — DVT Build Readiness Review (extended, 2 h)
