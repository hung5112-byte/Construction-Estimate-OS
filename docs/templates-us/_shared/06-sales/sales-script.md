### PROMPT 06: Sales Script

#### Description
A standardized set of sales scripts for each channel (inside sales, in-person consult, online chat) and each product/buyer persona. Not "recite from memory" but a framework to navigate the conversation effectively.

#### Information to collect (ask the user before generating)
1. Main sales channels needing a script? (inside sales / face-to-face / online chat / video call)
2. Products/services needing a script? (top 3)
3. Main buyer personas? (title, pain points, buying triggers)
4. Average length of a consult?
5. Most common objections? (top 5)
6. Desired call-to-action? (book a meeting / demo / buy now / trial)
7. An existing script? Its weaknesses?

#### Suggested template
Structure:
- **How to use the script**: guidelines — adapt, don't recite
- **Inside Sales Script**: Opening → Discovery → Presentation → Close → Follow-up
- **In-Person Consult Script**: Greeting → Discover needs → Demo/present → Handle objections → Close
- **Online Chat Script**: Auto-greeting → Quick qualify → Value proposition → CTA → Move offline
- **Per-Persona Variations**: Persona A → adjust messaging, Persona B → adjust messaging
- **Power Phrases**: good questions, good closing lines, good objection-handling lines
- **Anti-patterns**: lines NOT to say
- **Appendix**: roleplay scenarios, scoring rubric

Confirm the structure before generating.

#### File-generation prompt
```
Create a Sales Script.

CONTEXT:
- Company: [Name] — Products/services: [top 3]
- Channels: [inside sales / face-to-face / chat / video call]
- Persona: [Persona name | Title | Pain point | Trigger]
- Average length: [minutes]
- Top 5 objections: [list]
- CTA: [book meeting / demo / buy / trial]

FORMAT:
- Script structure per channel: flowchart of stages + length per stage
- Verbatim script: greeting → opener → discovery questions (5-7) → pitch → close
- Branching: IF the customer says X THEN → response A; IF Y THEN → response B
- Persona variations: table Stage | Persona A | Persona B | Persona C
- Power phrases: 10 good questions + 10 good closes + 10 bridges
- Anti-patterns: 10 lines NOT to say + why + what to say instead
- Practice scenarios: 3 roleplays (easy / medium / hard)
- Scoring: a call/consult evaluation rubric

TONE: Natural, consultative (not "salesy"), professional.
LENGTH: 8-12 pages.
```

---
✍️ Author: Brian H. Doan
