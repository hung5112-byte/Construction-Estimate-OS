# Industry Packs

Packs are optional overlays that add departments, agents, and templates on top of
the core division departments. The pack **mechanism** (`core/agents/pack_loader.py`,
`bd_onboard(packs=[...])`) is fully supported; no packs ship by default.

The original generic-business packs (`fnb/`, `retail/`, `tech-saas/`) were removed
on 06/09/2026 when the repo was specialized into a hardware engineering & supply
chain division OS. They remain available in the pre-restructure backup.

## Creating a pack

```
packs/<code>/
├── pack.yaml                 # name, code, adds_departments, brain_template, compliance_refs
├── brain-template/           # Brain file overrides/additions
└── departments/
    └── NN-name/
        ├── department.yaml
        └── agents/*.md
```

See `docs/how-to-create-pack.md` for field documentation. Enable a pack per vault
via `.bd-os.yaml` (`packs: [<code>]`) or `bd_onboard(packs=["<code>"])`.
