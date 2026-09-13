#!/usr/bin/env python3
"""Generate the synthetic bid package used as the test fixture and the golden eval set.

Prairie Creek Office/Warehouse — 12,000 SF single-story (4,000 SF office + 8,000 SF warehouse),
fictional, Plano TX. Nine vector sheets (ARCH D 36x24 in, 1/8" = 1'-0") plus a Project Manual,
built from SVG/HTML through headless Chrome so the PDFs keep a real text layer (title blocks,
tags, dimension strings, schedules) and real vector geometry (walls, door swings, windows).

Ground truth is written next to the PDFs (ground_truth.json) — every count and area is exact by
construction, so the takeoff tools and the evals can be scored without a human.

Usage:  python scripts/make_sample_set.py [--out docs/tests/fixtures/sample-set-prairie-creek]
Needs Google Chrome (or Chromium) on the machine
the generated PDFs are committed so CI does not.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "chromium", "chromium-browser",
]

# ----------------------------------------------------------------------------- geometry basis
# Sheet: 36 x 24 in, SVG user units = 1/100 in → 3600 x 2400. Scale 1/8" = 1'-0" → 1 ft = 12.5 u.
U_PER_FT = 12.5
OX, OY = 520.0, 460.0            # building origin (north-west corner) on the sheet
BLD_L, BLD_W = 120.0, 100.0      # ft (x east-west, y north-south)
OFFICE_L = 40.0                  # ft, west portion
PROJECT = "PRAIRIE CREEK OFFICE/WAREHOUSE — BUILDING 2"
CLIENT = "BLACKLAND COMMERCIAL BUILDERS (SYNTHETIC DEMO)"
DATE = "09/12/2026"


def x(ft: float) -> float:
    return OX + ft * U_PER_FT


def y(ft: float) -> float:
    return OY + ft * U_PER_FT


# Rooms: (number, name, x0, y0, x1, y1) in ft from the NW corner
ROOMS = [
    ("101", "LOBBY", 0, 0, 20, 25),
    ("102", "CONFERENCE", 20, 0, 40, 25),
    ("103", "OFFICE", 0, 25, 20, 50),
    ("104", "OFFICE", 20, 25, 40, 50),
    ("105", "BREAK ROOM", 0, 50, 20, 75),
    ("108", "OFFICE", 20, 50, 40, 75),
    ("106", "RESTROOM M", 0, 75, 20, 87.5),
    ("107", "RESTROOM W", 0, 87.5, 20, 100),
    ("109", "IT / STORAGE", 20, 75, 40, 100),
    ("200", "WAREHOUSE", 40, 0, 120, 100),
]

# Doors: (mark, x_ft, y_ft, wall 'h'|'v', swing quadrant, width_ft, type)
DOORS = [
    ("101", 10, 0, "h", "se", 6.0, "STOREFRONT PAIR"),        # lobby entrance, north wall
    ("102", 20, 12, "v", "ne", 3.0, "HM/WOOD"),
    ("103", 20, 37, "v", "nw", 3.0, "HM/WOOD"),
    ("104", 20, 30, "v", "ne", 3.0, "HM/WOOD"),
    ("105", 20, 62, "v", "nw", 3.0, "HM/WOOD"),
    ("106", 10, 75, "h", "se", 3.0, "HM/WOOD"),
    ("107", 10, 87.5, "h", "se", 3.0, "HM/WOOD"),
    ("108", 20, 55, "v", "ne", 3.0, "HM/WOOD"),
    ("109", 20, 80, "v", "ne", 3.0, "HM/WOOD"),
    ("110", 40, 45, "v", "ne", 3.0, "HM RATED 90 MIN"),       # office ↔ warehouse
    ("200A", 80, 100, "h", "ne", 3.0, "HM EXTERIOR"),          # warehouse south wall
    ("200B", 120, 60, "v", "nw", 3.0, "HM EXTERIOR"),          # warehouse east wall
]
OVERHEAD_DOORS = [("OH-1", 120, 20, 12.0, 14.0), ("OH-2", 120, 85, 12.0, 14.0)]  # east wall, w x h ft

# Windows: (mark, x_ft, y_ft, wall, width_ft)
WINDOWS = (
    [("W1", 0, yy, "v", 4.0) for yy in (6, 14, 31, 39, 56, 64)]          # west wall
    + [("W1", xx, 0, "h", 4.0) for xx in (26, 34, 3, 16)]                 # north wall (102 ×2, 101 ×2)
)

# Structural grid: columns lines A..D at x = 0,40,80,120 ; rows 1..3 at y = 0,50,100 ; office rows at 25' oc
GRID_X = {"A": 0, "B": 40, "C": 80, "D": 120}
GRID_Y = {"1": 0, "2": 50, "3": 100}
COLUMNS = [(gx, gy) for gx in ("B", "C", "D") for gy in ("1", "2", "3")]  # 9 warehouse columns
FOOTING_SCHEDULE = [
    ("F1", "4'-0\" x 4'-0\" x 1'-6\"", "(6) #5 EA WAY", 9),
    ("F2", "CONT. 2'-0\" x 1'-0\"", "(3) #5 CONT.", 440),  # LF
]
SLABS = [("OFFICE", 4, 4000), ("WAREHOUSE", 6, 8000)]  # thickness in, SF
STEEL = [
    ("B1", "W16x31", 40.0, 6, 31.0),      # beams between warehouse columns along rows 1,2,3 (2 bays × 3 rows)
    ("J1", "24K4", 50.0, 32, 8.4),         # warehouse joists spanning 50' between rows, 4 bays × 8
    ("J2", "18K3", 40.0, 21, 6.6),         # office joists spanning 40' at 5' oc
    ("C1", "HSS8x8x1/4", 24.0, 9, 25.8),   # warehouse columns
    ("C2", "HSS6x6x1/4", 14.0, 5, 19.0),   # office columns on grid B at 25' oc
]
DECK = [("WAREHOUSE", "1-1/2\" TYPE B 22 GA", 8000), ("OFFICE", "1-1/2\" TYPE B 22 GA", 4000)]

HVAC_EQUIP = [
    ("RTU-1", "PACKAGED ROOFTOP UNIT", "7.5 TON / 3000 CFM", "460V/3PH", "OFFICE EAST"),
    ("RTU-2", "PACKAGED ROOFTOP UNIT", "7.5 TON / 3000 CFM", "460V/3PH", "OFFICE WEST"),
    ("UH-1", "GAS UNIT HEATER", "150 MBH", "120V/1PH", "WAREHOUSE"),
    ("UH-2", "GAS UNIT HEATER", "150 MBH", "120V/1PH", "WAREHOUSE"),
    ("EF-1", "CEILING EXHAUST FAN", "150 CFM", "120V/1PH", "RESTROOM 106"),
    ("EF-2", "CEILING EXHAUST FAN", "150 CFM", "120V/1PH", "RESTROOM 107"),
]
DIFFUSERS = 12
PLUMBING_FIXTURES = [
    ("WC-1", "WATER CLOSET, FLOOR MOUNT, 1.28 GPF", 4),
    ("UR-1", "URINAL, WALL HUNG, 0.125 GPF", 1),
    ("LAV-1", "LAVATORY, WALL HUNG", 4),
    ("SK-1", "BREAK ROOM SINK, DOUBLE BOWL", 1),
    ("MS-1", "MOP SINK", 1),
    ("EWC-1", "ELECTRIC WATER COOLER, BI-LEVEL", 1),
    ("WH-1", "ELECTRIC WATER HEATER, 40 GAL", 1),
    ("HB-1", "HOSE BIBB", 4),
]
SPRINKLER = {"office_sf": 4000, "office_sf_per_head": 200, "warehouse_sf": 8000, "warehouse_sf_per_head": 130}
ELECTRICAL = {
    "service": "400A, 480Y/277V, 3PH, 4W",
    "gear": [("MDP", "400A MAIN DISTRIBUTION PANEL 480Y/277V"), ("T-1", "45 KVA TRANSFORMER 480-208Y/120V"),
             ("LP-1", "208Y/120V PANELBOARD, 42 CKT"), ("HP-1", "480Y/277V PANELBOARD, 30 CKT")],
    "fixtures": [("A", "2x4 LED TROFFER, 4000 LM", 40), ("B", "LED HIGH BAY, 20000 LM", 24),
                 ("C", "LED WALL PACK, EXTERIOR", 8), ("X", "LED EXIT SIGN W/ BATTERY", 6)],
    "receptacles": 48, "data_outlets": 24,
    "fire_alarm": [("FACP", 1), ("PULL STATION", 4), ("HORN/STROBE", 10), ("SMOKE DETECTOR", 6)],
}


# ----------------------------------------------------------------------------- SVG helpers
def svg_open() -> list[str]:
    return ['<svg xmlns="http://www.w3.org/2000/svg" width="36in" height="24in" viewBox="0 0 3600 2400" '
            'font-family="Helvetica, Arial, sans-serif">',
            '<rect x="0" y="0" width="3600" height="2400" fill="white"/>',
            '<rect x="40" y="40" width="3520" height="2320" fill="none" stroke="black" stroke-width="4"/>']


def title_block(sheet: str, title: str, scale: str, rev: str = "2", extra: list[str] | None = None) -> list[str]:
    o = ['<g id="titleblock" font-size="22">',
         '<rect x="2960" y="1980" width="600" height="380" fill="none" stroke="black" stroke-width="3"/>',
         '<line x1="2960" y1="2080" x2="3560" y2="2080" stroke="black" stroke-width="2"/>',
         '<line x1="2960" y1="2180" x2="3560" y2="2180" stroke="black" stroke-width="2"/>',
         '<line x1="2960" y1="2270" x2="3560" y2="2270" stroke="black" stroke-width="2"/>',
         f'<text x="2980" y="2015" font-size="24" font-weight="bold">{CLIENT}</text>',
         f'<text x="2980" y="2050" font-size="20">{PROJECT}</text>',
         '<text x="2980" y="2110" font-size="18">SHEET TITLE</text>',
         f'<text x="2980" y="2150" font-size="28" font-weight="bold">{title}</text>',
         f'<text x="2980" y="2210" font-size="20">SCALE: {scale}</text>',
         f'<text x="3300" y="2210" font-size="20">DATE: {DATE}</text>',
         f'<text x="2980" y="2250" font-size="20">REV: {rev}   ADDENDUM 1: 09/19/2026</text>',
         '<text x="2980" y="2305" font-size="18">SHEET NUMBER</text>',
         f'<text x="3300" y="2330" font-size="44" font-weight="bold">{sheet}</text>',
         '</g>']
    if extra:
        o.extend(extra)
    return o


def north_arrow() -> list[str]:
    return ['<g id="north" stroke="black" fill="none" stroke-width="2">',
            '<circle cx="3300" cy="300" r="60"/>', '<path d="M3300,250 L3320,330 L3300,310 L3280,330 Z" fill="black"/>',
            '<text x="3285" y="400" font-size="26" stroke="none" fill="black">N</text>', '</g>']


def wall_rect(x0, y0, x1, y1, width=10) -> str:
    return (f'<rect x="{x(x0):.1f}" y="{y(y0):.1f}" width="{(x1-x0)*U_PER_FT:.1f}" '
            f'height="{(y1-y0)*U_PER_FT:.1f}" fill="none" stroke="black" stroke-width="{width}"/>')


def line(xa, ya, xb, yb, width=3, dash: str | None = None, cls: str = "") -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    c = f' class="{cls}"' if cls else ""
    return f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="black" stroke-width="{width}"{d}{c}/>'


def text(px, py, s, size=20, weight="normal", anchor="start", rotate: float | None = None) -> str:
    r = f' transform="rotate({rotate} {px:.1f},{py:.1f})"' if rotate else ""
    return (f'<text x="{px:.1f}" y="{py:.1f}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}"{r}>{s}</text>')


def door(mark: str, xf: float, yf: float, wall: str, quad: str, width_ft: float) -> list[str]:
    """Door swing: leaf line + quarter arc; tag hexagon with the mark next to it."""
    r = width_ft * U_PER_FT
    cx, cy = x(xf), y(yf)
    out = ['<g class="door" stroke="black" fill="none" stroke-width="3">']
    if wall == "h":  # door in a horizontal (E-W) wall; hinge at (cx,cy), swing to the south if 'se'
        sy = 1 if "s" in quad else -1
        out.append(line(cx, cy, cx, cy + sy * r))                       # leaf perpendicular to wall
        out.append(f'<path d="M{cx:.1f},{cy + sy * r:.1f} A{r:.1f},{r:.1f} 0 0 {1 if sy < 0 else 0} {cx + r:.1f},{cy:.1f}"/>')
        tx, ty = cx + r / 2, cy + sy * (r + 30)
    else:            # door in a vertical (N-S) wall; hinge at (cx,cy); swing east if 'e'
        sx = 1 if "e" in quad else -1
        out.append(line(cx, cy, cx + sx * r, cy))
        out.append(f'<path d="M{cx + sx * r:.1f},{cy:.1f} A{r:.1f},{r:.1f} 0 0 {1 if sx > 0 else 0} {cx:.1f},{cy + r:.1f}"/>')
        tx, ty = cx + sx * (r + 40), cy + r / 2
    out.append('</g>')
    # hexagon door tag
    out.append(f'<polygon points="{tx-28:.1f},{ty:.1f} {tx-14:.1f},{ty-22:.1f} {tx+14:.1f},{ty-22:.1f} {tx+28:.1f},{ty:.1f} '
               f'{tx+14:.1f},{ty+22:.1f} {tx-14:.1f},{ty+22:.1f}" fill="white" stroke="black" stroke-width="2"/>')
    out.append(text(tx, ty + 7, mark, 18, "bold", "middle"))
    return out


def window(mark: str, xf: float, yf: float, wall: str, width_ft: float) -> list[str]:
    w = width_ft * U_PER_FT
    out = ['<g class="window" stroke="black" stroke-width="3">']
    if wall == "h":
        cx, cy = x(xf), y(yf)
        out.append(line(cx, cy - 6, cx + w, cy - 6))
        out.append(line(cx, cy + 6, cx + w, cy + 6))
        tx, ty = cx + w / 2, cy - 40
    else:
        cx, cy = x(xf), y(yf)
        out.append(line(cx - 6, cy, cx - 6, cy + w))
        out.append(line(cx + 6, cy, cx + 6, cy + w))
        tx, ty = cx - 45, cy + w / 2
    out.append('</g>')
    out.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="22" fill="white" stroke="black" stroke-width="2"/>')
    out.append(text(tx, ty + 6, mark, 16, "bold", "middle"))
    return out


def dim_h(x0f, x1f, yu, label) -> list[str]:
    a, b = x(x0f), x(x1f)
    return [line(a, yu, b, yu, 1.5), line(a, yu - 12, a, yu + 12, 1.5), line(b, yu - 12, b, yu + 12, 1.5),
            text((a + b) / 2, yu - 10, label, 20, anchor="middle")]


def dim_v(y0f, y1f, xu, label) -> list[str]:
    a, b = y(y0f), y(y1f)
    return [line(xu, a, xu, b, 1.5), line(xu - 12, a, xu + 12, a, 1.5), line(xu - 12, b, xu + 12, b, 1.5),
            text(xu - 14, (a + b) / 2, label, 20, anchor="middle", rotate=-90)]


def grid_bubbles() -> list[str]:
    out = ['<g id="grid" font-size="22">']
    for gx, ft in GRID_X.items():
        px = x(ft)
        out.append(line(px, y(-27), px, y(BLD_W + 6), 1, dash="14,10"))
        out.append(f'<circle cx="{px:.1f}" cy="{y(-31):.1f}" r="26" fill="white" stroke="black" stroke-width="2"/>')
        out.append(text(px, y(-31) + 8, gx, 22, "bold", "middle"))
    for gy, ft in GRID_Y.items():
        py = y(ft)
        out.append(line(x(-30), py, x(BLD_L + 6), py, 1, dash="14,10"))
        out.append(f'<circle cx="{x(-34):.1f}" cy="{py:.1f}" r="26" fill="white" stroke="black" stroke-width="2"/>')
        out.append(text(x(-34), py + 8, gy, 22, "bold", "middle"))
    out.append('</g>')
    return out


def table(px, py, title, headers, rows, col_w, row_h=34, size=18) -> list[str]:
    out = [text(px, py - 12, title, 24, "bold")]
    w = sum(col_w)
    n = len(rows) + 1
    out.append(f'<rect x="{px}" y="{py}" width="{w}" height="{n*row_h}" fill="none" stroke="black" stroke-width="2"/>')
    for i in range(1, n):
        out.append(line(px, py + i * row_h, px + w, py + i * row_h, 1))
    cx = px
    for cw in col_w[:-1]:
        cx += cw
        out.append(line(cx, py, cx, py + n * row_h, 1))
    def row(vals, yy, bold=False):
        cx = px
        for v, cw in zip(vals, col_w):
            out.append(text(cx + 8, yy + row_h - 10, str(v), size, "bold" if bold else "normal"))
            cx += cw
    row(headers, py, True)
    for i, r in enumerate(rows, 1):
        row(r, py + i * row_h)
    return out


def notes(px, py, title, items, size=18, gap=30) -> list[str]:
    out = [text(px, py, title, 24, "bold")]
    for i, it in enumerate(items, 1):
        out.append(text(px, py + 12 + i * gap, f"{i}. {it}", size))
    return out


# ----------------------------------------------------------------------------- sheets
def sheet_g001() -> str:
    o = svg_open()
    o.append(text(1800, 300, PROJECT, 60, "bold", "middle"))
    o.append(text(1800, 370, "12,000 SF SINGLE-STORY OFFICE / WAREHOUSE — 2201 PRAIRIE CREEK PKWY, PLANO, TX 75074 (FICTIONAL)", 26, anchor="middle"))
    o.append(text(1800, 420, "BID SET — ISSUED FOR BID 09/12/2026 — SYNTHETIC DEMO DATA, NOT A REAL PROJECT", 24, anchor="middle"))
    index = [("G-001", "COVER SHEET, INDEX, CODE SUMMARY"), ("A-101", "FLOOR PLAN"), ("A-201", "EXTERIOR ELEVATIONS"),
             ("A-601", "DOOR, WINDOW & FINISH SCHEDULES"), ("S-101", "FOUNDATION PLAN & GENERAL NOTES"),
             ("S-201", "ROOF FRAMING PLAN"), ("M-101", "HVAC PLAN & SCHEDULES"), ("P-101", "PLUMBING PLAN & FIXTURE SCHEDULE"),
             ("E-101", "POWER & LIGHTING PLAN, ONE-LINE, PANEL SCHEDULES")]
    o += table(300, 560, "SHEET INDEX", ["SHEET", "TITLE", "REV"], [(s, t, "2") for s, t in index], [180, 900, 100])
    code = [("BUILDING TYPE", "OFFICE / WAREHOUSE (B / S-1)"), ("CONSTRUCTION TYPE", "II-B"), ("GROSS AREA", "12,000 SF"),
            ("OFFICE AREA", "4,000 SF"), ("WAREHOUSE AREA", "8,000 SF"), ("STORIES", "1"), ("HEIGHT", "OFFICE 14'-0\" / WAREHOUSE 24'-0\""),
            ("SPRINKLERS", "YES — NFPA 13, DESIGN-BUILD"), ("OCCUPANT LOAD", "B: 40 / S-1: 16"), ("CODES", "IBC 2021, IECC 2021, NEC 2023, TAS 2012")]
    o += table(1600, 560, "CODE SUMMARY", ["ITEM", "VALUE"], code, [420, 800])
    o += notes(300, 1000, "GENERAL NOTES", [
        "DO NOT SCALE DRAWINGS. FIGURED DIMENSIONS GOVERN.",
        "SCHEDULES GOVERN OVER PLANS WHERE THEY DIFFER; NOTIFY THE ARCHITECT OF CONFLICTS BY PRE-BID RFI.",
        "ALL DIMENSIONS ARE TO FACE OF CMU OR FACE OF STUD UNLESS NOTED.",
        "EXTERIOR WALLS: 8\" CMU, GROUTED SOLID, WITH BRICK VENEER AT OFFICE; SEE A-201 AND SPEC 04 22 00.",
        "INTERIOR PARTITIONS: TYPE P1 3-5/8\" MTL STUD 16\" OC, 5/8\" GWB EACH SIDE TO DECK UNLESS NOTED.",
        "ROOF: MECHANICALLY FASTENED 60-MIL TPO OVER POLYISO (R-30 AVG), TAPERED CRICKETS; 20-YEAR NDL WARRANTY.",
        "SPRINKLER SYSTEM IS DESIGN-BUILD BY THE FIRE PROTECTION SUBCONTRACTOR PER NFPA 13.",
        "SIGNAGE ALLOWANCE $25,000 — SEE SPEC 01 21 00.",
    ], 20, 34)
    o += table(1600, 1000, "ABBREVIATIONS", ["ABBR", "MEANING"], [("CMU", "CONCRETE MASONRY UNIT"), ("GWB", "GYPSUM WALL BOARD"), ("HM", "HOLLOW METAL"),
                                                           ("NIC", "NOT IN CONTRACT"), ("OC", "ON CENTER"), ("TYP", "TYPICAL"), ("VIF", "VERIFY IN FIELD"),
                                                           ("ACT", "ACOUSTICAL CEILING TILE"), ("SOG", "SLAB ON GRADE"), ("AFF", "ABOVE FINISHED FLOOR")], [160, 700])
    o += title_block("G-001", "COVER SHEET, INDEX, CODE SUMMARY", "NONE")
    o.append("</svg>")
    return "\n".join(o)


def floor_plan_base(with_rooms: bool = True, room_font=20) -> list[str]:
    o = []
    o.append(wall_rect(0, 0, BLD_L, BLD_W, 12))                     # exterior CMU
    o.append(line(x(OFFICE_L), y(0), x(OFFICE_L), y(BLD_W), 10))      # office/warehouse demising wall (CMU, rated)
    # office partitions (P1) — columns at x=20, rows at 25, 50, 75, restroom split 87.5
    o.append(line(x(20), y(0), x(20), y(BLD_W), 5))
    for yy in (25, 50, 75):
        o.append(line(x(0), y(yy), x(OFFICE_L), y(yy), 5))
    o.append(line(x(0), y(87.5), x(20), y(87.5), 5))
    if with_rooms:
        for num, name, x0, y0, x1, y1 in ROOMS:
            cx, cy = (x(x0) + x(x1)) / 2, (y(y0) + y(y1)) / 2
            area = int((x1 - x0) * (y1 - y0))
            o.append(text(cx, cy - 14, f"{num} {name}", room_font, "bold", "middle"))
            o.append(text(cx, cy + 16, f"{area:,} SF", room_font - 2, anchor="middle"))
    return o


def sheet_a101() -> str:
    o = svg_open()
    o += grid_bubbles()
    o += floor_plan_base()
    for d in DOORS:
        o += door(*d[:6])
    for mark, xf, yf, w, h in OVERHEAD_DOORS:
        o.append(line(x(xf) - 6, y(yf), x(xf) - 6, y(yf + w), 6, dash="8,6"))
        o.append(text(x(xf) - 60, y(yf + w / 2), f"{mark} 12'x14' OH", 16, "bold", "end"))
    for wdw in WINDOWS:
        o += window(*wdw)
    o += dim_h(0, OFFICE_L, y(-17), "40'-0\"") + dim_h(OFFICE_L, BLD_L, y(-17), "80'-0\"") + dim_h(0, BLD_L, y(-24), "120'-0\"")
    o += dim_v(0, BLD_W, x(-26), "100'-0\"") + dim_v(0, 25, x(-19), "25'-0\"") + dim_v(25, 50, x(-19), "25'-0\"") + dim_v(50, 75, x(-19), "25'-0\"") + dim_v(75, 100, x(-19), "25'-0\"")
    o += table(2140, 1900, "KEYNOTES", ["KEY", "NOTE"], [("1", "8\" CMU EXTERIOR WALL, SEE S-101"), ("2", "PARTITION TYPE P1 TO DECK"),
                                                       ("3", "1-HR RATED CMU DEMISING WALL"), ("4", "ALUM. STOREFRONT ENTRANCE, SEE A-201"),
                                                       ("5", "OVERHEAD SECTIONAL DOOR 12'x14'"), ("6", "CONCRETE STOOP, SEE S-101")], [80, 700], 30, 16)
    o += table(2140, 2170, "LEGEND", ["SYMBOL", "MEANING"], [("HEX TAG", "DOOR MARK — SEE A-601"), ("CIRCLE TAG", "WINDOW MARK — SEE A-601"),
                                                             ("NNN NAME / SF", "ROOM NUMBER, NAME, AREA")], [160, 620], 30, 16)
    o += north_arrow()
    o += title_block("A-101", "FLOOR PLAN", "1/8\" = 1'-0\"")
    o.append("</svg>")
    return "\n".join(o)


def sheet_a201() -> str:
    o = svg_open()
    # four elevations drawn as rectangles with window/door openings; heights: office 14', warehouse 24'
    def elev(px, py, label, length_ft, height_ft, openings):
        L, H = length_ft * U_PER_FT, height_ft * U_PER_FT
        o.append(text(px, py - 20, label, 24, "bold"))
        o.append(f'<rect x="{px}" y="{py}" width="{L:.1f}" height="{H:.1f}" fill="none" stroke="black" stroke-width="4"/>')
        o.append(line(px - 40, py + H, px + L + 40, py + H, 3))
        o.append(text(px + L + 50, py + H + 8, "T.O. SLAB 0'-0\"", 16))
        o.append(text(px + L + 50, py + 8, f"T.O. WALL +{height_ft:.0f}'-0\"", 16))
        for (ox_, oy_, w_, h_, kind) in openings:
            o.append(f'<rect x="{px + ox_*U_PER_FT:.1f}" y="{py + H - (oy_+h_)*U_PER_FT:.1f}" width="{w_*U_PER_FT:.1f}" height="{h_*U_PER_FT:.1f}" '
                     f'fill="none" stroke="black" stroke-width="2"/>')
            o.append(text(px + (ox_ + w_ / 2) * U_PER_FT, py + H - (oy_ + h_) * U_PER_FT - 6, kind, 14, anchor="middle"))
    # NORTH elevation: office 40' (14' high) + warehouse 80' (24' high); windows W1 4' wide x 5' at sill 3'
    elev(300, 300, "NORTH ELEVATION (SCALE 1/8\" = 1'-0\")", 120, 24,
         [(3, 3, 4, 5, "W1"), (16, 3, 4, 5, "W1"), (26, 3, 4, 5, "W1"), (34, 3, 4, 5, "W1"), (10, 0, 6, 7, "101")])
    elev(300, 800, "SOUTH ELEVATION", 120, 24, [(80, 0, 3, 7, "200A")])
    elev(300, 1300, "EAST ELEVATION", 100, 24, [(20, 0, 12, 14, "OH-1"), (85, 0, 12, 14, "OH-2"), (60, 0, 3, 7, "200B")])
    elev(1900, 1300, "WEST ELEVATION", 100, 14, [(6, 3, 4, 5, "W1"), (14, 3, 4, 5, "W1"), (31, 3, 4, 5, "W1"), (39, 3, 4, 5, "W1"), (56, 3, 4, 5, "W1"), (64, 3, 4, 5, "W1")])
    o += notes(1900, 300, "ELEVATION NOTES", [
        "EXTERIOR WALLS: 8\" CMU, GROUTED SOLID; BRICK VENEER ON OFFICE (WEST 100 LF + NORTH 40 LF x 14'-0\").",
        "WAREHOUSE CMU EXPOSED, PAINTED; PARAPET COPING PREFINISHED ALUMINUM 440 LF.",
        "STOREFRONT: CLEAR ANODIZED ALUMINUM, 1\" INSULATED LOW-E GLASS; ENTRANCE 101 PAIR 6'-0\" x 7'-0\".",
        "WINDOWS W1: 4'-0\" x 5'-0\" FIXED ALUMINUM, SILL AT 3'-0\" AFF, QTY 10.",
        "OVERHEAD DOORS OH-1, OH-2: 12'-0\" x 14'-0\" INSULATED SECTIONAL, MOTOR OPERATED.",
        "ROOF: TPO, 1/4\" PER FT SLOPE TO INTERNAL DRAINS (4) WITH OVERFLOWS (4).",
    ], 18, 32)
    o += title_block("A-201", "EXTERIOR ELEVATIONS", "1/8\" = 1'-0\"")
    o.append("</svg>")
    return "\n".join(o)


def sheet_a601() -> str:
    o = svg_open()
    rows = []
    for mark, xf, yf, wall, quad, w, typ in DOORS:
        rated = "90 MIN" if "RATED" in typ else "-"
        hw = {"101": "HW-1 ENTRANCE", "110": "HW-3 RATED/CLOSER", "200A": "HW-4 EXTERIOR", "200B": "HW-4 EXTERIOR"}.get(mark, "HW-2 OFFICE")
        frame = "ALUM" if "STOREFRONT" in typ else "HM"
        size = "PR 3'-0\" x 7'-0\"" if w == 6.0 else "3'-0\" x 7'-0\""
        rows.append((mark, size, typ, frame, rated, hw))
    for mark, xf, yf, w, h in OVERHEAD_DOORS:
        rows.append((mark, "12'-0\" x 14'-0\"", "INSULATED SECTIONAL OH", "STEEL JAMB", "-", "MOTOR OPERATOR"))
    o += table(200, 200, "DOOR SCHEDULE", ["MARK", "SIZE", "TYPE", "FRAME", "RATING", "HARDWARE SET"], rows, [120, 240, 360, 160, 140, 300], 34, 17)
    o += table(1650, 200, "WINDOW SCHEDULE", ["MARK", "SIZE", "TYPE", "GLAZING", "QTY"], [("W1", "4'-0\" x 5'-0\"", "FIXED ALUMINUM", "1\" IGU LOW-E", "10")], [120, 240, 300, 260, 100], 34, 17)
    finish_rows = []
    for num, name, x0, y0, x1, y1 in ROOMS:
        if num == "200":
            finish_rows.append((num, name, "SEALED CONC.", "NONE", "PAINTED CMU", "EXPOSED", "24'-0\""))
        elif num in ("106", "107"):
            finish_rows.append((num, name, "PORC. TILE", "TILE 6\"", "TILE WAINSCOT/PAINT", "GWB PAINTED", "9'-0\""))
        elif num == "101":
            finish_rows.append((num, name, "LVT", "RUBBER 4\"", "PAINT", "ACT 2x2", "10'-0\""))
        else:
            finish_rows.append((num, name, "CARPET TILE", "RUBBER 4\"", "PAINT", "ACT 2x2", "9'-0\""))
    o += table(200, 800, "ROOM FINISH SCHEDULE", ["NO.", "NAME", "FLOOR", "BASE", "WALLS", "CEILING", "CLG HT"], finish_rows, [90, 240, 220, 180, 300, 220, 140], 34, 17)
    o += table(1650, 800, "PARTITION TYPES", ["TYPE", "DESCRIPTION"], [("P1", "3-5/8\" MTL STUD 16\" OC, 5/8\" GWB EA SIDE, TO DECK, BATT INSUL."),
                                                                    ("P2", "P1 WITH 5/8\" TYPE X GWB EA SIDE, 1-HR (RESTROOMS)"),
                                                                    ("CMU-8", "8\" CMU GROUTED SOLID, EXTERIOR / DEMISING")], [120, 900], 34, 16)
    o += table(1650, 1100, "HARDWARE SETS (SEE 08 71 00)", ["SET", "CONTENTS"], [("HW-1", "PAIR: CONTINUOUS HINGES, PANIC EXIT DEVICES, CLOSERS, CYLINDERS, WEATHERSTRIP"),
                                                                                ("HW-2", "SINGLE: 3 HINGES, OFFICE LOCKSET, WALL STOP"),
                                                                                ("HW-3", "SINGLE RATED: 3 HINGES, STOREROOM LOCK, CLOSER, SMOKE SEAL"),
                                                                                ("HW-4", "EXTERIOR: 3 HINGES, STOREROOM LOCK, CLOSER, THRESHOLD, WEATHERSTRIP")], [120, 900], 34, 15)
    o += title_block("A-601", "DOOR, WINDOW & FINISH SCHEDULES", "NONE")
    o.append("</svg>")
    return "\n".join(o)


def sheet_s101() -> str:
    o = svg_open()
    o += grid_bubbles()
    o.append(wall_rect(0, 0, BLD_L, BLD_W, 8))
    o.append(line(x(OFFICE_L), y(0), x(OFFICE_L), y(BLD_W), 6))
    # continuous footing dashed outline (offset 1' each side of the wall) — drawn as dashed rect inside/outside
    o.append(f'<rect x="{x(-1):.1f}" y="{y(-1):.1f}" width="{(BLD_L+2)*U_PER_FT:.1f}" height="{(BLD_W+2)*U_PER_FT:.1f}" fill="none" stroke="black" stroke-width="2" stroke-dasharray="10,8"/>')
    o.append(f'<rect x="{x(1):.1f}" y="{y(1):.1f}" width="{(BLD_L-2)*U_PER_FT:.1f}" height="{(BLD_W-2)*U_PER_FT:.1f}" fill="none" stroke="black" stroke-width="2" stroke-dasharray="10,8"/>')
    for gx, gy in COLUMNS:
        cx, cy = x(GRID_X[gx]), y(GRID_Y[gy])
        s = 4 * U_PER_FT / 2
        o.append(f'<rect x="{cx-s:.1f}" y="{cy-s:.1f}" width="{2*s:.1f}" height="{2*s:.1f}" fill="none" stroke="black" stroke-width="2" stroke-dasharray="6,5" class="footing"/>')
        o.append(f'<rect x="{cx-5:.1f}" y="{cy-5:.1f}" width="10" height="10" fill="black"/>')
        o.append(text(cx + 30, cy - 30, "F1", 16, "bold"))
    o.append(text(x(70), y(50), "6\" SOG, 4000 PSI, #4 @ 18\" OC EW, ON VAPOR BARRIER", 18, anchor="middle"))
    o.append(text(x(20), y(50), "4\" SOG, 4000 PSI, 6x6-W2.9xW2.9 WWM", 16, anchor="middle"))
    o += dim_h(0, OFFICE_L, y(-17), "40'-0\"") + dim_h(OFFICE_L, 80, y(-17), "40'-0\"") + dim_h(80, BLD_L, y(-17), "40'-0\"")
    o += dim_v(0, 50, x(-19), "50'-0\"") + dim_v(50, 100, x(-19), "50'-0\"")
    o += table(2140, 1560, "FOOTING SCHEDULE", ["MARK", "SIZE", "REINF.", "QTY"], [(m, s, r, q if m == "F1" else f"{q} LF") for m, s, r, q in FOOTING_SCHEDULE], [100, 300, 260, 120], 34, 17)
    o += notes(2140, 300, "STRUCTURAL GENERAL NOTES", [
        "CODES: IBC 2021; ASCE 7-22. ROOF LL 20 PSF; WIND 115 MPH EXP C; SEISMIC SDC A.",
        "CONCRETE: f'c = 4,000 PSI AT 28 DAYS ALL FOOTINGS AND SLABS; 3,000 PSI FILL.",
        "REINFORCING: ASTM A615 GR 60. WWM ASTM A1064.",
        "CMU: ASTM C90, f'm = 2,000 PSI, TYPE S MORTAR, GROUT ALL CELLS SOLID; #5 @ 32\" OC VERT.",
        "STRUCTURAL STEEL: W-SHAPES ASTM A992; HSS ASTM A500 GR C; JOISTS SJI K-SERIES; DECK ASTM A653.",
        "BEARING: 3,000 PSF ALLOWABLE PER GEOTECH REPORT (TERRA-TEX 26-1188); FOOTINGS 24\" MIN BELOW GRADE.",
        "SPECIAL INSPECTIONS PER IBC CH. 17: CONCRETE, MASONRY, STEEL BOLTING/WELDING — SEE 01 45 00.",
        "SLAB CONTROL JOINTS AT 12'-0\" OC MAX EACH WAY, SAW CUT 1/4 DEPTH.",
    ], 17, 32)
    o += north_arrow()
    o += title_block("S-101", "FOUNDATION PLAN & GENERAL NOTES", "1/8\" = 1'-0\"")
    o.append("</svg>")
    return "\n".join(o)


def sheet_s201() -> str:
    o = svg_open()
    o += grid_bubbles()
    o.append(wall_rect(0, 0, BLD_L, BLD_W, 8))
    o.append(line(x(OFFICE_L), y(0), x(OFFICE_L), y(BLD_W), 6))
    # warehouse beams along rows 1,2,3 between B-D
    for gy in ("1", "2", "3"):
        py = y(GRID_Y[gy])
        o.append(line(x(40), py, x(120), py, 6))
        o.append(text(x(60), py - 12, "B1 W16x31", 16, "bold", "middle"))
        o.append(text(x(100), py - 12, "B1 W16x31", 16, "bold", "middle"))
    # warehouse joists spanning N-S between rows at 5' oc within B-C and C-D
    for xf in range(45, 120, 5):
        o.append(line(x(xf), y(0), x(xf), y(100), 2))
    o.append(text(x(80), y(25), "24K4 @ 5'-0\" OC (TYP)", 18, "bold", "middle"))
    o.append(text(x(80), y(75), "24K4 @ 5'-0\" OC (TYP)", 18, "bold", "middle"))
    # office joists spanning E-W between A and B at 5' oc
    for yf in range(0, 101, 5):
        o.append(line(x(0), y(yf), x(40), y(yf), 2))
    o.append(text(x(20), y(50) + 30, "18K3 @ 5'-0\" OC", 18, "bold", "middle"))
    for gx, gy in COLUMNS:
        cx, cy = x(GRID_X[gx]), y(GRID_Y[gy])
        o.append(f'<rect x="{cx-8:.1f}" y="{cy-8:.1f}" width="16" height="16" fill="black"/>')
        o.append(text(cx + 20, cy + 30, "C1", 15, "bold"))
    for yf in (0, 25, 50, 75, 100):
        cx, cy = x(40), y(yf)
        o.append(text(cx - 40, cy - 20, "C2", 15, "bold"))
    o += table(2140, 1500, "STEEL SCHEDULE", ["MARK", "SECTION", "LENGTH", "QTY", "PLF"], [(m, s, f"{L:.0f}'-0\"", q, plf) for m, s, L, q, plf in STEEL], [100, 220, 140, 90, 90], 34, 17)
    o += table(2140, 1770, "ROOF DECK", ["AREA", "DECK", "SF"], [(a, d, f"{sf:,}") for a, d, sf in DECK], [200, 320, 120], 34, 17)
    o += notes(2140, 300, "FRAMING NOTES", [
        "ROOF DECK 1-1/2\" TYPE B 22 GA GALVANIZED, 36/4 PATTERN, WELDED; 12,000 SF TOTAL.",
        "JOIST BRIDGING PER SJI; BEARING PLATES AT CMU WALLS.",
        "BEAMS B1 SIMPLE SHEAR CONNECTIONS, 3/4\" A325 BOLTS; CONNECTION DESIGN BY FABRICATOR.",
        "COLUMNS C1 HSS8x8x1/4 x 24'-0\" (9); C2 HSS6x6x1/4 x 14'-0\" (5) AT GRID B.",
        "ROOF SCREENS AND RTU FRAMES: PROVIDE ANGLE FRAMES AT RTU-1 AND RTU-2 CURBS.",
    ], 17, 32)
    o += north_arrow()
    o += title_block("S-201", "ROOF FRAMING PLAN", "1/8\" = 1'-0\"")
    o.append("</svg>")
    return "\n".join(o)


def sheet_m101() -> str:
    o = svg_open()
    o += floor_plan_base(with_rooms=True, room_font=16)
    # RTUs on roof shown dashed over office, diffusers as squares with X
    for tag, cx_ft, cy_ft in (("RTU-1", 30, 37), ("RTU-2", 10, 37)):
        o.append(f'<rect x="{x(cx_ft)-45:.1f}" y="{y(cy_ft)-30:.1f}" width="90" height="60" fill="none" stroke="black" stroke-width="3" stroke-dasharray="8,6"/>')
        o.append(text(x(cx_ft), y(cy_ft) + 6, tag, 16, "bold", "middle"))
    k = 0
    for num, name, x0, y0, x1, y1 in ROOMS:
        if num == "200":
            continue
        n = 2 if (x1 - x0) * (y1 - y0) >= 500 else 1
        for i in range(n):
            if k >= DIFFUSERS:
                break
            cx, cy = x(x0 + (x1 - x0) * (i + 1) / (n + 1)), y(y0 + 6)
            o.append(f'<rect x="{cx-14:.1f}" y="{cy-14:.1f}" width="28" height="28" fill="none" stroke="black" stroke-width="2" class="diffuser"/>')
            o.append(line(cx - 14, cy - 14, cx + 14, cy + 14, 1))
            o.append(line(cx + 14, cy - 14, cx - 14, cy + 14, 1))
            k += 1
    # duct mains: simple double lines from RTUs
    o.append(line(x(10), y(37), x(10), y(90), 4, dash="20,8"))
    o.append(line(x(30), y(37), x(30), y(90), 4, dash="20,8"))
    o.append(text(x(10) + 10, y(60), "24x12 SUPPLY", 14))
    o.append(text(x(30) + 10, y(60), "24x12 SUPPLY", 14))
    for tag, cx_ft, cy_ft in (("UH-1", 60, 10), ("UH-2", 100, 90)):
        o.append(f'<circle cx="{x(cx_ft):.1f}" cy="{y(cy_ft):.1f}" r="26" fill="none" stroke="black" stroke-width="3"/>')
        o.append(text(x(cx_ft), y(cy_ft) + 6, tag, 14, "bold", "middle"))
    for tag, cx_ft, cy_ft in (("EF-1", 10, 81), ("EF-2", 10, 94)):
        o.append(f'<circle cx="{x(cx_ft):.1f}" cy="{y(cy_ft):.1f}" r="16" fill="none" stroke="black" stroke-width="2"/>')
        o.append(text(x(cx_ft) + 22, y(cy_ft) + 5, tag, 13, "bold"))
    o += table(2140, 300, "HVAC EQUIPMENT SCHEDULE", ["TAG", "TYPE", "CAPACITY", "ELECTRICAL", "LOCATION"], HVAC_EQUIP, [90, 300, 240, 140, 200], 34, 15)
    o += notes(2140, 700, "MECHANICAL NOTES", [
        f"SUPPLY DIFFUSERS: 24x24 LAY-IN, QTY {DIFFUSERS}; RETURN GRILLES 24x24 QTY 6 (NOT SHOWN).",
        "DUCTWORK: GALVANIZED, SMACNA 2\" WG; LINED 10' FROM RTUs; APPROX. 640 LF TRUNK/BRANCH.",
        "GAS PIPING TO UH-1, UH-2 AND WH-1 BY PLUMBING CONTRACTOR; SEE P-101.",
        "CONTROLS: PROGRAMMABLE THERMOSTATS; NO BMS. TAB PER 23 05 93.",
        "ROOF CURBS 14\" BY MECHANICAL CONTRACTOR; STRUCTURAL FRAMES BY STEEL FABRICATOR (S-201).",
    ], 16, 30)
    o += north_arrow()
    o += title_block("M-101", "HVAC PLAN & SCHEDULES", "1/8\" = 1'-0\"")
    o.append("</svg>")
    return "\n".join(o)


def sheet_p101() -> str:
    o = svg_open()
    o += floor_plan_base(with_rooms=True, room_font=16)
    # fixtures in restrooms as small symbols with tags
    fx = [("WC-1", 4, 78), ("WC-1", 9, 78), ("WC-1", 4, 91), ("WC-1", 9, 91), ("UR-1", 14, 78), ("LAV-1", 16, 84), ("LAV-1", 18, 84),
          ("LAV-1", 16, 97), ("LAV-1", 18, 97), ("SK-1", 4, 55), ("MS-1", 36, 96), ("EWC-1", 21, 50), ("WH-1", 36, 90)]
    for tag, xf, yf in fx:
        o.append(f'<rect x="{x(xf)-12:.1f}" y="{y(yf)-12:.1f}" width="24" height="24" fill="none" stroke="black" stroke-width="2"/>')
        o.append(text(x(xf) + 16, y(yf) + 5, tag, 12, "bold"))
    for i, (xf, yf) in enumerate(((0, 40), (60, 100), (120, 40), (60, 0))):
        o.append(text(x(xf) + (10 if xf == 0 else -10), y(yf) + (14 if yf == 100 else -8), "HB-1", 12, "bold", "start" if xf == 0 else "end"))
    o.append(line(x(20), y(0), x(20), y(100), 3, dash="6,6"))
    o.append(text(x(20) + 8, y(40), "2\" CW MAIN", 13))
    o.append(line(x(0), y(-6), x(120), y(-6), 3, dash="12,6"))
    o.append(text(x(60), y(-12), "4\" SANITARY TO 5' OUTSIDE BLDG (SITE UTILITIES BY CIVIL)", 14, anchor="middle"))
    o += table(2140, 300, "PLUMBING FIXTURE SCHEDULE", ["TAG", "DESCRIPTION", "QTY"], PLUMBING_FIXTURES, [90, 520, 80], 34, 15)
    o += table(2140, 720, "FIRE PROTECTION BASIS (DESIGN-BUILD)", ["AREA", "HAZARD", "SF/HEAD", "HEADS"], [
        ("OFFICE 4,000 SF", "LIGHT", "200", str(SPRINKLER["office_sf"] // SPRINKLER["office_sf_per_head"])),
        ("WAREHOUSE 8,000 SF", "ORDINARY GRP 2", "130", str(-(-SPRINKLER["warehouse_sf"] // SPRINKLER["warehouse_sf_per_head"]))),
    ], [260, 200, 120, 100], 34, 15)
    o += notes(2140, 900, "PLUMBING NOTES", [
        "DOMESTIC WATER: 2\" SERVICE WITH RPZ BACKFLOW; COPPER TYPE L ABOVE GRADE, PEX-A PERMITTED IN WALLS.",
        "SANITARY: PVC SCH 40 UNDERGROUND, CAST IRON ABOVE GRADE; APPROX. 420 LF TOTAL.",
        "GAS: 1-1/2\" TO UH-1/UH-2 AND 3/4\" TO WH-1; METER BY UTILITY.",
        "ROOF DRAINS (4) AND OVERFLOWS (4) WITH 6\" LEADERS TO STORM; SEE CIVIL FOR SITE STORM.",
        "SPRINKLER: WET PIPE, 6\" RISER, FDC AT NORTH WALL; FLOW TEST 09/2026 TO BE PROVIDED BY OWNER.",
    ], 16, 30)
    o += north_arrow()
    o += title_block("P-101", "PLUMBING PLAN & FIXTURE SCHEDULE", "1/8\" = 1'-0\"")
    o.append("</svg>")
    return "\n".join(o)


def sheet_e101() -> str:
    o = svg_open()
    o += floor_plan_base(with_rooms=True, room_font=15)
    # lighting: troffers in office (40), high bays in warehouse (24) as small symbols
    n = 0
    for num, name, x0, y0, x1, y1 in ROOMS:
        if num == "200":
            for i in range(6):
                for j in range(4):
                    cx, cy = x(40 + 80 * (i + 0.5) / 6), y(100 * (j + 0.5) / 4)
                    o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="10" fill="none" stroke="black" stroke-width="2" class="highbay"/>')
            continue
        cnt = 6 if (x1 - x0) * (y1 - y0) >= 500 else 2
        for i in range(cnt):
            cols = 2
            rows = cnt // cols
            r_, c_ = divmod(i, cols)
            cx = x(x0 + (x1 - x0) * (c_ + 0.5) / cols)
            cy = y(y0 + (y1 - y0) * (r_ + 0.5) / rows)
            o.append(f'<rect x="{cx-16:.1f}" y="{cy-8:.1f}" width="32" height="16" fill="none" stroke="black" stroke-width="2" class="troffer"/>')
            n += 1
    # receptacles as small triangles along walls (48)
    k = 0
    for num, name, x0, y0, x1, y1 in ROOMS:
        per = 4 if num != "200" else 12
        for i in range(per):
            if k >= ELECTRICAL["receptacles"]:
                break
            cx = x(x0 + (x1 - x0) * (i + 0.5) / per)
            cy = y(y1) - 10
            o.append(f'<polygon points="{cx-7:.1f},{cy:.1f} {cx+7:.1f},{cy:.1f} {cx:.1f},{cy-12:.1f}" fill="black" class="receptacle"/>')
            k += 1
    o.append(text(x(60), y(-20), "ELECTRICAL ROOM 109: MDP, T-1, LP-1, HP-1; SERVICE 400A 480Y/277V FROM PAD-MOUNT XFMR (UTILITY)", 14, anchor="middle"))
    o += table(2140, 300, "ONE-LINE (TABULAR) / GEAR SCHEDULE", ["TAG", "DESCRIPTION"], ELECTRICAL["gear"], [90, 620], 34, 15)
    o += table(2140, 520, "LIGHTING FIXTURE SCHEDULE", ["TYPE", "DESCRIPTION", "QTY"], [(t, d, q) for t, d, q in ELECTRICAL["fixtures"]], [80, 500, 80], 34, 15)
    o += table(2140, 760, "PANEL LP-1 (208Y/120V, 42 CKT) — SUMMARY", ["CKT", "LOAD", "BKR"], [
        ("1-9", "OFFICE RECEPTACLES (28)", "20A/1P"), ("11-15", "WAREHOUSE RECEPTACLES (12)", "20A/1P"),
        ("17-19", "RESTROOM/BREAK RECEPTACLES (8)", "20A/1P"), ("21", "WH-1", "30A/2P"), ("23-25", "EF-1, EF-2, UH-1, UH-2", "20A/1P"),
        ("27-29", "FACP, IT RACK", "20A/1P"), ("SPARE", "12 SPARES", "-")], [90, 400, 110], 32, 14)
    o += table(2140, 1060, "PANEL HP-1 (480Y/277V, 30 CKT) — SUMMARY", ["CKT", "LOAD", "BKR"], [
        ("1-3", "RTU-1 (35 FLA)", "50A/3P"), ("5-7", "RTU-2 (35 FLA)", "50A/3P"), ("9-11", "OFFICE LIGHTING (40 x A)", "20A/1P"),
        ("13-15", "WAREHOUSE LIGHTING (24 x B)", "20A/1P"), ("17", "EXTERIOR LIGHTING (8 x C)", "20A/1P"), ("19", "T-1 45 KVA", "70A/3P")], [90, 400, 110], 32, 14)
    o += table(2140, 1340, "FIRE ALARM DEVICES", ["DEVICE", "QTY"], [(d, q) for d, q in ELECTRICAL["fire_alarm"]], [300, 100], 32, 14)
    o += notes(2140, 1560, "ELECTRICAL NOTES", [
        "SERVICE: 400A, 480Y/277V, 3PH, 4W; UTILITY PAD-MOUNT TRANSFORMER AND PRIMARY BY ONCOR (NIC).",
        f"RECEPTACLES: {ELECTRICAL['receptacles']} DUPLEX 20A; DATA OUTLETS: {ELECTRICAL['data_outlets']} (RACEWAY AND BOXES ONLY; CABLING BY OWNER).",
        "BRANCH CIRCUITS 3/4\" EMT WITH THHN; FEEDERS PER ONE-LINE; APPROX. 3,400 LF CONDUIT.",
        "LIGHTING CONTROLS: OCCUPANCY SENSORS IN ALL OFFICES; PHOTOCELL/TIMECLOCK FOR EXTERIOR.",
        "FIRE ALARM: ADDRESSABLE, MONITORED; SPRINKLER FLOW/TAMPER SUPERVISION.",
    ], 15, 28)
    o += north_arrow()
    o += title_block("E-101", "POWER & LIGHTING PLAN, ONE-LINE, PANEL SCHEDULES", "1/8\" = 1'-0\"")
    o.append("</svg>")
    return "\n".join(o)


SHEETS = [("G-001", sheet_g001), ("A-101", sheet_a101), ("A-201", sheet_a201), ("A-601", sheet_a601), ("S-101", sheet_s101),
          ("S-201", sheet_s201), ("M-101", sheet_m101), ("P-101", sheet_p101), ("E-101", sheet_e101)]


# ----------------------------------------------------------------------------- project manual
def project_manual_html() -> str:
    sec = []
    def s(num, title, paras):
        body = "".join(f"<p>{p}</p>" for p in paras)
        sec.append(f'<div class="section"><h2>SECTION {num} — {title}</h2>{body}</div>')
    s("00 11 13", "ADVERTISEMENT FOR BIDS", ["Blackland Commercial Builders (synthetic demo) invites sealed bids for the Prairie Creek Office/Warehouse — Building 2, a 12,000 SF single-story office/warehouse in Plano, Texas.",
                                           "Bids are due 09/26/2026 at 2:00 PM local time. A pre-bid site visit is scheduled for 09/16/2026 at 10:00 AM."])
    s("00 21 13", "INSTRUCTIONS TO BIDDERS", ["Pre-bid requests for information (RFI) must be received in writing by 09/19/2026 at 5:00 PM; answers are issued by addendum to all bidders.",
                                            "A bid bond of 5% of the base bid is required. Performance and payment bonds of 100% are required on award. Bids are valid for 60 days.",
                                            "Contract form: AIA A101-2017 with A201-2017 General Conditions as amended by the Supplementary Conditions. Drawings and specifications are complementary; specifications govern in a direct conflict."])
    s("00 41 00", "BID FORM", ["Base Bid: the complete work shown and specified, lump sum. Contract duration: 240 calendar days from Notice to Proceed. Liquidated damages: $750 per calendar day.",
                             "Alternate No. 1 (ADD): epoxy floor coating in Warehouse 200 in lieu of sealed concrete. Alternate No. 2 (DEDUCT): delete brick veneer at office, paint CMU.",
                             "Unit Price No. 1: rock excavation, per cubic yard. Unit Price No. 2: select fill import, per cubic yard in place.",
                             "Acknowledge Addendum No. 1 dated 09/19/2026."])
    s("01 10 00", "SUMMARY", ["The Work includes a 12,000 SF single-story building: 4,000 SF office with brick veneer on CMU, 8,000 SF warehouse with exposed painted CMU, steel joist and deck roof, TPO roofing, storefront entrance, complete MEP and fire sprinkler systems, and site work per the civil drawings (civil drawings are not included in this bid set; site work is by a separate contract).",
                              "Owner-furnished, contractor-installed: none. Not in contract: low-voltage cabling, furniture, warehouse racking, utility company charges."])
    s("01 21 00", "ALLOWANCES", ["Include a cash allowance of $25,000 for exterior and interior signage. Include a contingency allowance of $15,000 for unforeseen conditions, to be used only with the Owner's written authorization."])
    s("01 22 00", "UNIT PRICES", ["Unit Price No. 1: rock excavation, removal and disposal, per CY of bank measure. Unit Price No. 2: imported select fill, placed and compacted, per CY in place."])
    s("01 23 00", "ALTERNATES", ["Alternate No. 1 (ADD): 100% solids epoxy floor coating, 20 mils, in Warehouse 200 (8,000 SF). Alternate No. 2 (DEDUCT): delete modular brick veneer at office walls (west 100 LF and north 40 LF, 14 feet high); paint exposed CMU."])
    s("01 45 00", "QUALITY CONTROL", ["Special inspections per IBC Chapter 17 for concrete, masonry and structural steel are paid by the Owner; the Contractor coordinates and provides access. Concrete testing: one set of cylinders per 100 CY or fraction per day."])
    s("01 50 00", "TEMPORARY FACILITIES AND CONTROLS", ["Provide a 12x40 job trailer, temporary power and water (utility charges by Contractor), temporary chain-link fence around the site, two portable toilets, dumpsters, and a weekly cleaning. Provide a 6-foot construction fence for the duration."])
    s("03 30 00", "CAST-IN-PLACE CONCRETE", ["Concrete f'c 4,000 psi at 28 days for all footings and slabs; 3,000 psi for fill. Air-entrained exterior flatwork. Reinforcing ASTM A615 Grade 60. Slab on grade: 4 inches in office on 10-mil vapor barrier with 6x6-W2.9xW2.9 WWM; 6 inches in warehouse with #4 at 18 inches each way. Finish: steel trowel; sealed concrete in the warehouse (base bid)."])
    s("04 22 00", "CONCRETE UNIT MASONRY", ["8-inch CMU ASTM C90, f'm 2,000 psi, Type S mortar, all cells grouted solid, #5 at 32 inches vertical, horizontal joint reinforcing at 16 inches. Modular brick veneer ASTM C216 Grade SW at the office with 1-inch air space, ties at 16 inches each way, and flashing/weeps."])
    s("05 12 00", "STRUCTURAL STEEL FRAMING", ["W-shapes ASTM A992; HSS ASTM A500 Grade C; bolts ASTM A325 3/4 inch; shop primer. Connection design by the fabricator under a Texas PE seal. Steel joists SJI K-series with standard bridging; roof deck 1-1/2 inch Type B 22 gauge galvanized."])
    s("07 54 00", "THERMOPLASTIC MEMBRANE ROOFING", ["60-mil TPO mechanically fastened over polyisocyanurate insulation, R-30 average, with tapered crickets and 1/2-inch cover board; 20-year NDL manufacturer's warranty. Prefinished aluminum coping 440 LF; four roof drains and four overflow drains."])
    s("08 11 13", "HOLLOW METAL DOORS AND FRAMES", ["16-gauge hollow metal frames, 18-gauge doors, factory primed; 90-minute rated assembly at Door 110. Exterior doors insulated with thermal break frames."])
    s("08 41 13", "ALUMINUM-FRAMED ENTRANCES AND STOREFRONTS", ["Clear anodized aluminum storefront, 1-inch insulated low-E glazing; entrance 101 pair 6'-0\" x 7'-0\" with panic hardware and closers. Windows W1 4'-0\" x 5'-0\" fixed, quantity 10."])
    s("08 71 00", "DOOR HARDWARE", ["Hardware sets HW-1 through HW-4 per the schedule on A-601. Grade 1 locksets, Grade 1 closers, continuous hinges at the entrance pair, cylinders keyed to the Owner's system."])
    s("09 29 00", "GYPSUM BOARD", ["5/8-inch Type X gypsum board on 3-5/8-inch 20-gauge metal studs at 16 inches on center; Level 4 finish in offices, Level 5 at the lobby feature wall; moisture-resistant board in restrooms; batt insulation in all partitions."])
    s("09 51 13", "ACOUSTICAL PANEL CEILINGS", ["2x2 lay-in acoustical panels in a 15/16-inch grid, NRC 0.70, in all office rooms except restrooms (painted gypsum ceilings) and the warehouse (exposed)."])
    s("09 65 00", "RESILIENT AND CARPET FLOORING", ["Luxury vinyl tile in the lobby; carpet tile in offices, conference and break room; porcelain tile in restrooms with 6-inch tile base; 4-inch rubber base elsewhere."])
    s("09 91 23", "INTERIOR PAINTING", ["Two finish coats over primer on all gypsum board; block filler plus two coats on exposed CMU in the warehouse; epoxy paint in restrooms."])
    s("21 13 13", "WET-PIPE SPRINKLER SYSTEMS", ["Design-build wet-pipe system per NFPA 13: light hazard in the office and Ordinary Hazard Group 2 in the warehouse; 6-inch riser, FDC, backflow preventer; flow test data provided by the Owner. Fire pump is not anticipated; confirm with the flow test."])
    s("22 40 00", "PLUMBING FIXTURES", ["Fixtures per the schedule on P-101; water closets 1.28 gpf floor mounted, urinal 0.125 gpf, wall-hung lavatories with sensor faucets, bi-level electric water cooler, 40-gallon electric water heater, mop sink, four hose bibbs."])
    s("23 74 13", "PACKAGED ROOFTOP AIR-CONDITIONING UNITS", ["Two 7.5-ton packaged rooftop units with gas heat, economizers and programmable thermostats on 14-inch curbs; two 150 MBH gas unit heaters in the warehouse; two ceiling exhaust fans; galvanized ductwork per SMACNA; testing, adjusting and balancing per 23 05 93."])
    s("26 24 16", "PANELBOARDS", ["400A main distribution panel 480Y/277V; 45 kVA transformer; 42-circuit 208Y/120V panelboard and 30-circuit 480Y/277V panelboard, copper bus, bolt-on breakers. Utility service by Oncor is not in contract."])
    s("26 51 00", "INTERIOR LIGHTING", ["LED fixtures per the schedule on E-101 (40 troffers, 24 high bays, 8 wall packs, 6 exit signs) with occupancy sensors in offices and photocell/timeclock control for exterior lighting; 10-year fixture warranty."])
    s("28 31 00", "FIRE DETECTION AND ALARM", ["Addressable fire alarm control panel, four pull stations, ten horn/strobes, six smoke detectors, sprinkler flow and tamper supervision, monitored by a UL-listed central station."])
    s("31 23 00", "EXCAVATION AND FILL", ["Building pad excavation and backfill to the geotechnical report Terra-Tex 26-1188; 3,000 psf bearing; footings 24 inches minimum below finished grade; rock excavation paid under Unit Price No. 1. Site grading, paving and utilities beyond 5 feet of the building are by a separate contract."])
    toc = "".join(f"<li>{t.split(' — ')[0].replace('SECTION ', '')} — {t.split(' — ')[1]}</li>" for t in [x_.split('<h2>')[1].split('</h2>')[0] for x_ in sec])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
    @page {{ size: 8.5in 11in; margin: 0.8in; }} body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11pt; }}
    h1 {{ font-size: 20pt; }} h2 {{ font-size: 13pt; margin-top: 18pt; page-break-before: always; }} .section p {{ margin: 6pt 0; }} .toc h2 {{ page-break-before: auto; }}
    </style></head><body>
    <h1>PROJECT MANUAL — {PROJECT}</h1><p>{CLIENT}. Issued for bid {DATE}. SYNTHETIC DEMO DATA — not a real project.</p>
    <div class="toc"><h2>TABLE OF CONTENTS</h2><ul>{toc}</ul></div>
    {''.join(sec)}
    </body></html>"""


