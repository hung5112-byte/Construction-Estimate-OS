# PROMPT 01: Company Profile

#### Description
An overview document introducing the business — for partners, customers, investors, and government agencies. Combines hard information (legal, numbers) and soft information (story, values, vision).

#### Information to collect (ask the user before generating)
1. Primary audience? (B2B partners / investors / customers / recruiting / all)
2. What does the company most want to emphasize? (technology / experience / scale / values / team)
3. Any case studies / flagship customers to include?
4. Key numbers: revenue, headcount, years of experience, # projects, # customers?
5. Desired format? (Markdown report / designed PDF / presentation)
6. Logo, images, intro video available?

#### Suggested template
Structure (10-15 pages):
- **Cover page** — logo, name, tagline, contact info
- **Table of contents**
- **A letter from the CEO** — half a page, personal, inspiring
- **Overview** — founding, legal entity, headquarters, industry
- **Vision / Mission / Core Values** — a 1-page summary
- **Products & Services** — main catalog, USP
- **Capabilities & Strengths** — certifications, technology, processes
- **Team** — key people, headcount, expertise
- **Achievements & Milestones** — awards, impressive numbers, media coverage
- **Flagship Customers & Case Studies** — logo wall, 2-3 short case studies
- **Commitment & Why Choose Us** — 5-7 reasons why
- **Contact information** — multi-channel

Confirm the structure before generating.

#### File-generation prompt
```
Create a Company Profile.

CONTEXT:
- Company: [Full legal name] — Brand/short name: [name]
- Founded: [year] — EIN: [number] — Headquarters: [address]
- Industry: [main industry]
- Primary audience: [B2B partners / investors / customers / all]
- USP: [main differentiator]
- Key numbers: Revenue [number] | Headcount [number] | Customers [number] | Projects [number]
- Case studies: [summarize 2-3 cases]
- Awards/Media: [list]

FORMAT:
- Professional document, convertible to a polished PDF
- Each section: header + 1-2 paragraphs + data points
- Infographic-ready: key numbers as "10+ years | 500+ customers | 50+ employees"
- Logo-wall placeholder: [Logo 1] [Logo 2] ...
- Case-study format: Challenge → Solution → Result (half a page each)
- Closing CTA: contact us to partner

TONE: Professional, confident, not boastful. Light storytelling.
LENGTH: 10-15 pages.
```

---
✍️ Author: Brian H. Doan
