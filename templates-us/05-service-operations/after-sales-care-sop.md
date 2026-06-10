### PROMPT 03: After-Sales Care SOP

#### Description
A process to care for customers after a purchase/contract — follow-up schedule, satisfaction check, upsell/cross-sell, renewal, and re-engagement for inactive customers. Existing customers drive most new revenue — after-sales care is the highest-return investment.

#### Information to collect (ask the user before generating)
1. Average purchase cycle? (one-time / monthly / annual)
2. Any upsell/cross-sell products? List?
3. Term-limited contracts? Renewal process?
4. After how long with no purchase is a customer "inactive"?
5. Any after-sales follow-up today? Who does it?

#### Suggested template
Structure:
- **Follow-up schedule**: Day 3 (thank you) → Day 7 (satisfied?) → Day 30 (review?) → Day 60 (upsell) → Day 90 (referral)
- **Satisfaction check**: call/email script, handling dissatisfaction
- **Upsell/Cross-sell**: trigger events, script, offer
- **Renewal**: reminder timeline, renewal process, incentive
- **Re-engagement**: detect inactive customers, win-back email/call sequence
- **VIP treatment**: special care for tier-A customers

Confirm the structure before generating.

#### File-generation prompt
```
Create an After-Sales Care SOP.

CONTEXT:
- Company: [Name] — Purchase cycle: [frequency]
- Upsell/Cross-sell: [Yes/No] — Products: [list]
- Term-limited contract: [Yes/No] — Term: [months/year]
- Inactive threshold: [days]
- Current follow-up: [describe]

FORMAT:
- Follow-up calendar: timeline — Day 3/7/30/60/90/180/365 | Action | Channel | Script | Owner
- Satisfaction check script: 3 versions (call / email / chat) — questions + reactions by result
- Upsell playbook: Trigger | Recommended product | Script | Offer | Timing
- Renewal pipeline: Mermaid — 90 days before expiry → 60 → 30 → 7 → Expiry → Grace period
- Re-engagement sequence: 5 touchpoints — email 1 → email 2 → call → offer → final
- KPI tracking: Retention rate | Upsell rate | NPS | Churn rate | LTV

TONE: Relationship-focused, proactive, value-adding.
LENGTH: 6-8 pages.
```

---
✍️ Author: Brian H. Doan
