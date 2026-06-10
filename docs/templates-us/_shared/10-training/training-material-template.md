### PROMPT 06: Training Material Template

#### Description
A standardized template for all training materials — lesson structure, slide deck, handout, and facilitator guide. Ensures consistency, professionalism, and easy maintenance/updates. Applies instructional-design principles per the ADDIE model.

#### Information to collect (ask the user before generating)
1. Main training-material format? (slide / document / video script / e-learning)
2. Branding guidelines? (logo, colors, fonts)
3. Who is the main user of the template? (internal trainer / external trainer / self-study)
4. What sections to include? (objectives, content, activities, assessment, handout)
5. Average length of a training session? (1h / half-day / full-day)
6. Need an assessment/quiz in the material?

#### Suggested template
Structure:
- **Part 1** — Cover-page template: course name, trainer, date, version, branding
- **Part 2** — Course overview: learning objectives (SMART), target audience, prerequisites, duration
- **Part 3** — Facilitator guide template: timeline, instructions, talking points, activity facilitation
- **Part 4** — Content slides template: structure of each module — hook, content, practice, review
- **Part 5** — Participant handout template: key takeaways, exercises, notes space, resources
- **Part 6** — Assessment template: pre-test, post-test, quiz, practical exercise
- **Part 7** — Supplementary materials: case studies, role-play scenarios, worksheets
- **Appendix**: training branding guidelines, file naming convention

Confirm the structure before generating.

#### File-generation prompt
```
Create a Training Material Template.

CONTEXT:
- Company: [Name] — Main format: [slide / document / e-learning]
- Branding: [Yes/No] — Logo: [Yes] — Brand colors: [hex]
- Template user: [internal trainer / external / self-study]
- Average length: [X hours]
- Assessment: [Yes/No]

FORMAT:
- Cover-page template: [Course name] | [Trainer] | [Date] | [Version] | [Logo] — layout mockup
- Course-overview template:
  - Learning objectives: "After the course, learners can..." — use Bloom's Taxonomy verbs
  - Audience profile: [___] | Prerequisites: [___] | Duration: [___]
  - Agenda: Module | Topic | Duration | Method | Materials
- Facilitator-guide template per module:
  - Time | Slide # | Trainer says/does | Learner does | Materials | Notes
  - Transition cues, activity instructions, debrief questions
- Content template: each module — Hook (question/story) → Teach (content) → Practice (activity) → Review (summary)
- Slide-design rules:
  - Min font size | max bullets per slide | image guidelines | branding placement
  - Template slides: Title, Content, Activity, Quote, Case study, Q&A
- Handout template: Module | Key points | Notes space | Action items | Resources/Links
- Assessment templates:
  - Pre-test: 5-10 questions to measure baseline
  - Post-test: 5-10 questions to measure learning gain
  - Practical exercise: Scenario | Task | Expected output | Evaluation criteria
- File naming convention: [Dept]-[Topic]-[Type]-[Version]-[Date] — e.g. HR-Onboarding-FacGuide-v1.0-2026Q1

TONE: Professional, easy to customize, instructional-design-driven.
LENGTH: 4-6 pages.
```

---
✍️ Author: Brian H. Doan
