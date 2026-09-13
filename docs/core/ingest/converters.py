"""Tiered document→markdown converters (ADR-004 Addendum A §3, report §6).

All local, no API keys, MIT/Apache tools only (marker/PyMuPDF rejected on
license). Tiers implemented here: T0 plain text, T1 Office via MarkItDown +
a custom openpyxl serializer for spreadsheets, T2 digital PDFs (MarkItDown/
pdfminer text layer; Docling+OCR auto-detected if installed for scans).
CAD/engineering formats are roadmap Step 6.
"""
from __future__ import annotations

import csv as csv_mod
from pathlib import Path

from core.ingest.base import ConversionResult
from core.ingest.cad import CAD_EXTS, convert_cad

__all__ = ["ConversionResult", "SUPPORTED_EXTS", "convert"]

DOC_EXTS = {".docx", ".pptx", ".pdf", ".xlsx", ".txt", ".csv"}
SUPPORTED_EXTS = DOC_EXTS | CAD_EXTS
SHEET_ROW_HEAD = 150
SHEET_ROW_TAIL = 20


def convert(path: Path) -> ConversionResult:
    ext = path.suffix.lower()
    if ext in (".txt", ".csv"):
        return _convert_plain(path)
    if ext == ".xlsx":
        return _convert_xlsx(path)
    if ext in CAD_EXTS:
        return convert_cad(path)
    if ext == ".pdf" and _docling_available():
        return _convert_pdf_docling(path)
    if ext in (".docx", ".pptx", ".pdf"):
        return _convert_markitdown(path)
    raise ValueError(f"Unsupported extension: {ext}")


# ------------------------------------------------------------------ T0 plain

def _convert_plain(path: Path) -> ConversionResult:
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".csv":
        import io

        # csv.reader on a stream keeps quoted multi-line fields intact
        # (splitlines() broke them into bogus extra rows — review finding)
        rows = list(csv_mod.reader(io.StringIO(text)))
        body = _markdown_table(rows) if rows else "(empty file)"
    else:
        body = text
    return ConversionResult(body=body, converter="plain", tier="T0", confidence="high")


# ------------------------------------------------------------- T1 MarkItDown

def _convert_markitdown(path: Path) -> ConversionResult:
    import markitdown
    from markitdown import MarkItDown  # lazy — heavy import chain

    name = f"markitdown-{getattr(markitdown, '__version__', '?')}"
    ext = path.suffix.lower()
    if ext in (".docx", ".pptx"):
        with path.open("rb") as f:
            magic = f.read(4)
        if magic != b"PK\x03\x04":
            # MarkItDown silently falls back to treating non-zip bytes as plain
            # text — carding that at HIGH confidence was dishonest (review
            # finding); the conf≥0.7 gate downstream must see the truth.
            text = path.read_text(encoding="utf-8", errors="replace").strip()
            return ConversionResult(
                text or "(no extractable text)", name, "T1", "low",
                "file is not a valid Office archive — raw bytes treated as text",
            )
    text = (MarkItDown().convert(str(path)).text_content or "").strip()
    if not text:
        note = (
            "no text layer found — likely a scanned document; install the OCR "
            "extra (docling + ocrmac) and re-ingest"
            if ext == ".pdf" else "converter produced no text"
        )
        return ConversionResult("(no extractable text)", name, "T1", "low", note)
    if ext == ".pdf":
        # pdfminer text layer: fine for digital PDFs, tables lose structure
        return ConversionResult(text, name, "T2", "med",
                                "digital-PDF text layer; table structure approximate")
    return ConversionResult(text, name, "T1", "high")


# --------------------------------------------------------- T1 xlsx serializer

def _convert_xlsx(path: Path) -> ConversionResult:
    """Purpose-built for BOM/inventory workbooks: per-sheet sections, computed
    values (cached results; formulas without a saved cache render empty), row
    caps so one giant sheet can't blow the chunker."""
    from openpyxl import load_workbook  # already an engine dependency

    from collections import deque

    wb = load_workbook(path, data_only=True, read_only=True)
    parts: list[str] = []
    for ws in wb.worksheets:
        # Stream — never materialize a giant sheet (review finding): keep the
        # head list, a bounded tail deque, and a running count.
        head: list[list] = []
        tail: deque = deque(maxlen=SHEET_ROW_TAIL)
        total = 0
        for row in ws.iter_rows(values_only=True):
            if not any(c is not None and str(c).strip() != "" for c in row):
                continue
            total += 1
            if len(head) < SHEET_ROW_HEAD:
                head.append(list(row))
            else:
                tail.append(list(row))
        title = str(ws.title).replace("\n", " ")
        parts.append(f"## Sheet: {title} ({total} rows)")
        if not total:
            parts.append("(empty sheet)")
            continue
        if total > SHEET_ROW_HEAD + SHEET_ROW_TAIL:
            omitted = total - SHEET_ROW_HEAD - len(tail)
            parts.append(_markdown_table(head))
            parts.append(f"*(… {omitted} rows omitted …)*")
            parts.append(_markdown_table(list(tail)))
        else:
            parts.append(_markdown_table(head + list(tail)))
    wb.close()
    return ConversionResult(
        body="\n\n".join(parts), converter="openpyxl-serializer-1",
        tier="T1", confidence="high",
    )


def _markdown_table(rows: list[list]) -> str:
    def cell(v) -> str:
        return "" if v is None else str(v).replace("|", "\\|").replace("\n", " ")

    width = max(len(r) for r in rows)
    lines = []
    for i, row in enumerate(rows):
        padded = [cell(c) for c in list(row) + [None] * (width - len(row))]
        lines.append("| " + " | ".join(padded) + " |")
        if i == 0:
            lines.append("|" + "---|" * width)
    return "\n".join(lines)


# ------------------------------------------------------- T2/T3 Docling (opt-in)

def _docling_available() -> bool:
    try:
        import docling  # noqa: F401 — optional heavy dependency

        return True
    except ImportError:
        return False


def _convert_pdf_docling(path: Path) -> ConversionResult:
    """Upgrade path for scans: `pip install docling ocrmac` and re-ingest."""
    from docling.document_converter import DocumentConverter

    result = DocumentConverter().convert(str(path))
    body = result.document.export_to_markdown()
    return ConversionResult(
        body=body or "(no extractable text)", converter="docling",
        tier="T2", confidence="high" if body else "low",
    )
