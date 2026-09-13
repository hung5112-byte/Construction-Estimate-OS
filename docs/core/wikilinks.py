"""Wikilink generator — create Brain hub + Department hub + cross-link agents.

Idempotent: re-running does not break existing files. Appends `## Links` only when the marker is absent.
"""
from __future__ import annotations
from pathlib import Path

import yaml


LINK_MARKER = "## Links"


def generate_wikilinks(vault: Path) -> dict:
    """Create index.md hubs + add wikilinks to agent files.

    Returns:
        dict with the number of files written/updated.
    """
    vault = Path(vault)
    brain = vault / "00-Brain"
    depts_root = vault / "01-Departments"

    summary = {"brain_hub": False, "dept_hubs": 0, "agents_linked": 0}

    if not brain.exists() or not depts_root.exists():
        return summary

    brain_stems = sorted(
        f.stem for f in brain.glob("*.md") if f.stem != "index"
    )
    dept_dirs = sorted(
        d for d in depts_root.iterdir()
        if d.is_dir() and not d.name.startswith("_")
    )

    summary["brain_hub"] = _write_brain_hub(brain, brain_stems, dept_dirs)

    for d in dept_dirs:
        meta = _read_dept_meta(d)
        if meta is None:
            continue
        if _write_dept_hub(d, meta, brain_stems):
            summary["dept_hubs"] += 1
        summary["agents_linked"] += _link_agents(d, meta, brain_stems)

    return summary


def _write_brain_hub(
    brain: Path, brain_stems: list[str], dept_dirs: list[Path]
) -> bool:
    target = brain / "index.md"
    if target.exists():
        return False
    lines = [
        "---",
        "type: hub",
        'aliases: ["Brain", "Knowledge Hub", "Brain Hub"]',
        "---",
        "# 🧠 Brain — Knowledge hub",
        "",
        "Navigation hub for all Brain files and the division departments.",
        "",
        "## Brain Files",
        "",
    ]
    lines += [f"- [[{s}]]" for s in brain_stems]
    lines += ["", "## Departments", ""]
    for d in dept_dirs:
        meta = _read_dept_meta(d)
        label = meta.get("name_local", d.name) if meta else d.name
        lines.append(f"- [[01-Departments/{d.name}/index|🏢 {label} ({d.name})]]")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def _write_dept_hub(d: Path, meta: dict, brain_stems: list[str]) -> bool:
    target = d / "index.md"
    if target.exists():
        return False
    name_local = meta.get("name_local", d.name)
    agents = meta.get("agents", []) or []
    manager = meta.get("default_speaker", "") or ""
    depends_on = meta.get("depends_on", []) or []
    aliases_extra = meta.get("aliases_local", []) or []

    aliases = [name_local] + [a for a in aliases_extra if a != name_local]
    aliases_inline = "[" + ", ".join(f'"{a}"' for a in aliases) + "]"

    lines = [
        "---",
        "type: hub",
        f"aliases: {aliases_inline}",
        "---",
        f"# 🏢 {name_local}",
        f"_Department code: `{d.name}`_",
        "",
        "← [[../../00-Brain/index|🧠 Brain Hub]]",
        "",
        "## Team",
        "",
    ]
    # Org chart: manager (default speaker) first, then the team agents
    if manager and manager in agents:
        lines.append(f"- **Manager:** [[{manager}]] ⭐ _(speaks for the department)_")
        lines += [f"- [[{a}]]" for a in agents if a != manager]
    else:
        lines += [f"- [[{a}]]" for a in agents]
    lines += ["", "## Brain References", ""]
    lines += [f"- [[{s}]]" for s in brain_stems]
    if depends_on:
        lines += ["", "## Works with", ""]
        for dep in depends_on:
            dep_meta = _read_dept_meta(d.parent / dep)
            label = dep_meta.get("name_local", dep) if dep_meta else dep
            lines.append(f"- [[../{dep}/index|{label}]] (`{dep}`)")

    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def _link_agents(d: Path, meta: dict, brain_stems: list[str]) -> int:
    agents_dir = d / "agents"
    if not agents_dir.exists():
        return 0
    name_local = meta.get("name_local", d.name)
    manager = meta.get("default_speaker", "") or ""
    key_refs = [s for s in ("strategy", "laws", "state") if s in brain_stems]

    count = 0
    for agent_file in agents_dir.glob("*.md"):
        text = agent_file.read_text(encoding="utf-8")
        if LINK_MARKER in text:
            continue
        block = [
            "",
            LINK_MARKER,
            "",
            f"- Department: [[../index|🏢 {name_local}]]",
            "- Brain Hub: [[../../../00-Brain/index|🧠 Brain]]",
        ]
        # Team agents get a link to their manager (the department's speaker)
        if manager and agent_file.stem != manager:
            block.append(f"- Manager: [[{manager}]]")
        if key_refs:
            refs = " · ".join(f"[[{s}]]" for s in key_refs)
            block.append(f"- Refs: {refs}")
        agent_file.write_text(
            text.rstrip() + "\n" + "\n".join(block) + "\n",
            encoding="utf-8",
        )
        count += 1
    return count


def _read_dept_meta(d: Path) -> dict | None:
    yaml_path = d / "department.yaml"
    if not yaml_path.exists():
        return None
    try:
        return yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None
