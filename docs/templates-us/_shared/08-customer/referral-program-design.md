### PROMPT 11: Referral Program Design

#### Description
Design a referral program — incentive structure (for referrer and referee), mechanics, tracking, terms & conditions, promotional plan. Referral is the lowest-cost, highest-converting channel to acquire new customers.

> US note: referral and "refer-a-friend" incentives are generally allowed, but if you reward customers for reviews/endorsements, the connection must be disclosed (FTC Endorsement Guides). Cash sweepstakes/contests have separate state rules [verify].

#### Information to collect (ask the user before generating)
1. Any current referral program? How effective?
2. Incentive for the referrer? (cash / credit / gift / % commission)
3. Incentive for the referee? (discount / gift / extended trial)
4. Average value of a new customer? (to set a sensible referral budget)
5. Channels to promote the program? (email / in-app / social / CS team)
6. An existing affiliate / member-get-member system?

#### Suggested template
Structure:
- **Program Design**: name, goal, double-sided incentive, budget
- **Mechanics**: how to get a referral link/code, share, track, validate, pay
- **Incentive Structure**: what the referrer gets, what the referee gets, tier bonuses
- **Tracking System**: referral link → registration → qualification → reward
- **Terms & Conditions**: eligibility, expiry, fraud prevention, caps
- **Promotional Plan**: launch, ongoing promotion, seasonal boost

Confirm the structure before generating.

#### File-generation prompt
```
Create a Referral Program Design.

CONTEXT:
- Company: [Name] — Current referral: [yes/no] — Results: [describe]
- Referrer incentive: [cash / credit / gift / % commission]
- Referee incentive: [discount / gift / trial]
- Average CAC: [USD] — Target referral CAC: [USD]
- Promotion channels: [email / in-app / social / CS]
- Affiliate system: [yes/no] — Platform: [name]

FORMAT:
- Program 1-pager: Name | Tagline | How it works (3 steps) | Rewards | T&C summary
- Incentive matrix: table Action | Referrer reward | Referee reward | Conditions | Cap (USD)
- Tier bonuses: 1-5 referrals → reward A | 6-15 → reward B | 16+ → reward C (gamification)
- Tracking flow: Mermaid — Share link → Click → Register → Qualify → Verify → Reward both
- Fraud prevention: 5-7 rules — self-referral, duplicate, abuse patterns, verification
- Promotional calendar: Month × Channel × Message × CTA
- KPIs: Referral rate | Conversion rate | CAC via referral | Viral coefficient | Revenue from referrals
- Email/message templates: 3 templates — invite, reminder, reward notification

TONE: Growth-focused, viral, win-win.
LENGTH: 6-8 pages.
```

---
✍️ Author: Brian H. Doan
