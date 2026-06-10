# P-HWE-07: Architecture Trade-off Study

#### Description
A decision document comparing 2-3 architecture options for a platform-level choice (SoC family, connectivity approach, partitioning, reuse strategy). Optimizes for the product family and the roadmap, names the binding assumption, and tags reversibility.

#### Information to collect (ask the user before generating)
1. The decision at stake, and how many products it affects?
2. Options on the table (2-3)?
3. Decision criteria and weights? (cost, power, schedule, cert scope, supply risk, reuse)
4. Roadmap context from the Brain? (markets, volumes, next products)
5. What deadline forces the decision?

#### Suggested template
Structure:
- **Decision framing**: what's being decided, for which products, by when, reversibility (cheap-to-change vs. locked-in)
- **Options**: per option — description, BOM cost delta, power, schedule impact,
  certification scope impact [verify with certification], supply risk, reuse value
- **Comparison matrix**: criteria × options, weighted if useful
- **Recommendation**: the pick + the key assumption that would change it
- **Consequences**: what each team inherits (EE/ME/FW work, sourcing changes, cert programs)
- **Decision record**: approver, date → entry for `decisions-log.md`

Confirm the structure before generating.

#### File-generation prompt
```
Create an Architecture Trade-off Study.

CONTEXT:
- Decision: [statement] — Products affected: [list] — Deadline: [date]
- Options: [A/B/C summaries] — Criteria: [list with weights]

FORMAT:
- Framing with reversibility tag; option sections with the six standard lenses
  (cost/power/schedule/cert/supply/reuse)
- Comparison matrix; recommendation + binding assumption
- Per-team consequences; decision record block

RULES: exactly one recommendation; the assumption that would flip it is stated;
certification scope impact is verified, not guessed.
```

---
✍️ Author: Brian H. Doan
