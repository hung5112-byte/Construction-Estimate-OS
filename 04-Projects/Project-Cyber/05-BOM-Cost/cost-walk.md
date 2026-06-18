---
type: project-doc
project: Cyber
section: bom
tags: [demo, synthetic, cost]
last_updated: 06/17/2026
---
# CY-80 — Cost Walk ($168.90 → $151.20 → $148 target)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Daniel Reyes / Priya Nair · @ 100k/yr

## Cost trajectory
| Stage | BOM | Driver |
|---|---|---|
| SOP (02/2025) | $168.90 | Launch pricing, single sources, low volume |
| Year-1 exit (02/2026) | $156.40 | Volume tier breaks, SoC erosion, passives consolidation |
| **Current (rev D, 06/2026)** | **$151.20** | Battery dual-source, memory re-quote, mech re-source |
| Target (Q3 2026) | $148.00 | Display dual-source (Crystalview), further SoC erosion |

## Cost-down walk (SOP → today, −$17.70)
| Lever | $/unit | Notes |
|---|---|---|
| SoC price erosion (volume + roadmap) | −$4.20 | QCM6125 standard curve |
| Display volume tier + yield | −$3.60 | Optera tier-3 break at 100k |
| Memory re-quote (UFS/LPDDR) | −$2.90 | Kioxia annual + spot blend |
| Battery dual-source (Quanex tension) | −$1.80 | Competitive 2nd source |
| Mechanical re-source (housing, TPU) | −$2.40 | Local Penang molder qualified |
| Passives / connector consolidation | −$1.60 | rev C/D BOM scrub |
| Packaging optimization | −$1.20 | Recyclable tray, fewer SKUs |

## Path to $148 (−$3.20 remaining)
| Lever | $/unit | Status |
|---|---|---|
| Display 2nd source (Crystalview) | −$2.10 | 🟡 Qual Q3 (ECO-CY-048) |
| SoC next price step | −$0.70 | 🟢 Contracted |
| Scan engine 2nd source competitive tension (Aurora) | −$0.40 | 🟡 Pending qual (R-02) |

## What we will NOT touch
- Payment module (PCI-locked, single-source by design)
- Drop/seal-critical mechanical content — **no reliability-negative cost-down**. Year-1 taught the lesson: the corner bumper and display bond line are off-limits. A $0.30 saving that adds 0.2% AFR costs ~$86k/yr in warranty — a losing trade. This rule is the reason the AFR glidepath and cost-down can run in parallel → [[field-reliability-report]].

## Economic context
At 100k/yr, the realized $17.70 cost-down since SOP returns **~$1.77M/yr**. Reaching $148 adds ~$320k/yr. Finance view → [[00-Brain/budget|division budget]].
