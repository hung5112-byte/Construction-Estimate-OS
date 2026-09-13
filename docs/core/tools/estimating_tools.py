"""BaseTool wrappers so the research phase / tool router can call the estimating extractors.

Query grammar (strict, like the other deterministic tools):
  sheet_register  <pdf-or-dir>
  sheet_geometry  <pdf> [page=N]
  sheet_text      <pdf> [page=N]
  sheet_tables    <pdf> [page=N]
  spec_index      <pdf>
  cost_engine     <ledger.json> [city=Plano] [class=2] [building=office-warehouse]
  benchmark_check total=<usd> sf=<n> building=<type> [gc=<usd>] [direct=<usd>] [labor=<usd>]
  review_gates    <estimate-folder>
Every ToolResult carries sources (file paths / data files) and retrieved_at (RULE 5).
"""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from core.tools.base_tool import BaseTool, ToolResult


def _kv(parts: list[str]) -> dict[str, str]:
    return {k: v for k, v in (p.split("=", 1) for p in parts if "=" in p)}


def _page(kv: dict) -> int:
    return max(0, int(kv.get("page", "1")) - 1)


class SheetRegisterTool(BaseTool):
    name = "sheet_register"
    description = "log every drawing sheet (id, title, discipline, scale, revision, vector/scanned) from a PDF or a folder of PDFs — document control + the scale gate"
    cache_ttl_seconds = 0

    def run(self, query: str, **kwargs) -> ToolResult:
        from core.estimating import sheet_register

        target = Path(query.split()[0]) if query.strip() else None
        if not target or not target.exists():
            return ToolResult(data={}, notes="invalid format — sheet_register <pdf-or-dir>")
        pdfs = sorted(target.glob("*.pdf")) if target.is_dir() else [target]
        reg = sheet_register.build_register(pdfs)
        return ToolResult(data=[asdict(s) for s in reg], sources=[str(p) for p in pdfs])


class SheetGeometryTool(BaseTool):
    name = "sheet_geometry"
    description = "vector geometry of a plan sheet → door-swing and window candidates, wall LF, exterior perimeter and footprint (needs a parsed scale)"
    cache_ttl_seconds = 0

    def run(self, query: str, **kwargs) -> ToolResult:
        from core.estimating import sheet_geometry, sheet_register
        from core.estimating.pdfio import open_pdf

        parts = query.split()
        if not parts or not Path(parts[0]).exists():
            return ToolResult(data={}, notes="invalid format — sheet_geometry <pdf> [page=N]")
        pdf_path, page_index = Path(parts[0]), _page(_kv(parts[1:]))
        with open_pdf(pdf_path) as pdf:
            page = pdf.pages[page_index]
            info = sheet_register.describe_page(page, pdf_path.name, page_index)
            g = sheet_geometry.summarize(page, info.scale)
        data = g.to_dict() | {"sheet_id": info.sheet_id, "scale": info.scale_label, "doors": [asdict(d) for d in g.doors], "windows": [asdict(w) for w in g.windows]}
        return ToolResult(data=data, sources=[f"{pdf_path}#page={page_index + 1}"], notes="" if info.scale_label else "NO SCALE PARSED — candidates counted, nothing measured")


class SheetTextTool(BaseTool):
    name = "sheet_text"
    description = "text layer of a sheet → room tags with areas, dimension strings, general notes / keynotes / legend blocks, title block"
    cache_ttl_seconds = 0

    def run(self, query: str, **kwargs) -> ToolResult:
        from core.estimating import sheet_text
        from core.estimating.pdfio import open_pdf

        parts = query.split()
        if not parts or not Path(parts[0]).exists():
            return ToolResult(data={}, notes="invalid format — sheet_text <pdf> [page=N]")
        pdf_path, page_index = Path(parts[0]), _page(_kv(parts[1:]))
        with open_pdf(pdf_path) as pdf:
            page = pdf.pages[page_index]
            ws = sheet_text.words(page)
            lines = sheet_text.text_lines(ws)
            data = {"room_tags": [asdict(t) for t in sheet_text.room_tags(ws)], "dimension_strings": sorted({d.text for d in sheet_text.dimension_strings(ws)}),
                    "notes": sheet_text.notes_blocks(lines), "title_block": sheet_text.title_block_text(lines, float(page.width), float(page.height))}
        return ToolResult(data=data, sources=[f"{pdf_path}#page={page_index + 1}"])


class SheetTablesTool(BaseTool):
    name = "sheet_tables"
    description = "schedules on a sheet (door, window, finish, footing, steel, equipment, fixture, panel) as header + rows — the schedule is the count"
    cache_ttl_seconds = 0

    def run(self, query: str, **kwargs) -> ToolResult:
        from core.estimating import sheet_tables, sheet_text
        from core.estimating.pdfio import open_pdf

        parts = query.split()
        if not parts or not Path(parts[0]).exists():
            return ToolResult(data={}, notes="invalid format — sheet_tables <pdf> [page=N]")
        pdf_path, page_index = Path(parts[0]), _page(_kv(parts[1:]))
        with open_pdf(pdf_path) as pdf:
            page = pdf.pages[page_index]
            ws = sheet_text.words(page)
            scheds = sheet_tables.extract_schedules(page, ws, sheet_text.text_lines(ws))
        return ToolResult(data=[s.to_dict() for s in scheds], sources=[f"{pdf_path}#page={page_index + 1}"])


