### PROMPT 17: Meeting Policy — EOS Meeting Pulse

#### Description
A meeting policy based on the EOS Meeting Pulse framework — standardizing meeting types, frequency, agenda, and rules. Fewer pointless meetings, more effective ones. Uses the L10 Meeting format.

#### Information to collect (ask the user before generating)
1. How many meetings/week now? Too many / too few?
2. Meeting types needed? (Daily standup / Weekly / Monthly / Quarterly / Annual)
3. Average attendees per meeting?
4. Any problems with current meetings? (too long, no decisions, no follow-up)
5. Adopt the L10 Meeting (EOS)?

#### Suggested template
Structure:
- **Meeting principles**: start/end on time, agenda in advance, action items after, no-devices rule
- **Meeting types**: Daily Standup (15 min) | Weekly L10 (90 min) | Monthly Review (2h) | Quarterly Planning (1 day)
- **L10 Meeting format**: Segue (5 min) → Scorecard (5 min) → Rock review (5 min) → Customer/Employee headlines (5 min) → To-do review (5 min) → IDS (60 min) → Conclude (5 min)
- **Rules**: who calls it, who must attend, substitutes, canceling
- **Action items**: format Who | What | When | Status
- **Metrics**: % meetings on time, % action items completed

Confirm the structure before generating.

#### File-generation prompt
```
Create a Meeting Policy (EOS Meeting Pulse).

CONTEXT:
- Company: [Name] — Current meetings: [#/week] — Problems: [describe]
- Meeting types needed: [Daily / Weekly / Monthly / Quarterly / Annual]
- L10 format: [Yes/No]
- Average attendees: [number]

FORMAT:
- Meeting matrix: Type | Frequency | Duration | Participants | Facilitator | Agenda template
- L10 agenda card: 1 page — 7 segments × time box
- Daily standup template: 3 questions (Yesterday | Today | Blockers)
- Rules poster: 10 rules — printable one page
- Action-items tracker: from meeting → task → owner → due → status
- Meeting-effectiveness survey: 5 questions, run monthly

TONE: EOS-inspired, effective, action-oriented.
LENGTH: 5-7 pages.
```

---
✍️ Author: Brian H. Doan
