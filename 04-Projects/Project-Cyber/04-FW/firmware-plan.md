---
type: project-doc
project: Cyber
section: fw
tags: [demo, synthetic, firmware]
last_updated: 06/17/2026
---
# CY-80 — Firmware Release Train & OTA Fleet Status

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Raj Mehta · Dept: [[01-Departments/01-hardware-engineering/index|Hardware Eng]]

## Platform
- Android 13 (AOSP), locked launcher, MDM-managed, A/B OTA with rollback
- Monthly security patch cadence + quarterly feature train
- Staged OTA rings: ring 0 (internal) → ring 1 (5% canary) → ring 2 (40%) → GA

## Release train
| Version | Released | Highlights |
|---|---|---|
| 1.6.2 | 11/2025 | UFS init fix (ISS-CY-033 boot regression) |
| 1.7.0 | 02/2026 | Security baseline, MSR retry, scan-decode tuning |
| **1.8.0** | 05/2026 | **On-device diagnostic code** at RMA claim (attacks NTF); contactless touch-reject v2 (ISS-CY-066) |
| 1.8.3 | in beta | CY-80L thermal governor retune (ISS-CY-064) — 2 DC sites |
| 1.9.0 | planned 08/2026 | Aurora AX-20 scan-engine driver (2nd source), battery capacity-grade reporting |

## OTA fleet status (06/2026)
| Metric | Value |
|---|---|
| Active devices reporting | ~121k / ~128k fleet (94.5%) |
| On FW 1.8.x | 61% (ring 2 rolling) |
| On FW ≤ 1.6 (stale) | 3.1% (offline / MDM-held) |
| OTA success rate | 99.3% (A/B rollback caught 0.7%) |

## FW-led field fixes (no hardware change)
| Issue | FW remedy | Status |
|---|---|---|
| ISS-CY-064 LTE thermal throttle | 1.8.3 governor retune | 🟡 beta |
| ISS-CY-066 contactless ghosting | 1.8.0 touch-reject v2 | 🟡 ring 2 |
| NTF reduction | 1.8.0 on-device diag code at claim | 🟢 rolling → [[rma-dashboard]] |
| Battery "won't last shift" complaints | 1.9.0 capacity-grade self-report | ⚪ planned |

## Why FW matters to the P&L this year
Three of the seven open issues are **fixable in firmware over the air** — no truck roll, no RMA, no BOM hit. The on-device diagnostic code (1.8.0) is the single highest-ROI sustaining feature: it writes a fault code at claim time so the depot stops "repairing" healthy units, directly attacking the **9% NTF** rate → ~$11/unit of avoided depot labor across ~530 RMAs/mo.
