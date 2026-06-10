# P-PPL-22: 360-Degree Feedback Form

#### Description
A 360-degree feedback form — gathering input from four angles: self, manager, peers, and direct reports. Assesses competencies (rather than KPIs) — complements the KPI template.

#### Information to collect (ask the user before generating)
1. Competencies to assess? (e.g. Leadership, Communication, Teamwork, Problem Solving, Innovation, Integrity...)
2. Number of competencies: 8-12 or more?
3. Scale: 1-5 or 1-7?
4. Open comments? (required or optional)
5. Anonymity: are peers and direct reports anonymous?
6. Frequency: annual / semi-annual?

#### Suggested template
Structure:
- **Self Form**: employee self-assessment — 20-25 statements × 1-5 scale
- **Manager Form**: manager assessment — same statements
- **Peer Form**: peers (2-3 people) — same statements + anonymous
- **Direct Report Form**: direct reports (if any) — same statements + anonymous
- **Summary**: radar-chart data — Self vs. Manager vs. Peer vs. DR
- **Development Plan**: gap analysis → 2-3 areas to improve → action plan

Confirm the structure before generating.

#### File-generation prompt
```
Create a 360-Degree Feedback Form.

CONTEXT:
- Company: [Name] — Competencies: [list 8-12]
- Scale: [1-5 / 1-7]
- Open comments: [Required / Optional]
- Peer/DR anonymity: [Yes/No]
- Frequency: [Semi-annual / Annual]

FORMAT:
- 4 separate forms: Self | Manager | Peer | Direct Report
- Each competency: 2-3 behavioral statements × 1-5 scale
  e.g. "Leadership" → "Inspires the team to hit its goals" [1-2-3-4-5]
- Rubric per score: 1 = Rarely demonstrates | 3 = Frequently | 5 = Always, a role model
- Open-comment section: "Greatest strength?" + "What to improve?" + "Advice?"
- Summary template: table Competency | Self | Manager | Peer Avg | DR Avg | Gap (Self vs Others)
- Radar-chart data: 8-12 axes × 4 sources
- Development plan: top 3 gaps → Action | Timeline | Support needed | Success measure

TONE: Constructive, development-focused — not a negative performance review.
LENGTH: 4-6 pages (4 forms + summary + dev plan).
```

---
✍️ Author: Brian H. Doan
