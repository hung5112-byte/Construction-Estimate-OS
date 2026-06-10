### PROMPT 13: Daily Operations Checklist

#### Description
A daily task checklist — open, check, operate, close. Ensures nothing is missed, especially when swapping people or training a new hire.

#### Information to collect (ask the user before generating)
1. Type of operation? (office / retail store / factory / warehouse / F&B)
2. Operating hours? (open – close)
3. Any shifts? How many?
4. Who is responsible for opening/closing?
5. What equipment needs a daily check? (POS, HVAC, IT systems, production machinery...)
6. Any weekly/monthly-specific tasks? (e.g. Friday inventory count, end-of-month deep clean)
7. Current sign-off process? (who checks, who approves)

#### Suggested template
Structure:
- **Opening checklist (AM)**: 8-12 items — power on, check equipment, prep the area, open systems
- **During-day checklist**: 5-8 items — periodic checks, restock, handle issues
- **Closing checklist (PM)**: 8-12 items — power off, lock up, back up data, security check
- **Weekly task sheet**: Mon-Sun × specific tasks
- **Monthly task sheet**: Weeks 1-4 × monthly tasks
- **Sign-off**: performer signs + manager review + abnormal notes

Confirm the structure before generating.

#### File-generation prompt
```
Create a Daily Operations Checklist.

CONTEXT:
- Company: [Name] — Industry: [industry] — Operating hours: [hours]
- Type: [office / store / factory / warehouse]
- Shifts: [Yes/No] — # shifts: [number]
- Equipment to check: [list]

FORMAT:
- 3 main tables: Opening (AM) | During-day | Closing (PM)
- Each item: ☐ Task | Time | Performer | Notes
- Weekly tasks: a separate table (e.g. Friday inventory count)
- Monthly tasks: a separate table
- Sign-off: performer signs at end of day + manager review
- Exception log: notes on anything abnormal during the day

TONE: Operational, checklist-style, ready to print and use.
LENGTH: 2-3 pages.
```

---
✍️ Author: Brian H. Doan
