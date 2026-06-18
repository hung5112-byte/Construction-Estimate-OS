---
type: project-doc
project: Cyber
section: reliability
tags: [demo, synthetic, ort, reliability]
last_updated: 06/17/2026
---
# CY-80 — Ongoing Reliability Test (ORT) Plan

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Rachel Adeyemi · Dept: [[01-Departments/03-quality-reliability/index|Quality & Reliability]]

## Purpose
In mass production, PRT becomes **ORT** — a continuous pull from the line to catch drift, validate ECOs and 2nd sources, and correlate to field AFR. CY-80 ORT pulls **30 units/month** from Meridian production + dedicated qual lots for source changes.

## Standing ORT suite (monthly pull, 30 units)
| Test | Condition | Pass criteria |
|---|---|---|
| Drop | 1.2 m × 26 faces to concrete | No display crack, functional |
| Tumble | 0.5 m, 500 tumbles | Cosmetic only |
| Thermal cycle | −10 → 60 °C, 50 cyc | No solder/contact failure |
| Humidity / spill | IP54 re-verify + spill panel | No ingress to payment/scan |
| Battery cycle | 500 cyc to 80% | No swell, ≥ 80% capacity |
| Scan endurance | 250k decodes + grease soak | Read rate ≥ 99%, no haze |
| Connector cycle | USB-C 10k, pogo 30k | Within contact-R spec |
| Payment endurance | EMV 50k insertions, NFC | Read rate, no tamper trip |

## ECO / 2nd-source qual lots (event-driven)
| Lot | Purpose | Status |
|---|---|---|
| Aurora AX-20 scan engine (200 u) | 2nd-source qual (R-02) | 🟡 In ORT — aim-stability data 07/2026 |
| Crystalview display (120 u) | 2nd-source qual (ECO-048) | 🟡 Optical + drop subset running |
| Quanex battery (DC vs QX) | cell 2nd-source parity | 🟢 Passed cycle, monitoring swell |
| ECO-CY-051 graphite pad | thermal margin (ISS-CY-064) | ⚪ Queued behind FW-first |

## Field-correlation loop
ORT results are correlated monthly against field returns ([[mtbf-afr-model]]). Two correlations drove action this year:
1. **Scan haze**: lab grease-soak reproduced the field haze → confirmed ECO-CY-039 coating fixed it (recurrence < 0.3%).
2. **Battery swell**: ORT cycle flagged the DynaCell DC26xx lot variance **before** field volume grew → 100% X-ray containment (ISS-CY-070).

## Open ORT actions
- Aurora aim-stability + decode-margin report → gate for ECO-CY-052 release (Rachel + Grace, 07/2026)
- Add "aged-cell capacity grade" to ORT to back the FW 1.9 capacity-report feature
