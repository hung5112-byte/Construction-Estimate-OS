### PROMPT 03: Customer Journey Map

#### Description
A customer journey map — from awareness → consideration → decision → purchase → retention → advocacy. Maps each touchpoint, emotion, pain point, and opportunity at each stage. Helps marketing and sales jointly optimize the customer experience.

#### Information to collect (ask the user before generating)
1. Which product/service to map? (pick one flagship product)
2. Main persona? (who is the typical customer?)
3. Current touchpoints? (website, social, email, phone, in person, events?)
4. Biggest pain points, and at which stage?
5. Average time from awareness to purchase? (days/weeks/months?)
6. Any NPS or customer-feedback data?

#### Suggested template
Structure:
- **Persona Summary**: a summary of the persona being mapped
- **Journey Stages**: 6 stages (Awareness → Consideration → Decision → Purchase → Retention → Advocacy)
- **Per Stage**: Actions | Touchpoints | Emotions | Pain Points | Opportunities | KPIs
- **Moments of Truth**: the most important decision points
- **Gap Analysis**: the gap between current experience and expectations
- **Action Plan**: prioritized improvements per stage

Confirm the structure before generating.

#### File-generation prompt
```
Create a Customer Journey Map.

CONTEXT:
- Company: [Name] — Product: [product/service name]
- Persona: [persona name] — [short description]
- Touchpoints: [list]
- Cycle time: [awareness → purchase]
- Main pain points: [list]
- NPS / Feedback: [yes/no — data]

FORMAT:
- Journey map visual: table Stage × (Actions | Touchpoints | Emotions 😊😐😞 | Pain Points | Opportunities)
- Emotion curve: ASCII graph — positive/negative by stage
- Touchpoint matrix: table Touchpoint | Stage | Channel | Owner | Current Rating | Target
- Moments of Truth: top 3-5 critical moments — What | Why | Current | Ideal
- Gap analysis: table Stage | Customer Expectation | Current Experience | Gap | Priority
- Action plan: table # | Action | Stage | Impact | Effort | Owner | Timeline
- Quick wins: 3-5 actions doable within 30 days

TONE: Customer-centric, empathetic, insight-driven.
LENGTH: 5-7 pages.
```

---
✍️ Author: Brian H. Doan
