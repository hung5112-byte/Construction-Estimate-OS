# P-HWE-16: Battery & Charging Design Review (EE)

#### Description
A focused review of the battery, charger, protection, and thermal behavior — the highest-liability subsystem in a portable device (safety, recalls, airline rules).

#### Information to collect (ask the user before generating)
1. Cell chemistry, capacity, and supplier; pack or single cell?
2. Charger IC, input source (USB-C PD), and charge profile?
3. Protection scheme (fuel gauge, PCM, OVP/OCP/thermal)?
4. Hot-swap or removable battery?
5. Applicable safety standards (UL 2054/62133, UN 38.3 transport)?

#### Suggested template
Structure:
- Architecture: source -> charger -> protection -> cell + gauge
- Charge profile + thermal limits (charge/discharge, ambient)
- Protection coverage matrix: over/under V, over-current, over-temp, short
- Safety/transport compliance plan (62133, UN 38.3)
- Failure analysis: connector intermittency, swell, thermal runaway mitigations

Confirm the structure before generating.

#### File-generation prompt
```
Create a Battery & Charging Design Review (EE).

CONTEXT:
- Cell: [chem/mAh/supplier] — Charger: [IC] — Source: [USB-C PD W]
- Protections: [...] — Standards: [UL/IEC/UN 38.3]

FORMAT:
- Architecture diagram description; charge/thermal profile
- Protection coverage matrix; compliance plan
- Failure-mode + mitigation table

RULES: protection coverage must be complete for over-V, under-V, over-current, over-temp, and short before approval; cite safety/transport standards [verify with lab].
```

---
✍️ Author: Brian H. Doan
