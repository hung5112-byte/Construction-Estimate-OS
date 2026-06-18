---
type: project-doc
project: Cyber
section: quality
tags: [demo, synthetic, capa, 8d]
last_updated: 06/17/2026
---
# 8D / CAPA CY-26-007 — Scan-Engine Window Haze (Helios N4200)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Champion: Rachel Adeyemi · SQE: Grace Lim · Dept: [[01-Departments/03-quality-reliability/index|Quality & Reliability]] + [[01-Departments/04-mfg-supplier-quality/index|MSQ]]
> Status: **Closed (D8) 03/2026** — verification ongoing via [[ort-plan|ORT]]

## D1 — Team
Rachel Adeyemi (champion), Grace Lim (SQE), Priya Nair (EE), Tom Becker (ME/optics), Sofia Ramirez (field FA), Wei Lim (ODM), Helios SQE (supplier).

## D2 — Problem
Barcode **no-read / slow-decode** complaints rising from QSR sites ~9 months in service. FA: a **hazy/oily film on the scan window** scattering the aimer and degrading decode. Field return code SCAN-NR climbed to **19% of confirmed failures** (Y1 Q4) before action.

## D3 — Containment (interim)
- Depot: clean-and-verify step added; window replacement on any SCAN-NR RMA
- Field: cleaning-cloth + SOP card shipped to top-5 QSR chains
- Production: incoming window inspection tightened

## D4 — Root cause
1. **Occurrence:** original window had no oleophobic coating; airborne fryer grease + repeated wipe cycles etched a haze (confirmed by lab grease-soak reproducing field haze → [[ort-plan]]).
2. **Escape:** ORT grease-soak duration too short at NPI to surface a 9-month mechanism; spec gap, not a process defect.

## D5 — Permanent corrective action
- **ECO-CY-039:** oleophobic anti-smudge coated scan window + recessed protective lip (reduces wipe abrasion). Cut-in 02/2026, line-break SN logged in PLM.
- Helios supplier change-note accepted; coating adhesion spec added to incoming.

## D6 — Validation
- ORT extended grease-soak (4× duration) + 250k decode: **recurrence < 0.3%** on post-ECO units
- Field: SCAN-NR share fell 19% → **13% and declining** as pre-039 fleet ages out → [[mtbf-afr-model]]

## D7 — Prevent recurrence (systemic)
- ORT spec library updated: **environmental-soak duration must cover ≥ 12-month field exposure** for optical/sealed surfaces — applied to Aurora AX-20 2nd-source qual too
- DFMEA item #3 Detection improved; quarterly field-pareto → DFMEA review instituted → [[dfmea-top-items]]

## D8 — Closure & residual
- Closed 03/2026. **Residual:** pre-ECO-039 fleet (~built before 02/2026) still carries the old window — handled by **retrofit-on-RMA** (ISS-CY-061), no proactive recall (cost/benefit, decided 06/04 → [[meeting-minutes-2026-06-04]]).
- Note: this 8D number also tracks the **battery-swell containment model** reused for ISS-CY-070 (DynaCell DC2611) — same X-ray/quarantine playbook.
