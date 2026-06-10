# Roadmap — US One Person Company

> ⚠️ HISTORICAL (06/09/2026): this roadmap describes the original generic-business
> product. The repo has since been specialized into a 5-department hardware
> engineering & supply chain division OS — see `README.md` for the current state.
> Pack/industry plans below are superseded.

> The path from alpha (founder-only) to v1 public open-source (5-10 dev contributors) to a real SaaS (used by non-tech business owners).

**Updated:** 2026-05-08
**Current status:** Alpha — runs on the founder's machine with DeepSeek, but several blocker bugs for other devs.

---

## 🎯 Product goal

**End goal:** an open-source tool for US freelancers + solo business owners to run a full set of "virtual" departments via AI agents debating, for only ~$10-25/month (DeepSeek API + Claude Pro subscription).

**Target users:**

| Phase | Persona | Their requirement |
|---|---|---|
| Alpha (now) | Founder + 1-2 dev contributors | Can read code, no docs needed |
| v1 (1-2 months) | 5-10 US devs self-setting-up for their own business | Good README + setup guide, clear errors |
| v2 (3-6 months) | Non-tech founder (via web app) | Zero install, browser only |
| v3 (6-12 months) | Mass adoption (1000+ businesses) | Multi-tenant SaaS, billing |

---

## 📋 Phase v1 — Dev-Friendly (1-2 months)

Target: another dev clones the repo, follows the README, and uses it for their own business **without asking the maintainer**.

### 🔴 P0 — BLOCKER (must finish before v1 release)

| # | Item | Status | Effort | Owner |
|---|---|---|---|---|
| 1 | Official multi-LLM provider (DeepSeek/OpenAI/Gemini, not just Anthropic) | 🟡 Done 80% (DeepSeek) | 2h left | TBD |
| 2 | CLI commands load `vault/.env` correctly | ✅ Done | - | - |
| 3 | DeepSeek thinking-mode toggle (default OFF for meeting speed) | ✅ Done | - | - |
| 4 | Lenient Brain parser — accept `## Vision (3-5 years)`, not only `## Vision` | ❌ TODO | 2h | TBD |
| 5 | English error messages instead of Python tracebacks | ❌ TODO | 4h | TBD |
| 6 | `vn-os doctor` command — verify env, .vncoderc, .env, brain → checklist | ❌ TODO | 3h | TBD |
| 7 | Pin LangGraph version (using 0.2.0+ — high version churn) | ❌ TODO | 1h | TBD |
| 8 | Tests pass with the DeepSeek provider (currently 261 tests, may have hardcoded Anthropic) | ❌ TODO | 4h | TBD |

### 🟡 P1 — CRITICAL (needed for other devs to use smoothly)

| # | Item | Status | Effort |
|---|---|---|---|
| 9 | Brain wizard CLI — `vn-os brain-wizard` asks 16 questions → auto-fills 8 files | ❌ TODO | 1 day |
| 10 | Task templates — `vn-os run --template employment-agreement` | ❌ TODO | 1 day |
| 11 | Better progress indicator — "Calling 7 departments to meet... (3/7)" | ❌ TODO | 0.5 day |
| 12 | Resumable tasks — a meeting that fails midway can resume | ❌ TODO | 1 day |
| 13 | Per-task cost tracker — print cost in USD after finishing | ❌ TODO | 0.5 day |
| 14 | README update (DeepSeek setup, examples, troubleshooting) | ❌ TODO | 0.5 day |
| 15 | `examples/` folder with 3 sample vaults (F&B, Retail, Tech-SaaS) with the Brain filled | ❌ TODO | 1 day |
| 16 | 5-minute demo video on YouTube (setup + run one task end-to-end) | ❌ TODO | 0.5 day |

### 🟢 P2 — NICE-TO-HAVE (after v1 release)

| # | Item | Effort |
|---|---|---|
| 17 | Docker image | 1 day |
| 18 | GitHub Actions CI (test on Win/Mac/Linux) | 1 day |
| 19 | Cookbook — examples for 5-10 industries beyond the v1 packs | 1 week |
| 20 | A more detailed contributor guide than the current `CONTRIBUTING.md` | 1 day |

---

## 🐛 Bugs found in the 2026-05-08 session

> End-to-end debug session with a sample vault + Cowork + CLI.

