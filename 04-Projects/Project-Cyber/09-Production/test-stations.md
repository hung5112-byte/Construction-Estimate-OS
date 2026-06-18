---
type: project-doc
project: Cyber
section: production
tags: [demo, synthetic, test]
last_updated: 06/17/2026
---
# CY-80 — Factory Test Stations

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Hassan Ali · Dept: [[01-Departments/04-mfg-supplier-quality/index|Mfg & Supplier Quality]]

## Station list (assembly/test line)
| # | Station | Checks | Notes |
|---|---|---|---|
| 1 | AOI (post-SMT) | solder, placement | both SMT lines |
| 2 | ICT | shorts/opens, rails | bed-of-nails |
| 3 | FCT (functional) | boot, UFS, sensors, USB-C PD | golden-image flash |
| 4 | Scan-aim cal | aimer alignment, decode margin | golden barcodes; **Aurora reuses this fixture** |
| 5 | Touch cal | linearity, edge, ghosting | auto-cal v3 |
| 6 | Display | dot/particle, uniformity, nits | AOI + photometer |
| 7 | Payment provisioning | EMV/NFC, key injection, tamper | dual-control room (PCI) |
| 8 | RF cal | Wi-Fi/BT (+LTE on CY-80L) | golden-unit referenced |
| 9 | Run-in / burn | 2 h soak, thermal | catches infant mortality |
| 10 | OQC | cosmetic, label, FW ver, AQL 0.65 | sample audit |

## Depot mini-FCT (subset for repair verify)
Stations **3, 4, 5, 7, 8** replicated at Fort Worth depot for post-repair verification → [[rma-dashboard]]. Payment provisioning (7) runs in the PCI-compliant dual-control room.

## Calibration & PM
- Golden units re-referenced weekly (RF, scan, display) to catch fixture drift — a top yield-defect source → [[factory-yield-mp]]
- Fixture pin PM every 25k cycles (pogo/ICT)

## Changes in flight
- **Aurora AX-20** scan-station config (station 4) — parameter set + golden barcodes prepped; gated on ORT/FW 1.9 (R-02)
- On-device diag (FW 1.8) cross-checked at station 3 so depot diag codes match factory baseline
