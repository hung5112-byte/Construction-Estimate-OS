# MIGRATION REPORT — Vietnam → US (Federal) + Texas

**Status:** Substantially complete. The entire **runnable system**, all **192 document templates** (content **and filenames** — `templates-us/` with English slugs), all **user-facing docs**, all **root docs**, and the **major dev-history/plans** are converted, re-localized, and test-verified (273 passed). Phase 3 link verification is done. A small set of **internal dev build-log files** is explicitly deferred — see §7.
**Date:** 06/09/2026
**Backups:** Per the agreed Phase-1 decision, the pristine Vietnamese originals are preserved as a **full-tree snapshot** (outside the working tree). Nothing was deleted from the working tree.

> ⚠️ **This is general information, NOT legal or tax advice.** Every US/Texas legal statement marked `[UNCERTAIN]`/`[verify]` must be confirmed with a licensed Texas attorney and CPA before you rely on it. Per your stop conditions, I have **not resolved** any `[UNCERTAIN]`/`[UNVERIFIED]` item — they are flagged for your review.

---

## 1. Verification status

- **Test suite (as of the code pass): 273 passed, 3 skipped, 1 failed.**
  - The 3 skips require live API keys (`TAVILY_API_KEY` / `ANTHROPIC_API_KEY`).
  - The 1 failure is **pre-existing and unrelated to localization**: `test_phase_tags_present` runs `git tag` expecting `phase-0X-complete` tags, which don't exist because this repo was delivered as a **zip with no git history**. I did not fabricate git tags. *(Run under `PYTHONUTF8=1` on Windows so the CLI's `✓`/unicode output doesn't hit a cp1252 console error.)*
- **`core/`, `tests/`, `departments/`, `packs/`, `vault-template/` are free of Vietnamese** (verified by Vietnamese-diacritic grep). Two late misses were found and fixed in this pass: a stray `từ` in `core/agents/agent_loader.py` (docstring) and an untranslated `packs/tech-saas/departments/13-engineering/department.yaml` (`name_vn`/description/aliases). The only remaining `đ` in code is the **intentional** `str.replace("đ","d")` in `_slugify` (diacritic-stripping logic, kept for robustness).

---

## 2. Decisions applied (from the audit + your steering)

| Decision | Choice applied |
|---|---|
| Backups | Full-tree snapshot of the Vietnamese originals (kept outside the working tree) |
| Code identifiers | Kept the MCP/package contract (`vn_run`…, `vn-business-os`, `vn-os`); anglicized internals (`vn_law_search`→`us_law_search`, `vn_local_regulation`→`us_local_regulation`, `*_vnd`→`*_usd`, `benchmarks-vn.yaml`→`benchmarks-us.yaml`) |
| TX locale | State-level only (texas.gov / Comptroller / SOS / TWC / DSHS / TDLR; "City, TX") |
| Display name | "Hardware Division OS" |
| MODORO footer | Keep credit + link, translate the label (applied to all 192 templates) |
| Routing keywords | VN→EN (so English briefs route) |
| Templates pass | **Full careful pass on all 192** |
| `[UNCERTAIN]` handling | State widely-published **stable** figures with citation (SE tax 15.3%, C-corp 21%, TX state sales tax 6.25%, federal min wage $7.25, FICA 6.2%+1.45%, no TX personal income tax); keep **year-specific** brackets/thresholds/wage-bases flagged `[UNCERTAIN]` |

---

## 3. Completed changes — by area

