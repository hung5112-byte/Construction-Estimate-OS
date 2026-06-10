---
type: project-doc
project: AMG
section: rma
tags: [demo, synthetic, rma, service]
last_updated: 06/10/2026
---
# AMG-100 — RMA & Depot Readiness (+ TS-90 baseline dashboard)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: Carlos Mendez · Dept: [[01-Departments/05-service-operations/index|Service Operations]] · Depot: Fort Worth, TX

## TS-90 Current Dashboard (the baseline AMG must beat)
| KPI | May 2026 | Target | Trend |
|---|---|---|---|
| Fleet AFR (annualized) | 3.1% | — | flat |
| RMA receipts / month | 1,067 | — | +4% (fleet aging) |
| Depot TAT (dock-to-dock) | 2.1 days | ≤ 3 | 🟢 |
| First-time-fix rate | 91% | ≥ 90% | 🟢 |
| NTF (no trouble found) | 14% | ≤ 10% | 🔴 — triage script update in work |
| Repair cost / unit | $31.40 | ≤ $35 | 🟢 |
| Refurb (TS-90R) output / month | 720 | demand-driven | 🟢 |

TS-90 failure pareto feeds AMG design → [[mtbf-prediction]] (connector 28%, display 22%, battery 18%, USB board 12%, liquid 11%)

## AMG-100 RMA Flow (designed, live at MP)
```
Restaurant site → ops portal claim (SN + fault code from on-device diag)
  → advance-exchange unit ships same day from DC pool (target: site down < 24 h)
  → failed unit to Fort Worth depot → triage (auto diag script, 8 min)
  → FRU repair (< 12 min for top-5) → test (mini-FCT) → refurb pool
  → weekly FA pareto → quality data lake → ORT/design feedback loop
```
Key upgrade vs TS-90: **on-device diagnostic code** at claim time (FW 1.0.0 feature) — attacks the 14% NTF problem; target NTF ≤ 6% on AMG.

## Depot Readiness Plan (MP gate items)
| Item | Status | Due |
|---|---|---|
| FRU repair SOPs (top-5: display, battery, main PCBA, SP-30, USB-C board) | 2 of 5 verified < 12 min on EVT teardowns → [[mechanical-design]] | all 5 by PVT |
| **PCI-compliant SP-30 handling**: tamper-evident bags, key re-injection room (dual-control), chain-of-custody log | Room spec'd; build-out Aug | 09/30 |
| Mini-FCT depot test rack (subset of [[test-stations]] stations 4/7/8/9/11) | Quote $38k, order 07/01 | 10/15 |
| FRU seed stock from PVT build: 60 kits (display 20, battery 60, PCBA 15, SP-30 10, USB-C 40) | Allocated in [[build-plan]] | PVT |
| Advance-exchange pool sizing: 1.5% of fleet month 1 → 375 units by M3 | From [[mtbf-prediction]] AFR curve | M1 |
| +1 depot tech (AMG adds ~400 RMA/yr steady-state) | In [[00-Brain/headcount\|headcount]] gaps | Q1 FY27 |
| Warranty terms: 2-yr standard, advance-exchange SLA next-business-day | Contract template w/ legal* | 08/01 |

*General information only — warranty/SLA language to be confirmed with a licensed Texas attorney.

## AMG Projected RMA Economics
| Element | Value |
|---|---|
| Yr-1 RMA volume @ 1.7% AFR, 25k fleet | ~425 units |
| Repair cost target / unit | $26 (FRU design + diag code) |
| Advance-exchange freight (2-way) | $14.20 |
| Refurb recovery value | ~$118/unit back to pool |