class SpecIndexTool(BaseTool):
    name = "spec_index"
    description = "Project Manual → MasterFormat section index + Division 00/01 cost-carrying items (bid date, RFI cutoff, bonds, duration, LDs, allowances, alternates, unit prices)"
    cache_ttl_seconds = 0

    def run(self, query: str, **kwargs) -> ToolResult:
        from core.estimating import spec_index

        parts = query.split()
        if not parts or not Path(parts[0]).exists():
            return ToolResult(data={}, notes="invalid format — spec_index <pdf>")
        p = Path(parts[0])
        texts = spec_index.page_texts(p)
        idx = spec_index.index_manual(p, texts)
        return ToolResult(data={"sections": [asdict(s) for s in idx.sections], "division_01": spec_index.division_01_summary(texts)}, sources=[str(p)])


class CostEngineTool(BaseTool):
    name = "cost_engine"
    description = "price a takeoff ledger JSON against the cost library (BYO first, seed second, marked) with location factor — returns priced lines + summary; never guesses a missing price"
    cache_ttl_seconds = 0

    def __init__(self, vault_root: Path | None = None, **_):
        self.vault_root = Path(vault_root) if vault_root else None

    def run(self, query: str, **kwargs) -> ToolResult:
        from core.estimating import spec_index
        from core.estimating.cost_engine import (
            library_paths,
            load_library,
            load_location_factor,
            price_ledger,
            summary_by_division,
        )
        from core.estimating.takeoff_ledger import Ledger

        parts = query.split()
        if not parts or not Path(parts[0]).exists():
            return ToolResult(data={}, notes="invalid format — cost_engine <ledger.json> [city=..] [sf=..]")
        kv = _kv(parts[1:])
        led = Ledger.from_json(Path(parts[0]).read_text(encoding="utf-8"))
        paths = library_paths(self.vault_root)
        lib = load_library(paths)
        factor, src = load_location_factor(kv.get("city", "National"))
        lines = price_ledger(led, lib, location_factor=factor)
        summary = summary_by_division(lines, float(kv.get("sf", 0) or 0), spec_index.DIVISIONS)
        return ToolResult(data={"lines": [ln.to_dict() for ln in lines], "summary": summary, "location_factor": factor},
                          sources=[str(p) for p in paths] + [src], notes="rows from the seed library are [UNCERTAIN] placeholders" )


class BenchmarkCheckTool(BaseTool):
    name = "benchmark_check"
    description = "$/SF vs the building-type band plus GC and labor ratio checks — every result names its source (benchmarks_dfw_2026.csv / 00-Brain/benchmarks.md)"
    cache_ttl_seconds = 0

    def run(self, query: str, **kwargs) -> ToolResult:
        from core.estimating.cost_engine import DATA_DIR, benchmark_check

        kv = _kv(query.split())
        try:
            total, sf = float(kv["total"]), float(kv["sf"])
        except (KeyError, ValueError):
            return ToolResult(data={}, notes="invalid format — benchmark_check total=<usd> sf=<n> building=<type> [gc=] [direct=] [labor=]")
        res = benchmark_check(total, sf, kv.get("building", ""), float(kv.get("gc", 0) or 0), float(kv.get("direct", total) or total), float(kv.get("labor", 0) or 0))
        return ToolResult(data=res, sources=[str(DATA_DIR / "benchmarks_dfw_2026.csv")] + [c["source"] for c in res["checks"]])


class ReviewGatesTool(BaseTool):
    name = "review_gates"
    description = "run the deterministic hard gates (G1–G10) on an estimate folder → pass/fail per gate + verdict APPROVE/REVISE"
    cache_ttl_seconds = 0

    def run(self, query: str, **kwargs) -> ToolResult:
        from core.estimating import pipeline

        parts = query.split()
        folder = Path(parts[0]) if parts else None
        if not folder or not (folder / "06-estimate.json").exists():
            return ToolResult(data={}, notes="invalid format — review_gates <estimate-folder with 06-estimate.json>")
        gates, v = pipeline.review(folder)
        return ToolResult(data={"verdict": v, "gates": gates}, sources=[str(folder / "06-estimate.json"), str(folder / "04-takeoff-ledger.json")])


ESTIMATING_TOOLS = {
    "sheet_register": SheetRegisterTool, "sheet_geometry": SheetGeometryTool, "sheet_text": SheetTextTool, "sheet_tables": SheetTablesTool,
    "spec_index": SpecIndexTool, "cost_engine": CostEngineTool, "benchmark_check": BenchmarkCheckTool, "review_gates": ReviewGatesTool,
}
