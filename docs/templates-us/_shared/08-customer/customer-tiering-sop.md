### PROMPT 08: Customer Tiering SOP

#### Description
A process to classify customers into tiers A/B/C/D — based on criteria (revenue, frequency, potential, engagement). Each tier gets a different level of care. Migration rules when a customer moves up/down a tier.

#### Information to collect (ask the user before generating)
1. Do you tier customers today? By what criteria?
2. Average revenue per customer? Min-max range?
3. Purchase frequency? Range?
4. Include potential, or just history?
5. How many tiers? (3: VIP/Standard/Basic or 4: A/B/C/D)
6. How does each tier's care differ?

#### Suggested template
Structure:
- **Tiering criteria**: Revenue (40%) + Frequency (25%) + Potential (20%) + Engagement (15%)
- **Tier definitions**: A (Top 10%) → B (Next 20%) → C (Next 40%) → D (Bottom 30%)
- **Benefits per tier**: dedicated CSM, response priority, exclusive offers, events
- **Migration rules**: re-evaluate quarterly, conditions to move up/down
- **Data sources**: CRM, billing, support tickets, engagement metrics

Confirm the structure before generating.

#### File-generation prompt
```
Create a Customer Tiering SOP.

CONTEXT:
- Company: [Name] — # customers: [number] — Revenue range: [min-max USD/month]
- Current tiering: [yes/no] — Criteria: [describe]
- # tiers: [3/4] — Tier names: [VIP/Gold/Silver/Bronze or A/B/C/D]
- Re-evaluation frequency: [quarterly / semi-annual]

FORMAT:
- Scoring model: table Criteria | Weight | Scoring rule (1-10) | Data source
- Tier matrix: Tier | Score range | % customers | Revenue contribution | Description | Color code
- Benefits matrix: Tier | Dedicated CSM | Response SLA | Discount | Events | Gifts | Review freq
- Migration rules: conditions to move up (2 consecutive quarters ≥ threshold) | move down | grace period
- Implementation: Step 1 (data collection) → 2 (scoring) → 3 (assignment) → 4 (communication) → 5 (review)
- Dashboard: tier distribution | revenue by tier | movement (up/down/stable) | at-risk customers

TONE: Strategic, data-driven, fair.
LENGTH: 5-7 pages.
```

---
✍️ Author: Brian H. Doan
