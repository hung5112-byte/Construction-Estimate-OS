---
type: project-doc
project: AMG
section: quality
tags: [demo, synthetic, quality, yield]
last_updated: 05/10/2026
---
# AMG-100 — EVT Build Yield & Defect Pareto

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · EVT build 03/23–03/27, 50 units, BrightPath line 2 · Owner: Omar Haddad (MfgE) + factory-test-yield team [[../../01-Departments/04-mfg-supplier-quality/index|MSQ]]

## Headline
- **FPY (all stations): 78.0%** (39/50 first-pass) — normal for EVT; DVT target ≥ 88%, PVT ≥ 92%, MP ≥ 95%
- RTY after rework: 96.0% (48/50 shipped to test allocation; 2 units became teardown donors)
- SMT yield (AOI+SPI): 99.2% defect-free boards — strong start

## Station-by-Station FPY

| Station | Tested | Fail | FPY | Top failure |
|---|---|---|---|---|
| SPI/AOI (SMT) | 52 boards | 4 | 92.3% | Paste insufficient on shield pads (2), tombstone 0402 (2) |
| ICT (bed-of-nails) | 52 | 1 | 98.1% | Open on J7 flex connector (workmanship) |
| FW download + boot | 50 | 2 | 96.0% | eMMC timing (ISS-007 — fixed FW 0.8.2) |
| **Touch calibration** | 50 | **4** | **92.0%** | Cal drift after lamination relax — cal moved post-aging in DVT plan |
| **Wi-Fi/BT cal + test** | 50 | **3** | **94.0%** | TX power variance — golden-unit method replaces scalar limits in DVT |
| Camera/audio test | 50 | 1 | 98.0% | Speaker buzz threshold (ISS-027) |
| Payment module pairing | 50 | 0 | 100% | — |
| FATP functional | 50 | 1 | 98.0% | Button flex misrouted (workmanship, SOP photo added) |
| Cosmetic OQC (grade B for EVT) | 50 | 2 | 96.0% | Bezel scuff from fixture — fixture relined ✅ |
| **Cumulative FPY** | | | **78.0%** | |

## Pareto of all defects (n=18)
1. Touch cal drift — 4 (22%) → **fix: cal after 24 h aging, DVT**
2. Wi-Fi cal variance — 3 (17%) → **fix: golden-unit + fixture RF cal daily, DVT** (new RF cal fixture $12k → [[budget-tracker]] ws7)
3. SMT paste/passives — 4 (22%) → stencil aperture + nozzle change ✅ done
4. Workmanship (flex routing) — 2 (11%) → SOP photos + jig
5. Cosmetic handling — 2 (11%) → fixture relining ✅
6. Boot/eMMC — 2 (11%) → FW fixed ✅
7. Audio — 1 (6%) → mech fix in DVT

## DVT yield plan (to hit ≥ 88%)
Modeled FPY with fixes: touch 97% × Wi-Fi 97.5% × SMT 99.5% (station-level) → cum ~89–91% ✅ plausible. Risks: new antenna rework step (line-side, first 40 units) adds an operation — temporary station with dedicated QC gate; tracked in DVT build readiness review 06/12 → [[meeting-minutes-2026-06-05]]

## Test time (cost input → [[cost-walk]])
EVT total test time 14.2 min/unit → MP target 8.4 min (parallel RF cal, cut soak from 30→12 min with data) — worth −$1.10/unit conversion
