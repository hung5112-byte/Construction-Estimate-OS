---
type: project-doc
project: Cyber
section: reliability
tags: [demo, synthetic, mtbf, afr]
last_updated: 06/17/2026
---
# CY-80 — MTBF / AFR Model vs Field Actuals

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Rachel Adeyemi · Dept: [[01-Departments/03-quality-reliability/index|Quality & Reliability]]

## Headline
| Metric | Predicted (NPI) | Field actual (Y2) | Target |
|---|---|---|---|
| MTBF (predicted, parts-count) | 38,000 h | — | — |
| Field AFR (annualized) | 3.2% | **3.9%** | ≤ 3.5% |
| First-year retention (no return) | 96.8% | 96.1% | ≥ 96.5% |

> The model under-predicted AFR because parts-count reliability **does not capture drops and grease** — the two dominant handheld-POS failure mechanisms. Field reality is mechanical/environmental, not electronic.

## AFR glidepath (rolling 3-mo annualized)
| Period | AFR | Inflection |
|---|---|---|
| Y1 Q1 (2025) launch | 6.8% | drop + USB-C + scan haze stacking |
| Y1 Q2 | 5.9% | early drop-education with chains |
| Y1 Q3 | 4.8% | **ECO-CY-031** USB-C cut-in |
| Y1 Q4 | 4.3% | drop-rate plateau |
| Y2 Q1 (2026) | 4.0% | **ECO-CY-039** scan coating |
| Y2 Q2 (current) | **3.9%** | ECO-CY-044 battery; long tail = pre-039 fleet |
| Y2 Q4 (forecast) | 3.5% | retrofit-on-RMA + NTF reduction |

## Failure-mode contribution to AFR
| Mode | Share | Trend | Lever |
|---|---|---|---|
| Display crack (drop) | 27% | flat | bumper durometer, customer drop-education |
| Battery (fade/swell/contact) | 18% | ↓ | ECO-044, capacity-grade, X-ray containment |
| Scan engine (haze/no-read) | 13% | ↓↓ | ECO-039 (closed) + Aurora 2nd source |
| USB-C / charging | 11% | ↓ | ECO-031 (closed) |
| Touch / ghosting | 8% | ↓ | FW 1.8 OTA |
| Payment (EMV/NFC) | 7% | flat | wear item, depot FRU |
| Liquid ingress | 6% | flat | IP54 limit; spill education |
| Audio | 4% | flat | ISS-CY-073 sort |
| NTF / other | 6% | ↓ | FW 1.8 on-device diag |

## Cost linkage
Each 0.5% AFR ≈ **$215k/yr** (repair + advance-exchange freight + refurb churn at 100k/yr). Closing the 3.9% → 3.5% gap (~0.4%) is worth **~$170k/yr** — the financial case for the retrofit-on-RMA + NTF program → [[rma-dashboard]] · [[field-reliability-report]].
