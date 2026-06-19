"""Resolve template path per RULE 6:
1. vault/00-Templates-Custom/<dept>/<template>* (Department Head custom)
2. vault/01-Departments/<dept>/refs/<template>*
3. repo/templates-us/<dept>/<template>*
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import Optional


SUPPORTED_EXT = [".md", ".docx", ".xlsx"]


class TemplateResolver:
    def __init__(self, vault_root: Path, repo_templates: Path):
        self.vault = Path(vault_root)
        self.repo = Path(repo_templates)

    def resolve(self, template_name: str, dept_code: str) -> Optional[Path]:
        dept = self._resolve_dept(dept_code)
        candidates = [
            self.vault / "00-Templates-Custom" / dept,
            self.vault / "01-Departments" / dept / "refs",
            self.repo / dept,
        ]
        for folder in candidates:
            if not folder.exists():
                continue
            found = self._find_in(folder, template_name)
            if found:
                return found
        return None

    @staticmethod
    def _slug(s: str) -> str:
        """Normalize a name/label for comparison: lowercase, alnum tokens, hyphens."""
        return re.sub(r"[^a-z0-9]+", "-", s.lower().strip()).strip("-")

    def _dept_folders(self) -> list[str]:
        """Department-code folders available under the repo template root."""
        if not self.repo.exists():
            return []
        return sorted(p.name for p in self.repo.iterdir() if p.is_dir())

    def _resolve_dept(self, dept_code: str) -> str:
        """Map a dept code OR friendly label to the real folder name.

        Accepts '02-npi-program-management', 'npi-program-management',
        'NPI Program Management', 'Manufacturing & Supplier Quality', etc.
        Uses best token-overlap (ignoring numeric prefixes) so friendly labels
        with abbreviations (e.g. 'Manufacturing' → 'mfg') still map. Falls back
        to the input unchanged when nothing matches better.
        """
        folders = self._dept_folders()
        if not folders or dept_code in folders:
            return dept_code
        want = {t for t in self._slug(dept_code).split("-") if t}
        best, best_score = dept_code, 0
        for f in folders:
            ftoks = {t for t in self._slug(f).split("-") if t and not t.isdigit()}
            score = len(want & ftoks)
            if score > best_score:
                best, best_score = f, score
        return best

    @staticmethod
    def _find_in(folder: Path, name: str) -> Optional[Path]:
        want = TemplateResolver._slug(name)
        for f in folder.iterdir():
            if not f.is_file():
                continue
            if f.suffix.lower() not in SUPPORTED_EXT:
                continue
            stem = TemplateResolver._slug(f.stem)
            if want and (stem.startswith(want) or want in stem):
                return f
        return None

    def get_resolution_log(self, template_name: str, dept_code: str) -> dict:
        path = self.resolve(template_name, dept_code)
        if not path:
            return {"found": False, "name": template_name, "dept": dept_code}

        rel = path.resolve()
        if str(rel).startswith(str((self.vault / "00-Templates-Custom").resolve())):
            source = "custom"
        elif str(rel).startswith(str(self.vault.resolve())):
            source = "pack"
        else:
            source = "default"
        return {"found": True, "path": str(rel), "source": source,
                "dept": dept_code, "name": template_name}
