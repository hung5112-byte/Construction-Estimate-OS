---
type: brain
section: cost-library
aliases: ["Cost Library", "Unit Costs", "Historical Costs"]
last_updated: 09/12/2026
label: internal
trust_tier: brain
---
# Cost library policy

The pricing engine resolves unit costs in this order (highest priority first):
1. `03-Cost-Library/*.csv` — Blackland's own buyout history and sub/vendor quotes (columns: `item_code, description, unit, labor, material, equipment, sub, source, quote_date, valid_until, location`)
2. `docs/core/tools/data/unit_costs_seed.csv` — seed library shipped with the engine, national-average placeholders marked **[UNCERTAIN]**
3. No match → the line is carried as `[UNPRICED]` and listed in the report; the engine never invents a price

Every priced line in the estimate cites the row it used (`source` + `quote_date`). Quotes past `valid_until` are flagged for re-quote.

Location factor and escalation come from `benchmarks.md`; markups from `markup-policy.md`.
