# P-FIN-13: Cash Voucher Templates

#### Description
A set of vouchers — cash receipt, payment voucher, payment/check request, and (optionally) an advance request — for a US small business. Designed to capture the required information, be easy to fill, and be easy to control.

#### Information to collect (ask the user before generating)
1. Does your accounting software print vouchers, or do you use manual/printable forms?
2. Voucher numbering convention? (e.g. CR-2026-001 for cash receipts, PV-2026-001 for payment vouchers)
3. Cash-handling controls? (e.g. a maximum amount to be paid in cash before requiring a check/ACH)
4. Do you need a separate advance (employee advance / petty cash) request form?

> Note: US small businesses commonly settle larger payments by check or ACH rather than cash, and rely on bank records plus these vouchers for an audit trail. There is no national cash-payment ceiling here; set your own internal threshold.

#### Suggested template
A set of forms:
- **Cash Receipt (CR)**: header (company name, EIN, address), receipt #, date, received from, purpose, amount (figures + words), account/deposit, signatures (preparer | approver | recipient)
- **Payment Voucher (PV)**: similar to CR — paid to, purpose, supporting documents attached, approval signature
- **Payment / Check Request**: requester, description, amount, attached invoice/receipt, approver
- **(Optional) Advance Request**: purpose, amount, reconciliation due date

Confirm the structure before generating.

#### File-generation prompt
```
Create a set of cash-voucher templates.

CONTEXT:
- Company: [Name] — EIN: [number]
- Software: [QuickBooks / Xero / printable forms]
- Numbering: [convention]
- Advance form: [Yes/No]
- Internal cash threshold: [amount above which check/ACH is required]

FORMAT:
- 4-5 separate templates, each one page
- Header: Logo + Company name + EIN + Address
- Fill fields: [___] + sample hint
- Amount: figures + words
- Signatures: correct positions (Owner/Approver | Bookkeeper/Controller | Cashier | Preparer | Recipient)
- Numbering format: [Type]-[Year]-[3-digit number]
- A short usage note attached to each form

TONE: Standard accounting, formal forms.
LENGTH: 5-7 pages (one page per form + 1-2 pages of instructions).
```

---
✍️ Author: Brian H. Doan
