---
type: project-doc
project: AMG
section: production
tags: [demo, synthetic, production, ramp]
last_updated: 06/10/2026
---
# AMG-100 — MP Ramp Plan

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: Sarah Whitfield + Kevin Tran · MP gate: 11/09/2026

## Ramp Curve

| Month | Build | Cum. | Line config | FPY gate | Notes |
|---|---|---|---|---|---|
| M1 — Nov 2026 | 2,000 | 2,000 | Line 5, 1 shift | ≥ 92% | Air freight wave-1 deployment units → [[logistics-plan]] |
| M2 — Dec | 3,000 | 5,000 | 1 shift + Sat | ≥ 94% | Ocean transition begins; eMMC coverage ends → ISS-030 decision point |
| M3 — Jan 2027 | 5,000 | 10,000 | +2nd shift partial | ≥ 95% | **Pre-build +6k for Tet** (R-07); launch wave 1 (01/12) |
| Feb 2027 | 1,200 (Tet 2 wks) | 11,200 | shutdown buffer | — | Safety stock at DC covers deployments |
| Mar–Jun 2027 | 4,500/mo avg | ~29k | steady | ≥ 95% | Year-1 25k target hit ~May |

## Ramp Gates & Kill-Switches
| Gate | Criteria | If missed |
|---|---|---|
| MP gate 11/09 | PVT exit ✅, certs granted/scheduled (PTS OTA-activation plan OK), FPY ≥ 92%, zero Sev-1/2 open, 2 sources on A-risk parts | Hold MP; deploy schedule slips week-for-week, customer comms by VP |
| M1 → M2 step-up | FPY ≥ 94% sustained 2 wks, ORT clean, field DOA < 0.5% | Hold at 2k/mo; root-cause sprint |
| M2 → M3 step-up | AFR early-signal < 1.0% annualized (90-day cohort), depot TAT < 3 days | Hold at 3k/mo |
| Any point | ORT Sev-1 fail OR confirmed safety issue | **Stop-ship**, containment per QMS, VP + customers notified 24 h |

## Supply Readiness (ramp-critical)
| Item | Coverage | Risk |
|---|---|---|
| eMMC (Kioxia) | PO through M2 | 🔴 ISS-030 — SanDisk qual closes at PVT or broker buy |
| Battery (Veltron + DynaCell) | Dual by PVT, split 70/30 target | 🟡 D6 verification 07/08 → [[capa-8d-AMG-26-004]] |
| Display (BOE) | LOI 30k; panel B qual PVT | 🟢 |
| SP-30 modules (NovaPay) | Firm PO 12k, forecast +24k | 🟢 8-wk lead, no allocation |
| Long-lead passives | BrightPath buffer 8 wks | 🟢 |

## People & Logistics during ramp
- Omar resident at BrightPath Sep–Dec (MfgE); James on 50% travel for supplier audits
- Weekly ramp war-room (M1–M3): 30 min daily first 2 weeks of M1, then 3×/wk — chaired by Sarah, VP joins Mondays
- Fort Worth DC staffing +2 temps from M1 → [[logistics-plan]] · Depot FRU seeding 60 kits from PVT build → [[rma-process-dashboard]]
