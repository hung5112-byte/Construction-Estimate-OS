---
type: project-doc
project: Cyber
section: production
tags: [demo, synthetic, production]
last_updated: 06/17/2026
---
# CY-80 — Production Plan & Capacity (100k/yr)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Wei Lim / Hassan Ali · Dept: [[01-Departments/04-mfg-supplier-quality/index|Mfg & Supplier Quality]] · Site: Meridian EMS, Penang

## Volume plan
| Period | Plan | Actual |
|---|---|---|
| Year 1 (02/2025–01/2026) | 95k | **92.4k** (ramp + Q3 component gap) |
| Year 2 (02/2026–01/2027) | 100k | 41.8k YTD (on plan) |
| Run rate | ~8,300/mo | 8,410 (May) 🟢 |
| Q4 retail peak (Oct–Dec) | +15% (~9,600/mo) | build-ahead from Aug |

## Mix
| SKU | Share | Note |
|---|---|---|
| CY-80 (Wi-Fi) | 78% | base retail/QSR |
| CY-80L (LTE) | 17% | mobile / curbside |
| CYS-10 cradle | (accessory) | ~1 per 4 devices |
| CY-80R (refurb) | service pool | depot output → [[rma-dashboard]] |

## Capacity posture
- 2 SMT + 3 assembly/test lines; nominal 8.3k/mo, peak 11k/mo with 3rd line
- **Q4 build-ahead**: pre-build ~4k buffer Aug–Sep to cover retail peak + Hari Raya 2027 (R-10)
- Component-gated, not line-gated: the binding constraints are **scan engine** (single source, R-02) and **UFS** (allocation, R-04), not assembly capacity

## Material readiness
| Item | Coverage | Risk |
|---|---|---|
| Scan engine (Helios) | 8-wk safety stock | 🔴 single source → Aurora qual (R-02) |
| UFS (Kioxia) | firm thru Q1 2027 | 🔴 LTB/SanDisk decision (R-04) |
| SoC (QCM6125) | firm FY26 | 🟡 EOL watch 2027 |
| Battery (dual) | healthy | 🟢 |
| Display | dual-source qual underway | 🟢 |

## Quality gates in line
- AOI → ICT → FCT → scan-aim cal → touch-cal → payment provisioning → RF cal → run-in → OQC
- FPY 94.5%, OQC AQL 0.65 → [[factory-yield-mp]] · stations → [[test-stations]]

## Open production actions
1. Lock Q4 build-ahead PO + scan-engine safety stock top-up (Wei, Jul)
2. 3rd-line staffing plan for peak (Wei, Aug)