# ----------------------------------------------------------------------------- ground truth
def ground_truth() -> dict:
    rooms = [{"number": n, "name": nm, "area_sf": int((x1 - x0) * (y1 - y0))} for n, nm, x0, y0, x1, y1 in ROOMS]
    steel_lb = {m: q * L * plf for m, s, L, q, plf in STEEL}
    return {
        "project": PROJECT, "gross_sf": 12000, "office_sf": 4000, "warehouse_sf": 8000, "stories": 1,
        "scale": "1/8\" = 1'-0\"", "sheet_size_in": [36, 24],
        "sheets": [s for s, _ in SHEETS],
        "rooms": rooms,
        "door_marks": [d[0] for d in DOORS], "door_count": len(DOORS), "door_leaves": sum(2 if d[5] == 6.0 else 1 for d in DOORS),
        "overhead_doors": [o[0] for o in OVERHEAD_DOORS], "window_count": len(WINDOWS), "window_marks": ["W1"],
        "exterior_wall_lf": 2 * (BLD_L + BLD_W), "demising_wall_lf": BLD_W,
        "interior_partition_lf": 100 + 3 * 40 + 20,  # x=20 line (100) + three 40' rows + restroom split 20'
        "footings": {"F1_count": 9, "F1_cy_each": round(4 * 4 * 1.5 / 27, 3), "F2_lf": 440, "F2_cy": round(440 * 2 * 1 / 27, 1)},
        "slabs": [{"area": a, "thickness_in": t, "sf": sf, "cy": round(sf * t / 12 / 27, 1)} for a, t, sf in SLABS],
        "steel": [{"mark": m, "section": s, "length_ft": L, "qty": q, "plf": plf, "total_lb": q * L * plf} for m, s, L, q, plf in STEEL],
        "steel_total_tons": round(sum(steel_lb.values()) / 2000, 2),
        "deck_sf": sum(sf for _, _, sf in DECK),
        "hvac_equipment": [e[0] for e in HVAC_EQUIP], "diffusers": DIFFUSERS,
        "plumbing_fixtures": {t: q for t, _, q in PLUMBING_FIXTURES},
        "sprinkler_heads": SPRINKLER["office_sf"] // SPRINKLER["office_sf_per_head"] + -(-SPRINKLER["warehouse_sf"] // SPRINKLER["warehouse_sf_per_head"]),
        "electrical": {"service": ELECTRICAL["service"], "fixtures": {t: q for t, _, q in ELECTRICAL["fixtures"]},
                       "receptacles": ELECTRICAL["receptacles"], "data_outlets": ELECTRICAL["data_outlets"],
                       "fire_alarm": {d: q for d, q in ELECTRICAL["fire_alarm"]}},
        "spec": {"bid_due": "09/26/2026", "rfi_cutoff": "09/19/2026", "duration_days": 240, "bid_bond_pct": 5, "ld_per_day": 750,
                 "allowances": {"signage": 25000, "contingency": 15000}, "alternates": 2, "unit_prices": 2, "addenda": ["Addendum No. 1 dated 09/19/2026"]},
    }


