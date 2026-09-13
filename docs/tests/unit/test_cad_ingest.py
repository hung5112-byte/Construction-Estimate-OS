"""Tests for Step-6 CAD/engineering file extraction."""
from __future__ import annotations

from pathlib import Path

import pytest

from core.ingest.cad import convert_cad
from core.ingest.pipeline import card_path_for, ingest_file
from core.obsidian.frontmatter import parse as parse_frontmatter


@pytest.fixture()
def vault(tmp_path: Path) -> Path:
    root = tmp_path / "vault"
    (root / "05-Sources").mkdir(parents=True)
    return root


# ------------------------------------------------------------------ DXF

def _make_dxf(path: Path) -> Path:
    import ezdxf

    doc = ezdxf.new("R2010")
    doc.layers.add("NOTES")
    msp = doc.modelspace()
    msp.add_text("CY80 ENCLOSURE REV C", dxfattribs={"height": 5, "layer": "NOTES"})
    msp.add_mtext("Material: 6061-T6 aluminum")
    blk = doc.blocks.new("TITLEBLOCK")
    blk.add_attdef("DRAWN_BY")
    blk.add_attdef("PART_NO")
    ins = msp.add_blockref("TITLEBLOCK", (0, 0))
    ins.add_auto_attribs({"DRAWN_BY": "B. Doan", "PART_NO": "CY80-ENC-003"})
    doc.saveas(path)
    return path


def test_dxf_extracts_title_block_and_text(vault: Path):
    src = _make_dxf(vault / "05-Sources" / "enclosure.dxf")
    r = convert_cad(src)
    assert r.tier == "T4" and r.confidence == "high"
    assert "CY80-ENC-003" in r.body  # title-block attribute
    assert "B. Doan" in r.body
    assert "CY80 ENCLOSURE REV C" in r.body  # TEXT
    assert "6061-T6 aluminum" in r.body  # MTEXT
    assert "NOTES" in r.body  # layer inventory


def test_dxf_becomes_citable_shadow_card(vault: Path):
    src = _make_dxf(vault / "05-Sources" / "enclosure.dxf")
    res = ingest_file(vault, src)
    assert res.status == "ingested"
    fm, body = parse_frontmatter(card_path_for(src).read_text(encoding="utf-8"))
    assert fm["trust_tier"] == "ingested-doc"
    assert fm["tier"] == "T4"
    assert "CY80-ENC-003" in body


# ------------------------------------------------------------------ KiCad

def test_kicad_schematic_component_table(vault: Path):
    sch = vault / "05-Sources" / "board.kicad_sch"
    sch.write_text(
        '(kicad_sch\n'
        '  (symbol (lib_id "Device:R")\n'
        '    (property "Reference" "R1")\n'
        '    (property "Value" "10k")\n'
        '    (property "Footprint" "R_0402")\n'
        '  )\n'
        '  (symbol (lib_id "Device:C")\n'
        '    (property "Reference" "C3")\n'
        '    (property "Value" "100nF")\n'
        '    (property "Footprint" "C_0402")\n'
        '  )\n'
        ')\n',
        encoding="utf-8",
    )
    r = convert_cad(sch)
    assert r.confidence == "high"
    assert "| R1 | 10k | R_0402 |" in r.body
    assert "| C3 | 100nF | C_0402 |" in r.body
    assert "Device:R" in r.body  # library inventory


# ------------------------------------------------------------------ Gerber

def test_gerber_x3_component_records(vault: Path):
    gbr = vault / "05-Sources" / "top.gtl"
    gbr.write_text(
        "%TF.FileFunction,Copper,L1,Top*%\n"
        "%TF.Part,Single*%\n"
        "%TO.C,R1*%\n"
        "%TO.C,U5*%\n"
        "G04 actual image data*\n",
        encoding="utf-8",
    )
    r = convert_cad(gbr)
    assert r.confidence == "high"
    assert "FileFunction" in r.body and "Copper,L1,Top" in r.body
    assert "R1" in r.body and "U5" in r.body


def test_bare_gerber_degrades_low(vault: Path):
    gbr = vault / "05-Sources" / "plain.gbr"
    gbr.write_text("G04 no attributes*\nX100Y100D01*\nM02*\n", encoding="utf-8")
    r = convert_cad(gbr)
    assert r.confidence == "low"
    assert "geometry not indexed" in r.body


# ------------------------------------------------------------------ STEP

def test_step_assembly_products(vault: Path):
    stp = vault / "05-Sources" / "assembly.step"
    stp.write_text(
        "ISO-10303-21;\nHEADER;\n"
        "FILE_NAME('cy80-assy.stp','2026-07-17',(''),(''),'','','');\n"
        "ENDSEC;\nDATA;\n"
        "#10=PRODUCT('CY80-ENCLOSURE','enclosure',' ',(#2));\n"
        "#20=PRODUCT('CY80-LID','lid',' ',(#2));\n"
        "#30=PRODUCT('CY80-ENCLOSURE','enclosure',' ',(#2));\n"
        "ENDSEC;\nEND-ISO-10303-21;\n",
        encoding="utf-8",
    )
    r = convert_cad(stp)
    assert r.confidence == "high"
    assert "CY80-ENCLOSURE" in r.body and "CY80-LID" in r.body
    assert "3 instances, 2 unique" in r.body  # dedup counting


# ------------------------------------------------------------------ firmware

def test_elf_firmware_version_strings(vault: Path):
    elf = vault / "05-Sources" / "app.elf"
    elf.write_bytes(
        b"\x7fELF\x02\x01\x01" + b"\x00" * 9
        + b"garbage\x00firmware v2.3.1\x00"
        + b"\x00build 2026-07-01\x00" + b"\xff" * 20
        + b"Copyright 2026 Acme\x00"
    )
    r = convert_cad(elf)
    assert r.confidence == "high"
    assert "firmware v2.3.1" in r.body
    assert "ELF" in r.body


