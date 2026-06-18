---
type: project-doc
project: Cyber
section: rma
tags: [demo, synthetic, rma, service]
last_updated: 06/17/2026
---
# CY-80 — RMA & Depot Dashboard (live field data)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Carlos Mendez · Analyst: Sofia Ramirez · Dept: [[01-Departments/05-service-operations/index|Service Operations]] · Depot: Fort Worth, TX

## Fleet & RMA headline (06/2026)
| KPI | Value | Target | Trend |
|---|---|---|---|
| Active fleet | ~128k (134k shipped) | — | ↑ |
| **Field AFR (annualized)** | **3.9%** | ≤ 3.5% | ↓ (was 4.0%) 🟡 |
| RMA receipts / month | ~530 | — | flat |
| Warranty failures / mo | ~416 | — | ↓ |
| Accidental / out-of-warranty / mo | ~114 | — | flat |
| Depot TAT (dock-to-dock) | 2.4 days | ≤ 3 | 🟢 |
| First-time-fix rate | 93% | ≥ 90% | 🟢 |
| **NTF (no trouble found)** | 9% | ≤ 8% | 🟡 (FW 1.8 diag rolling) |
| Repair cost / unit | $33.80 | ≤ $36 | 🟢 |
| Refurb (CY-80R) output / mo | ~360 | demand-driven | 🟢 |
| Advance-exchange pool | ~2,560 (2% of fleet) | ≥ AE demand | 🟢 |

## RMA flow (live)
```
Store/chain → ops portal claim (SN + on-device diag code, FW 1.8)
  → advance-exchange unit ships same/next day from DC pool (site-down < 24 h SLA)
  → failed unit → Fort Worth depot → triage (auto diag script ~6 min)
  → capacity-grade step (battery) → FRU repair (top-5 < 14 min) → mini-FCT
  → refurb pool (CY-80R)  → weekly FA pareto → quality data lake → ECO/CAPA loop
```
Key lever: **on-device diagnostic code at claim** (FW 1.8) writes the fault before the unit ships — directly attacks the 9% NTF and the battery-fade "won't last a shift" complaints that aren't true failures → [[power-budget]].

## Failure pareto (rolling 6-mo, confirmed failures)
| # | Mode | Share | Status |
|---|---|---|---|
| 1 | Display crack (drop) | 27% | drop-education w/ chains; bumper durometer held |
| 2 | Battery (fade/swell/contact) | 18% | ECO-044; X-ray containment (ISS-CY-070) |
| 3 | Scan engine (haze/no-read) | 13% | ECO-039 closed; retrofit-on-RMA (ISS-CY-061) |
| 4 | USB-C / charging | 11% | ECO-031 closed |
| 5 | Touch / ghosting | 8% | FW 1.8 OTA (ISS-CY-066) |
| 6 | Payment (EMV/NFC) | 7% | wear FRU |
| 7 | Liquid ingress | 6% | spill-education |
| 8 | Audio | 4% | ISS-CY-073 sort |
| — | NTF / other | 6% | FW 1.8 diag |

Full analysis & glidepath → [[field-reliability-report]] · model → [[mtbf-afr-model]]

## Depot readiness (steady state)
| Item | Status |
|---|---|
| Top-5 FRU SOPs (display, battery, scan, USB-C, PCBA) | ✅ all ≤ target swap time → [[mechanical-design]] |
| PCI-compliant payment-module handling (dual-control room) | ✅ live, audited |
| Mini-FCT depot rack (stations 3/4/5/7/8) | ✅ → [[test-stations]] |
| FRU stock (rolling 8-wk) | 🟢 scan-engine FRU on single-source watch (R-02) |
| Q4 refurb pre-stage (+400 CY-80R) | 🟡 building (R-06) |

## RMA economics (Year 2)
| Element                                   | Value                   |
| ----------------------------------------- | ----------------------- |
| Y2 warranty RMA volume @ 3.9% AFR         | ~5,000 units            |
| Repair cost / unit                        | $33.80                  |
| Advance-exchange freight (2-way)          | $13.60                  |
| Refurb recovery value                     | ~$122/unit back to pool |
| Battery-only swap (vs full repair) saving | ~$19/unit               |
