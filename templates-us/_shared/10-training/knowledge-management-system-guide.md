### PROMPT 09: Knowledge Management System Guide

#### Description
A guide to build and run a knowledge management system (KMS) — where the organization's knowledge is stored, organized, shared, and updated. Includes taxonomy, contribution guidelines, quality standards, and governance. Ensures knowledge isn't lost when employees leave, and that everyone can easily find what they need.

#### Information to collect (ask the user before generating)
1. Where is knowledge stored today? (Google Drive / Notion / SharePoint / wiki / in people's heads)
2. An existing knowledge base/wiki? What platform?
3. Which knowledge matters most? (process / product / customer / technical / best practices)
4. Who contributes content? (subject-matter experts / all employees / a dedicated team)
5. Biggest problem: knowledge lost when people leave / can't find it / outdated / nobody uses it?
6. AI/chatbot support for knowledge search?

#### Suggested template
Structure:
- **Part 1** — Vision & objectives: why a KMS, goals, success criteria
- **Part 2** — Knowledge taxonomy: explicit vs. tacit, categories, tags
- **Part 3** — Platform & architecture: tool selection, structure, search, access control
- **Part 4** — Content standards: article templates, quality criteria, review process
- **Part 5** — Contribution process: who writes, submit → review → publish
- **Part 6** — Governance: owner, maintenance, update cycle, retirement
- **Part 7** — Adoption strategy: training, gamification, KPIs
- **Part 8** — Knowledge capture: exit interviews, after-action reviews, lessons learned
- **Appendix**: article template, taxonomy tree, platform comparison

Confirm the structure before generating.

#### File-generation prompt
```
Create a Knowledge Management System Guide.

CONTEXT:
- Company: [Name] — Headcount: [number]
- Current knowledge: [Google Drive / Notion / wiki / in heads]
- KMS platform: [chosen / need advice]
- Priority knowledge: [process / product / technical / best practices]
- Contributors: [SMEs / all employees / dedicated team]
- Main problem: [lost when people leave / can't find / outdated]

FORMAT:
- KMS vision: 1 paragraph — "Every employee finds the right info in X minutes"
- Knowledge taxonomy:
  - Level 1: Categories (Process, Product, Customer, Technical, HR, Leadership)
  - Level 2: Sub-categories per L1
  - Level 3: Article types (How-to, FAQ, Policy, Template, Case study, Lesson learned)
  - Tagging convention: [Category]-[Sub]-[Type]-[Audience]
- Platform architecture: Mermaid — structure of spaces/databases/folders
- Content standards:
  - Article template: Title | Summary (2 lines) | Body | Author | Date | Review date | Tags | Related articles
  - Quality criteria: Accurate | Current | Actionable | Searchable | Reviewed
  - Writing guidelines: plain language, max 1000 words, include visuals, link to related
- Contribution workflow: Mermaid — Draft → Peer review → SME approve → Publish → Schedule review
- Governance model:
  - Roles: KMS Owner | Content leads per dept | Contributors | Reviewers
  - Review cycle: table Content type | Review frequency | Owner | Archive after
  - Metrics: table Usage | Contribution | Quality | Search effectiveness
- Knowledge-capture processes:
  - Exit-interview checklist: critical knowledge areas | documentation status | handover plan
  - After-Action Review: what happened | what was expected | why different | lessons | actions
  - Communities of Practice: topic | members | meeting cadence | output
- Adoption plan:
  - Launch: communicate | train | seed content | quick wins
  - Sustain: gamification | recognition | KPIs in reviews | leadership modeling
  - KPIs: active users % | articles created/month | search success rate | time-to-find-info | content freshness %

TONE: Practical, adoption-focused, balancing structure with usability.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
