---
type: project-doc
project: Cyber
section: pm
tags: [demo, synthetic, minutes]
last_updated: 06/04/2026
---
# Project Cyber — Monthly MP Review (06/04/2026)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Chair: Brian H. Doan · Scribe: Daniel Reyes
> Attendees: Reyes, Nair, Becker, Mehta, Adeyemi, Lim (G), Lim (W, remote Penang), Ali, Mendez, Ramirez

## 1. Production & supply (Wei Lim / Grace Lim)
- May output 8,410 units (plan 8,300) — ahead, build-ahead buffer for Q4 peak started. FPY 94.5% (May), best month yet.
- **Scan-engine 2nd source:** Aurora AX-20 qual lot built into 200 units, now in ORT. Read-rate parity confirmed at incoming; aim-stability data due 07/2026. *Action (Grace): ORT interim report by 07/10.*
- UFS allocation: Kioxia confirmed firm through Q1 2027 only. Decision needed on LTB vs SanDisk transition. *Action (Daniel): LTB cost model to Brian by Q3.*

## 2. Field quality & RMA (Sofia Ramirez / Carlos Mendez)
- Rolling AFR **3.9%** (was 4.0% Apr) — glidepath to 3.5% on track but slowing; pre-ECO-039 fleet is the long tail.
- Pareto unchanged: display-crack #1 (27%), battery #2 (18%), scan haze #3 (13%, declining).
- Depot TAT 2.4 d 🟢; NTF 9% 🟡 — new on-device diag code (FW 1.8) expected to pull NTF under 8%. *Action (Mendez): NTF re-measure after FW 1.8 fleet hits 60%.*
- **ISS-CY-070** DynaCell DC2611 swell: 4 returns, contained, 100% X-ray live. No safety incidents. Quanex 2nd-source cells in qual.

## 3. Engineering / ECO (Priya Nair / Raj Mehta)
- Cost-down at $151.20; Crystalview display 2nd-source qual on track for Q3 → $148 path holds.
- **ISS-CY-064** CY-80L thermal throttle: FW 1.8.3 governor retune in field beta at 2 DC sites; graphite-pad ECO-CY-051 under eval if FW insufficient.
- **ISS-CY-066** contactless ghosting: OTA touch-FW fix in ring 2, ~40% fleet, no regressions.

## 4. Decisions
| # | Decision | Owner |
|---|---|---|
| D-1 | Approve Aurora AX-20 ORT spend ($22k, under CCB threshold) | Daniel |
| D-2 | Hold proactive recall on scan haze — retrofit-on-RMA only (cost/benefit favors) | Brian |
| D-3 | Pre-build +400 CY-80R refurb units before Oct retail peak (R-06) | Carlos |
| D-4 | Greenlight Gen-1.5 refresh **study** (no NRE commit yet) | Brian |

## 5. Risks moved
- R-02 (scan single-source) stays 🔴 until Aurora ORT clears — top program risk.
- R-04 (UFS/SoC EOL) raised to 🔴 12 — LTB decision now on critical path → [[risk-register]].

## Next review: 07/02/2026 · Pre-reads: ORT interim, LTB cost model, AFR glidepath → [[monthly-dashboard-2026-05]]
