"""Engineering/CAD file extraction (roadmap Step 6; report §6 T4 tiers).

The PLM lesson (Windchill, SOLIDWORKS PDM): nobody indexes geometry — extract
METADATA and text annotations into the shadow card. All local, deterministic:
- DXF        ezdxf (MIT): title-block attributes, TEXT/MTEXT, dimensions, layers
- DWG        LibreDWG `dwg2dxf` subprocess when installed (GPL — never vendored),
             else a stub card with the install hint
- KiCad      s-expression text: component table (ref/value/lib), net count
- Gerber     X2 %TF file attributes + X3 %TO component records via regex —
             no dependency; bare RS-274X degrades to a low-confidence stub
- STEP       ASCII regex: FILE_NAME/DESCRIPTION header + PRODUCT names
- ELF/BIN    printable-strings scan filtered to version/build/id patterns
- IGES/STL/SolidWorks/Altium native → policy stub cards (intake rules)
"""
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from core.ingest.base import ConversionResult

DXF_EXTS = {".dxf"}
DWG_EXTS = {".dwg"}
KICAD_EXTS = {".kicad_sch", ".kicad_pcb", ".kicad_pro"}
GERBER_EXTS = {".gbr", ".ger", ".gtl", ".gbl", ".gts", ".gbs", ".gto", ".gbo", ".gko", ".gml"}
STEP_EXTS = {".step", ".stp"}
FIRMWARE_EXTS = {".elf", ".bin"}
STUB_EXTS = {".iges", ".igs", ".stl", ".sldprt", ".sldasm", ".schdoc", ".pcbdoc"}

CAD_EXTS = (DXF_EXTS | DWG_EXTS | KICAD_EXTS | GERBER_EXTS | STEP_EXTS
            | FIRMWARE_EXTS | STUB_EXTS)

_STUB_POLICIES = {
    ".iges": "prefer STEP AP214/AP242 from the supplier (IGES carries no PMI)",
    ".igs": "prefer STEP AP214/AP242 from the supplier (IGES carries no PMI)",
    ".stl": "mesh only — request the native CAD or STEP source",
    ".sldprt": "intake rule: request STEP + PDF drawing sidecars alongside SolidWorks natives",
    ".sldasm": "intake rule: request STEP + PDF drawing sidecars alongside SolidWorks natives",
    ".schdoc": "intake rule: request ASCII SchDoc, a KiCad export, or Gerber X3 + CSV BOM sidecars",
    ".pcbdoc": "never parsed (binary Altium) — request Gerber X2/X3 + ODB++ or IPC-2581",
}


def convert_cad(path: Path) -> ConversionResult:
    ext = path.suffix.lower()
    if ext in DXF_EXTS:
        return _convert_dxf(path)
    if ext in DWG_EXTS:
        return _convert_dwg(path)
    if ext in KICAD_EXTS:
        return _convert_kicad(path)
    if ext in GERBER_EXTS:
        return _convert_gerber(path)
    if ext in STEP_EXTS:
        return _convert_step(path)
    if ext in FIRMWARE_EXTS:
        return _convert_firmware(path)
    if ext in STUB_EXTS:
        return _stub(path, _STUB_POLICIES[ext])
    raise ValueError(f"Not a CAD extension: {ext}")


# ------------------------------------------------------------------ DXF / DWG

def _convert_dxf(path: Path) -> ConversionResult:
    import ezdxf  # lazy

    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    parts: list[str] = []

    attribs = [
        (a.dxf.tag, a.dxf.text)
        for insert in msp.query("INSERT")
        for a in insert.attribs
        if str(a.dxf.text).strip()
    ]
    if attribs:
        parts.append("## Title Block / Block Attributes\n\n| Tag | Value |\n|---|---|")
        parts.extend(f"| {t} | {v} |" for t, v in attribs)

    texts = [e.dxf.text for e in msp.query("TEXT") if str(e.dxf.text).strip()]
    texts += [e.plain_text() for e in msp.query("MTEXT") if e.plain_text().strip()]
    if texts:
        parts.append("## Text Annotations\n")
        parts.extend(f"- {t}" for t in texts[:300])

    dims = list(msp.query("DIMENSION"))
    overrides = [d.dxf.text for d in dims if str(d.dxf.text).strip() not in ("", "<>")]
    if dims:
        parts.append(f"## Dimensions\n\n{len(dims)} dimension(s)"
                     + (f"; text overrides: {', '.join(overrides[:50])}" if overrides else ""))

    layers = sorted(layer.dxf.name for layer in doc.layers)
    parts.append("## Layers\n\n" + ", ".join(layers[:100]))
    blocks = sorted(b.name for b in doc.blocks if not b.name.startswith("*"))
    if blocks:
        parts.append("## Blocks\n\n" + ", ".join(blocks[:100]))

    return ConversionResult(
        body="\n".join(parts) or "(empty drawing)",
        converter=f"ezdxf-{ezdxf.__version__}", tier="T4",
        confidence="high" if (attribs or texts) else "med",
    )


