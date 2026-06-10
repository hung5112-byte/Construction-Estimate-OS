### PROMPT 01: Office Management SOP

#### Description
A standardized daily office-management process — cleaning, equipment maintenance, meeting-room management, reception, keys/access cards, and utilities (water, power, internet). Keeps the office ready and professional.

#### Information to collect (ask the user before generating)
1. Office leased or owned? Square footage? Number of floors?
2. A dedicated admin/receptionist?
3. Outsourced services: cleaning, security, IT?
4. Meeting rooms: how many? Booking system?
5. Shared equipment: printer, projector, kitchen, supplies?
6. Office open/close hours?

#### Suggested template
Structure:
- **Daily management**: open, close, cleaning checklist, equipment check
- **Meeting rooms**: booking, prep, cleanup, usage rules
- **Equipment & utilities**: scheduled maintenance, handling breakdowns, technician contacts
- **Reception & visitors**: greeting, sign-in, wayfinding
- **Keys & access**: issuance, recovery, lost/damaged
- **Office vendors**: cleaning, security, water/coffee, office supplies

Confirm the structure before generating.

#### File-generation prompt
```
Create an Office Management SOP.

CONTEXT:
- Company: [Name] — Office: [leased/owned] — Size: [sq ft] — [number] floors
- Admin: [Yes/No] — Outsourced: [cleaning/security/IT]
- Meeting rooms: [number] — Booking: [Google Calendar/Slack/manual]
- Office hours: [hours]

FORMAT:
- Opening checklist: 5-8 items ☐ + time + performer
- Closing checklist: 5-8 items ☐
- Meeting-room booking rules: table Room | Capacity | Equipment | Booking method | Rules
- Maintenance schedule: table Equipment | Frequency | Owner | Maintenance vendor | Contact
- Office incident handling: flowchart — issue type → severity → handler → time
- Vendor directory: Service | Vendor | Contact | Agreement # | Expiry

TONE: Operational, practical, easy to follow.
LENGTH: 5-7 pages.
```

---
✍️ Author: Brian H. Doan
