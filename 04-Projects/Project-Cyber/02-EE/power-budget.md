---
type: project-doc
project: Cyber
section: ee
tags: [demo, synthetic, power]
last_updated: 06/17/2026
---
# CY-80 — Power Budget & Battery Life

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Priya Nair · Dept: [[01-Departments/01-hardware-engineering/index|Hardware Eng]]

## Battery
- 5,000 mAh / 3.7 V nominal (18.5 Wh), **hot-swap removable** — retail staff swap mid-shift
- Dual-source cells: DynaCell DC-50 (primary) / Quanex QX-50 (2nd) → [[risk-register]] R-01
- Fuel gauge calibrated at factory; cycle-life spec 500 cyc to 80% capacity

## Power profile (measured, production FW 1.8)
| Mode | Current @ 3.7 V | Notes |
|---|---|---|
| Idle (screen on, 50% bright) | 380 mA | typical between-transaction |
| Active POS (scan + touch + Wi-Fi) | 720 mA | line-busting duty cycle |
| Continuous scan burst | 1,180 mA | inventory/receiving |
| CY-80L LTE upload + scan | 1,460 mA | thermal-limited > 40 °C (ISS-CY-064) |
| Sleep (cradle docked) | 22 mA | charging in CYS-10 |

## Battery-life model
| Duty profile | Est. runtime | Field actual (telemetry) |
|---|---|---|
| Mixed retail shift (60% idle / 35% active / 5% scan burst) | 9.8 h | 9.1 h median (aged fleet) |
| QSR line-bust (heavy scan) | 6.4 h | 6.0 h |
| Spec (advertised) | ≥ 8 h mixed | ✅ met new; 🟡 aged cells trend down |

## Charging
- USB-C PD 18 W: 0→80% in ~95 min
- CYS-10 5-bay cradle pogo: 5 V / 3 A per bay, full bank charges overnight
- Hot-swap: device runs ~90 s on supercap bridge during cell swap (no reboot)

## Field note — capacity fade
Battery is the #2 RMA driver (18%). Most are **capacity-fade complaints** ("won't last a shift") on units > 14 months, not true failures — this inflates NTF. Depot now runs a capacity-grade step ([[rma-dashboard]]) and ships a fresh cell rather than the whole unit where possible, cutting battery-RMA cost ~$19/unit.