### 3.1 Jurisdiction-core code (highest risk) ✅ verified
- **`core/tools/tax_calculator.py`** — fully rewritten. VN VAT/PIT/CIT/foreign-contractor → **Texas sales-and-use tax (6.25%, Tex. Tax Code §151.051), self-employment tax (15.3% = 12.4% SS + 2.9% Medicare, IRC §1401), federal income tax (progressive, IRC §1), federal corporate tax (21%, IRC §11), Texas franchise tax (Tex. Tax Code ch. 171)**. Stable rates stated with citation; every year-specific figure (brackets, wage base, no-tax-due threshold) flagged `[UNCERTAIN]` with the responsible authority (IRS / Texas Comptroller). VN-only `lệ phí môn bài` and `thuế nhà thầu` **removed** (noted inline). `*_vnd`→`*_usd`. Not-advice `_DISCLAIMER` constant added.
- **`core/tools/us_law_search.py`** (renamed) — trusted domains → `irs.gov, uscode.house.gov, ecfr.gov, statutes.capitol.texas.gov, comptroller.texas.gov, sos.state.tx.us, sba.gov, dol.gov, usa.gov`.
- **`core/tools/us_local_regulation.py`** (renamed) — `texas.gov, comptroller.texas.gov, sos.state.tx.us, twc.texas.gov, dshs.texas.gov, tdlr.texas.gov`.
- **`core/tools/data/benchmarks-us.yaml`** (renamed) — VND→USD, all flagged `[UNCERTAIN]`.
- **`core/orchestrator/classifier_rules.yaml`** — routing keywords VN→EN.
- **`core/brain/schema.py` + `reader.py`** — `*_vnd`→`*_usd`; parser headings → English (`Vision`, `Target Customer (ICP)`, `Total budget:`, `Stage`); laws-parser regex generalized to **US citation formats**.

### 3.2 Orchestration prompts ✅ verified
All English: router, gap analyzer, clarifier, tool router, pro/con advocates, perspective debators (Growth/Cautious/Balanced), synthesizer, execution planner, document executor, perspectives collector, base-agent scaffolding, citation validator (currency/law regexes → USD/`U.S.C.`/`§`/`Act`), translator pipeline (`terms_dictionary.yaml` `vn:`→`en:` with USD examples). TL;DR marker `📌 Tóm lại`→`📌 Bottom line`.

### 3.3 Departments (12 configs + 33 agent prompts) ✅
All `department.yaml` (`name_vn`/descriptions/keywords/aliases) and all 33 agent `.md` prompts translated; legal/finance agents re-mapped with cited authority + `[UNCERTAIN]` flags. `Base/Bull/Bear`→`Base/Upside/Downside`.

### 3.4 Industry packs (3 packs, 19 files) ✅
- **F&B**: `NĐ 15/2018 VSATTP`→**FDA Food Code + Texas DSHS**; temps→°F; fire→local/NFPA.
- **Retail**: Shopee/Lazada/Tiki→Amazon/Walmart/Etsy/Shopify; GHN/GHTK/J&T→USPS/UPS/FedEx/DHL; consumer law→FTC + Texas DTPA.
- **Tech-SaaS**: `NĐ 13/2023`→**TDPSA + HIPAA/GLBA / GDPR** (flagged). (The one missed pack dept yaml was fixed in this final pass — see §1.)

### 3.5 Brain templates + fixtures ✅
`vault-template/00-Brain/*.md` (8) + `00-Templates-Custom/README.md` (English/USD; `laws.md` pre-fills TBOC/FLSA/IRC). Fixtures `demo-vault` + `techco-vault` (16 files) English/USD.

### 3.6 Supporting code ✅ verified
`mcp_server.py`, `cli.py`, `flow_controller.py`, `draft.py`, `onboard.py`, `upgrade.py`, `wikilinks.py`, `install_mcp.py`, `providers.py`, `config.py`, `base_tool.py`, `competitor_research.py`, `web_search.py`, `memory.py`, `meeting_graph.py`, `registry.py`, `agent_loader.py` — comments/docstrings/user-strings English. `draft.py` re-maps to US law + not-advice disclaimer.

### 3.7 Tests, scripts, adapters ✅
All ~50 test files updated in lockstep (suite green). `scripts/onboard.py`, `scripts/add_*_aliases.py`, `scripts/dev/*` English. `adapters/claude-code` + `claude-cowork` skill **trigger descriptions**, READMEs, `install.sh`, `plugin.json` → English (trigger now activates on **US** business operations).

