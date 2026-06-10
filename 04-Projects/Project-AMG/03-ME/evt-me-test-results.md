---
type: project-doc
project: AMG
section: me
tags: [demo, synthetic, me, report]
last_updated: 05/05/2026
---
# AMG-100 — EVT ME Test Results (drop / thermal / environmental)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · 12 PRT units, rev A housings (T0 parts) · Author: Miguel Torres, with Dr. Henry Wu

## Verdict: **CONDITIONAL PASS** — drop fail at USB-C boss (ISS-023, fixed in T1 mod); sanitizer gloss waiver W-02

## Drop Test (1.0 m onto vinyl-over-concrete, 26-drop sequence, 8 units)
| Orientation group | Units cracked | Functional fail | Notes |
|---|---|---|---|
| Faces (6) | 0 | 0 | |
| Edges (12) | 0 | 0 | |
| **Corners (8)** | **3 of 8 — crack at USB-C boss, front housing** | 0 (cosmetic-structural) | Stress concentration at boss web; ISS-023 → rib + radius, T1 mod verified 10-shot 05/20 |
- Glass: zero fractures (AG ion-exchange OK at 1.0 m)
- Retest plan: full 26-drop on 8 DVT units with T1-mod housings → [[prt-plan]]

## Tumble (0.5 m, 300 tumbles, 2 units)
- Pass — corner scuffs within cosmetic spec, no functional loss

## Thermal
| Test | Spec | Result |
|---|---|---|
| Operating sweep | 0–40 °C full function | ✅ (touch ghost at 45 °C = beyond spec, logged ISS-019 for robustness) |
| Storage | −20 to +60 °C, 96 h | ✅ |
| Thermal shock | −20↔60 °C, 50 cycles | ✅ no delamination, no gasket set |
| Skin temp | ≤ 43 °C @ 25 °C amb | 41.2 °C ✅ (governor handles 40 °C amb case → [[power-budget]]) |

## Environmental (restaurant-specific)
| Test | Spec | Result |
|---|---|---|
| Spill: 60 ml soda poured on face, powered | No ingress to electronics, full function after wipe | ✅ IP54 front gasket held; liquid channel drains clear of USB-C |
| Spill: 60 ml water into dock pocket | Dock survives, no tablet damage | ✅ |
| **Sanitizer wipe (quat + 70% IPA alternating, 10,000 cycles)** | No cracking; ΔGloss ≤ 5 | **ΔGloss = 6.8 on rear housing** → no cracking/embrittlement; **waiver W-02**: spec relaxed to ≤ 8 (cosmetic only, matte texture masks it) → [[00-Brain/decisions-log\|log]] |
| Humidity 85 °C/85 %RH, 168 h, powered | Full function | ✅ minor label adhesive lift — label spec changed (3M 7872) |
| UV (indoor window, 500 h equiv) | ΔE ≤ 3 | ΔE 1.9 ✅ |

## Mechanical durability
| Test | Spec | Result |
|---|---|---|
| Button life (vol/svc) | 200k cycles | ✅ 200k, force change −8% (limit −20%) |
| USB-C insertion | 10k cycles | ✅ retention within spec |
| Dock pogo insertion | 30k cycles | 🟡 wear marks at 5k on dock pins (tablet side OK) → ISS-031 |
| Torsion/bend (handheld carry) | 5 N·m, no creak/crack | ✅ |
| Stand fatigue (25 N push × 50k) | no loosening | ✅ |

## Sign-off
ME: Miguel Torres ✅ 05/05 · Reliability: Dr. Henry Wu ✅ 05/05 · Carried items: ISS-023 (verify DVT), ISS-031, W-02 waiver
