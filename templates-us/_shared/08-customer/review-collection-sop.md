### PROMPT 12: Review Collection SOP

#### Description
A process to collect reviews/testimonials from customers — timing, channels, templates, follow-up, moderation, usage rights, response protocol. Reviews are the strongest social proof — most customers read reviews before buying.

> US compliance note: collect reviews honestly. Don't suppress or "gate" negative reviews, don't post fake or incentivized-without-disclosure reviews, and disclose any incentive given for a review (FTC Act, 15 U.S.C. §45; FTC Rule on Consumer Reviews and Testimonials, 16 CFR Part 465 [verify]). You may ask all customers for honest reviews regardless of sentiment.

#### Information to collect (ask the user before generating)
1. Most important review channels? (Google, Yelp, Facebook, website, Amazon, Trustpilot...)
2. Current review rate? Target?
3. Any incentive for reviews? (discount, gift, points) — must be disclosed and not condition on positivity
4. Who manages reviews? A process to respond to negative reviews?
5. Where are reviews used? (website, ads, social, brochure)

#### Suggested template
Structure:
- **Timing**: when to ask? (after successful onboarding, after project completion, after 30 days of use)
- **Channels**: Google Business, Yelp, Facebook Page, website, marketplace, video testimonial
- **Request Templates**: email, SMS, in-app notification — 3 versions (ask for an honest review)
- **Follow-up**: one reminder after 3 days
- **Moderation**: negative reviews — respond within 24h, escalate if needed (never delete honest negative reviews)
- **Usage Rights**: get permission to use, attribution, privacy
- **Response Protocol**: positive → thank + share | negative → acknowledge + resolve + follow-up

Confirm the structure before generating.

#### File-generation prompt
```
Create a Review Collection SOP.

CONTEXT:
- Company: [Name] — Main review channels: [Google / Yelp / FB / website / Amazon / Trustpilot]
- Current review rate: [%] — Target: [%]
- Incentive: [yes/no] — Type: [discount / gift / points] (disclosed, not conditioned on positive)
- Review manager: [who]
- Usage: [website / ads / social / brochure]
- Compliance: FTC Rule on reviews/testimonials (16 CFR Part 465) — honest reviews, disclose incentives, no fake reviews

FORMAT:
- Timing matrix: table Trigger event | Channel | Template | Owner | Auto/Manual
- Request templates: 3 versions — Email (subject + body) | SMS (160 chars) | In-app notification (ask for an honest review)
- Follow-up sequence: Day 0 (request) → Day 3 (reminder) → Day 7 (final + disclosed incentive)
- Response playbook: Review type | Response template | Timeline | Escalation
  - 5-star → Thank + share | 4-star → Thank + note | 3-star → Thank + investigate
  - 2-star → Apologize + resolve + follow-up | 1-star → Urgent escalate + CS Manager respond
- Moderation guidelines: fake-review detection, removal request (only for policy-violating/fake — not honest negatives), legal considerations
- Usage rights: permission template — email to request use of a testimonial
- KPI tracking: review volume | avg rating | response rate | response time | review-to-referral conversion
- Video testimonial guide: suggested script (5 questions) + technical requirements + release form

TONE: Proactive, appreciative, reputation-focused.
LENGTH: 5-7 pages.
```

---
✍️ Author: Brian H. Doan
