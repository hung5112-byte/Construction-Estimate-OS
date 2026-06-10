# Contributing to US One Person Company

Thanks for your interest! Here's a short guide to getting involved.

## Dev environment setup

```bash
git clone https://github.com/<owner>/<repo>.git
cd <repo>
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run tests

```bash
python -m pytest docs/tests/ -q
```

All 261+ tests must pass before submitting a PR.

## Coding standards

- **Python 3.11+**, type hints required for the public API
- **English** in: agent prompts, output reports, user-facing strings, code comments, variable names, commit messages
- **kebab-case** for Python files, **snake_case** for functions/variables
- Small files (<200 lines), modularize if larger
- Do NOT hardcode API keys or personal paths

## The 6 RULES (immutable)

1. **Brain-first** — don't ask the CEO before reading the Brain
2. **Domain-neutral** — do NOT leak finance/trading jargon
3. **Single source of truth** — the Obsidian vault is canonical
4. **CEO-friendly language** — translator pipeline for output
5. **Live research with citations** — searches must cite + validator
6. **BYOT** — company custom > pack > default

PRs that violate the RULES will be rejected.

## PR process

1. Fork + branch: `feat/<feature>` or `fix/<bug>`
2. Implement + tests (TDD encouraged)
3. Commit: conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`)
4. Do NOT mention AI/Claude in commit messages
5. The PR clearly describes: the problem, the solution, which RULES apply
6. CI must be green

## Folder structure

```
docs/core/                 # Python engine
├── brain/            # Brain layer (reader, gap, schema)
├── agents/           # Agent loaders + base
├── meeting/          # LangGraph debate engine
├── orchestrator/     # FlowController + Router + tools
├── tools/            # 6 research tools
├── translator/       # CEO-friendly language pipeline
├── obsidian/         # Vault I/O + DocWriter + Git
└── llm/              # LLM provider abstraction (MCP sampling, Anthropic)
docs/departments/          # 12 core departments (YAML + agent .md)
docs/packs/                # Industry packs (F&B, Retail, Tech-SaaS)
docs/templates-us/         # 192 US/Texas-aligned templates
docs/vault-template/       # Obsidian scaffold for onboarding
docs/adapters/             # Claude Code/Cowork integration
docs/tests/                # unit / integration / e2e
docs/                 # User docs
docs/plans/                # Implementation plans (dev notes)
```

## How to add a new Pack

See `docs/how-to-create-pack.md`.

## How to add a research Tool

1. Create `docs/core/tools/<name>.py` extending `BaseTool`
2. Implement `is_available()` (check key/dep)
3. Implement `run(query, **kwargs) -> ToolResult`
4. Register it in `docs/core/orchestrator/research_phase.py:TOOL_REGISTRY`
5. Update `docs/core/tools/tool_router.py:_FULL_TOOL_DESCRIPTIONS`
6. Test (`docs/tests/unit/test_tool_<name>.py`)

## Reporting bugs / proposing features

Open an issue on GitHub with the appropriate template.

## License

Contributing means you agree your code is released under the **Apache License 2.0** (see [LICENSE](LICENSE) and [NOTICE](NOTICE)).
