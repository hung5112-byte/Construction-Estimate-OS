---
type: project-doc
project: Cyber
section: me
tags: [demo, synthetic, me]
last_updated: 06/17/2026
---
# CY-80 — Mechanical Design, Ruggedization & FRUs

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Tom Becker · Dept: [[01-Departments/01-hardware-engineering/index|Hardware Eng]]

## Form factor
- 8.0" handheld, 228 × 132 × 16.5 mm, **382 g**, single-hand grip with hand-strap boss
- Housing: glass-filled PC+ABS, over-molded TPU bumpers on 4 corners (drop energy)
- **IP54**, MIL-STD-810H (drop/vibe/thermal), 1.2 m drop to concrete, 0–50 °C operating
- Gorilla Glass 5 cover; optically-bonded touch (no air gap → survives flex)

## Ruggedization rationale (handheld POS reality)
Retail/QSR handhelds get **dropped daily**. The whole ME strategy is energy management on corner drops + sealing against spills/grease. Drop-cracked display remains the **#1 field failure (27%)** — see [[field-reliability-report]] — so corner bumper durometer and display bond line are the highest-leverage parameters.

## FRU strategy (depot serviceability — top-5)
| FRU | Field % of repairs | Swap time target | Notes |
|---|---|---|---|
| Display + digitizer module | 27% (drops) | < 9 min | Bonded module, no separate glass replace at depot |
| Battery (hot-swap) | 18% | < 1 min (customer) | Often field-swapped; depot only on contact/swizzle faults |
| Scan engine (Helios N4200) | 13% | < 7 min | Aurora AX-20 must be mechanically interchangeable (ECO-052) |
| USB-C / charge board | 11% | < 8 min | Post ECO-031 |
| Main PCBA | ~7% | < 14 min | Includes payment module handling (PCI) |

> Top-5 FRUs cover ~76% of repair actions; all verified ≤ target on depot teardowns → [[rma-dashboard]].

## Field-driven ME changes (Year 1)
| Issue | Change | ECO |
|---|---|---|
| USB-C boss cracking on drop | Rib + steel bracket | ECO-CY-031 |
| Scan window hazing (grease) | Oleophobic coated window, recessed lip | ECO-CY-039 |
| Cradle pogo pin wear (ISS-CY-068) | Au 0.76 µm + spring upgrade | in production 05/2026 |
| Speaker rattle (ISS-CY-073) | De-flash + foam gasket spec | sort at incoming |

## CYS-10 cradle
- 5-bay charge/sync, pogo 5 V/3 A/bay, security-slot, cable-management
- Pogo wear was under-spec (18k vs 30k insertions) — hardness upgrade in production; field-swap pin kit at depot

## Open ME actions
1. Validate Aurora AX-20 fits Helios mechanical envelope + window stack (ECO-CY-052) — Tom, with Priya
2. Confirm cradle pogo upgrade field-return rate drop by Q3 (ISS-CY-068)