# ----------------------------------------------------------------------------- main
def find_chrome() -> str | None:
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
        w = shutil.which(c)
        if w:
            return w
    return None


def html_to_pdf(chrome: str, html_path: Path, pdf_path: Path) -> None:
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}",
                    "--virtual-time-budget=3000", f"file://{html_path.resolve()}"], check=True, capture_output=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="docs/tests/fixtures/sample-set-prairie-creek")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    chrome = find_chrome()
    if not chrome:
        print("Chrome/Chromium not found — cannot render PDFs (the committed PDFs remain valid).", file=sys.stderr)
        return 2
    (out / "svg").mkdir(exist_ok=True)
    for sheet, fn in SHEETS:
        svg = fn()
        html = f'<!doctype html><html><head><style>@page{{size:36in 24in;margin:0}} html,body{{margin:0;padding:0}} svg{{display:block}}</style></head><body>{svg}</body></html>'
        hp = out / "svg" / f"{sheet}.html"
        hp.write_text(html, encoding="utf-8")
        (out / "svg" / f"{sheet}.svg").write_text(svg, encoding="utf-8")
        html_to_pdf(chrome, hp, out / f"{sheet}.pdf")
        hp.unlink()
        print("rendered", sheet)
    mp = out / "svg" / "project-manual.html"
    mp.write_text(project_manual_html(), encoding="utf-8")
    html_to_pdf(chrome, mp, out / "Project-Manual.pdf")
    mp.unlink()
    print("rendered Project-Manual")
    (out / "ground_truth.json").write_text(json.dumps(ground_truth(), indent=2), encoding="utf-8")
    (out / "package.json").write_text(json.dumps({
        "name": "Prairie Creek Office/Warehouse — Building 2 (synthetic)", "client": CLIENT, "issued": DATE,
        "drawings": [f"{s}.pdf" for s, _ in SHEETS], "specifications": ["Project-Manual.pdf"], "ground_truth": "ground_truth.json"}, indent=2), encoding="utf-8")
    print("ground truth + package manifest written to", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