### 3.8 Templates — all 192 ✅ (this pass)
Full careful pass across every directory: `01-governance` (19), `02-strategy` (18), `03-finance` (20), `04-people` (22), `05-operations` (20), `06-sales` (17), `07-marketing` (10), `08-customer` (12), `09-product-tech` (13), `10-training` (10), `11-reporting` (10), `12-growth` (12), `_orchestrator` (9). Each: VND→USD, MM/DD/YYYY dates, US phone/address, US GAAP, MODORO footer translated, and legal/tax re-mapping with cited authority + `[UNCERTAIN]`/not-advice disclaimers where relevant. Key legal re-maps include:
- Governance: TBOC entity formation, at-will/FLSA employment agreement, Texas-governed NDA, TDPSA data policy, FCPA/EEOC ethics, shareholders/members agreement.
- Finance: Texas Sales-and-Use Tax worksheet (Comptroller), US GAAP statements/notes, AR/AP allowance under ASC 326, MACRS/de-minimis capitalization note.
- People: workplace conduct (at-will/EEOC/OSHA), comp & benefits (FLSA/FICA, no 13th-month), leave/PTO (FMLA 50+; no federal paid-leave mandate), offer letter (at-will + Form I-9), benefits (FICA/FUTA/SUTA + ACA 50-FTE note + **Texas optional workers' comp**), offboarding (Texas Payday Law final-pay timing + COBRA 20+), recruitment (Title VII/ADA/ADEA/I-9/FCRA).
- Operations: OSHA safety, ISO 9001 quality, US capitalization/MACRS, LIFO/FIFO note.
- Sales: Texas/UCC Art. 2 contract + **liquidated-damages (not penalty) caveat**, Texas §15.50 non-compete reasonableness.
- Marketing: FTC truthful-ads + CAN-SPAM + FTC endorsement/influencer disclosure.
- Customer: refund/warranty (Magnuson-Moss + Texas DTPA + FTC), FTC honest-reviews rule.
- Product-tech: cybersecurity (TDPSA + NIST + Tex. Bus. & Com. Code ch. 521 breach notice).
- Training: training-repayment-agreement (TRAP) enforceability caveat.
- Growth: **FTC Franchise Rule (FDD, 14-day) + Texas Business Opportunity Act**; **Reg D 506(b)/(c) + Form D** securities flags on term sheet / cap table / investment memo / pitch deck; QSBS exit-tax note.

### 3.9 Docs (all) ✅
`CLAUDE.md`, `README.md`, `docs/getting-started.md`, `docs/architecture.md`, `docs/configuration.md`, `docs/user-guide.md`, `docs/troubleshooting.md`, `docs/install-claude-code.md`, `docs/how-to-create-agent.md`, `docs/how-to-create-pack.md`, `docs/superpowers/specs/2026-05-08-claude-code-mcp-support-design.md`, root `.env.example`, `.gitattributes` → English + US/TX. Worked examples re-localized (holiday campaign in USD, FDA/DSHS, TDPSA, no VN ad pre-clearance, `us_law_search`).

### 3.10 Root + dev-history docs ✅
`README-USER.md` (full 1636-line non-coder guide rewritten in English: USD, FLSA/at-will, FDA/DSHS, TDPSA, English Brain headings matching the parser, "Lone Star Coffee" / "Misty Morning Café" example), `SPEC.md`, `START-HERE.md`, `ROADMAP.md`, `NEXT-STEPS.md`, `DECISIONS.md`, `SESSION-LOG.md`, `CONTRIBUTING.md`, `NOTICE`, `references/README.md`. **plans/**: `plan.md`, `v2-roadmap.md` (proposed pack compliance re-mapped to TREC/HIPAA/FERPA/TDLR/etc.), `v2-mcp-sampling-260506.md`, `v3-vietnamization-future.md` (flagged **OBSOLETE/superseded** by this US localization), `session-log-260506-implementation.md`, `reports/fix-260507-p1-fixes-summary-vn.md`.

---

## 4. VN-only items REMOVED (no US analog) — noted for your review

| Removed | Reason |
|---|---|
| `lệ phí môn bài` (annual business-license tax) | No general US/Texas annual business-license tax |
| `thuế nhà thầu nước ngoài` (foreign-contractor withholding) | Different concept; replaced conceptually by 1099 / W-8BEN handling, flagged for CPA |
| Mandatory e-invoice format (`TT 78/2021`) | US invoices are free-form; no mandated e-invoice / pre-clearance |
| 8% statutory contract-penalty cap (`Luật Thương mại`) | No US statutory cap; replaced with Texas liquidated-damages (not penalty) doctrine |
| Government-mandated chart of accounts (`TT 200/2014`) | US GAAP has no mandated chart of accounts |
| Company seal requirement | US businesses generally do not use/require a seal |
| Ad-content pre-registration with DOLISA/Dept. of Info & Comms (`NĐ 70/2021`) | US has no government ad pre-clearance (FTC: truthful + substantiated, post-hoc) |
| Registered "Internal Labor Regulations" filing (BLLĐ 2019, ≥10 employees) | US has no equivalent filing; replaced by an (unfiled) employee handbook + at-will |
| VN regional minimum wage + BHXH/BHYT/BHTN social-insurance mandates | Replaced with FLSA minimum wage + FICA/FUTA/SUTA + (Texas-optional) workers' comp |
| VN payment-method bias (COD), marketplaces (Shopee/Tiki/Lazada), Zalo | Replaced with US norms (ACH/card, Amazon/Shopify/Etsy, Slack/Teams) |

---

## 5. `[UNCERTAIN]` / `[UNVERIFIED]` flags — **require your attorney/CPA confirmation**

Written into the files next to the relevant content (never asserted as fact). Stable, widely-published figures are stated **with citation**; year-specific figures are flagged. High-level list:

**Tax (IRS / Texas Comptroller):**
- U1 — Federal income-tax **bracket thresholds** (year-specific placeholders in `tax_calculator.py`).
- U2 — Texas franchise-tax **no-tax-due threshold + margin rates** (year-specific).
- U3 — Local sales-tax add-on (state 6.25% confirmed; local up to 2% varies by jurisdiction).
- U4 — FICA **wage base** + FUTA/SUTA rates (current year; the 6.2%+1.45% rates are stated).
- U5 — Federal min wage $7.25 stated; any local/Texas variations to confirm.
- U6 — Pass-through vs. C-corp treatment specifics for the operator's entity.
- U7 — 1099 / W-8BEN foreign-contractor handling.

**Other law:**
- U8 — TDPSA effective scope/thresholds; sector laws (HIPAA/GLBA); breach notice (Tex. Bus. & Com. Code ch. 521).
- U9 — FDA Food Code temperatures/ppm + Texas DSHS permit / Certified Food Manager specifics.
- U10 — USPTO trademark term; FTC substantiation/endorsement specifics; liquidated-damages wording.
- U11 — Securities: Reg D 506(b)/506(c) + accredited-investor verification (`fundraising-lead`, term sheet, cap table, investment memo, pitch deck).
- U12 — FTC Franchise Rule / FDD 23-items + Texas Business Opportunity Act filing; FMLA eligibility (50+); COBRA (20+); Texas Payday Law final-pay timing; TRAP (training-repayment) enforceability; QSBS §1202 exit eligibility.

**Illustrative figures** (not law): example salaries, budgets, benchmark ranges, and office/rent costs were **re-set to realistic US figures**, not mechanically FX-converted from VND.

---

## 6. Phase 3 — link verification (done)

Verified live (WebFetch) that the replacement authoritative sources resolve and are correct:

| URL | Result |
|---|---|
| irs.gov …/self-employment-tax… | ✅ "Self-employment tax" — confirms **15.3% (12.4% SS + 2.9% Medicare)** |
| comptroller.texas.gov/taxes/sales/ | ✅ "Sales and Use Tax" — confirms **6.25% state**, up to 2% local (8.25% max) |
| comptroller.texas.gov/taxes/franchise/ | ✅ "Franchise Tax" — confirms privilege tax, annual report due **May 15** |
| statutes.capitol.texas.gov | ✅ Official Texas Constitution & Statutes — hosts **Business Organizations Code, Tax Code, Labor Code, Business & Commerce Code** |
| sos.state.tx.us …/businessstructure | ✅ "Selecting a Business Structure" — sole prop, partnership, corp, LLC, LP, LLP; certificate of formation |
| irs.gov …/apply-for-an-ein-online | ✅ "Get an employer identification number" — free EIN application |
| dol.gov/agencies/whd/flsa | ⚠️ Returns **HTTP 403 to automated fetch (bot-blocking)** — the URL is the standard DOL Wage & Hour FLSA page; the statutory anchor (29 U.S.C. §201 et seq.) is authoritative. Marked **[UNVERIFIED via automated fetch]** — open it in a browser to confirm. |

All other US/Texas references are anchored to **statutory citations** (IRC §, U.S.C. §, C.F.R., Tex. Tax/Labor/Bus.&Com./Bus.Orgs. Code), which are the durable source of truth regardless of any one agency page URL.

---

## 7. Remaining / deferred — internal dev build-logs (explicit, for your decision)

The following are **internal developer build-logs** (step-by-step implementation instructions from the original Vietnamese build). They contain Vietnamese but have **no user-facing, legal, financial, or runtime impact** — the shipped system, templates, docs, and all legal content are fully localized. They are deferred as a clearly-scoped follow-up rather than risk an incomplete report:

1. **`plans/phase-01-foundation.md` … `plans/phase-06-adapters-e2e-onboard.md`** (6 files, ~8,000 lines total) — the original phase-by-phase implementation plans.
2. **`plans/reports/`** — `fix-260507-p0-fixes-summary.md`, `fix-260507-p0-fixes-summary-vn.md`, `fix-260507-p2-fixes-summary-vn.md`, `audit-260507-repo-completeness-vn.md` (the **`audit-260507-repo-completeness.md`** non-`-vn` twin is already English). The `-vn` files are Vietnamese duplicates of their English twins.
3. **`docs/superpowers/plans/2026-05-08-claude-code-mcp-support.md`** (~403 lines) — implementation plan (its **spec** counterpart is already translated).

**Recommendation:** translate these in a focused follow-up pass; collapse the `-vn` report duplicates into their English twins (a deletion — held back here per your "show a diff before deleting" stop condition).

### Directory/filename rename ✅ DONE (06/09/2026)
The directory is renamed **`templates-vn/` → `templates-us/`** and all **178 Vietnamese-slugged files renamed to English slugs** derived from each template's translated title (14 already had English names; 192 total, zero collisions). The full old→new map is recorded at `plans/reports/template-rename-map.json`. All ~30 referencing files updated (`document_executor.py`, `template_resolver.py`, smoke/e2e/unit tests, CLAUDE.md, README, docs, adapters skill files, `.gitignore`, vendor script, plans). Test mocks updated from VN names to `business-plan`/`annual-budget`/etc. **This closed the one critical post-translation runtime break found in review:** the execution-planner LLM emits English template names, and the resolver substring-matches file stems — with Vietnamese stems, every `vn_execute` document render would have been silently skipped. `scripts/dev/vendor-bb-plugin.sh` now carries a do-not-re-run warning (re-running would restore Vietnamese-named files from the upstream zip). Suite re-verified: **273 passed, 3 skipped, 1 pre-existing git-tag failure** (unchanged).

### Review-pass doc fixes (06/09/2026)
- `README-USER.md` — products example switched to whole-dollar prices (the Brain parser strips `.`/`,`, so `3.50` would have been stored as `350`); header matched to the shipped vault-template (`Code | Name | Price | Margin | Status`); citation-warning section title matched to the validator's actual output.
- `docs/user-guide.md`, `docs/troubleshooting.md`, `plans/reports/fix-260507-p1-fixes-summary-vn.md` — citation-warning title aligned to `## ⚠️ Warning: claims missing a source` (verbatim from `citation_validator.py`).
- `START-HERE.md` (×4) + `NEXT-STEPS.md` (×2) — stale template count 191 → 192 (matches the test assertions).
- `adapters/claude-cowork/.claude-plugin/plugin.json` — credits key `templates_vn` → `templates_us`.

### Out of scope / untouched (per your constraints)
- `references/business-builder.plugin` (vendored upstream blob).
- `LICENSE`, lockfiles, `.env`/secrets, build artifacts, `.git/`.
- The MCP tool names / package slug / `vn-os` CLI (API contract — kept by design).

---

## 8. Acceptance-criteria status

| Criterion | Status |
|---|---|
| No Vietnamese in shipped UI/docs/prompts/comments | ✅ for all runtime code, templates, departments, packs, docs, root docs, and major plans. ⚠️ Remaining only in the deferred internal dev build-logs (§7). |
| No VN law/agency/link refs except flagged | ✅ All re-mapped to US/Texas or removed (§4) or flagged `[UNCERTAIN]` (§5). |
| All currency/date/address/phone US/Texas | ✅ USD, MM/DD/YYYY, US phone/address throughout. |
| Every legal/tax claim attributed or flagged | ✅ Stable facts cited to agency/statute; year-specific items flagged `[UNCERTAIN]`. |
| MIGRATION_REPORT.md summarizes changes/removals/flags | ✅ This document. |

*Prepared as general information only — confirm all legal/tax specifics with a licensed Texas attorney and CPA.*