def _convert_dwg(path: Path) -> ConversionResult:
    dwg2dxf = shutil.which("dwg2dxf")
    if not dwg2dxf:
        return _stub(
            path,
            "DWG is proprietary — install LibreDWG (`brew install libredwg`) and "
            "re-ingest for full extraction, or request DXF from the author",
        )
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / (path.stem + ".dxf")
        # GPL tool invoked as an external subprocess only — never vendored.
        proc = subprocess.run(
            [dwg2dxf, "-o", str(out), str(path)],
            capture_output=True, text=True, timeout=120,
        )
        if proc.returncode != 0 or not out.exists():
            return _stub(path, f"dwg2dxf conversion failed: {proc.stderr.strip()[:200]}")
        result = _convert_dxf(out)
    result.converter = f"libredwg+{result.converter}"
    return result


# ------------------------------------------------------------------ KiCad

_KICAD_PROP_RE = re.compile(
    r'\(property\s+"(Reference|Value|Footprint)"\s+"([^"]*)"', re.IGNORECASE
)
_KICAD_LIB_RE = re.compile(r'\(lib_id\s+"([^"]+)"')
_KICAD_NET_RE = re.compile(r'\(net\s+\d+\s+"([^"]*)"\)')


def _iter_sexpr_blocks(text: str, head: str):
    """Yield the balanced-paren substring of each top-level `(head …)` block."""
    i = 0
    while True:
        idx = text.find(head, i)
        if idx == -1:
            return
        depth, j = 0, idx
        while j < len(text):
            ch = text[j]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    j += 1
                    break
            j += 1
        yield text[idx:j]
        i = max(j, idx + 1)


def _strip_sexpr_block(text: str, head: str) -> str:
    out, i = [], 0
    for block in _iter_sexpr_blocks(text, head):
        idx = text.find(block, i)
        out.append(text[i:idx])
        i = idx + len(block)
    out.append(text[i:])
    return "".join(out)


def _convert_kicad(path: Path) -> ConversionResult:
    text = path.read_text(encoding="utf-8", errors="replace")
    # Every KiCad ≥6 schematic embeds a (lib_symbols …) DEFINITION block whose
    # template properties (Reference="R", Value="R") would masquerade as real
    # components — strip it before reading instance properties.
    instance_text = _strip_sexpr_block(text, "(lib_symbols")
    parts: list[str] = []

    rows: list[dict] = []
    for block in _iter_sexpr_blocks(instance_text, "(symbol "):
        props = {k.capitalize(): v for k, v in _KICAD_PROP_RE.findall(block)}
        if "Reference" in props or "Value" in props:  # a placed instance
            rows.append(props)
    if not rows:  # .kicad_pcb footprints use (fp_text reference …) instead
        for block in _iter_sexpr_blocks(instance_text, "(footprint "):
            m = re.search(r'\(fp_text\s+reference\s+"([^"]*)"', block)
            ref = re.search(r'\(property\s+"Reference"\s+"([^"]*)"', block)
            val = re.search(r'\(property\s+"Value"\s+"([^"]*)"', block)
            if m or ref:
                rows.append({
                    "Reference": (m or ref).group(1) if (m or ref) else "",
                    "Value": val.group(1) if val else "",
                })
    if rows:
        parts.append("## Components\n\n| Reference | Value | Footprint |\n|---|---|---|")
        parts.extend(
            f"| {r.get('Reference', '')} | {r.get('Value', '')} | {r.get('Footprint', '')} |"
            for r in rows[:300]
        )

    libs = sorted(set(_KICAD_LIB_RE.findall(instance_text)))
    if libs:
        parts.append("## Symbol Libraries\n\n" + ", ".join(libs[:100]))
    nets = sorted({n for n in _KICAD_NET_RE.findall(text) if n})
    if nets:
        parts.append(f"## Nets\n\n{len(nets)} named net(s): " + ", ".join(nets[:80]))

    if not parts:  # e.g. .kicad_pro project json — index as capped text
        parts.append(text[:8000])
    return ConversionResult(
        body="\n".join(parts), converter="kicad-sexpr-1", tier="T4",
        confidence="high" if props or libs else "med",
    )


# ------------------------------------------------------------------ Gerber

_GERBER_TF_RE = re.compile(r"%TF\.([\w.]+),([^*%]*)\*%")
# Reference-designator attribute ONLY (comma right after `.C`); the `.Cxxx`
# characteristic attributes (.CVal/.CRot/.CMfr/.CMPN/.CFtp/.CMnt) are captured
# separately so refdes counts stay honest.
_GERBER_TO_RE = re.compile(r"%TO\.C,([^*%]*)\*%")
_GERBER_TOCHAR_RE = re.compile(r"%TO\.C(Val|Rot|Mfr|MPN|Ftp|Mnt),([^*%]*)\*%")


