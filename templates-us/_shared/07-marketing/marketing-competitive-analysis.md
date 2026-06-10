### PROMPT 04: Marketing Competitive Analysis

#### Description
A detailed analysis of competitors' marketing — positioning, messaging, media channels, content, social media, paid ads, SEO, and perceived share of voice. Helps the company find its competitive advantage and differentiation opportunities.

#### Information to collect (ask the user before generating)
1. Competitors to analyze? (3-5 names + websites)
2. Direct or indirect competitors?
3. Which channels to focus on? (Social, SEO, Paid Ads, Content, PR?)
4. Any existing data on them? (traffic estimate, social followers, ad library?)
5. Purpose of the analysis? (find gaps, benchmark, repositioning?)

#### Suggested template
Structure:
- **Overview**: an overview matrix — Us vs. Competitor A vs. B vs. C
- **Positioning & Messaging**: brand promise, tagline, key messages, tone
- **Channel Analysis**: social media, website/SEO, paid ads, email, PR, events
- **Content Analysis**: content types, frequency, engagement, top-performing content
- **Digital Footprint**: traffic, domain authority, keyword rankings, backlinks
- **SWOT of Each Competitor**: each competitor's marketing strengths/weaknesses
- **Opportunities & Recommendations**: gaps the company can exploit

Confirm the structure before generating.

#### File-generation prompt
```
Create a Marketing Competitive Analysis.

CONTEXT:
- Company: [Name] — Website: [URL]
- Competitors: [A: URL] | [B: URL] | [C: URL]
- Type: [direct / indirect]
- Focus: [Social / SEO / Ads / Content / All]
- Available data: [traffic estimate / social stats / ad library]
- Purpose: [find gaps / benchmark / repositioning]

FORMAT:
- Comparison matrix: table Criterion | Us | Competitor A | B | C — 15+ criteria
- Social media scorecard: table Platform | Followers | Engagement Rate | Post Frequency | Top Content Type — per competitor
- SEO comparison: table Domain Authority | Organic Traffic | Top Keywords | Content Volume | Backlinks
- Content audit: table Content Type | Frequency | Avg Engagement | Best Performer — per competitor
- Messaging map: table Competitor | Tagline | Key Messages | Tone | Target Audience
- Gap analysis: table Channel/Tactic | Competitor A | B | C | Us | GAP/Opportunity
- Recommendations: top 5 actions ranked by Impact × Feasibility

TONE: Analytical, objective, competitive intelligence.
LENGTH: 6-8 pages.
```

---
✍️ Author: Brian H. Doan
