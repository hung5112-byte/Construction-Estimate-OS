### PROMPT 10: Content Calendar Template

#### Description
A standardized content-calendar template — daily/weekly/monthly views, content-type classification, distribution channel, production status, owner, and performance tracking. Helps the marketing team plan, execute, and measure content systematically.

#### Information to collect (ask the user before generating)
1. How many content channels to manage?
2. How many posts/content pieces per week?
3. Production workflow: how many steps? (Idea → Brief → Create → Review → Approve → Publish)
4. Management tool: spreadsheet / Notion / Trello / dedicated?
5. Track performance on the calendar?

#### Suggested template
Structure:
- **Monthly View**: month × week — themes, campaigns, holidays
- **Weekly View**: 7 days × channel × content type — detailed
- **Production Pipeline**: Idea → Brief → Draft → Review → Approved → Scheduled → Published
- **Content Details**: title, type, channel, copy, visual, CTA, hashtags, links
- **Performance Tracking**: reach, engagement, clicks, conversions — per post
- **Legend**: color codes for content type, status, channel

Confirm the structure before generating.

#### File-generation prompt
```
Create a Content Calendar Template.

CONTEXT:
- Company: [Name] — Channels: [list] — # content/week: [number]
- Workflow: [# steps]
- Tool: [Spreadsheet / Notion / Trello]
- Track performance: [Yes/No]

FORMAT:
- Monthly overview: table Weeks 1-4 × Theme | Campaign | Key dates | Content count
- Weekly detail: table Mon-Sun × Channel | Content Type | Title | Status | Owner | Publish Time
- Content card template: Title | Type | Channel | Copy (excerpt) | Visual brief | CTA | Hashtags | Link | Status | Owner | Due | Published | Performance
- Status workflow: Idea 💡 → Briefed 📋 → Creating ✏️ → Review 👀 → Approved ✅ → Scheduled 📅 → Published 🚀 → Analyzed 📊
- Performance tracker: table Post | Date | Channel | Reach | Engagement | Clicks | Conv | Notes
- Recurring content: table Series/Recurring | Frequency | Day | Template

TONE: Practical, visual, easy to maintain.
LENGTH: 3-5 pages.
```

---
✍️ Author: Brian H. Doan
