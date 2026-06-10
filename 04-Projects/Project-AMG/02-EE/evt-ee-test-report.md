---
type: project-doc
project: AMG
section: ee
tags: [demo, synthetic, ee, report]
last_updated: 05/06/2026
---
# AMG-100 — EVT EE Test Report (summary)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Rev A, 20 bench units, FW 0.8.5 · Test window 03/30–04/30/2026 · Author: David Chen

## Verdict: **CONDITIONAL PASS** — 3 fails carried as ISS-014 / ISS-025 / game-mode power, all with DVT fixes

## Results Matrix

| # | Test | Spec | Result | P/F |
|---|---|---|---|---|
| 1 | Power-on/boot (1,000 cycles × 5 units) | 0 failures | 2 failures (ISS-007, eMMC timing) → fixed FW 0.8.2, re-run clean | ✅ after fix |
| 2 | Rail sequencing & ripple | per PMIC spec | All rails within ±3% | ✅ |
| 3 | Power budget by use case | → [[power-budget]] | Game mode −0.42 W over | 🟡 FW 0.9 tune |
| 4 | Display: luminance/uniformity | 400 nits ±10%, uniformity > 80% | 412 nits avg, 84% | ✅ |
| 5 | Touch: linearity, 10-pt, wet-finger | < 1.5 mm error | 1.1 mm; ghosting > 45 °C → ISS-019 | 🟡 |
| 6 | Wi-Fi conducted TX/RX all rates | per MT7921 spec | Conducted ✅ | ✅ |
| 7 | **Wi-Fi OTA (TIS/TRP)** | TRP ≥ 14 dBm 5 GHz | **11.8 dBm — antenna detuned by metal trim → ISS-014** | ❌ fix in DVT |
| 8 | BT range | ≥ 10 m | 14 m | ✅ |
| 9 | NFC field strength (4 corners + center) | ISO 14443 class | All positions pass, 1.2× min field | ✅ |
| 10 | EMV L1 contact pre-test (lab) | per EMVCo | Pass (module pre-cert held) | ✅ |
| 11 | **EMC radiated pre-scan** | FCC 15B Class B | **5.8 GHz harmonic +1.2 dB → ISS-025** | ❌ fix in DVT |
| 12 | ESD bench (±4 kV pre-test) | no reset | 1 soft reset at 4 kV on USB-C — TVS swap rev B | 🟡 |
| 13 | Audio: SPL/THD | 78 dB SPL @ 0.5 m, THD < 1% | 79 dB; buzz at max vol → ISS-027 (mech) | 🟡 |
| 14 | Camera: QR decode speed | < 800 ms @ 200 lux | 620 ms | ✅ |
| 15 | USB-C PD matrix (12 chargers) | all negotiate | 2 fails → ISS-016 fixed, re-run clean | ✅ after fix |
| 16 | Battery: capacity & 200-cycle | ≥ 4,900 mAh; no swell | Capacity ✅; **3 cells swell lot VE2605A → ISS-021/8D** | 🟡 contained |
| 17 | Thermal imaging at max load | no comp > derate | PMIC hotspot 92 °C (limit 105) | ✅ |
| 18 | Current leakage (off/ship) | ≤ 80 µW | 62 µW | ✅ |

## Defect Pareto (bench, 20 units)
Touch cal drift (4) · Wi-Fi cal variance (3) · cosmetic (2) · boot (2, fixed) · audio buzz (1) — feeds factory test plan → [[factory-yield-evt]]

## Sign-off
- EE lead: David Chen ✅ 05/06 · Quality: Rachel Adeyemi ✅ 05/07 (conditions logged) · Gate: EVT exit 05/08 with waivers → [[00-Brain/decisions-log|decisions log]]
