---
type: project-doc
project: Cyber
section: data
tags: [demo, synthetic, dashboard]
last_updated: 06/04/2026
---
# CY-80 Program Dashboard — May 2026

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Auto-compiled from MES/PLM/telemetry/RMA extracts · Owner: Daniel Reyes

## Program Health: 🟡 GREEN-YELLOW · MP Year-2, month 4

| Dimension | Status | Driver |
|---|---|---|
| Volume / production | 🟢 | 8,410 built (plan 8,300); FPY 94.5% best month → [[factory-yield-mp]] |
| Field reliability | 🟡 | AFR 3.9% (target 3.5%); glidepath slowing on pre-039 tail → [[field-reliability-report]] |
| Supply | 🔴 | Scan-engine single source (R-02) + UFS allocation (R-04) → [[risk-register]] |
| Cost | 🟢 | BOM $151.20; $148 path on track → [[cost-walk]] |
| Quality / issues | 🟡 | 7 open (0 Sev-1, 3 Sev-2) → [[open-issues]] |

## KPI snapshot
| KPI | This month | Last month | Target | Trend |
|---|---|---|---|---|
| Units built | 8,410 | 8,260 | ~8,300 | 🟢 |
| FPY | 94.5% | 94.1% | 95% | ↑ 🟢 |
| Field AFR (annualized) | 3.9% | 4.0% | ≤ 3.5% | ↓ 🟡 |
| RMA receipts | 528 | 541 | — | ↓ 🟢 |
| Depot TAT (days) | 2.4 | 2.5 | ≤ 3 | 🟢 |
| NTF | 9% | 10% | ≤ 8% | ↓ 🟡 |
| Repair cost / unit | $33.80 | $34.60 | ≤ $36 | 🟢 |
| BOM ($) | 151.20 | 152.10 | 148 | ↓ 🟢 |
| OTA on FW 1.8.x | 61% | 38% | GA | ↑ 🟢 |

## This month's highlights
1. **FW 1.8.0 on-device diagnostic** crossed 60% fleet → NTF down to 9%, trending to target
2. **Aurora AX-20** scan-engine 2nd-source qual lot entered ORT — top supply risk being closed (R-02)
3. ECO-CY-044 battery-contact post-cut returns showing the expected drop
4. ISS-CY-070 DynaCell DC2611 swell **contained** (4 units, 100% X-ray, no safety incident)

## Watch items / next month
- 🔴 Scan-engine 2nd source — ORT aim-stability data due 07/10 (gates ECO-CY-052)
- 🔴 UFS/SoC EOL — LTB cost model to Brian (R-04)
- 🟡 CY-80L thermal FW 1.8.3 field-beta result (ISS-CY-064)
- 🟡 Q4 build-ahead + refurb pre-stage kickoff (R-06/R-10)

## Data sources
Meridian MES (yield/genealogy) · PLM (BOM rev D, ECO log) · fleet telemetry (~121k reporting) · Fort Worth depot RMA system · workstream trackers → [[Project-Cyber-Hub]]
