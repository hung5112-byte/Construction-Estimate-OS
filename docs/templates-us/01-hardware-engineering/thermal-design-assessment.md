# P-HWE-03: Thermal Design Assessment

#### Description
A thermal budget and risk assessment for a device or design change — dissipation sources, paths, margins, and what must be verified by test. Thermal margins are designed before DVT, not discovered at it.

#### Information to collect (ask the user before generating)
1. Product/enclosure and the operating ambient range?
2. Major heat sources (components + estimated dissipation)?
3. Cooling strategy? (passive conduction, vents, heatsink, none)
4. Component temperature limits that bind? (battery, processor, display)
5. Any field thermal failures or DVT marginals driving this?

#### Suggested template
Structure:
- **Thermal budget table**: source, power (W), path to ambient, est. rise, limit, margin
- **Worst case definition**: ambient, duty cycle, orientation, solar/enclosure load
- **Risk areas**: components with < [X]°C margin; battery charge-temperature window
- **Design measures**: spreading, pads/TIMs, vent strategy, duty-cycle limits in firmware
- **Verification plan**: thermocouple map, soak profile, pass criteria per component
- **Handoffs**: test execution (validation/reliability), enclosure changes (ME), firmware thermal management (FW)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Thermal Design Assessment.

CONTEXT:
- Product: [model] — Ambient range: [min-max °C] — Cooling: [strategy]
- Heat sources: [component: W, ...] — Binding limits: [component: °C]

FORMAT:
- Thermal budget table with margins; worst-case definition
- Risk list ordered by margin; design measures
- Verification plan (instrumentation, profile, pass criteria per component)
- Handoff list

RULES: every margin under 10°C is a named risk with a measure or a test;
battery thermal limits get their own row [verify cell spec].
```

---
✍️ Author: Brian H. Doan