def _convert_gerber(path: Path) -> ConversionResult:
    text = path.read_text(encoding="utf-8", errors="replace")
    attrs = _GERBER_TF_RE.findall(text)
    components = _GERBER_TO_RE.findall(text)
    parts: list[str] = []
    if attrs:
        parts.append("## Gerber X2 File Attributes\n\n| Attribute | Value |\n|---|---|")
        parts.extend(f"| {k} | {v} |" for k, v in attrs[:50])
    if components:
        refdes = sorted({c.strip() for c in components if c.strip()})
        parts.append(f"## X3 Component Records ({len(refdes)})\n")
        parts.extend(f"- {c}" for c in refdes[:200])
        chars = _GERBER_TOCHAR_RE.findall(text)
        if chars:
            parts.append("\n### Component Characteristics\n")
            parts.extend(f"- {k}: {v}" for k, v in chars[:200])
    if not parts:
        return ConversionResult(
            body="(bare RS-274X — no X2/X3 metadata; geometry not indexed)",
            converter="gerber-x2-regex-1", tier="T4", confidence="low",
            notes="ask the fab/EDA export to enable Gerber X2 attributes",
        )
    return ConversionResult(
        body="\n".join(parts), converter="gerber-x2-regex-1", tier="T4",
        confidence="high",
    )


# ------------------------------------------------------------------ STEP

_STEP_PRODUCT_RE = re.compile(r"PRODUCT\s*\(\s*'([^']*)'")
_STEP_HEADER_RE = re.compile(r"(FILE_NAME|FILE_DESCRIPTION)\s*\(\s*(.{0,400}?)\)\s*;", re.DOTALL)


def _convert_step(path: Path) -> ConversionResult:
    text = path.read_text(encoding="utf-8", errors="replace")
    parts: list[str] = []
    for key, raw in _STEP_HEADER_RE.findall(text[:20000]):
        parts.append(f"- **{key}**: {' '.join(raw.split())[:300]}")
    products = [p for p in _STEP_PRODUCT_RE.findall(text) if p.strip()]
    unique = sorted(set(products))
    if unique:
        parts.append(f"\n## Assembly Products ({len(products)} instances, "
                     f"{len(unique)} unique)\n")
        parts.extend(f"- {p}" for p in unique[:200])
    return ConversionResult(
        body="\n".join(parts) or "(no ASCII STEP metadata found)",
        converter="step-regex-1", tier="T4",
        confidence="high" if unique else "low",
    )


# ------------------------------------------------------------------ firmware

_INTERESTING_RE = re.compile(
    r"(v?\d+\.\d+(\.\d+)?([+-][\w.]+)?$|version|build|copyright|firmware|boot|"
    r"\d{4}-\d{2}-\d{2}|[A-Za-z]{3}\s+\d{1,2}\s+\d{4})",
    re.IGNORECASE,
)
# Printable-ASCII run of ≥6 chars — a compiled bytes-regex, not a per-byte
# Python loop (a 500MB blob would otherwise pin a core and hold >1GB).
_FW_STRING_RE = re.compile(rb"[\x20-\x7e]{6,}")
_FW_SCAN_CAP = 8 * 1024 * 1024  # scan at most 8 MB — enough for version strings


def _convert_firmware(path: Path) -> ConversionResult:
    total = path.stat().st_size
    with path.open("rb") as f:
        data = f.read(_FW_SCAN_CAP)
    truncated = total > _FW_SCAN_CAP
    is_elf = data[:4] == b"\x7fELF"
    runs = (m.group().decode("ascii", "replace") for m in _FW_STRING_RE.finditer(data))
    seen: list[str] = []
    for r in runs:
        r = r.strip()
        if _INTERESTING_RE.search(r) and r not in seen:
            seen.append(r)
            if len(seen) >= 100:
                break
    scanned = f"{min(total, _FW_SCAN_CAP):,} of {total:,} bytes" if truncated \
        else f"{total:,} bytes"
    parts = [f"- Format: {'ELF' if is_elf else 'raw binary'} ({scanned})"]
    if seen:
        parts.append("\n## Version / Build Strings\n")
        parts.extend(f"- `{s[:200]}`" for s in seen)
    note = "" if seen else "no version/build strings found — metadata card only"
    if truncated:
        note = (note + "; " if note else "") + f"scan capped at {_FW_SCAN_CAP // (1024*1024)} MB"
    return ConversionResult(
        body="\n".join(parts), converter="fw-strings-1", tier="T4",
        confidence="high" if (is_elf and seen) else ("med" if seen else "low"),
        notes=note,
    )


# ------------------------------------------------------------------ stubs

def _stub(path: Path, policy: str) -> ConversionResult:
    return ConversionResult(
        body=(f"(binary engineering format — metadata card only)\n\n"
              f"- Format: `{path.suffix.lower()}`\n- Policy: {policy}"),
        converter="stub-card-1", tier="T4", confidence="low", notes=policy,
    )
