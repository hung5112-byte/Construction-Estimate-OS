---
type: project-doc
project: AMG
section: reliability
tags: [demo, synthetic, reliability, prt]
last_updated: 06/10/2026
---
# AMG-100 — Product Reliability Test (PRT) Plan

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: Dr. Henry Wu · Dept: [[../../01-Departments/03-quality-reliability/index|Quality & Reliability]] · Ref: validation-reliability team

## Philosophy
Restaurant duty cycle is brutal: 14 h/day powered, daily chemical wipe-down, spills, drops by guests, 24/7 dock cycling. PRT mirrors **3 years of field life** compressed. Gate rule: DVT exit needs full PRT pass or approved waiver; PVT repeats the full suite on MP-representative units + starts ORT.

## Sample Allocation
| Phase | Units | Coverage |
|---|---|---|
| EVT | 12 | Full suite, first pass → [[prt-results-evt]] |
| DVT | 60 | Full suite + fix verification (ISS-019/023/027) + cert support |
| PVT | 100 | Full suite on MP tools/process + ORT start (40 units, ongoing) |
| MP | 10/month | ORT: rotating sample off line, key tests monthly |

## Test Matrix (per-phase, key tests)

| # | Test | Condition | Sample | Accept |
|---|---|---|---|---|
| T1 | Thermal cycling | −20 ↔ +60 °C, 200 cycles, 15 min dwell | 8 | No functional/cosmetic fail |
| T2 | High-temp operating life (HTOL) | 60 °C, 100% load profile, 1,000 h | 8 | 0 fail; param drift < 5% |
| T3 | Humidity soak | 85 °C / 85% RH, 168 h, powered | 6 | No corrosion/ingress |
| T4 | Drop | 1.0 m, 26-drop sequence, vinyl/concrete | 8 | No loss of function; no glass fracture |
| T5 | Tumble | 0.5 m × 300 | 2 | Cosmetic within spec |
| T6 | Vibration (transport) | ASTM D4169 truck profile, packaged | 4 boxes | No damage → [[packaging-spec]] |
| T7 | ESD | ±8 kV contact / ±15 kV air, IEC 61000-4-2 | 4 | No hard fail; soft reset OK if auto-recover |
| T8 | Spill | 60 ml soda/water/coffee on face + dock pocket, powered | 4 | No ingress, full function |
| T9 | Sanitizer chemical | Quat + 70% IPA alternating wipe, 10k cycles | 4 | No crack; ΔGloss ≤ 8 (per W-02) |
| T10 | Connector durability | USB-C 10k, dock pogo 30k, card slot 100k swipes | 4 | Within retention/contact spec |
| T11 | Button life | 200k actuations | 4 | Force −20% max |
| T12 | Battery cycle life | 0.5C/0.5C, 500 cycles, 25 °C + 45 °C legs | 24 cells/source | ≥ 80% capacity; **zero swelling > 0.5 mm** (tightened post ISS-021) |
| T13 | Power cycling | 10k AC/dock removal cycles | 4 | 0 boot fail |
| T14 | Torsion/flex fatigue | 5 N·m × 10k | 2 | No creak/crack |
| T15 | Life-sim combined | 30-day chamber script: thermal + duty + wipe robot | 6 | The "dinner-rush simulator" — uptime ≥ 99.5% |

## DVT additions (fix verification)
- T4 repeat with T1-mod housing (ISS-023) — 8 units, corner emphasis
- T2 with touch monitor at 45 °C (ISS-019 regression watch)
- Speaker buzz sweep pre/post foam gasket (ISS-027)
- Battery: DynaCell source added to T12 (R-03) — 24+24 cells

## ORT (PVT→MP)
Monthly: 10 units × (T1 reduced 50 cyc, T4 6-drop, T8, functional soak 72 h). Trigger: any ORT fail → containment + lot trace within 24 h with [[../../01-Departments/04-mfg-supplier-quality/index|MSQ]].

## Reliability targets
MTBF ≥ 50,000 h → prediction 62,000 h ([[mtbf-prediction]]) · AFR yr-1 ≤ 2.0% · 3-yr survival ≥ 93% · Depot TAT contribution: FRU design < 12 min → [[mechanical-design]]
