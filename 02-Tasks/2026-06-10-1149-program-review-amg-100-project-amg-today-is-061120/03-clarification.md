---
type: clarification
answered: false
---

# 🤖 Questions from the system (Brain-first)

> Tick `[x]` for the Department Head's choice, or fill in free text. Save the file.

## Q1 [CRITICAL]
_Cite: 00-Brain/strategy.md_

The Brain records the annual budget as $6.8M with no AMG-100 project allocation and spent_year_to_date as $0. The brief states a $2.0M program ceiling with $111.6k contingency remaining. Before recommending any additional spend: is the $2.0M ceiling formally approved within the $6.8M annual budget, and who has authority to approve spend beyond the remaining $111.6k contingency?

- [ ] A – Yes, $2.0M is board-approved; Department Head can approve contingency drawdowns up to the full $111.6k; anything above requires CFO sign-off
- [ ] B – Yes, $2.0M is approved; but all contingency use requires CFO approval regardless of amount
- [ ] C – The $2.0M ceiling is informal; need to ratify it and define approval authority before this review
- [x] D – Other (please specify)

**Answer (Brian):** The $2.0M program budget is formally approved inside the $6.8M division budget (see 00-Brain/budget.md, Program Budgets table). Authority per the budget guardrails: contingency draws > $25k need CCB approval; any single PO > $50k needs VP (Brian) approval; spend beyond the $2.0M ceiling requires a division-level reallocation approved by Brian. For this review, treat up to +$150k of justified additional spend as approvable — cost is negotiable, quality is not.

## Q2 [CRITICAL]
_Cite: 00-Brain/strategy.md_

The Brain's compliance register lists FCC Part 15 and UL/IEC 62368-1 but omits PCI PTS and EMV (L1/L2) entirely. These are described in the brief as inviolable quality gates. Should PCI PTS and EMVCo L1/L2 be added to the Brain as mandatory regulatory requirements for AMG-100 right now, and is there a designated internal certification owner for each?

- [ ] A – Yes, add both to the Brain immediately; certification owner is already assigned internally
- [ ] B – Yes, add both; but no internal owner exists yet — one needs to be appointed as part of this review
- [ ] C – PCI PTS yes, EMV is handled by the payment-module vendor and does not need a separate internal owner
- [x] D – Other (please specify)

**Answer (Brian):** Add both to the Brain compliance register now. Internal owner exists: Rachel Adeyemi (Quality lead) owns the cert plan with the certification team; Atlas Security Labs is the external PCI/EMV lab. Known gap (00-Brain/headcount.md): no dedicated in-house PCI/EMV compliance engineer — hire planned Q4 FY26. EMV L1/L2 rides the NovaPay SP-30 module pre-certs, but integration-level responsibility stays with Rachel — do NOT treat it as fully vendor-delegated.

## Q3 [CRITICAL]
_Cite: 00-Brain/strategy.md_

The Brain records zero expertise gaps, but the risk register (R-09) identifies a single RF engineer as a named bus-factor risk — meaning if that person is unavailable, RF validation and antenna rework could stall the DVT build on 06/22. What is the approved mitigation: has a backup been identified, and is budget available to engage a contract RF engineer if needed?

- [x] A – A contract RF engineer has already been identified and can be engaged quickly; budget exists
- [ ] B – No backup yet; authorizing a search for a contract RF engineer is part of this review
- [ ] C – The risk is accepted; no mitigation planned
- [ ] D – Other (please specify)

**Note:** Per risk register R-09: contract RF consultant on retainer from 07/01 + cross-training Marcus Lee. Open question for this review: should the retainer start be pulled in BEFORE the 06/22 DVT build (antenna rework window), and what does that cost?

## Q4 [WARN]
_Cite: 00-Brain/strategy.md_

The brief treats the two-qualified-sources rule as an inviolable quality policy, but the Brain contains no supply-chain policy and no definition of what 'qualified' means (for example, whether PPAP or a formal audit is required). Does a written dual-source qualification policy exist somewhere outside the Brain, and should it be added to the Brain so procurement and engineering can apply it consistently?

- [ ] A – Yes, a written policy exists; it should be added to the Brain during this review
- [x] B – No written policy exists; this review should produce one
- [ ] C – The rule is applied case-by-case by the Department Head; formal documentation is not needed
- [ ] D – Other (please specify)

**Note:** Precedents to codify: 04/24/2026 decision (battery dual-source mandate, no MP gate single-sourced — 00-Brain/decisions-log.md) and the AVL 2-sources-on-A-risk practice (bom-evt.md). The policy should define "qualified" (audit + qual lot + PRT leg + ODM AVL listing) — make writing it a deliverable of this review.

## Q5 [WARN]
_Cite: 00-Brain/strategy.md_

The Brain shows AMG-100 margin at 42% at a $329 price point, but the BOM has changed since DVT started (antenna rework, potential eMMC dual-source premium). Is the 42% margin target still valid at mass-production scale, or does it need to be recalculated before ramp gates are set?

- [ ] A – The 42% target is still valid; BOM changes have already been reflected
- [ ] B – The target needs recalculating; a refreshed cost walk should be a deliverable of this review
- [ ] C – Margin target will be revisited only after DVT yields are confirmed
- [x] D – Other (please specify)

**Answer (Brian):** The cost walk (cost-walk.md) is current as of 06/10: MP forecast $142.70 vs target $142 ± 3, with the issue-fix adders (shield can, foam gasket, standoff: +$0.43) already banked. The 42% margin stands on that forecast. The tracked exception is the eMMC broker scenario (ISS-030, +$2.10) — if it activates at the PVT checkpoint, refresh the cost walk and re-state margin at that point. No full recalculation needed now.

## Q6 [WARN]
_Cite: 00-Brain/strategy.md_

The Brain's ICP profile requires fleet uptime above 99.5%, but records no minimum MTBF or AFR (annual failure rate) that the ICP contract or sales commitments actually require. The brief uses 2.0% AFR as the pass/fail threshold. Is the 2.0% AFR target a hard contractual SLA with customers, an internal engineering target, or something else — and does it need to be added to the Brain as a formal ICP requirement?

- [ ] A – It is a hard contractual SLA already committed to customers; add it to the Brain
- [ ] B – It is an internal engineering target only; no customer contract references it
- [x] C – It is referenced in sales materials but not yet a signed contractual obligation
- [ ] D – Other (please specify)

**Note:** 2.0% AFR is the internal year-1 target communicated to the anchor chains; warranty/SLA contract language is being finalized (due 08/01 per rma-process-dashboard.md). Add it to the Brain as a formal ICP requirement when the warranty terms are signed — and flag in this review if any improvement action would jeopardize meeting it.
