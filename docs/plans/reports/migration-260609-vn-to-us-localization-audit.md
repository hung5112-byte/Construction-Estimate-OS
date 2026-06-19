# MIGRATION AUDIT — Vietnam → US (Federal) + Texas

**Status:** Phase 1 (Audit only). **No source files have been edited.**
**Date:** 06/05/2026
**Scope:** Translate all Vietnamese → US English and re-localize legal/regulatory/financial/reference content from Vietnam to US federal law + Texas state law, for a solo operator in Texas.

> ⚠️ **This audit is a planning document, not legal/tax advice.** Every US/Texas legal target named below is a *candidate* that must be confirmed with a licensed Texas attorney and CPA before it ships as fact. Items I cannot attribute with high confidence are marked `[UNCERTAIN]`.

---

## 0. Headline numbers

| Metric | Value |
|---|---|
| Total files in repo | ~480 (incl. binaries) |
| Files containing Vietnamese text | **411** |
| Total Vietnamese-text occurrences (lines) | **~12,134** |
| Hard-coded VN legal/tax logic (code) | 4 files (`tax_calculator.py`, `vn_law_search.py`, `vn_local_regulation.py`, `classifier_rules.yaml`) |
| VN gov/legal domains hard-coded | 8 (`thuvienphapluat.vn`, `luatvietnam.vn`, `vbpl.vn`, `moj.gov.vn`, `chinhphu.vn`, `tphcm.gov.vn`, `hanoi.gov.vn`, `danang.gov.vn`) + `gso.gov.vn` (tests) |
| VN business templates (`templates-vn/`) | ~192 `.md` meta-prompt files + 9 orchestrator files |
| Department agent prompts (`departments/`) | 33 agent `.md` + 12 `department.yaml` |
| Industry-pack files (`packs/`) | ~20 (F&B, Retail, Tech-SaaS) |
| Core Python files w/ VN comments/strings | ~30 |
| Test files w/ VN content | ~50 (several assert on VN strings/keywords) |
| Planning/history docs (`plans/`) | ~15 large files (dev history) |

> ⚠️ **This is NOT a git repository** (`git rev-parse` → not a repo). The "keep originals in git history" option from your brief is therefore unavailable as-is. A backup strategy decision is required — see §6, Decision D0.

---

## 1. Repo orientation (what the system is)

A Python + LangGraph "AI Operating System" for a department head. The Department Head chats in Claude Desktop/Code → an MCP server (`bd-business-os`) exposes tools (`bd_run`, `bd_resume`, `bd_meeting`, `bd_approve`, `bd_execute`, `bd_draft`, `bd_status`, `bd_onboard`, `bd_upgrade`) → 12 "departments" of AI agents debate → produce reports and render `.docx/.xlsx` into an Obsidian vault. Heavy Vietnamese localization is baked into: agent prompts, ~192 document templates, the Brain (vault knowledge base), tax/law tools, routing keywords, and all docs.

**Code identifiers / API contracts that MUST be preserved unchanged** (per your constraints): the MCP tool names (`vn_*`), the package/CLI names (`bd-os`, `bd-os-mcp`, slug `bd-business-os`), Python module/class/field names (incl. the dataclass field `name_vn`), and the 5-stage flow. These are addressed under "Decisions" rather than translated blindly.

---

## 2. Category (a) — PLAIN TRANSLATION (Vietnamese → US English)

No legal change; just language. Largest bucket by volume.

