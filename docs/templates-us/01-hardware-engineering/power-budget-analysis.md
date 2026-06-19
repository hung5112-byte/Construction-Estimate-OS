# P-HWE-11: Power Budget Analysis (EE)

#### Description
A rail-by-rail and mode-by-mode power budget — proves the supply, battery life, and thermal headroom claims with numbers, not guesses.

#### Information to collect (ask the user before generating)
1. Product and supply architecture (battery, USB-C PD, dock)?
2. Operating modes (active, idle, sleep, charging) and duty cycles?
3. Major loads per rail (SoC, display, radios, payment, peripherals)?
4. Battery capacity and runtime target?
5. Worst-case ambient and thermal limit?

#### Suggested template
Structure:
- Rail map: source -> regulators -> loads, with efficiency
- Per-mode load table: current/power by block, totals per rail
- Battery-life estimate from duty-cycle weighted average
- Headroom: regulator/connector/PD limits vs. peak
- Risks: peak transients, charging-while-active, derating

Confirm the structure before generating.

#### File-generation prompt
```
Create a Power Budget Analysis (EE).

CONTEXT:
- Product: [model] — Supply: [battery mAh / USB-C PD W / dock]
- Modes + duty cycle: [active/idle/sleep %] — Ambient: [°C]

FORMAT:
- Rail/efficiency map; per-mode load tables with totals
- Battery-life calc with assumptions
- Headroom + risk table with margins (%)

RULES: every load figure carries a source (datasheet typ/max or measurement) [verify]; budgets use worst-case max for thermal and weighted-average for battery life.
```

---
✍️ Author: Brian H. Doan
