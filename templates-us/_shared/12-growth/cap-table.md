### PROMPT 04: Cap Table

#### Description
A capitalization table — tracking who owns what %, which share class, vesting schedules, and dilution across funding rounds. A clean cap table is a must-have for any investor. General information only — share issuances are securities; confirm with a corporate/securities attorney.

#### Information to collect (ask the user before generating)
1. Entity type? (LLC / C-corporation — investors typically prefer a Delaware C-corp; a Texas LLC/corp is also possible)
2. Current owners? (name, % ownership, share class)
3. Any funding rounds yet? (detail each round)
4. An ESOP (Employee Stock Option Plan)? Pool size?
5. Any convertible notes / SAFEs not yet converted?
6. Founder vesting schedule? (cliff, vesting period)

#### Suggested template
Structure:
- **Part 1** — Current cap table: current owners — fully diluted
- **Part 2** — Historical: each round — pre-money, investment, post-money, new shares, % dilution
- **Part 3** — ESOP pool: allocated, granted, exercised, available
- **Part 4** — Convertible instruments: notes/SAFE details, conversion scenarios
- **Part 5** — Pro-forma: next round → new cap-table simulation
- **Part 6** — Dilution waterfall: chart showing founder dilution across rounds
- **Part 7** — Vesting schedules: per shareholder — cliff, monthly/quarterly, acceleration
- **Appendix**: share-class rights, voting rights, liquidation preference

Confirm the structure before generating.

#### File-generation prompt
```
Create a Cap Table.

CONTEXT:
- Company: [Name] — Entity type: [LLC / C-corp]
- Authorized/issued capital: [number]
- Owners: [Name | % | Share class | Date]
- Funding rounds: [list: Round | Valuation | Amount | Investor]
- ESOP: [Yes/No] — Pool: [%]
- Convertibles: [Yes/No] — Detail: [amount, cap, discount]

FORMAT:
- Current cap table: Shareholder | Share class | # Shares | % Ownership (basic) | % Ownership (fully diluted) | Investment | Vesting status (USD)
- Historical rounds: Round | Date | Pre-money | Investment | Post-money | New shares | Price/share | Lead investor
- ESOP tracking: Grantee | Grant date | # Options | Vesting schedule | Exercised | Remaining | Exercise price
- Convertible tracker: Holder | Instrument | Amount | Cap | Discount | Conversion trigger | Estimated shares
- Pro-forma simulation: Current → After Series [X] → After ESOP refresh → Fully diluted
- Dilution waterfall: chart data — Founding | Seed | Series A | ESOP → % per group
- Vesting: Shareholder | Total | Cliff | Vesting period | Monthly/Quarterly | Accelerated if [event]
- Rights summary: Share class | Voting | Dividend | Liquidation preference | Anti-dilution | Board seat

⚠️ LEGAL NOTE: The cap table should be reviewed by a corporate attorney. Share issuances are securities (Securities Act of 1933; Reg D / Form D for exempt offerings). Entity governance under Delaware corporate law or the Texas Business Organizations Code (TBOC).

TONE: Financial, precise, legal-aware.
LENGTH: 4-6 pages.

NOTE: General information, not legal advice.
```

---
✍️ Author: Brian H. Doan
