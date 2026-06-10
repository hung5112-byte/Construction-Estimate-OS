---
type: project-doc
project: AMG
section: ee
tags: [demo, synthetic, ee]
last_updated: 06/10/2026
---
# AMG-100 — Schematic & PCB Status

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: David Chen

## Revision History (main board)
| Rev | Phase | Released | Changes | Result |
|---|---|---|---|---|
| P0 | Bring-up | 01/30/2026 | First proto, 12 boards | 9/12 alive; 14 bodges logged |
| A | EVT | 03/06/2026 | P0 bodges absorbed; payment isolation zone | EVT build 50 units — [[evt-ee-test-report]] |
| **B** | **DVT** | **06/02/2026** | Shield can PMIC (ISS-025), antenna feed re-match (ISS-014), eMMC drive-strength straps for SanDisk qual (ISS-030), bridge IC deleted (native DSI, −$3.20) | Fab ETA at BrightPath 06/13 |
| C (planned) | PVT | 08/21/2026 | DVT learnings only; target zero functional change | MP intent |

## Schematic Review Status (rev B, 38 pages)
| Block | Pages | Review | Findings |
|---|---|---|---|
| Power tree / PMIC | 6 | ✅ 05/21 | 2 minor (test point adds) — closed |
| SoC core / memory | 8 | ✅ 05/21 | 1 major: eMMC strap conflict w/ boot mode — **fixed before release** |
| Display / touch / cam | 5 | ✅ 05/22 | 0 |
| RF (Wi-Fi/BT + antenna feed) | 4 | ✅ 05/23 + RF consultant | 1 minor (matching pad layout) — closed |
| Payment (SP-30 + isolation) | 4 | ✅ 05/27 incl. Atlas pre-review | 0 — secure boundary unchanged ✅ (R-01) |
| Audio / sensors / IO | 6 | ✅ 05/22 | 1 minor — closed |
| USB-C / charge sub-board | 5 | ✅ 05/23 | 0 |

## PCB / DFM
- 8L HDI 1+6+1, via-in-pad on BGA field; min trace 60 µm — BrightPath fab partner capable, CpK data on file
- DFM review with BrightPath SMT 05/28: 3 findings (fiducial clearance, panel rail width, shield-can paste aperture) — all incorporated rev B
- Panelization 2-up; expected SMT cycle time 38 s/board both sides

## Bring-up & Test Hooks
- 42 test points mapped to FCT bed-of-nails → [[test-stations]]
- Boundary scan chain on SoC + memory; eMMC pre-programmed (FW 0.9.0 golden image)
- Service UART pogo pads — eFuse disable at MP (PCI), keep-out documented for depot

## Open EE risks
- Rev B fab on critical path: arrives 06/13 for 06/22 build — single fab lot, no split ⚠️
- If pre-scan #2 (07/14) still fails ISS-025 → rev B2 spin localized to shield region; 3-wk impact, eats PVT buffer → [[risk-register]] R-05
