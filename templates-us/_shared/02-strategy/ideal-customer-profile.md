# PROMPT 09: Ideal Customer Profile — ICP & Buyer Persona

#### Description
A portrait of the ideal customer at two levels: ICP (company/organization level for B2B, or a segment for B2C) and Buyer Persona (the individual decision-maker). The foundation for sales targeting, marketing messaging, and product development.

#### Information to collect (ask the user before generating)
1. B2B or B2C? (or both)
2. Your 5 best current customers? (describe: industry, size, why they buy)
3. Your 3 worst customers? (describe: why they don't fit)
4. Buying decision process? (who decides, who influences, how long)
5. Main pain points that bring customers to you?
6. Channels customers use to find solutions? (Google, referral, social, events...)
7. Any customer data? (CRM, survey, interviews)

#### Suggested template
Structure:
- **ICP (Company-level, B2B)** — industry, size (revenue/employees), geography, tech stack, budget, buying trigger, disqualification criteria
- **Buyer Persona (Individual-level)** — 2-3 personas, each with:
  - Name + avatar (fictional)
  - Demographics: age, title, income, education
  - Goals & challenges: 3 goals + 3 challenges
  - Decision criteria: how they evaluate a purchase
  - Objections: 3-5 common objections + how to handle them
  - Content preferences: channel, format, frequency
  - Quote: a representative line ("I need...")
  - Journey map: Awareness → Consideration → Decision → Post-purchase
- **Anti-Persona** — profile of the customer who does NOT fit (avoid wasted effort)
- **Scoring Model** — lead-scoring criteria based on ICP fit

Confirm the structure before generating.

#### File-generation prompt
```
Create an ICP & Buyer Persona.

CONTEXT:
- Company: [Name] — Model: [B2B / B2C / B2B2C]
- Top 5 good customers: [short description each]
- Top 3 bad customers: [short description + reason]
- Buying process: [describe]
- Customer pain points: [list]
- Channels used: [list]
- Data source: [CRM / survey / interview / estimate]

FORMAT:
- ICP card: 1 page, visual, key criteria + thresholds
- Buyer Persona: 2-3 personas × 1 page each (visual card format)
- Anti-Persona: half a page — "DON'T sell to..."
- Objection Handling: table Objection | Root cause | Response
- Journey Map per persona: 4 stages × Touchpoints/Actions/Emotions/Needs
- Lead Scoring: Criteria | Weight | Score range | Threshold (MQL/SQL)

TONE: Marketing strategy — empathetic, data-informed, actionable.
LENGTH: 8-12 pages.
```

---
✍️ Author: Brian H. Doan
