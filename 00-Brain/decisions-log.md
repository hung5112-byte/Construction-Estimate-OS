---
type: brain
section: decisions
aliases: ["Decisions Log", "Decisions", "Decision History"]
last_updated: 09/12/2026
label: internal
trust_tier: brain
---
# Decisions log (append-only)

> [!note] New decisions are recorded automatically in [[decision-ledger]] at Stop-2 approval. This prose log is history; do not add entries here.
> ⚠️ SYNTHETIC DEMO DATA — fictional decisions of Blackland Commercial Builders (BCB).

### 03/14/2026 — No bid without a documented second-person review
- Owner: Chief Estimator
- Decision: Every estimate goes through the 16-point bid-day gate by someone other than the lead estimator, at least 24 hours before the bid is due.
- Reason: two FY2025 bids lost money on missed addenda and a transposed markup; both would have been caught by a reviewer.
- Reference: `06-estimate-review` charter

### 05/02/2026 — Pricing from our own buyout history first
- Owner: Cost Engineering
- Decision: Unit costs come from `03-Cost-Library/` (our buyouts and quotes) first; published cost data is a fallback and is marked as such on every line.
- Reason: our DFW buyout data beat published national averages by 8–14% on concrete and drywall in FY2025; published data is for sanity checks.

### 07/21/2026 — Escalation and allowances on long-lead electrical gear
- Owner: Cost Engineering + MEP
- Decision: Every switchgear/transformer line carries a named allowance and an escalation line tied to the Turner Building Cost Index until a sub quote with a validity date replaces it.
- Reason: 40–60 week lead times and 5%+ annual escalation; two bids in Q2 were under-carried.
