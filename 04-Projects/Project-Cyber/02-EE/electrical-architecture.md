---
type: project-doc
project: Cyber
section: ee
tags: [demo, synthetic, ee]
last_updated: 06/17/2026
---
# CY-80 — Electrical Architecture

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Priya Nair · Dept: [[01-Departments/01-hardware-engineering/index|Hardware Eng]]

## System block diagram
```
                +-------------------+
   13MP rear ---|                   |--- 8.0" WUXGA 1920x1200 IPS (MIPI-DSI, 450 nit)
   5MP front ---|   Qualcomm        |--- 10-pt cap touch (I2C, Gorilla Glass 5)
   Helios N4200 |   QCM6125 SoC     |--- Wi-Fi 6 + BT 5.2 (QCA combo, M.2)
   2D imager ---|   (Kryo 4xx octa) |--- 4G LTE Cat-4 (CY-80L only, M.2 + eSIM)
   (UART/USB)   |                   |
                |   4GB LPDDR4X     |--- NovaPay SP-25 secure module (EMV+NFC+MSR)
                |   64GB UFS 2.2    |       (USB-HID + tamper GPIO, PCI PTS boundary)
                +---------+---------+
                          |
                   +------+------+
                   |  PMIC PMK8350 + fuel gauge (BQ-series)
                   |  USB-C PD 18W sink  |  pogo charge (cradle, 5V/3A)
                   +------+------+
                          |
              5,000 mAh hot-swap Li-ion (dual-source DynaCell / Quanex)
```

## Key rails & domains
| Rail | V | Load | Notes |
|---|---|---|---|
| VPH_PWR | 3.6–4.4 | system | battery direct, fuel-gauged |
| VREG_S1 | 0.9 | SoC core | DVFS, thermal-governed (ISS-CY-064 watch) |
| VREG_L_disp | 5.8 boost | backlight | 450 nit, dimmed in idle |
| VREG_payment | 3.3 | SP-25 | isolated; tamper kills key store |
| VBUS_scan | 5.0 | Helios N4200 | gated; inrush-limited |

## Production rev (electrical)
- **PCB rev D** in mass production (rev history → [[schematic-pcb-status]])
- Payment boundary frozen since PVT — **no change permitted without PCI PTS re-cert** (R-08)
- Power detail & battery-life model → [[power-budget]]

## Field-relevant electrical learnings (Year 1 → ECO)
| Symptom | Root cause | Fix |
|---|---|---|
| USB-C intermittent charge after drops | Connector pad-stack fatigue under shock | ECO-CY-031 bracket + pad-stack (rev C) |
| Battery "not charging" intermittents | Contact spring relaxation over cycles | ECO-CY-044 spring force +18%, Au plating (rev D) |
| CY-80L throttle under LTE load | S1 thermal headroom thin at >40 °C | FW governor + graphite pad eval (ISS-CY-064) |

> Architecture is mature and stable; sustaining EE work is cost-down ([[cost-walk]]) + the scan-engine 2nd source (Aurora AX-20) drop-in, which must be pin/protocol compatible to avoid a PCB spin.
