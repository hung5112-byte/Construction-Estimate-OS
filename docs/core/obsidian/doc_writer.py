"""Render document tu template + data -> .docx hoac .xlsx."""
from __future__ import annotations
from pathlib import Path
from typing import Any


class DocWriter:
    def __init__(self, output_root: Path):
        self.output_root = Path(output_root)

    def write_docx(
        self,
        template_path: Path,
        output_rel: str,
        substitutions: dict[str, Any],
    ) -> Path:
        from docx import Document

        out_path = self.output_root / output_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if template_path.suffix == ".docx":
            doc = Document(str(template_path))
            self._substitute_docx(doc, substitutions)
        else:
            doc = Document()
            text = template_path.read_text(encoding="utf-8")
            text = self._substitute(text, substitutions)
            for line in text.split("\n"):
                if line.startswith("# "):
                    doc.add_heading(line[2:], level=1)
                elif line.startswith("## "):
                    doc.add_heading(line[3:], level=2)
                elif line.startswith("### "):
                    doc.add_heading(line[4:], level=3)
                else:
                    doc.add_paragraph(line)

        doc.save(str(out_path))
        return out_path

    def write_xlsx(
        self,
        template_path: Path,
        output_rel: str,
        rows: list[dict],
    ) -> Path:
        from openpyxl import load_workbook, Workbook

        out_path = self.output_root / output_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if template_path.suffix == ".xlsx" and template_path.exists():
            wb = load_workbook(str(template_path))
        else:
            wb = Workbook()

        ws = wb.active
        if rows and ws.max_row == 1 and ws.cell(1, 1).value is None:
            headers = list(rows[0].keys())
            for col, h in enumerate(headers, 1):
                ws.cell(1, col, h)

        if rows:
            headers = [ws.cell(1, c).value for c in range(1, ws.max_column + 1)]
            for row in rows:
                next_row = ws.max_row + 1
                for col, h in enumerate(headers, 1):
                    ws.cell(next_row, col, row.get(h, ""))

        wb.save(str(out_path))
        return out_path

    @staticmethod
    def _substitute(text: str, subs: dict[str, Any]) -> str:
        for k, v in subs.items():
            text = text.replace(f"{{{{{k}}}}}", str(v))
        return text

    @staticmethod
    def _substitute_docx(doc, subs: dict):
        for para in doc.paragraphs:
            for k, v in subs.items():
                if f"{{{{{k}}}}}" in para.text:
                    for run in para.runs:
                        run.text = run.text.replace(f"{{{{{k}}}}}", str(v))

    def write_docx_text(self, text: str, output_rel: str, substitutions: dict | None = None) -> Path:
        """Render generated markdown TEXT (not a template path) into a .docx with
        real headings, tables, bullets and bold runs."""
        from docx import Document

        out_path = self.output_root / output_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if substitutions:
            text = self._substitute(text, substitutions)
        doc = Document()
        self._render_markdown(doc, text)
        doc.save(str(out_path))
        return out_path

    @staticmethod
    def _add_runs(paragraph, s: str):
        import re
        for part in re.split(r"(\*\*.+?\*\*)", s):
            if part.startswith("**") and part.endswith("**"):
                paragraph.add_run(part[2:-2]).bold = True
            elif part:
                paragraph.add_run(part)

    @classmethod
    def _render_markdown(cls, doc, text: str):
        import re

        def clean(v):
            return re.sub(r"\*\*(.+?)\*\*", r"\1", v).strip()

        lines = text.split("\n")
        i, n = 0, len(lines)
        while i < n:
            s = lines[i].strip()
            if not s:
                i += 1
                continue
            if s.startswith("|") and i + 1 < n and set(lines[i + 1].strip()) <= set("|-: "):
                rows = []
                while i < n and lines[i].strip().startswith("|"):
                    cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                    if set("".join(cells).replace(" ", "")) <= set("-:"):
                        i += 1
                        continue
                    rows.append(cells)
                    i += 1
                if rows:
                    ncol = max(len(r) for r in rows)
                    table = doc.add_table(rows=len(rows), cols=ncol)
                    try:
                        table.style = "Light Grid Accent 1"
                    except Exception:  # noqa: BLE001
                        try:
                            table.style = "Table Grid"
                        except Exception:  # noqa: BLE001
                            pass
                    for ri, r in enumerate(rows):
                        for ci in range(ncol):
                            table.cell(ri, ci).text = clean(r[ci]) if ci < len(r) else ""
                continue
            h = re.match(r"^(#{1,6})\s+(.*)$", s)
            if h:
                doc.add_heading(clean(h.group(2)), level=min(len(h.group(1)), 4))
                i += 1
                continue
            if re.match(r"^[-*]\s+", s):
                doc.add_paragraph(clean(re.sub(r"^[-*]\s+", "", s)), style="List Bullet")
                i += 1
                continue
            if re.match(r"^\d+\.\s+", s):
                doc.add_paragraph(clean(re.sub(r"^\d+\.\s+", "", s)), style="List Number")
                i += 1
                continue
            cls._add_runs(doc.add_paragraph(), s)
            i += 1
