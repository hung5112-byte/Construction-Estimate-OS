---
type: project-doc
project: AMG
section: reliability
tags: [demo, synthetic, reliability, mtbf]
last_updated: 05/15/2026
---
# AMG-100 — MTBF Prediction & AFR Model

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Method: Telcordia SR-332 Issue 4, Method I Case 3, + field-calibrated factors from TS-90 · Author: Dr. Henry Wu

## Headline
- **Predicted MTBF: 62,000 h** (target ≥ 50,000 h) at 35 °C avg internal, restaurant duty 14 h/day
- **Year-1 AFR model: 1.7%** (target ≤ 2.0%) — after infant-mortality screen (factory 4 h burn-in + ORT)
- TS-90 field calibration factor applied: prediction-to-field ratio 0.78 observed on Gen 2 (predictions optimistic) — already baked in above

## Contribution by Subsystem (FIT, calibrated)

| Subsystem | FIT | % of total | Notes |
|---|---|---|---|
| Display + backlight | 3,850 | 23.9% | Largest single block; panel B 2nd source must match |
| Main PCBA (SoC, memory, power) | 3,420 | 21.2% | HDI via fatigue dominated; thermal cycling data good |
| Battery pack | 2,610 | 16.2% | Post-8D: 100% X-ray incoming until PVT; wear-out (not random) dominates after yr 2 |
| Payment module SP-30 | 2,260 | 14.0% | Vendor FIT data + our connector; mostly connector/flex |
| USB-C / charge sub-board | 1,740 | 10.8% | **Why it's a FRU** — wear item by design |
| Speakers/camera/sensors | 1,190 | 7.4% | |
| Mechanical (hinge-free, but gaskets/buttons) | 1,050 | 6.5% | Gasket set; sanitizer aging factor from T9 data |
| **Total** | **16,120 FIT** | | → MTBF = 1/λ ≈ **62,000 h** |

## AFR Curve (model, 25k units yr 1)

| Period | AFR (annualized) | Driver | Expected RMA/month @ 25k fleet |
|---|---|---|---|
| Month 0–3 | 2.4% | Infant mortality residue + install damage | ~50 |
| Month 4–12 | 1.5% | Random failures | ~31 |
| Year 2 | 1.9% | Battery wear begins, connector wear | ~40 |
| Year 3 | 2.6% | Battery + display aging | ~54 |

→ Feeds depot sizing: [[rma-process-dashboard]] (Carlos Mendez) — +1 depot tech by Q1 FY27 per [[../../00-Brain/headcount|headcount]]

## TS-90 Field Baseline (Gen 2 reality check)
| TS-90 failure mode (41,300 fleet) | Share | AMG-100 design answer |
|---|---|---|
| Dock connector wear | 28% | Pogo (30k cyc) replaces blade; dock-side sacrificial pins (ISS-031 in work) |
| Display (backlight, touch) | 22% | Better panel grade; lamination QC at supplier |
| Battery swelling/capacity | 18% | Dual source, X-ray screen, longevity charge mode, 0.5 mm swell ORT limit |
| USB-C board | 12% | Now a 2-min FRU; TVS upgrade |
| Liquid damage | 11% | IP54 front + drain channel (was: none on TS-90) |
| Other | 9% | — |

## Assumptions & limits
Duty 14 h/day, 35 °C internal avg, 0.85 voltage stress factor on power tree. Prediction ≠ guarantee — DVT/PVT PRT + ORT + field trial validate; model refreshed each phase → [[prt-plan]]
