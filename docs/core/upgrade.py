"""Upgrade existing vault — refresh agents/depts/templates, preserve user data.

Use case: a user onboarded a vault from an older version. When the plugin upgrades
(enriched prompts, aliases, ...), push the new files into the existing vault
WITHOUT touching the data the Department Head filled in (Brain content, Tasks, Outputs).
"""
from __future__ import annotations
import shutil
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).parent.parent


# Brain files are NEVER overwritten (the Department Head filled them in)
PRESERVE_BRAIN = True


def upgrade_vault(
    vault_path: Path | str,
    refresh_agents: bool = True,
    refresh_dept_yaml: bool = True,
    refresh_brain_aliases: bool = True,
    regenerate_hubs: bool = False,
) -> dict:
    """Refresh code-controlled files in the vault, keeping user data intact.

    Args:
        vault_path: Path to the vault
        refresh_agents: Overwrite agent .md files (pull the new enriched prompts)
        refresh_dept_yaml: Overwrite department.yaml (new aliases_vn, routing_rules)
        refresh_brain_aliases: Add aliases to Brain files (keep the body content)
        regenerate_hubs: Delete old index.md + recreate (default NO, since the user
                        may have edited them manually)

    Returns:
        dict summary
    """
    vault = Path(vault_path).expanduser().resolve()
    if not vault.exists():
        return {"ok": False, "error": f"Vault not found: {vault}"}

    summary: dict = {
        "ok": True,
        "vault": str(vault),
        "agents_refreshed": 0,
        "dept_yaml_refreshed": 0,
        "brain_aliases_added": 0,
        "hubs_regenerated": False,
        "warnings": [],
    }

    # 1. Refresh agent .md files (overwrite, keep structure)
    if refresh_agents:
        summary["agents_refreshed"] = _refresh_agents(vault)

    # 2. Refresh department.yaml
    if refresh_dept_yaml:
        summary["dept_yaml_refreshed"] = _refresh_dept_yaml(vault)

    # 3. Add aliases to Brain files (idempotent, keep body)
    if refresh_brain_aliases:
        summary["brain_aliases_added"] = _add_brain_aliases(vault)

    # 4. Regenerate hubs (if the user requests it)
    if regenerate_hubs:
        _delete_hubs(vault)
        from core.wikilinks import generate_wikilinks
        wl = generate_wikilinks(vault)
        summary["hubs_regenerated"] = True
        summary["wikilinks"] = wl
    else:
        # Still run the generator to link new agent files (idempotent)
        from core.wikilinks import generate_wikilinks
        summary["wikilinks"] = generate_wikilinks(vault)

    return summary


def _refresh_agents(vault: Path) -> int:
    """Copy enriched agents from source departments/ + packs/ into the vault."""
    count = 0
    src_root = REPO_ROOT / "departments"
    dst_root = vault / "01-Departments"

    if not dst_root.exists():
        return 0

    for src_dept in src_root.iterdir():
        if not src_dept.is_dir() or src_dept.name.startswith("_"):
            continue
        src_agents = src_dept / "agents"
        dst_agents = dst_root / src_dept.name / "agents"
        if not src_agents.exists() or not dst_agents.exists():
            continue
        for src_agent in src_agents.glob("*.md"):
            dst_agent = dst_agents / src_agent.name
            shutil.copy2(src_agent, dst_agent)
            count += 1

    # Packs: only refresh if the vault already has that pack
    packs_root = REPO_ROOT / "packs"
    if packs_root.exists():
        for pack_dir in packs_root.iterdir():
            if not pack_dir.is_dir():
                continue
            for src_dept in (pack_dir / "departments").glob("*"):
                if not src_dept.is_dir():
                    continue
                dst_dept = dst_root / src_dept.name
                if not dst_dept.exists():
                    continue
                src_agents = src_dept / "agents"
                dst_agents = dst_dept / "agents"
                if not src_agents.exists() or not dst_agents.exists():
                    continue
                for src_agent in src_agents.glob("*.md"):
                    shutil.copy2(src_agent, dst_agents / src_agent.name)
                    count += 1
    return count


def _refresh_dept_yaml(vault: Path) -> int:
    count = 0
    dst_root = vault / "01-Departments"
    if not dst_root.exists():
        return 0

    for src_yaml in (REPO_ROOT / "departments").glob("*/department.yaml"):
        dept_code = src_yaml.parent.name
        dst_yaml = dst_root / dept_code / "department.yaml"
        if dst_yaml.exists():
            shutil.copy2(src_yaml, dst_yaml)
            count += 1

    for src_yaml in (REPO_ROOT / "packs").glob("*/departments/*/department.yaml"):
        dept_code = src_yaml.parent.name
        dst_yaml = dst_root / dept_code / "department.yaml"
        if dst_yaml.exists():
            shutil.copy2(src_yaml, dst_yaml)
            count += 1
    return count


def _add_brain_aliases(vault: Path) -> int:
    """Inject aliases into the frontmatter of Brain files. Keep the body intact."""
    from core.obsidian.frontmatter import parse as parse_frontmatter

    count = 0
    template_brain = REPO_ROOT / "vault-template" / "00-Brain"
    user_brain = vault / "00-Brain"
    if not template_brain.exists() or not user_brain.exists():
        return 0

    for tpl_file in template_brain.glob("*.md"):
        user_file = user_brain / tpl_file.name
        if not user_file.exists():
            continue
        # Parse the template to get the new aliases
        tpl_fm, _ = parse_frontmatter(tpl_file.read_text(encoding="utf-8"))
        aliases = tpl_fm.get("aliases")
        if not aliases:
            continue
        # Parse the user file, inject aliases if not present
        user_fm, user_body = parse_frontmatter(user_file.read_text(encoding="utf-8"))
        if "aliases" in user_fm:
            continue
        user_fm["aliases"] = aliases
        new_fm_yaml = yaml.safe_dump(
            user_fm,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        ).strip()
        new_text = f"---\n{new_fm_yaml}\n---\n\n{user_body.lstrip()}"
        user_file.write_text(new_text, encoding="utf-8")
        count += 1
    return count


def _delete_hubs(vault: Path) -> None:
    """Delete index.md hubs so the generator recreates them."""
    brain_idx = vault / "00-Brain" / "index.md"
    if brain_idx.exists():
        brain_idx.unlink()
    depts_root = vault / "01-Departments"
    if depts_root.exists():
        for d in depts_root.iterdir():
            idx = d / "index.md"
            if idx.exists():
                idx.unlink()
