---
type: project-doc
project: Cyber
section: fulfillment
tags: [demo, synthetic, logistics]
last_updated: 06/17/2026
---
# CY-80 — Logistics & Fulfillment

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Carlos Mendez · Dept: [[01-Departments/05-service-operations/index|Service Operations]]
> General information only — customs/trade classification and any contracts to be confirmed with a licensed customs broker / attorney.

## Lanes
| Lane | Mode | Transit | Use |
|---|---|---|---|
| Meridian Penang → Fort Worth DC | Ocean (40HQ) | ~24 days | base replenishment |
| Meridian Penang → Fort Worth DC | Air (peak/expedite) | ~5 days | Q4 peak, shortages |
| Fort Worth DC → chain DCs / stores | Ground (LTL/parcel) | 1–4 days | deployment |
| Advance-exchange pool → store | Parcel NBD | < 24 h | RMA SLA → [[rma-dashboard]] |

## Origin & trade
- Origin **Malaysia (Penang)** maintained for tariff position; documentation current (R-07)
- HTS classification on file; dormant China surge line qualified but unused
- Freight contract locked FY26; peak air budget reserved

## Inventory posture
| Node | Target | Note |
|---|---|---|
| Fort Worth DC finished goods | 4–6 wk | base + Q4 build-ahead buffer |
| Advance-exchange pool | 2% of fleet (~2,560) | refurb + new blend → R-06 |
| Scan-engine / UFS safety stock | 8 wk | single-source / allocation cover (R-02/R-04) |

## Peak plan (Q4 retail)
- Build-ahead from Aug; +4k buffer at Fort Worth before Oct
- Air-freight trigger defined if ocean ETA risks store-rollout dates
- Refurb pre-stage +400 CY-80R (R-06)

## Open actions
1. Confirm Q4 air-freight reservation + budget (Carlos, Jul)
2. Re-validate HTS/origin docs ahead of any tariff change (Daniel, ongoing)
