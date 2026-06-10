### PROMPT 06: Refund & Warranty Policy

#### Description
A refund and warranty policy — conditions, process, timeframes, responsibilities, exceptions. Used both internally (CS team follows it) and published to customers (website, contracts). General information only — not legal advice; have a licensed Texas attorney review.

> US legal note: the relevant US frameworks are the **Magnuson-Moss Warranty Act** (15 U.S.C. §2301, federal rules for consumer-product written warranties), **UCC implied warranties** of merchantability/fitness (Tex. Bus. & Com. Code ch. 2), the **FTC Act** (truthful representations, 15 U.S.C. §45), and the **Texas Deceptive Trade Practices-Consumer Protection Act (DTPA)** (Tex. Bus. & Com. Code §17.41 et seq.). There is no general federal "mandatory refund window," but the **FTC Cooling-Off Rule** gives 3 days to cancel certain door-to-door / off-premises sales of $25+ (16 CFR Part 429) [verify applicability]. A clearly posted refund policy is generally enforceable — but it must not be deceptive.

#### Information to collect (ask the user before generating)
1. Do products/services have a warranty? Term?
2. Current refund conditions? (within 7 days / 30 days / no refund)
3. Refund method? (cash / bank transfer / store credit / exchange)
4. Who approves a refund? Approval limit?
5. Any exceptions? (sale items, custom, digital...)
6. Which consumer-protection laws apply? (FTC; Texas DTPA; Magnuson-Moss)

#### Suggested template
Structure:
- **Refund policy**: conditions, timeframe, process, method, processing timeline
- **Warranty policy**: scope, term, what voids it, claim process (consistent with Magnuson-Moss for consumer products)
- **Returns/exchanges**: conditions, timeframe, shipping cost
- **Exceptions**: cases where the policy doesn't apply (disclose clearly to avoid DTPA issues)
- **Responsibilities**: company vs. customer
- **Legal basis**: FTC Act, Texas DTPA, Magnuson-Moss, UCC implied warranties

Confirm the structure before generating.

#### File-generation prompt
```
Create a Refund & Warranty Policy.

CONTEXT:
- Company: [Name] — Products/services: [list]
- Warranty: [term] — Scope: [describe]
- Refund: [conditions] — Timeframe: [days]
- Refund method: [cash / transfer / store credit / exchange]
- Refund approval: [who] — Limit: [USD]
- Exceptions: [list]
- Authority: FTC Act (15 U.S.C. §45); Texas DTPA (Tex. Bus. & Com. Code §17.41); Magnuson-Moss (15 U.S.C. §2301); UCC implied warranties (Tex. Bus. & Com. Code ch. 2)

FORMAT:
- Refund policy: table Condition | Timeframe | % refund | Method | Processing timeline
- Warranty policy: table Product | Warranty term | Scope | What voids it | Claim process
- Refund process: Mermaid flowchart — Request → Check conditions → Approve → Process → Complete
- Warranty claim process: flowchart — Report defect → Verify warranty → Repair/Replace → Return
- Exception list: Case | Reason not covered | Alternative
- Customer-facing version: a short, friendly version postable to the website (clear, not deceptive)
- Internal version: full version — incl. approval limits, escalation

TONE: Clear, fair, protects both customer and company.
LENGTH: 4-6 pages.

NOTE: General information, not legal advice. Have a licensed Texas attorney review; ensure the policy is not deceptive under the FTC Act/DTPA.
```

---
✍️ Author: Brian H. Doan
