---
type: clarification
answered: true
---

# 🤖 Questions from the system (Brain-first)

> Tick `[x]` for the Department Head's choice, or fill in free text. Save the file.

## Q1 [WARN]
_Cite: 00-Brain/products.json:AMG100.status = DVT_

The AMG-100 is in DVT (00-Brain/products.json:AMG100.status). Is a component cost-down at this stage acceptable, given it could disrupt final qualification testing?

- [ ] Yes, we accept the risk and will re-run affected DVT test cases
- [ ] No, cost-down should wait until after DVT exit and MP readiness
- [x] Only if limited to form/fit/function equivalent parts, no new DVT required

## Q2 [CRITICAL]
_Cite: 00-Brain/laws.json_

Given that any BOM change could trigger re-certification under FCC Part 15, UL/IEC 62368-1, or UN 38.3 (00-Brain/laws.json), which regulatory impact is the business willing to accept?

- [x] None — all cost-down changes must maintain existing certifications without retesting
- [ ] We will absorb re-testing cost and schedule delay if needed
- [ ] Non-RF, non-safety changes only (e.g., mechanical brackets, fasteners)
- [ ] We need regulatory to pre-screen every candidate part before sourcing

## Q3 [CRITICAL]
_Cite: 00-Brain/strategy.json:icp.pain_points[2]_

The AMG-100 ICP requires survival in harsh environments — spills, sanitizer chemicals, 24/7 duty cycle (00-Brain/strategy.json:icp.pain_points[2]). What is the minimum environmental reliability threshold that must not be degraded?

- [x] IP rating (e.g., IP54) and chemical resistance must be unchanged from current BOM
- [ ] We can relax from IP54 to IP53 if cost saving is substantial
- [ ] Duty cycle (24/7) is non-negotiable; ingress protection has some margin
- [ ] Let engineering define acceptable trade-offs and we approve exceptions case-by-case

## Q4 [CRITICAL]
_Cite: 00-Brain/strategy.json:icp.profile_

The ICP values payment security and PCI compliance (00-Brain/strategy.json:icp.profile). Will any cost-down candidate touching the payment module, secure element, or tamper-detection circuitry be automatically rejected?

- [ ] Yes — no changes to PCI-affecting components or security architecture
- [ ] We will allow if PCI lab confirms recertification is not required
- [x] PCI domain is off-limits for this cost-down; target other BOM lines
- [ ] Not yet decided — need PCI security architect to define the boundary

## Q5 [WARN]
_Cite: 00-Brain/strategy.json:icp.profile_

The ICP requires predictable supply (00-Brain/strategy.json:icp.profile). How do we ensure cost-down part swaps don't introduce lead-time risk or single-source dependency?

- [x] Every alternate part must have a qualified second source with confirmed lead time
- [ ] Cost-down is approved only for multi-source commodity parts (passives, interconnects)
- [ ] Supply chain team must pre-approve any new supplier before Engineering finalizes BOM
- [ ] We will accept minor lead-time risk if the part cost reduction is >$0.30/unit

## Q6 [CRITICAL]
_Cite: 00-Brain/brief.md_

How will we validate 'no performance regression' for CPU/GPU/UI/boot/payment speed after a BOM change? What gates are required?

- [ ] Run standard OS image benchmark suite; pass/fail against today's DVT baseline
- [x] Regression test every cost-down SKU through full system validation (boot, payment, UI lag)
- [ ] Benchmark only if the part change is in a compute-adjacent domain (e.g., PMIC, memory)
- [ ] Engineering proposes the validation plan and we approve per change

## Q7 [WARN]
_Cite: 00-Brain/laws.json_

The $0.50 cost-down target is ambiguous — is it per-tablet ex-factory BOM cost, or landed cost including logistics and tariffs (00-Brain/laws.json)?

- [ ] Ex-factory BOM cost only
- [x] Landed cost (BOM + freight + duty + tariffs)
- [ ] Total cost of goods sold (COGS) including manufacturing labor and warranty accrual
