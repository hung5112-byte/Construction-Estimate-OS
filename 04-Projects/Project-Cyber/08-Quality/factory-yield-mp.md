---
type: project-doc
project: Cyber
section: quality
tags: [demo, synthetic, yield]
last_updated: 06/17/2026
---
# CY-80 — MP Factory Yield (Meridian Penang)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Hassan Ali / Wei Lim · Dept: [[01-Departments/04-mfg-supplier-quality/index|Mfg & Supplier Quality]]

## First-pass yield trend
| Period | FPY | Note |
|---|---|---|
| PVT exit (12/2024) | 89.0% | aim-station + touch-cal limiting |
| SOP ramp (Q1 2025) | 90.5% | station rework |
| Y1 mid (mid-2025) | 92.8% | scan-aim fixture redesign |
| Y1 exit (02/2026) | 93.9% | — |
| **Current (05/2026)** | **94.5%** | best month; target 95% |

## Defect pareto (final FCT + AOI, rolling)
| Defect | Share | Action |
|---|---|---|
| Scan aim/decode cal fail | 22% | golden-sample re-cal; Aurora qual reuses fixture |
| Touch calibration fail | 18% | auto-cal v3 deployed |
| Display particle / dot | 14% | incoming AOI + cleanroom bond |
| Payment provisioning fail | 11% | key-injection station retry logic |
| Wi-Fi/BT RF cal | 9% | golden-unit drift PM |
| Connector / pogo continuity | 8% | fixture pin PM |
| Cosmetic (housing) | 9% | supplier sort (ISS-CY-073) |
| Other | 9% | — |

## Capacity & lines
- 2 SMT lines + 3 assembly/test lines at Meridian, ~8,300 units/mo nominal, 11k/mo peak
- 3rd assembly line on standby for Q4 retail-peak build-ahead → [[production-plan]]

## Genealogy / traceability
- Full unit genealogy in PLM (SoC, UFS, battery, scan-engine, payment SN) — enables ECO line-break ranges and field-FA back-trace (used in ISS-CY-070 lot containment).

## Open yield actions
1. Close the last 0.5% to 95% — payment-provisioning retry + cosmetic sort (Hassan, Q3)
2. Stand up Aurora AX-20 scan station config (reuses aim fixture) ahead of FW 1.9 (Hassan + Grace)
