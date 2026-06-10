---
type: project-doc
project: AMG
section: fw
tags: [demo, synthetic, fw]
last_updated: 06/10/2026
---
# AMG-100 — Firmware / Software Plan

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: Anna Volkov (FW lead) · QA: Tom Becker · Dept: [[01-Departments/01-hardware-engineering/index|Hardware Engineering]]

## Stack
- **OS:** Android 14 (AOSP, no GMS) on MediaTek Genio 700 BSP (via ODM, quarterly security patch contract through 2031)
- **Launcher:** locked kiosk launcher (Software BU owns app layer; HW FW owns below-launcher)
- **Update:** A/B seamless OTA, fleet-staged rollout (1% canary → 10% → 100%), signed images, rollback on boot-fail ×3
- **Security:** Verified boot (AVB 2.0), keys in SoC fuses; payment domain fully inside NovaPay SP-30 (out of Android trust scope — PCI boundary, R-01); service UART eFused off at MP

## Release Train
| Version | Phase | Date | Content | Status |
|---|---|---|---|---|
| 0.8.x | EVT | 03/23–05/08 | Bring-up, ISS-007 eMMC fix (0.8.2), PD stack fix (0.8.5) | ✅ done |
| **0.9.0** | **DVT build** | **06/18 freeze** | Roam params (ISS-032), NovaPay retry (ISS-028), GPU governor tune (game-mode power), palm-reject v2 (ISS-019), battery longevity dock-charge mode | 🟡 on track |
| 0.9.5 | DVT exit | 08/07 | DVT PRT findings, OTA pipeline E2E test vs staging fleet server | planned |
| 1.0.0-RC | PVT | 09/21 | Feature freeze; cert-final build (FCC/EMV configs locked) | planned |
| 1.0.0 | MP | 10/30 | Golden image for factory pre-program | planned |

## DVT FW Test Plan (Tom Becker) — with [[01-Departments/03-quality-reliability/index|Quality & Reliability]]
| Area | Cases | Automation |
|---|---|---|
| Stability: 72 h monkey + 14-day soak (10 units) | crash rate < 0.1/24 h | ✅ lab rack, auto-triage |
| OTA: 500 update cycles incl. pulled-power at 20/50/80% | 0 bricks | ✅ |
| Payment integration (SP-30): 10k simulated transactions | timeout < 0.05% (vs 0.3% now, ISS-028) | semi-auto |
| Wi-Fi roam: 4-AP testbed, 1,000 roams | drop < 0.5% | ✅ |
| Thermal governor: 40 °C chamber scenarios | no shutdown, skin ≤ 43 °C | manual + logger |
| Factory test hooks (FCT mode, cal storage) | all stations scriptable | with [[test-stations]] |

## Vendor FW dependencies
| Vendor | Item | Need by | Status |
|---|---|---|---|
| NovaPay | SP-30 v2.1.4 (handshake timeout, ISS-028) | 06/20 | 🟡 promised; escalation letter staged |
| MediaTek (via ODM) | BSP Q2-2026 security patch | 07/01 | 🟢 on schedule |
| Display/touch IC | Wet-finger FW lib v3.2 | in 0.9.0 | ✅ received 06/02 |

## Metrics (alpha trial, 24 EVT units, 3 sites, since 05/26)
- Uptime 99.1% (target 99.5% by PVT) · crashes 0.21/24 h (driver: SP-30 timeouts → ISS-028) · 2 roam-drop events → ISS-032 · OTA success 100% (3 pushes)
