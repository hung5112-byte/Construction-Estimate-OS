### PROMPT 18: Meeting Minutes Template

#### Description
A standard meeting-minutes template — capturing decisions, action items, owners, and deadlines. Unlike board meeting minutes (legal) in bb-governance, this is for everyday internal meetings.

#### Information to collect (ask the user before generating)
1. Which meetings need minutes? (Daily standup / Weekly / Monthly / Project / All-hands)
2. Who takes minutes? (a fixed secretary / rotating / attendees take their own)
3. Who receives the minutes after? (attendees only / the whole team / shared archive)
4. Track action items from the minutes? (Yes/No — if Yes, which tool?)
5. Do minutes require sign-off?
6. Where are minutes stored? (Google Drive / SharePoint / Notion / hard copy)

#### Suggested template
Structure:
- **Header**: meeting type | date | start-end time | location/link | chair | note-taker
- **Attendance**: table Name | Title | Present ☐ | Absent (with reason)
- **Agenda**: numbered items + estimated time per item
- **Discussion**: per agenda item → discussion summary | decision | action items
- **Action Items table**: # | Action | Owner | Due date | Priority | Status
- **Next meeting**: date | time | tentative agenda
- **Sign-off**: chair signs + note-taker signs (if needed)

Confirm the structure before generating.

#### File-generation prompt
```
Create an internal Meeting Minutes Template.

CONTEXT:
- Company: [Name] — Meeting type: [Daily / Weekly / Monthly / Project]
- Note-taker: [fixed / rotating]
- Storage: [Google Drive / SharePoint / Notion]
- Track action items: [Yes/No]

FORMAT:
- Header: meeting type | date | time | location/link | chair | note-taker
- Attendance: Name | Title | Present ☐
- Agenda: numbered items + time box
- Discussion: per agenda item → discussion | decision | action item
- Action-items summary: table # | Action | Owner | Due | Priority | Status
- Next meeting: date | tentative agenda
- One page max — concise, action-focused

TONE: Concise, action-focused, easy to scan.
LENGTH: 1-2 pages.

CROSS-REFERENCE: Links to the Meeting Policy (P-OPS-17) for agenda format and the L10 meeting.
```

---
✍️ Author: Brian H. Doan
