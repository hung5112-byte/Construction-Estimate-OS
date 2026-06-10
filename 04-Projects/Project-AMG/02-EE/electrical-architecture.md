---
type: project-doc
project: AMG
section: ee
tags: [demo, synthetic, ee]
last_updated: 06/10/2026
---
# AMG-100 — Electrical Architecture

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: David Chen (EE lead) · Dept: [[01-Departments/01-hardware-engineering/index|Hardware Engineering]]

## System Block Diagram (text)
```
                        ┌──────────────────────────────┐
  13.3" FHD IPS ◄──MIPI─┤                              ├──USB2──► NovaPay SP-30
  (BOE NV133FHM)  DSI×4 │   MediaTek Genio 700         │          payment module
  GFF touch ◄────I2C────┤   (MT8390)                   │          (EMV/NFC/MSR)
                        │   4GB LPDDR4X (Micron)       ├──I2S───► Audio amp TAS2563
  8MP cam ◄──MIPI CSI───┤   64GB eMMC 5.1 (Kioxia*)    │          → 2× 2W speakers
                        │                              ├──UART──► Debug (pogo, fused off at MP)
  Wi-Fi 6 + BT5.2 ◄PCIe─┤   PMIC MT6365                ├──I2C───► Sensors: ALS, accel (LIS2DW12)
  (MT7921 module)       │                              ├──GPIO──► LED ring, buttons (vol, svc)
                        └───────────┬──────────────────┘
                                    │
        USB-C PD 27W ◄── PD ctrl ───┤ Charger BQ25713 ── 1S2P 5,000 mAh pack
        Dock pogo 12V ◄─ OR-ing ────┘ Fuel gauge BQ40Z50 (SMBus)
```
*Second source: SanDisk iNAND (qual in DVT, ISS-030)

## Key Component Selections
| Block | Part | Rationale | Risk |
|---|---|---|---|
| SoC | MediaTek Genio 700 (MT8390) | Android 14 BSP longevity (10-yr supply program), 2× A78 + 6× A55, fits thermal envelope | BSP patch cadence via ODM |
| PMIC | MT6365 | Reference pairing with Genio 700 | — |
| Wi-Fi/BT | MT7921 module (M.2 1216 solder-down) | Wi-Fi 6, ODM has cal experience | Antenna detune → ISS-014 |
| Memory | 4 GB LPDDR4X Micron + 64 GB eMMC Kioxia | Cost/perf for locked launcher use | eMMC allocation → ISS-030 |
| Payment | NovaPay SP-30 (USB) | Pre-certified EMV L1/L2, PCI PTS — buy-not-build decision 02/06 | Vendor FW → ISS-028 |
| Charge | TI BQ25713 + BQ40Z50 gauge | Dock OR-ing + battery hot-warm-swap | — |
| Audio | TI TAS2563 smart amp | Speaker protection at max SPL | Buzz → ISS-027 (mech) |
| Display | BOE NV133FHM-N61, eDP→MIPI bridge deleted in rev B (native DSI panel) | Cost −$3.20 in DVT | — |

## PCBA Set
| Board | Layers | Size | Rev (DVT) | Notes |
|---|---|---|---|---|
| Main board | 8L HDI (1+6+1) | 168 × 92 mm | **B** | Shield can added over PMIC (ISS-025) |
| USB-C / charge sub-board | 4L | 42 × 18 mm | B | FRU — wears first, field-replaceable |
| Button/LED flex | 2L flex | — | A2 | — |
| Antenna feed flex | 2L flex | — | **B** | Re-match for ISS-014: new feed point + 0.5 mm standoff |
| Dock main (AMG-D10) | 4L | 120 × 80 mm | A | Printer driver + PoE-class power in |

## Interfaces & Expansion
- USB-C (PD 27 W sink, DisplayPort alt-mode disabled), dock 12 V/3 A pogo ×6
- Service UART on pogo pads — **disabled by eFuse at MP** (PCI requirement)
- Secure element zone: SP-30 module owns tamper domain; main SoC outside PCI boundary (key design choice → keeps PTS scope on module only, R-01)

## Open EE items for DVT
1. ISS-014 antenna re-match — rework kits ETA 06/16 → [[open-issues]]
2. ISS-025 shield can + ferrite — in rev B, pre-scan #2 on 07/14
3. SanDisk iNAND timing qual (ISS-030) — eMMC driver strength sweep on 5 rev-B boards
4. Power budget re-measure on rev B → [[power-budget]]