| # | Bug | Severity | Repro | Fix |
|---|---|---|---|---|
| B1 | `vn_run`, `vn_draft` via MCP time out at 60s (Cowork client cap) | 🔴 Critical | Call vn_draft with any brief via Cowork | Document the limitation. Recommend the CLI for heavy tasks. |
| B2 | CLI `run/resume/meeting/approve/execute` doesn't call `apply_vault_env_to_os` → DEEPSEEK_API_KEY not in env | 🔴 Critical | Create vault/.env, run vn-os run | ✅ Patched 2026-05-08 |
| B3 | `docs/core/llm/providers.py` only has ClaudeProvider + MCPSamplingProvider, no OpenAI/Gemini/DeepSeek despite pyproject.toml deps | 🔴 Critical | Set OPENAI_API_KEY → still uses Anthropic | ✅ Patched (DeepSeek). OpenAI/Gemini TODO. |
| B4 | DeepSeek v4-pro thinking mode default ON → meeting has 7 LLM calls × 30-90s = 5-10 min | 🟡 High | vn-os meeting with DeepSeek | ✅ Patched (extra_body disables thinking) |
| B5 | Brain parser requires the exact heading `## Vision`, fails with `## Vision (3-5 years)` | 🟡 High | Heading with a suffix | TODO P0-#4 |
| B6 | `docs/vault-template/01-Departments/` not present — must clone from `repo/departments/` | 🟢 Medium | Onboard a new vault | TODO — fix `vn_onboard` |
| B7 | `obsidian_delete_file` via the Obsidian REST API times out for a folder (only works for a file) | 🟢 Medium | MCP delete folder | Document — recommend deleting via the Obsidian app |

---

## 📊 Decisions locked in the 2026-05-08 session

1. **Default LLM:** DeepSeek v4-pro (instead of Claude Sonnet) — ~10x cheaper, good enough for operational tasks.
2. **Fallback:** Anthropic API (needs ANTHROPIC_API_KEY in .env). MCP sampling is only for the dev experience via Claude Desktop.
3. **Main workflow:** CLI (vn-os) instead of MCP tool calls — avoids the Cowork 60s timeout for heavy tasks.
4. **Thinking mode:** Default OFF for meetings (speed). User opt-in via config if they want deep reasoning.

---

## 🚀 Phase v2 — Non-Tech Founder (3-6 months)

Target: a 50-year-old restaurant owner who can't code, able to use it via a web browser.

| # | Item | Effort |
|---|---|---|
| 21 | Web UI Streamlit/Next.js — chat interface | 2 weeks |
| 22 | Onboarding wizard — pick industry → auto-apply pack → fill the Brain via a form | 1 week |
| 23 | Visual brain editor — drag-drop, no Markdown needed | 2 weeks |
| 24 | Auth + multi-tenant — one vault per user | 1 week |
| 25 | Deploy a hosted version — vn-os.app (custom domain) | 1 week |
| 26 | Stripe billing — free tier 5 tasks/month, pro $9/month | 1 week |

---

## 🌐 Phase v3 — Mass Adoption (6-12 months)

Target: 1000+ businesses. Marketing + community.

| # | Item |
|---|---|
| 27 | Mobile app (React Native) |
| 28 | Grammar/style check |
| 29 | Plugin marketplace — businesses sell templates, share packs |
| 30 | Integration: QuickBooks, Square, Shopify, Amazon API |
| 31 | Multi-language (Spanish, ...) |

---

## 🤝 How to contribute

Right now the repo needs:

1. **Code reviewers** — review PRs fixing P0/P1 bugs
2. **Test with other businesses** — run your real vault, log bugs to issues
3. **Docs** — improve README examples and guides
4. **Industry pack contributions** — open a pack for a new industry (Healthcare, Edu, Real Estate)
5. **Template contributions** — each pack needs 30-50 quality templates

Open an issue: https://github.com/<owner>/<repo>/issues
Discord community: TBD (if needed)

---

## 📜 License + Sustainability

- **License:** MIT (locked)
- **Sustainability model:** TBD — possibly combine an open-source core + paid hosted SaaS (BSL or COSS pattern)
- **Maintainer commitment:** the founder commits to maintain at least the first 6 months

---

## 📌 Current status, summarized

✅ **Working:**
- Brain reader/parser (with a strict format)
- 13 core departments + F&B pack scaffold
- DeepSeek provider (after the 2026-05-08 session patch)
- CLI run stage 1 (router + gap analyzer)
- Obsidian MCP integration for doc viewing/editing

🟡 **Needs urgent fixes:**
- The 6 P0 blockers listed above
- The meeting stage isn't verified end-to-end (LangGraph + 7 agents debating)
- Onboarding for new devs isn't polished

🔴 **Not done:**
- All of P1 (wizard, templates, progress, resumable)
- All of v2 (web UI)
- Test coverage for non-Anthropic providers

---

**Next step now:** Verify the meeting stage runs with DeepSeek + thinking mode disabled. If it fails → debug LangGraph compatibility with a non-Anthropic provider.
