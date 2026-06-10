"""Load industry pack: pack.yaml + departments + extends overrides."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import yaml


@dataclass
class PackExtension:
    target: str
    add_agents: list[str] = field(default_factory=list)


@dataclass
class Pack:
    name: str
    code: str
    version: str
    description: str
    target_industries: list[str] = field(default_factory=list)
    adds_departments: list[str] = field(default_factory=list)
    extends_departments: list[PackExtension] = field(default_factory=list)
    brain_template: Optional[str] = None
    compliance_refs: list[str] = field(default_factory=list)
    pack_dir: Optional[Path] = None


class PackLoader:
    def __init__(self, packs_root: Path):
        self.root = Path(packs_root)

    def load(self, code: str) -> Pack:
        pack_dir = self.root / code
        pack_yaml = pack_dir / "pack.yaml"
        if not pack_yaml.exists():
            raise FileNotFoundError(f"Pack not found: {code}")
        data = yaml.safe_load(pack_yaml.read_text(encoding="utf-8"))

        extends = [
            PackExtension(target=e["target"], add_agents=e.get("add_agents", []))
            for e in data.get("extends_departments", [])
        ]

        return Pack(
            name=data["name"],
            code=data["code"],
            version=data.get("version", "0.1.0"),
            description=data.get("description", ""),
            target_industries=data.get("target_industries", []),
            adds_departments=data.get("adds_departments", []),
            extends_departments=extends,
            brain_template=data.get("brain_template"),
            compliance_refs=data.get("compliance_refs", []),
            pack_dir=pack_dir,
        )

    def list_available(self) -> list[str]:
        if not self.root.exists():
            return []
        return [d.name for d in self.root.iterdir() if d.is_dir() and (d / "pack.yaml").exists()]
