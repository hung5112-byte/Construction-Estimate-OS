"""Onboard library — pure Python API for vault scaffold creation.

Split from scripts/onboard.py so the MCP tool can call it directly (no subprocess).
"""
from __future__ import annotations
import shutil
from pathlib import Path

import yaml

from core.paths import data_root

REPO_ROOT = data_root()


def onboard_vault(
    vault_path: Path | str,
    packs: list[str] | None = None,
    byot_src: Path | str | None = None,
    init_git: bool = True,
    overwrite_brain_template: bool = True,
    api_keys: dict[str, str] | None = None,
) -> dict:
    """Create vault scaffold for new company.

    Args:
        vault_path: Where to create the vault
        packs: List of pack codes to install (e.g. ["fnb", "retail"])
        byot_src: Optional path to existing template folder to import as BYOT
        init_git: Initialize Git repo (best-effort, never push)
        overwrite_brain_template: Use first pack's brain template if available
        api_keys: Optional dict {KEY_NAME: value} saved to <vault>/.env.
                  Common keys: TAVILY_API_KEY (search), GOOGLE/OPENAI/ANTHROPIC.
                  Search tools skip gracefully if missing.

    Returns:
        dict with status, paths created, packs installed, errors
    """
    repo = REPO_ROOT
    vault = Path(vault_path).expanduser().resolve()
    packs = packs or []

    result: dict = {
        "ok": True,
        "vault": str(vault),
        "steps": [],
        "warnings": [],
    }

    # Step 1: Copy vault scaffold
    template_src = repo / "vault-template"
    if not template_src.exists():
        return {"ok": False, "error": f"vault-template not found at {template_src}"}

    shutil.copytree(template_src, vault, dirs_exist_ok=True)
    result["steps"].append(f"Copied scaffold to {vault}")

    # Step 2: Copy core departments (12)
    _install_departments(repo / "departments", vault / "01-Departments")
    result["steps"].append("Installed core departments")

    # Step 3: Install selected packs
    installed_packs: list[str] = []
    for code in packs:
        pack_dir = repo / "packs" / code
        if not (pack_dir / "pack.yaml").exists():
            result["warnings"].append(f"Pack '{code}' not found, skipped")
            continue
        _install_pack(pack_dir, vault)
        installed_packs.append(code)
        result["steps"].append(f"Installed pack {code}")
    result["packs"] = installed_packs

    # Step 4: Brain template override (first pack only)
    if overwrite_brain_template and installed_packs:
        first_pack = installed_packs[0]
        pack_brain = repo / "packs" / first_pack / "brain-template"
        if pack_brain.exists():
            for f in pack_brain.glob("*.md"):
                target = vault / "00-Brain" / f.name
                shutil.copy(f, target)
            result["steps"].append(
                f"Overrode Brain templates from {first_pack} pack"
            )

    # Step 5: BYOT (optional)
    if byot_src:
        src_path = Path(byot_src).expanduser()
        if src_path.exists():
            count = _import_byot(src_path, vault / "00-Templates-Custom")
            result["steps"].append(
                f"Imported {count} BYOT files from {src_path}"
            )
        else:
            result["warnings"].append(f"BYOT source {src_path} not found, skipped")

    # Step 6: Git init (best-effort)
    if init_git and not (vault / ".git").exists():
        try:
            from git import Repo
            Repo.init(str(vault))
            result["steps"].append("Git initialized")
        except Exception as e:  # noqa: BLE001
            result["warnings"].append(f"Git init failed: {e}")

    # Step 6.5: Save API keys to vault/.env (if the user provides them)
    if api_keys:
        from core.utils.config import save_vault_env
        env_path = save_vault_env(vault, api_keys)
        keys_saved = [k for k, v in api_keys.items() if v]
        result["steps"].append(
            f"Saved {len(keys_saved)} API key(s) → {env_path.name} "
            f"({', '.join(keys_saved) if keys_saved else 'none'})"
        )
        result["api_keys_saved"] = keys_saved

    # Step 7: Generate wikilinks (Brain hub + Dept hubs + agent cross-links)
    from core.wikilinks import generate_wikilinks
    wl = generate_wikilinks(vault)
    result["wikilinks"] = wl
    result["steps"].append(
        f"Wikilinks: brain_hub={wl['brain_hub']}, "
        f"dept_hubs={wl['dept_hubs']}, agents_linked={wl['agents_linked']}"
    )

    # Step 8: Save config
    config_path = vault / ".bd-os.yaml"
    config_path.write_text(
        yaml.safe_dump(
            {
                "vault_path": str(vault),
                "packs": installed_packs,
                "version": "0.1.0",
            },
            allow_unicode=True,
        ),
        encoding="utf-8",
    )
    result["steps"].append("Saved .bd-os.yaml")

    result["next_steps"] = [
        f"Open {vault}/00-Brain/ and fill strategy.md, products.md, budget.md, headcount.md, state.md",
        f"Run: bd_run(brief='...', vault='{vault}')",
    ]

    return result


def _install_departments(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for child in src.iterdir():
        if child.is_dir() and not child.name.startswith("_"):
            shutil.copytree(child, dst / child.name, dirs_exist_ok=True)


def _install_pack(pack_dir: Path, vault: Path) -> None:
    pack_yaml = pack_dir / "pack.yaml"
    if not pack_yaml.exists():
        return
    pack_data = yaml.safe_load(pack_yaml.read_text(encoding="utf-8"))

    for dept_code in pack_data.get("adds_departments", []):
        src = pack_dir / "departments" / dept_code
        dst = vault / "01-Departments" / dept_code
        if src.exists():
            shutil.copytree(src, dst, dirs_exist_ok=True)


def _import_byot(src: Path, dst: Path) -> int:
    """Returns number of files imported."""
    dst.mkdir(parents=True, exist_ok=True)

    classify_keywords = {
        "01-bid-coordination": ["bid", "rfi", "register", "addend", "scope", "proposal", "basis-of-estimate", "profile"],
        "02-civil-structural": ["concrete", "footing", "slab", "steel", "masonry", "earthwork", "site", "structural"],
        "03-architectural": ["roof", "envelope", "interior", "finish", "door", "window", "partition", "specialt"],
        "04-mep": ["hvac", "plumbing", "sprinkler", "fire", "electrical", "lighting", "panel", "mep"],
        "05-cost-engineering": ["estimate", "pricing", "unit-cost", "general-conditions", "markup", "leveling", "risk", "contingency"],
        "06-estimate-review": ["review", "checklist", "turnover", "benchmark", "audit", "constructab"],
    }

    count = 0
    for f in src.rglob("*"):
        if not f.is_file() or f.suffix.lower() not in [".md", ".docx", ".xlsx", ".pdf"]:
            continue
        name_lower = f.stem.lower().replace("_", "-").replace(" ", "-")
        target_dept = "_unsorted"
        for dept, keywords in classify_keywords.items():
            if any(kw in name_lower for kw in keywords):
                target_dept = dept
                break
        target_dir = dst / target_dept
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(f, target_dir / f.name)
        count += 1
    return count
