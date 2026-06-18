---
type: project-doc
project: Cyber
section: bom
tags: [demo, synthetic, bom]
last_updated: 06/17/2026
---
# CY-80 — Bill of Materials (MP current, rev D)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Priya Nair / Daniel Reyes · @ 100k/yr · USD

## BOM summary
| Category | Cost | % of BOM |
|---|---|---|
| Compute (SoC, memory) | $34.10 | 22.6% |
| Display + touch | $31.40 | 20.8% |
| Payment module (NovaPay SP-25) | $19.80 | 13.1% |
| Scan engine (Helios N4200) | $14.60 | 9.7% |
| Battery (5,000 mAh) | $9.20 | 6.1% |
| Mechanical / housing / cradle IF | $13.90 | 9.2% |
| RF / connectivity (Wi-Fi/BT, LTE n/a base) | $8.70 | 5.8% |
| PCBA / passives / connectors | $11.30 | 7.5% |
| Camera (13MP + 5MP) | $4.80 | 3.2% |
| Misc (flex, speaker, mic, packaging IF) | $3.40 | 2.2% |
| **Total MP BOM (rev D)** | **$151.20** | 100% |

## Line items (key)
| Item | Part / vendor | Cost | Source status |
|---|---|---|---|
| SoC | Qualcomm QCM6125 | $21.40 | Single (EOL watch 2027, R-04) |
| Memory | 4GB LPDDR4X + 64GB UFS (Kioxia) | $12.70 | UFS dual-qual SanDisk (R-04) |
| Display | 8.0" WUXGA, Optera | $24.10 | Crystalview 2nd-source qual (ECO-048) |
| Touch | GG5 + bonded digitizer | $7.30 | Dual |
| Payment | NovaPay SP-25 (EMV+NFC+MSR) | $19.80 | Single (PCI-locked) |
| Scan engine | Helios N4200 2D imager | $14.60 | **Single — Aurora AX-20 qual (R-02)** |
| Battery | DynaCell DC-50 / Quanex QX-50 | $9.20 | Dual ✅ |
| Wi-Fi/BT combo | QCA M.2 | $5.10 | Dual |

## CY-80L (LTE) delta
| Add | Cost |
|---|---|
| 4G LTE Cat-4 module + eSIM + antenna | +$16.40 |
| CY-80L total BOM | $167.60 |

## Sourcing posture
- **2 dual-sourced, 3 single-source** of the high-value items. The two single-source items that matter: **scan engine** (active 2nd-source, R-02) and **SoC** (EOL/LTB, R-04). Payment is single by design (cert-locked).
- Full cost-down narrative and trajectory → [[cost-walk]]
