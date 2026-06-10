---
type: project-doc
project: AMG
section: reliability
tags: [demo, synthetic, reliability, report]
last_updated: 05/07/2026
---
# AMG-100 — EVT PRT Results

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · 12 units, rev A, T0 housings · Window 04/06–05/05/2026 · Author: Dr. Henry Wu

## Verdict: **CONDITIONAL PASS** — 2 fails (T4 drop → ISS-023 · T9 gloss → waiver W-02), 1 watch (T12 battery → ISS-021/8D)

| # | Test | Result | Detail |
|---|---|---|---|
| T1 | Thermal cycling 200cyc | ✅ | No fails; gasket compression set 8% (limit 15%) |
| T2 | HTOL 1,000 h @ 60 °C | ✅ | 0 fail; eMMC wear 2% — fine for 3-yr life. Touch ghost seen at 45 °C leg → ISS-019 (beyond-spec robustness item) |
| T3 | 85/85 168 h | ✅ | Label adhesive lift → label spec change (3M 7872), closed |
| **T4** | **Drop 26-seq** | **❌** | 3/8 corner crack at USB-C boss → ISS-023, T1 tool mod verified; **DVT retest required** → [[evt-me-test-results]] |
| T5 | Tumble 300 | ✅ | Cosmetic in spec |
| T6 | Vibration packaged | ✅ | First-article pack OK → [[packaging-spec]] |
| T7 | ESD ±8/±15 kV | 🟡→✅ | 1 soft reset 4 kV USB-C shell (auto-recovered, allowed); TVS upgraded rev B anyway |
| T8 | Spill suite | ✅ | Soda/water/coffee — IP54 front held; drain channel works |
| **T9** | **Sanitizer 10k wipes** | **❌→waiver** | ΔGloss 6.8 vs spec 5 (no cracking) → **W-02** spec relaxed to ≤8, matte texture masks. VP approved 05/08 → [[../../00-Brain/decisions-log\|log]] |
| T10 | Connector durability | ✅ tablet / 🟡 dock | Dock pogo wear at 5k → ISS-031 (dock-side pin hardness) |
| T11 | Button 200k | ✅ | Force −8% |
| **T12** | **Battery 500cyc dual-temp** | **🟡 contained** | Veltron lot VE2605A: 3/280 cells swell 1.8 mm @ ~200 cyc (45 °C leg) → ISS-021, [[capa-8d-AMG-26-004]]. Other lots: 0 swell, capacity 84% @ 500 cyc ✅ |
| T13 | Power cycling 10k | ✅ | 0 boot fail (post ISS-007 fix) |
| T14 | Torsion fatigue | ✅ | |
| T15 | 30-day dinner-rush sim | ✅ | Uptime 99.3% on EVT FW (driver: SP-30 timeouts → ISS-028); mech/thermal clean |

## Carried into DVT PRT
1. T4 full retest, corner emphasis, T1-mod housings (8 units)
2. T12 with DynaCell added (24+24 cells, both temps), swell limit tightened to 0.5 mm
3. T9 confirm on textured T2 parts at PVT (final cosmetic surface)
4. T15 target ≥ 99.5% on FW 0.9.x

## Sign-off
Reliability: Dr. H. Wu ✅ 05/07 · Quality: R. Adeyemi ✅ 05/07 · Gate: EVT exit 05/08 (waivers W-01*, W-02) — *W-01 = drop, ISS-023
