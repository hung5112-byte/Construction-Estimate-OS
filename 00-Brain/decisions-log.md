---
type: brain
section: decisions
aliases: ["Decisions Log", "Decisions", "Decision History"]
last_updated: 06/10/2026
---
# Decisions log (append-only)

> One entry per decision. Do NOT delete or edit old entries.
> ⚠️ SYNTHETIC DEMO DATA — fictional decisions.

## Format
```
### MM/DD/YYYY — [Decision slug]
- Owner: Brian / Dept X
- Decision: ...
- Reason: ...
- Reference: task `02-Tasks/.../`
```

---

### 12/18/2025 — AMG ODM selection: BrightPath Electronics (Bac Ninh, Vietnam)
- Owner: VP + 02-npi-program-management
- Decision: Award AMG-100 to BrightPath (VN) as primary ODM; keep China line (Dongguan) as qualified surge backup only.
- Reason: §301 tariff exposure on China-origin tablets; BrightPath quoted $4.10/unit lower landed cost at 25k/yr and has an existing EMV-capable line. Trade-off: longer ocean lead (32 days Haiphong→Dallas).
- Reference: `04-Projects/Project-AMG/01-PM/charter`

### 02/06/2026 — Payment module: buy (NovaPay SP-30), not build
- Owner: VP + 01-hardware-engineering
- Decision: Integrate NovaPay SP-30 certified payment module instead of in-house secure MCU design.
- Reason: SP-30 carries its own EMV L1/L2 + PCI PTS pre-certs — cuts cert risk ~6 months and ~$220k NRE. Cost adder $11.80/unit accepted within the $142 MP BOM target.
- Reference: [[cert-plan]]

### 04/24/2026 — Battery dual-source mandate after Veltron swelling lot
- Owner: 04-mfg-supplier-quality
- Decision: Qualify DynaCell as second battery source by PVT; no MP gate without two qualified cell sources. Veltron lot VE2605A quarantined (1,200 cells scrapped, $18.4k contingency draw).
- Reason: 8D root cause = electrolyte contamination at Veltron line 3; single-source A-risk unacceptable for 25k/yr ramp.
- Reference: [[capa-8d-AMG-26-004]]

### 05/08/2026 — EVT exit with 2 waivers
- Owner: VP (gate review chair)
- Decision: Exit EVT with waivers W-01 (drop crack at USB-C boss — fix verified at DVT, ISS-023) and W-02 (sanitizer wipe gloss change — cosmetic, spec relaxed from ΔGloss 5 to 8).
- Reason: Both have verified fixes or accepted spec changes; holding EVT would slip DVT build past the BrightPath line slot (next slot +5 weeks).
- Reference: [[schedule-milestones]], [[prt-results-evt]]
