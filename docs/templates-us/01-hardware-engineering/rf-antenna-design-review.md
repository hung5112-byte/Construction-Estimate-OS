# P-HWE-31: RF & Antenna Design Review (EE)

#### Description
A review of the wireless subsystem — antenna placement/tuning, RF matching, coexistence, and regulatory test readiness for Wi-Fi/BT/NFC/LTE.

#### Information to collect (ask the user before generating)
1. Radios present (Wi-Fi 6, BT, NFC/contactless, LTE) and antennas?
2. Antenna type/placement and keep-out compliance?
3. Matching network + tuning plan (VSWR target)?
4. Coexistence concerns (Wi-Fi/BT, NFC near metal)?
5. Regulatory targets (FCC Part 15C, SAR if applicable)?

#### Suggested template
Structure:
- Radio/antenna inventory + placement vs. keep-out
- Matching + tuning plan, VSWR/efficiency targets
- Coexistence + isolation strategy between radios
- Contactless/NFC field considerations near metal/battery
- Regulatory test readiness (Part 15C, intentional radiator)

Confirm the structure before generating.

#### File-generation prompt
```
Create a RF & Antenna Design Review (EE).

CONTEXT:
- Radios: [Wi-Fi/BT/NFC/LTE] — Antennas: [type/placement]
- Targets: [VSWR/efficiency] — Regs: [Part 15C/SAR]

FORMAT:
- Inventory + placement review; matching/tuning targets
- Coexistence + NFC-near-metal assessment
- Regulatory readiness checklist

RULES: antenna keep-out and tuning targets (VSWR/efficiency) must be stated; intentional-radiator testing scope cited [verify with lab].
```

---
✍️ Author: Brian H. Doan
