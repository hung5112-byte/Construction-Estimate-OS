---
type: project-doc
project: Cyber
section: pm
tags: [demo, synthetic, issues]
last_updated: 06/17/2026
---
# Project Cyber — Sustaining Issue Tracker

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Sev-1 = stop-ship / safety / line-down, Sev-2 = field-impacting, fix this quarter, Sev-3 = monitor / fix when able

## Open Issues

| ID | Sev | Title | Found | Owner | Dept | Fix / Plan | Status |
|---|---|---|---|---|---|---|---|
| ISS-CY-061 | 3 | Scan-window haze recurrence on pre-ECO-039 fleet (units built < 02/2026) | Field RMA pareto 04/2026 | Sofia Ramirez | [[01-Departments/05-service-operations/index\|Service Ops]] | Retrofit oleophobic window on RMA touch; no proactive recall — aging out as fleet cycles | 🟡 Retrofit-on-RMA live |
| ISS-CY-064 | 2 | CY-80L (LTE) thermal throttle: CPU drops to 60% during continuous scan + 4G upload > 40 °C ambient | Customer DC site report 05/12 | Raj Mehta | [[01-Departments/01-hardware-engineering/index\|HW Eng]] | FW thermal-governor retune v1.8.3 + graphite pad add (ECO-CY-051 eval) | 🟡 FW fix in field beta |
| ISS-CY-066 | 2 | Touch ghosting near NFC antenna during contactless tap (1–2 phantom touches) | Field telemetry 05/2026 | Raj Mehta | HW Eng | Touch-controller FW palm/EMI reject v2; OTA in FW 1.8.x ring 2 | 🟡 OTA rolling |
| ISS-CY-068 | 3 | CYS-10 cradle pogo-pin wear marks at ~18k insertions (spec 30k) | Depot teardown 05/28 | Tom Becker | HW Eng | Au-plating 0.76 µm + spring upgrade in production from 05/2026; field-swap kit at depot | 🟡 Fix in production |
| ISS-CY-070 | 2 | Battery swell — DynaCell lot DC2611 (4 units of 5,000 returned, 1.6 mm bulge ~220 cyc) | RMA FA 06/03 | Grace Lim | [[01-Departments/04-mfg-supplier-quality/index\|MSQ]] | 8D → [[capa-8d-CY-26-007]] model; lot DC2611 quarantined; 100% X-ray; Quanex 2nd source | 🟡 Contained (D5) |
| ISS-CY-072 | 3 | UFS (Kioxia 64 GB) Q1-2027 allocation coverage gap | Sourcing review 05/27 | Daniel Reyes | [[01-Departments/02-npi-program-management/index\|NPI & PM]] | SanDisk UFS dual-qual in ORT; LTB decision Q4 2026; broker buy pre-approved ≤ $40k | 🟡 Open |
| ISS-CY-073 | 3 | Speaker rattle at max volume — housing supplier lot (rib flash, boss resonance) | QC audit 06/09 | Tom Becker | HW Eng | Supplier dunnage + de-flash at gate; foam gasket spec tightened; sort at incoming | 🆕 New |

## Closed Issues (selection — launch & Year 1)

| ID | Sev | Title | Resolution | Closed |
|---|---|---|---|---|
| ISS-CY-018 | 2 | USB-C port intermittent charge after drops (solder-joint fatigue) | ECO-CY-031 reinforcement bracket + pad-stack change | 09/2025 |
| ISS-CY-024 | 2 | Barcode no-read after ~9 mo in QSR (window haze/oil film) | ECO-CY-039 oleophobic coating → [[capa-8d-CY-26-007]] | 02/2026 |
| ISS-CY-029 | 2 | Intermittent battery charge — contact spring relaxation | ECO-CY-044 spring force +18%, Au contact | 04/2026 |
| ISS-CY-033 | 3 | Boot-time regression (+6 s) after FW 1.6.0 | UFS init sequence rollback, FW 1.6.2 | 11/2025 |
| ISS-CY-047 | 3 | MSR read rate 95% on worn loyalty cards | Head spring +15%, guide-rib mod (ECO-CY-040) | 03/2026 |

## Issue stats for dashboard → [[monthly-dashboard-2026-05]]
- Open: **7** (Sev-1: 0 · Sev-2: 3 · Sev-3: 4) · Closed lifetime: 58 · Avg days-to-close (Y2): 22
- Standing rule: any field issue with a **safety** vector (battery, payment, power) auto-escalates to Sev-1 pending FA, regardless of return count.
