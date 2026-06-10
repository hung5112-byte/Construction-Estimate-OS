# Custom Templates (BYOT)

Put your division's own templates into the right subfolder by **official department code** (see `departments/` in the repo):

```
00-Templates-Custom/
├── 01-hardware-engineering/      # design reviews, engineering inputs
├── 02-npi-program-management/    # BOMs, ECOs, cert trackers, sourcing SOPs
├── 03-quality-reliability/       # QMS docs, inspection plans, 8D reports
├── 04-mfg-supplier-quality/      # SCARs, vendor scorecards, process docs
└── 05-service-operations/        # RMA/fulfillment/inventory/deployment SOPs
```

Full department codes: 01-hardware-engineering, 02-npi-program-management, 03-quality-reliability, 04-mfg-supplier-quality, 05-service-operations

The system prioritizes templates here over the default templates.
Generic business templates (finance, HR, marketing, …) from the original library are
parked in the repo's `templates-us/_shared/` — copy any you need into a folder above.
Supported formats: .md, .docx, .xlsx
