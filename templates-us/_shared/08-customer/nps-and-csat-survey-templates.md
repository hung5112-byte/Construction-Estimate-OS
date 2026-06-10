### PROMPT 04: NPS & CSAT Survey Templates

#### Description
Survey templates to measure customer satisfaction and loyalty — NPS (Net Promoter Score), CSAT (Customer Satisfaction Score), CES (Customer Effort Score). Includes an analysis framework and action planning.

#### Information to collect (ask the user before generating)
1. Measured NPS/CSAT before? Results?
2. Preferred survey channel? (email / in-app / SMS / phone)
3. Desired survey frequency? (after each transaction / quarterly / annual)
4. How many customers to survey? Expected response rate?
5. Who will analyze the results and build the action plan?

#### Suggested template
Structure:
- **NPS Survey**: 1 core question (0-10) + 1 open "Why?" + classify Promoter/Passive/Detractor
- **CSAT Survey**: 3-5 questions by dimension (product, service, speed, staff, overall)
- **CES Survey**: "How easy was it to resolve your issue?" (1-7)
- **Analysis Framework**: formulas, industry benchmark, trend analysis
- **Action Planning**: score range → action → owner → timeline

Confirm the structure before generating.

#### File-generation prompt
```
Create NPS/CSAT/CES Survey Templates.

CONTEXT:
- Company: [Name] — B2B/B2C: [type]
- Measured before: [NPS=X / CSAT=X% / No]
- Channel: [email / in-app / SMS / phone]
- Frequency: [transactional / quarterly / annual]
- # customers: [number] — Response-rate target: [%]

FORMAT:
- NPS survey template: 1 core question + 1 open follow-up + thank-you page
- CSAT survey template: 5 rated questions (1-5) + 1 open + conditional logic
- CES survey template: 1 core question (1-7) + 1 follow-up
- Scoring guide: NPS formula (% Promoter - % Detractor) | CSAT formula (satisfied/total) | CES formula
- Benchmark: industry-average NPS/CSAT + target setting
- Analysis template: table Period | NPS | CSAT | CES | Trend | Top issues | Actions
- Action matrix: Score range | Urgency | Action | Owner | Timeline
- Closing the loop: customer follow-up after survey — Detractor (24h) | Passive (1 week) | Promoter (thank you + referral)

TONE: Data-driven, actionable, customer-focused.
LENGTH: 5-7 pages.
```

---
✍️ Author: Brian H. Doan
