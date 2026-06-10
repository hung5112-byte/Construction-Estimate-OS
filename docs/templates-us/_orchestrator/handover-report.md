# PROMPT 06: Handover Report

#### Description
A wrap-up report template for after the whole packaging project is complete. Summarizes what was created, how to use it, and next steps for the business.

#### Information to collect (ask the user before generating)
1. Hand over to whom? (Owner / Department Head / COO / management team)
2. Desired format? (PDF report / presentation / Markdown)
3. Need a training session as well?
4. Any follow-up commitment after handover? (30/60/90 days)

#### Suggested template
Structure:
- **Executive Summary** — 1 page: which company, what scope, overall results
- **Deliverables Inventory** — a table of all files created, by tier
- **Maturity Before/After** — spider chart: 9 dimensions, score before vs. after
- **Quick Start Guide** — the top 10 files to read first
- **Implementation Roadmap** — rollout plan: what to do in weeks 1-2-3-4
- **FAQ** — 10 common questions when starting to use the document set
- **Support & Next Steps** — support contact, follow-up schedule

Confirm the structure before generating.

#### File-generation prompt
```
Create a Handover Report template for the Business Packaging project.

CONTEXT:
- Company: [Company name] — Industry: [industry] — Size: [headcount]
- Scope: [Full / Selective] — Skills run: [list]
- Hand over to: [recipient's title]
- Follow-up: [Yes/No] — [30/60/90 days]

FORMAT:
- Professional report layout: cover page → TOC → body → appendix
- Executive Summary: 1 page, bullet points, highlight key wins
- Deliverables table: Tier | Skill | Files | Status | Usage priority
- Spider/radar chart data: 9 dimensions × before/after scores
- Quick Start: top 10 files + why to read them first
- Implementation Roadmap: Gantt-style by week
- FAQ: Q&A format, 10 questions
- Appendix: full file list, glossary reference

TONE: Executive — professional, confident, action-oriented.
LENGTH: 8-12 pages.
```

---
✍️ Author: Brian H. Doan