def test_raw_binary_without_strings_low(vault: Path):
    blob = vault / "05-Sources" / "blob.bin"
    blob.write_bytes(bytes(range(256)) * 4)
    r = convert_cad(blob)
    assert r.confidence in ("low", "med")
    assert "raw binary" in r.body


# ------------------------------------------------------------------ DWG + stubs

def test_dwg_without_libredwg_is_stub(vault: Path, monkeypatch):
    monkeypatch.setattr("core.ingest.cad.shutil.which", lambda _: None)
    dwg = vault / "05-Sources" / "legacy.dwg"
    dwg.write_bytes(b"AC1027" + b"\x00" * 100)
    r = convert_cad(dwg)
    assert r.confidence == "low"
    assert "LibreDWG" in r.body


def test_solidworks_native_is_policy_stub(vault: Path):
    src = vault / "05-Sources" / "part.sldprt"
    src.write_bytes(b"\xd0\xcf\x11\xe0" + b"\x00" * 64)  # OLE magic
    r = convert_cad(src)
    assert r.confidence == "low"
    assert "STEP" in r.body  # intake policy nudge


def test_cad_extensions_are_supported(vault: Path):
    from core.ingest.converters import SUPPORTED_EXTS

    for ext in (".dxf", ".dwg", ".kicad_sch", ".gtl", ".step", ".elf", ".stl", ".sldprt"):
        assert ext in SUPPORTED_EXTS


# ------------------------------------------------- review-fleet regression fixes

def test_kicad_ignores_lib_symbols_definitions(vault: Path):
    """Real KiCad >=6 embeds (lib_symbols ...) — its template props must not
    appear as phantom components."""
    sch = vault / "05-Sources" / "real.kicad_sch"
    sch.write_text(
        '(kicad_sch\n'
        '  (lib_symbols\n'
        '    (symbol "Device:R"\n'
        '      (property "Reference" "R")\n'
        '      (property "Value" "R")\n'
        '      (property "Footprint" "")\n'
        '    )\n'
        '    (symbol "Device:C"\n'
        '      (property "Reference" "C")\n'
        '      (property "Value" "C")\n'
        '    )\n'
        '  )\n'
        '  (symbol (lib_id "Device:R") (at 50 50 0) (uuid abc)\n'
        '    (property "Reference" "R1")\n'
        '    (property "Value" "10k")\n'
        '    (property "Footprint" "R_0402")\n'
        '  )\n'
        '  (symbol (lib_id "Device:C") (at 60 50 0) (uuid def)\n'
        '    (property "Reference" "C3")\n'
        '    (property "Value" "100nF")\n'
        '  )\n'
        ')\n',
        encoding="utf-8",
    )
    r = convert_cad(sch)
    assert "| R1 | 10k | R_0402 |" in r.body
    assert "| C3 | 100nF |" in r.body
    # No phantom template rows (Reference == bare "R"/"C")
    assert "| R | R |" not in r.body
    assert "| C | C |" not in r.body


def test_gerber_refdes_excludes_characteristics(vault: Path):
    gbr = vault / "05-Sources" / "x3.gtl"
    gbr.write_text(
        "%TO.C,R1*%\n%TO.CVal,10k*%\n%TO.CRot,90*%\n%TO.CMfr,Yageo*%\n"
        "%TO.C,U5*%\n%TO.CMPN,STM32F103*%\n%TO.CFtp,QFP48*%\n",
        encoding="utf-8",
    )
    r = convert_cad(gbr)
    assert "## X3 Component Records (2)" in r.body  # R1, U5 only — not 7
    assert "- R1" in r.body and "- U5" in r.body
    assert "10k" in r.body and "Yageo" in r.body  # characteristics kept separately
    # ...but not counted as refdes
    assert "- 10k" not in r.body.split("### Component Characteristics")[0]


def test_firmware_scan_is_size_capped(vault: Path, monkeypatch):
    import core.ingest.cad as cad

    monkeypatch.setattr(cad, "_FW_SCAN_CAP", 4096)
    big = vault / "05-Sources" / "big.bin"
    # 1 MB of noise, then a version string PAST the cap → not scanned
    big.write_bytes(b"\x00" * (1024 * 1024) + b"firmware v9.9.9 secret\x00")
    r = convert_cad(big)
    assert "of 1,048" in r.body or "capped" in (r.notes or "")  # reports truncation
    assert "v9.9.9" not in r.body  # beyond the cap, never read


def test_firmware_finds_early_version_string(vault: Path):
    elf = vault / "05-Sources" / "app.elf"
    elf.write_bytes(b"\x7fELF" + b"\x00" * 12 + b"firmware v2.3.1 build 2026-07-01\x00")
    r = convert_cad(elf)
    assert "firmware v2.3.1" in r.body and r.confidence == "high"


def test_dwg_subprocess_uses_list_form(vault: Path, monkeypatch):
    """A crafted filename must never reach a shell."""
    calls = {}

    def fake_run(args, **kw):
        calls["args"] = args
        import subprocess as sp
        return sp.CompletedProcess(args, 1, "", "no")

    monkeypatch.setattr("core.ingest.cad.shutil.which", lambda _: "/usr/bin/dwg2dxf")
    monkeypatch.setattr("core.ingest.cad.subprocess.run", fake_run)
    evil = vault / "05-Sources" / "a; rm -rf x.dwg"
    evil.write_bytes(b"AC1027")
    convert_cad(evil)
    assert isinstance(calls["args"], list)  # never a shell string
    assert "; rm -rf" in calls["args"][-1]  # passed as one literal arg
