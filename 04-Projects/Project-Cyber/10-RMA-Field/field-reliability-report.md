---
type: project-doc
project: Cyber
section: rma
tags: [demo, synthetic, field, reliability]
last_updated: 06/17/2026
---
# CY-80 — Field Reliability Report (Year 2)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Sofia Ramirez · Dept: [[01-Departments/05-service-operations/index|Service Operations]] + [[01-Departments/03-quality-reliability/index|Quality & Reliability]]

## Executive summary
CY-80 launched at a **6.8% AFR** — high but typical for a year-1 rugged handheld going into retail/QSR. Sixteen months and five ECOs later it sits at **3.9% and falling**, on a glidepath to the **3.5% target** by Y2-Q4. The remaining gap is not a new defect — it's the **long tail of pre-ECO-039 units** still in the field plus **NTF inflation** from battery-fade complaints. Both are being worked without new hardware spend.

## AFR glidepath (rolling 3-mo annualized)
| Period | AFR | What moved it |
|---|---|---|
| Y1 Q1 2025 (launch) | 6.8% | drop + USB-C + scan-haze stacking |
| Y1 Q2 | 5.9% | drop-education start |
| Y1 Q3 | 4.8% | ECO-CY-031 USB-C |
| Y1 Q4 | 4.3% | plateau |
| Y2 Q1 2026 | 4.0% | ECO-CY-039 scan coating |
| **Y2 Q2 (now)** | **3.9%** | ECO-CY-044 battery; long tail remains |
| Y2 Q4 (forecast) | **3.5%** | retrofit-on-RMA + FW 1.8 NTF cut |

## The three things that actually drive cost
1. **Drops (display, 27%)** — the dominant, stubborn mode. Not a defect; a usage reality. Levers are mechanical (bumper) — already optimized — and **behavioral**: a drop-education kit (lanyard/holster recommendation, drop-rate scorecard) deployed to the top-3 chains, whose stores show 1.6× the fleet-average drop RMA.
2. **Battery (18%) + NTF (now 9%)** — a chunk of "battery" returns are **capacity-fade complaints**, not failures. FW 1.9 capacity self-report + depot capacity-grade + battery-only swap converts these from full-unit RMAs to cell swaps (~$19/unit saved) and pulls NTF under 8%.
3. **Scan haze tail (13%, declining)** — closed by ECO-039 for new build; old fleet handled by **retrofit-on-RMA** (ISS-CY-061), no recall (cost/benefit decided 06/04 → [[meeting-minutes-2026-06-04]]).

## Cohort view (by build month)
| Cohort | Window | 12-mo AFR | Note |
|---|---|---|---|
| Launch (Q1–Q2 2025) | pre ECO-031/039 | 6.4% | worst; aging out |
| Mid Y1 (Q3–Q4 2025) | post ECO-031 | 4.6% | USB-C fixed, scan haze present |
| Y2 build (2026+) | post ECO-039/044 | **~3.1%** (tracking) | the "clean" cohort — proof the ECOs worked |

> The Y2-build cohort tracking ~3.1% is the headline: it shows the fleet **converges below target** as old cohorts retire. The blended 3.9% is a mixing artifact of the install base, not the current product.

## Top-chain field signals
| Chain (fictional) | Sites | AFR vs fleet | Lead issue |
|---|---|---|---|
| QSR-A | 1,200 | 1.6× | drops + grease (scan) |
| Retail-B | 800 | 0.9× | battery fade (long shifts) |
| Retail-C | 540 | 1.1× | drops |
| QSR-D | 410 | 1.4× | spills (ingress) |

## Recommendations (open)
1. Fund the **drop-education kit** for QSR-A/QSR-D (highest leverage, ~$0 BOM) — owner Sofia, Q3
2. Ship **FW 1.9** capacity-grade to convert battery-fade RMAs → cell swaps — owner Raj, Q3
3. Hold proactive scan-haze recall; continue retrofit-on-RMA — confirmed
4. Re-measure NTF after FW 1.8 reaches 60% fleet — owner Carlos