| Group | Files | Notes |
|---|---|---|
| Root docs | `README.md`, `README-USER.md` (702 VN lines — biggest single file), `SPEC.md`, `CLAUDE.md`, `START-HERE.md`, `ROADMAP.md`, `NEXT-STEPS.md`, `DECISIONS.md`, `CONTRIBUTING.md`, `SESSION-LOG.md`, `NOTICE` | User- and dev-facing prose. |
| `docs/` | `getting-started.md`, `user-guide.md`, `configuration.md`, `troubleshooting.md`, `architecture.md`, `install-claude-code.md`, `how-to-create-agent.md`, `how-to-create-pack.md` | |
| Agent prompts | `departments/**/agents/*.md` (33), `departments/**/department.yaml` (12), `packs/**` agents | Prose + frontmatter `name_vn`, `expertise`, `deliverables`. **Many also carry legal content → see (b).** |
| Templates | `templates-vn/**` (~201) | Meta-prompts. **Most also carry legal/finance/format content → see (b)/(d).** |
| Vault Brain templates | `vault-template/00-Brain/*.md` (strategy, products, budget, headcount, state, glossary, decisions-log), `vault-template/00-Templates-Custom/README.md` | **`laws.md`, `budget.md` → see (b)/(d).** |
| Translator data | `core/translator/terms_dictionary.yaml` (EN acronym → VN explanation; flip to EN explanation), `glossary.py`, `jargon_detector.py`, `simplifier.py`, `tldr_generator.py`, `pipeline.py` | RULE 4 ("Department-Head-friendly **Vietnamese**") becomes "plain **English**". |
| Core code comments/docstrings/user-strings | ~30 `core/**/*.py` incl. `mcp_server.py` (72 VN lines — tool descriptions shown in Claude Desktop), `flow_controller.py`, `cli.py`, `onboard.py`, `upgrade.py`, providers, brain, agents, orchestrator | Translate comments/docstrings/**user-visible strings**; do not touch identifiers. |
| MCP adapters | `adapters/claude-code/skill.md`, `adapters/claude-cowork/skills/bd-business-os/SKILL.md`, plugin READMEs, `plugin.json` description | The skill `description:` is the trigger text shown to Claude — translate. |
| Test fixtures & assertions | `tests/fixtures/**` (demo-vault, techco-vault Brain files), plus ~50 test files. **Tests that assert on VN strings/keywords must be updated in lockstep** (e.g., `test_router.py`, `test_citation_validator.py`, `test_b_campaign_high_income.py`). | Changing prose without updating asserts = red tests. |
| Scripts | `scripts/onboard.py`, `scripts/add_*_aliases.py`, `scripts/dev/*.sh` | Comments + echo strings. |

---

## 3. Category (b) — LEGAL / REGULATORY RE-MAPPING (Vietnam → US federal + Texas)

This is the substance of the migration. Each row: **VN concept found → candidate US/Texas target (authority + topic).** **All targets require attorney/CPA confirmation; specific rates/sections are `[UNCERTAIN]` until verified in Phase 3.**

### 3.1 Entity / formation / registration
| VN (found in repo) | Candidate US/TX target | Where |
|---|---|---|
| Luật Doanh nghiệp 2020 (59/2020/QH14); công ty TNHH MTV (single-member LLC); điều lệ; HĐQT/ĐHĐCĐ | **Texas Business Organizations Code (TBOC)** — entity formation; single-member LLC; *no 1:1 for HĐQT/ĐHĐCĐ governance organs* — a single-member LLC has no board/shareholder meeting requirement. Also surface **sole proprietorship + assumed name ("DBA")**. | `legal-officer.md`, `dieu-le-cong-ty.md`, `checklist-dkkd.md`, `thoa-thuan-co-dong.md`, `quy-che-hdqt.md`, `quy-che-bgd.md`, `bien-ban-hop-hdqt.md`, Brain `laws.md` |
| ĐKKD (đăng ký kinh doanh); MST (mã số thuế) | **Texas Secretary of State** (Certificate of Formation); **county Assumed Name Certificate** (DBA); **IRS EIN**; **Texas Comptroller** taxpayer number + sales-tax permit | same as above + finance templates |
| Luật Đầu tư 2020 — ngành nghề kinh doanh có điều kiện, giấy phép con | No federal omnibus analog; industry-specific federal/state/local licensing. *VN "giấy phép con" concept does not map 1:1* — flag removal/restate. | `legal-officer.md`, `danh-sach-giay-phep-con.md`, `compliance-checker.md` |

### 3.2 Tax (the highest-risk area)
| VN (found) | Candidate US/TX target | Where |
|---|---|---|
| Thuế GTGT / VAT (10%, mẫu 01/GTGT, TT 78/2021 e-invoice) | **Texas sales-and-use tax** via **Texas Comptroller** — *conceptually different from VAT* (no input-credit chain; no federal VAT exists). Mandatory e-invoice format has **no US analog** → remove, note. `[UNCERTAIN]` state rate 6.25% + local up to 2%. | `tax_calculator.py`, `accountant.md`, `bang-ke-thue-gtgt.md`, `cfo.md`, Brain `laws.md` |
| Thuế TNCN / PIT (progressive 5–35%, VND brackets, 11M deduction) | **IRS federal individual income tax** (filing-status brackets) **+ self-employment tax (Social Security + Medicare)**. **Texas has NO state personal income tax** — must reflect, not invent. `[UNCERTAIN]` all bracket figures/year. | `tax_calculator.py` (`TNCN_BRACKETS`), `accountant.md`, `cfo.md`, `financial-analyst.md` |
| Thuế TNDN / CIT (20%) | **IRS** — C-corp flat **21%** `[UNCERTAIN/verify]`, OR pass-through (LLC/sole-prop reported on owner's Form 1040). **Texas franchise (margin) tax** via Comptroller — `[UNCERTAIN]` no-tax-due threshold + rates. | `tax_calculator.py`, `cfo.md`, `accountant.md` |
| Thuế nhà thầu nước ngoài (foreign-contractor withholding, TT 103/2014, TT 60/2012) | Different concept: US **Form 1099-NEC** contractor reporting; foreign-payee withholding (W-8BEN / Form 1042, default 30%). `[UNCERTAIN/CPA]`. Consider removing this calculator branch. | `tax_calculator.py` (`_foreign_contractor_rates`) |
| Lệ phí môn bài (annual business-license tax) | **No direct US analog.** Texas has no general annual business-license fee. → Remove + note. | `tax_calculator.py` description, finance docs |

### 3.3 Labor / payroll / benefits
| VN (found) | Candidate US/TX target | Where |
|---|---|---|
| Bộ luật Lao động 2019 (45/2019/QH14): HĐLĐ xác định/không xác định thời hạn, thử việc ≤60 ngày, OT ≤200h/năm, trình tự sa thải | **US: at-will employment** (Texas); **FLSA** (federal min wage + overtime 1.5× >40h/wk). *VN fixed-term/probation/dismissal-procedure mandates largely have no Texas analog* → remove/restate + note. `[UNCERTAIN — attorney]` | `legal-officer.md`, `hr-manager.md`, `hop-dong-lao-dong-mau.md`, `noi-quy-lao-dong.md`, `sop-nghi-viec.md`, `chinh-sach-nghi-phep.md` |
| BHXH 8% + BHYT 1.5% + BHTN 1% = 10.5% (employee); lương cơ sở; lương tối thiểu vùng | **FICA**: Social Security 6.2% + Medicare 1.45% (employee), employer match; **FUTA** + **Texas SUTA** (employer-paid unemployment, TWC); **federal minimum wage** (FLSA) / Texas Minimum Wage Act. `[UNCERTAIN]` all percentages/wage-base figures/year. | `accountant.md`, `cfo.md`, `quy-che-luong-thuong.md`, `chinh-sach-phuc-loi.md`, Brain `laws.md` |
| Payday / wage payment | **Texas Payday Law** (Texas Workforce Commission). | HR/finance docs |

### 3.4 Accounting / invoicing
| VN (found) | Candidate US/TX target | Where |
|---|---|---|
| Luật Kế toán 2015 (88/2015/QH13); TT 200/2014/TT-BTC chart of accounts (TK 1xx–9xx); BCTC (BCĐKT/BCKQKD/LCTT); MISA/Fast software | **US GAAP (FASB)** for accrual; small businesses commonly cash-basis; **no government-mandated chart of accounts**; IRS recordkeeping. Software analogs (QuickBooks/Xero) are illustrative only. | `accountant.md`, `thuyet-minh-bctc.md`, `bang-can-doi-ke-toan.md`, `bao-cao-pl.md`, etc. |
| Hóa đơn điện tử bắt buộc (TT 78/2021) | **No US mandated e-invoice format** — invoices are free-form. Remove mandatory-format compliance steps + note. | `accountant.md`, `bang-ke-thue-gtgt.md`, retail pack |

### 3.5 Industry-specific compliance (packs)
| VN (found) | Candidate US/TX target | Where |
|---|---|---|
| VSATTP — NĐ 15/2018/NĐ-CP; Luật ATTP 2010; ATTP certificate | **FDA Food Code** + **Texas DSHS** food-establishment rules + **local health-dept permit**; HACCP still applies (FDA). `[UNCERTAIN — cite/verify]` | `packs/fnb/**` (`pack.yaml`, `hygiene-officer.md`, brain template) |
| PCCC — TCVN 5738:2021 (fire) | Local fire code / **NFPA** + municipal fire marshal (Texas). | `packs/fnb/pack.yaml`, ops docs |
| NĐ 13/2023 PDPA (data protection) | **Texas Data Privacy and Security Act (TDPSA)** `[UNCERTAIN — verify effective date/scope]`; no federal omnibus. GDPR references may remain (EU). | `packs/tech-saas/**`, `chinh-sach-bao-ve-du-lieu.md`, `security-officer.md`, `chinh-sach-an-ninh-mang.md` |

### 3.6 IP / contracts / commerce
| VN (found) | Candidate US/TX target | Where |
|---|---|---|
| SHTT — Cục SHTT, nhãn hiệu, bảo hộ 10 năm gia hạn | **USPTO** (federal trademark, 10-yr renewable terms `[verify]`); copyright (US Copyright Office); Texas trademark via SOS. | `legal-officer.md`, IP-related templates |
| Luật Thương mại — phạt vi phạm ≤8% giá trị HĐ | **No statutory 8% cap in US.** Liquidated-damages enforceability under **Texas common-law contract doctrine** (must be a reasonable forecast, not a penalty). Remove cap + restate. `[UNCERTAIN — attorney]` | `legal-officer.md`, `hop-dong-*.md` contract templates |

### 3.7 Benchmarks / statistics
| VN (found) | Candidate US/TX target | Where |
|---|---|---|
| GSO / gso.gov.vn (Tổng cục Thống kê) | **US Census Bureau** / **Bureau of Labor Statistics (BLS)** / **BEA**. | `test_citation_validator.py`, benchmark docs |
| `benchmarks-vn.yaml` — VND CAC/AOV, VN-tagged ratios | Re-source to US benchmarks (cite real reports). Some figures `[UNCERTAIN]` — need sourced US data, not FX-converted VND. | `core/tools/data/benchmarks-vn.yaml`, `industry_benchmark.py` |

---

## 4. Category (c) — LINK REPLACEMENT

| VN link (found) | Candidate authoritative US source | File(s) |
|---|---|---|
| `thuvienphapluat.vn`, `luatvietnam.vn`, `vbpl.vn` (law search trusted domains) | `irs.gov`, `comptroller.texas.gov`, `sos.state.tx.us` / `sos.texas.gov`, `statutes.capitol.texas.gov`, `uscode.house.gov`, `sba.gov`, `dol.gov`, `twc.texas.gov` | `core/tools/vn_law_search.py` (`TRUSTED_DOMAINS`), `SPEC.md`, tests |
| `moj.gov.vn`, `chinhphu.vn` | `usa.gov` + specific federal agency | `vn_law_search.py`, `vn_local_regulation.py` |
| `tphcm.gov.vn`, `hanoi.gov.vn`, `danang.gov.vn` (local-regulation domains) | `texas.gov` + **city/county sites** — **which city?** `[UNCERTAIN — needs your city]` (e.g., Houston/Austin/Dallas) or keep state-level only | `core/tools/vn_local_regulation.py` (`TRUSTED_LOCAL_DOMAINS`), `phase-04` plan, tests |
| `gso.gov.vn` | `census.gov`, `bls.gov` | `tests/unit/test_citation_validator.py` |
| `base.vn`, `misa.vn` (example competitors / accounting SaaS in tests) | US analogs (illustrative only, e.g., QuickBooks, Gusto) — low stakes | `tests/unit/test_competitor_research.py`, `phase-04` plan |
| `bio.ybai.me/777777` + "Tác giả: Quốc MODORO / Tài liệu được tạo bởi MODORO" footer (in ~100 `templates-vn/` files) | **Third-party attribution** from the vendored `business-builder.plugin` (see `NOTICE`). **Decision D5** — keep (translate label, retain link) vs remove. | every `templates-vn/**` file |
| `andyluu98/bd-business-os`, `<owner>/<repo>` GitHub URLs | Repo-owner's choice (placeholder) — leave or update per your repo | `README-USER.md`, `docs/install-claude-code.md` |

Non-jurisdiction links to **keep as-is**: `python.org`, `nodejs.org`, `obsidian.md`, `claude.ai`, `tavily.com`, `platform.deepseek.com`, `langchain-ai/langgraph`, `apache.org/licenses`, `modelcontextprotocol.io`, TradingAgents/agency-agents credits.

---

## 5. Category (d) — FORMAT / CURRENCY / DATE / PHONE / ADDRESS CONVERSION

| Item | Found | Conversion approach |
|---|---|---|
| **Currency** | VND everywhere: `8tr`/`50tr`/`1.2 tỷ` shorthand; literal amounts (`11000000` PIT deduction, `8000000` CAC, `450000` AOV); `*_vnd` keys in `tax_calculator.py`; budgets | VND → **USD**. **Illustrative example amounts** (salaries, campaign budgets) will be **re-set to realistic US figures for context**, not mechanically FX-converted (FX would imply false precision). Benchmark data → re-sourced US figures (see 3.7). `_vnd` dict keys in code are identifiers → **Decision D4** (rename to `_usd` vs keep). |
| **Date** | `last_updated: YYYY-MM-DD` frontmatter (ISO); prose dates `2026-05-06`; "T-5 ngày" reminders | Prose/display dates → **MM/DD/YYYY**. **Keep ISO in machine/frontmatter fields** to avoid breaking any parser (flagged, not assumed). |
| **Phone** | Placeholder phone fields in contract/HR templates | → US format `(XXX) XXX-XXXX`. |
| **Address** | VN address placeholders ("Quận 1 TPHCM", province/district) in contracts, JDs, examples | → US format (street, City, TX ZIP). Example locale → a Texas city `[UNCERTAIN — your city]`. |
| **Units / misc** | "trang A4" (paper size), °C temperatures (food-safety), VN regional terms | A4 → **Letter**; °C → keep or add °F (FDA Food Code uses °F) — note in food-safety pack. |

---

## 6. Category (e) — UNCERTAIN / NEEDS YOUR DECISION OR ATTORNEY/CPA REVIEW

### Legal/tax items requiring CPA/attorney sign-off (will be written with `[UNCERTAIN — verify with attorney/CPA]` + cited authority, never as bare fact):
- **U1** — All federal income-tax bracket figures, deductions, and the 2026 schedule (IRS).
- **U2** — Texas franchise-tax no-tax-due threshold + margin rates (Comptroller).
- **U3** — Texas sales-and-use tax state + local rates (Comptroller).
- **U4** — FICA/FUTA/SUTA percentages + wage bases for the current year (IRS/TWC).
- **U5** — Federal + Texas minimum wage figures (DOL/TWC).
- **U6** — C-corp 21% / pass-through treatment specifics (IRS).
- **U7** — Foreign-contractor / 1099 / W-8BEN withholding handling (IRS) — and whether to keep that calculator branch at all.
- **U8** — TDPSA effective date/applicability thresholds (Texas data-privacy law).
- **U9** — FDA Food Code / Texas DSHS food-establishment specifics + local permit naming.
- **U10** — USPTO trademark term specifics; Texas contract liquidated-damages doctrine wording.
- **U11** — Whether any VN labor mandate (severance, 13th-month, mandatory written contract) should be replaced vs simply removed (no Texas analog).

### Product/structure decisions I need from you before Phase 2:

- **D0 — Backup strategy (blocking).** Not a git repo, so "git history" isn't available. Options: (A) one full-tree snapshot copy `…\bd-business-os-master.vi-backup\` before any edit; (B) per-file `.vi` sibling for each of the ~411 edited files; (C) `git init` + initial commit, then edit on a branch. *(Recommend A or C.)*
- **D1 — Brand/product name.** Code contracts (`vn_*` MCP tools, `bd-os` CLI, slug `bd-business-os`, package name) **must stay** to avoid breaking the MCP/skill. But the human-readable title "VN Hardware Division OS / VN Business OS" can be rebranded (e.g., "Hardware Division OS" / "TX Business OS"). What do you want the displayed name to be? *(Recommend: keep code slugs; rename only display title.)*
- **D2 — `templates-vn/` directory name.** Referenced by `core/orchestrator/document_executor.py`, `core/obsidian/template_resolver.py`, and ~6 tests. Keep the path (zero code churn) vs rename to `templates/`/`templates-us/` (update all refs). *(Recommend: keep path, translate contents — lowest risk.)*
- **D3 — Template/agent filenames (Vietnamese slugs, e.g. `hop-dong-lao-dong-mau.md`).** Keep slugs (referenced by resolver + tests) vs anglicize (e.g., `employment-agreement-template.md`, requires updating tests + any references). *(Recommend: phase it — translate contents first; anglicize filenames as an optional follow-up.)*
- **D4 — Identifier-embedded jurisdiction tokens** (`name_vn` field, `*_vnd` dict keys, `benchmarks-vn.yaml` filename, `vn_law_search`/`vn_local_regulation` tool names). These are code identifiers. *(Recommend: keep identifiers unchanged to honor API contracts; translate only their string values. Note: `agent_loader.py`/`department.py` already support an optional `name_en` field we can populate.)*
- **D5 — MODORO attribution footer** in ~100 templates (third-party credit + `bio.ybai.me` link). Keep (translate the label, retain link/credit) vs remove. *(Recommend: keep attribution per NOTICE/Apache; translate surrounding label.)*
- **D6 — Routing keywords** (`classifier_rules.yaml`): currently Vietnamese ("chiến dịch", "tuyển dụng"…). They must become English ("campaign", "hiring"…) so English briefs route correctly. This is required language work but **does change which inputs trigger which route** — flagging because it brushes your "don't alter behavior" guardrail (it's a necessary consequence of switching the operating language). Confirm OK.
- **D7 — `plans/` directory (~15 large dev-history docs, incl. `audit-260507-*-vn.md` duplicates and `v3-vietnamization-future.md`).** In scope (translate everything) vs treat as historical artifacts (leave, or translate last)? *(Recommend: lower priority; translate user-facing docs/runtime first.)*
- **D8 — Example locale / city.** Several examples and the `vn_local_regulation` domains are city-specific (HCMC/Hanoi/Danang). What Texas city should examples and local-gov links use (e.g., Houston, Austin, Dallas), or stay state-level only?

### Explicitly OUT OF SCOPE / DO NOT TOUCH (per your constraints):
- `references/business-builder.plugin` (372 KB **vendored** blob — the upstream source of the templates; "do not touch vendored dependencies").
- `LICENSE` (Apache text), lockfiles, `.env`/secrets, `.git/`, build artifacts.
- `C:\Hardware Division OS\Vault\USA-TX Company\` — **your live Obsidian vault** (REST-API + terminal plugins), not part of this repo.
- Code identifiers, module/class/function names, the 5-stage flow, MCP tool names (translate descriptions only).

---

## 7. Proposed Phase 2 execution order (for when you approve)

1. **Backups** per D0.
2. **Jurisdiction core first** (highest risk, smallest surface): `tax_calculator.py`, `vn_law_search.py`, `vn_local_regulation.py`, `classifier_rules.yaml`, `benchmarks-vn.yaml`, Brain `laws.md`/`budget.md` — with `[UNCERTAIN]` flags + cited authorities.
3. **Agent prompts** (`departments/`, `packs/`) — legal-bearing roles (legal-officer, accountant, cfo, compliance-checker, hygiene-officer, security-officer) get re-mapping; others get plain translation.
4. **Templates** (`templates-vn/`) — translate + re-map legal/finance/format; handle MODORO footer per D5.
5. **Docs + root + adapters** — plain translation.
6. **Translator module + terms_dictionary** — flip VN→EN.
7. **Tests + fixtures** — update assertions in lockstep (tax tests depend on resolved `[UNCERTAIN]` rates).
8. **Links + verification (Phase 3)** — replace + verify each URL; mark `[UNVERIFIED — confirm manually]` where I can't confirm.
9. **`MIGRATION_REPORT.md`** — full change list + every removed VN-only item + every `[UNCERTAIN]`/`[UNVERIFIED]` flag.

---

**Phase 1 complete. Awaiting your review + decisions (D0–D8) before any edits.**
