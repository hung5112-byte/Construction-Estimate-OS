# P-FIN-15: Texas Sales-and-Use Tax Return Worksheet

#### Description
A worksheet to prepare your **Texas sales-and-use tax** return for filing with the **Texas Comptroller**. (The US has no VAT / input-credit chain — Texas sales tax is collected on taxable sales and remitted; use tax applies to taxable purchases where no sales tax was paid.) Helps you file accurately, completely, and on time to reduce penalty risk. General information only — not tax advice; confirm with a licensed Texas CPA.

#### Information to collect (ask the user before generating)
1. Do you have a Texas Sales and Use Tax Permit? (required to collect/remit)
2. Filing frequency? (monthly / quarterly / annual — based on your tax liability) [UNCERTAIN — verify your assigned frequency with the Comptroller]
3. How do you file? (Comptroller Webfile / eSystems, or an accounting integration)
4. What are your local sales-tax jurisdictions? (state 6.25% + city/county/special districts up to 2%, max 8.25% combined)
5. Any taxable purchases without sales tax paid (use tax owed)?

#### Suggested template
Structure:
- **Overview**: which return, where to file (Comptroller Webfile), deadline (generally the 20th of the month following the period [verify]), late-filing penalty
- **Taxable sales worksheet**: by jurisdiction — gross sales, exempt/resale, taxable amount, tax due
- **Use tax worksheet**: taxable purchases where no sales tax was paid
- **Return summary**: total tax collected by jurisdiction (state + local) = total due
- **Pre-filing checklist**: 10 items
- **Notes**: exempt/resale certificates on file, timely-filing discount [verify]

Confirm the structure before generating.

#### File-generation prompt
```
Create a Texas Sales-and-Use Tax Return Worksheet.

CONTEXT:
- Company: [Name] — Sales Tax Permit #: [number]
- Filing frequency: [monthly / quarterly / annual]
- Filing method: [Comptroller Webfile / eSystems / accounting software]
- Combined local rate: [your jurisdiction's % — state 6.25% + local up to 2%]
- Use tax owed: [Yes/No]
- Authority: Texas Tax Code ch. 151 (state rate 6.25%, § 151.051); Texas Comptroller (comptroller.texas.gov)

FORMAT:
- Taxable-sales table: # | Invoice # | Date | Customer | Gross sale | Exempt/resale | Taxable | Rate | Tax due
- Use-tax table: # | Purchase | Date | Vendor | Taxable amount | Rate | Use tax due
- Return summary: total taxable sales | state tax (6.25%) | local tax | total due
- Pre-submission checklist: 10 items ☐
- Filing calendar: 12 periods × deadline + reminder T-5 days
- FAQ: 10 common situations (resale certificates, exemptions, marketplace facilitator, nexus)

TONE: Tax — precise, compliance-focused, with specific references.
LENGTH: 5-7 pages.

NOTE: General information, not tax advice. Confirm rate, frequency, and rules with a licensed Texas CPA / the Comptroller.
```

---
✍️ Author: Brian H. Doan
