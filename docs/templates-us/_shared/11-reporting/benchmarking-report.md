### PROMPT 09: Benchmarking Report

#### Description
A report comparing the company's performance against industry benchmarks and competitors — helping the Department Head understand relative position and identify improvement opportunities. Covers financial benchmarks, operational metrics, HR metrics, and customer metrics.

#### Information to collect (ask the user before generating)
1. Specific industry? (to find the right benchmark)
2. Company size? (revenue, headcount — to compare the right peer group)
3. Main competitors? (3-5)
4. Which metrics to benchmark? (financial / operational / HR / customer)
5. Benchmark-data source: industry reports / surveys / public data / industry association?
6. Frequency: annual / quarterly?

#### Suggested template
Structure:
- **Executive Summary** — overall positioning, key gaps, top opportunities
- **Part 1** — Methodology: sources, peer-group definition, limitations
- **Part 2** — Financial benchmarks: revenue growth, margins, ROI vs. industry
- **Part 3** — Operational benchmarks: productivity, quality, cycle time vs. peers
- **Part 4** — People benchmarks: compensation, turnover, engagement vs. market
- **Part 5** — Customer benchmarks: NPS, retention, CAC vs. peers
- **Part 6** — Gap analysis & recommendations: prioritized improvement areas
- **Appendix**: data sources, detailed comparison tables

Confirm the structure before generating.

#### File-generation prompt
```
Create a Benchmarking Report.

CONTEXT:
- Company: [Name] — Industry: [industry] — Size: [revenue / headcount]
- Competitors: [3-5 names]
- Benchmark metrics: [financial / operational / HR / customer]
- Data source: [industry reports / survey / public / association]
- Frequency: [annual / quarterly]

FORMAT:
- Executive summary: 1 page — overall position (above/below median), top 3 gaps, top 3 strengths, key actions
- Methodology:
  - Peer group: Criteria | # companies | Source | Limitations
  - Data period: [year] — confidence level per metric
- Financial benchmarks:
  - Table: Metric | Us | Peer Median | Top Quartile | Bottom Quartile | Gap | Percentile rank
  - Metrics: Revenue growth | Gross margin | EBITDA margin | Net margin | ROE | ROA | Revenue/employee
  - Spider/radar chart: Us vs. Peer Median — 6-8 financial metrics
- Operational benchmarks:
  - Table: Metric | Us | Peer Median | Best-in-class | Gap
  - Metrics: Productivity | Quality rate | Cycle time | SLA compliance | Automation %
- People benchmarks:
  - Table: Metric | Us | Market Median | Gap
  - Metrics: Revenue/employee | Turnover % | Avg salary by role | Training hours | Engagement score | Time-to-hire
- Customer benchmarks:
  - Table: Metric | Us | Industry Avg | Top Performer | Gap
  - Metrics: NPS | CSAT | Retention rate | CAC | CLV | Response time
- Gap-analysis matrix: 2×2 — High gap + High impact = Priority 1 | categorize all gaps
- Recommendations: Priority | Gap area | Current | Target | Action | Timeline | Investment | Expected ROI
- Trend: year-over-year benchmarking — are we closing gaps or falling behind?

TONE: Analytical, objective, data-driven, actionable.
LENGTH: 8-12 pages.
```

---
✍️ Author: Brian H. Doan
