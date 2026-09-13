"""Rendering for the vision readers: overview, overlapping tiles, on-demand zoom, numbered markers.

pypdfium2 renders
Pillow crops and draws. Tiles are cut in the same top-left PDF-point frame the
extractors use, so a vector candidate and a vision confirmation share coordinates.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from core.estimating.pdfio import PT_PER_IN

BBox = tuple[float, float, float, float]


@dataclass
class TileInfo:
    path: str
    col: int
    row: int
    bbox_pt: list[float]   # x0, top, x1, bottom in PDF points
    px_w: int
    px_h: int
    dpi: int


def _page_image(pdf_path: Path, page_index: int, dpi: int):
    import pypdfium2 as pdfium  # lazy

    pdf = pdfium.PdfDocument(str(pdf_path))
    try:
        page = pdf[page_index]
        img = page.render(scale=dpi / PT_PER_IN).to_pil()
    finally:
        pdf.close()
    return img


def render_overview(pdf_path: Path, page_index: int, out_dir: Path, long_edge_px: int = 1600) -> Path:
    import pypdfium2 as pdfium

    pdf = pdfium.PdfDocument(str(pdf_path))
    try:
        page = pdf[page_index]
        w_pt, h_pt = page.get_size()
    finally:
        pdf.close()
    dpi = max(20, int(long_edge_px / (max(w_pt, h_pt) / PT_PER_IN)))
    img = _page_image(pdf_path, page_index, dpi)
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{pdf_path.stem}-p{page_index + 1}-overview.png"
    img.save(out)
    return out


def render_tiles(pdf_path: Path, page_index: int, out_dir: Path, dpi: int = 200, cols: int = 3, rows: int = 2,
                 overlap: float = 0.2) -> list[TileInfo]:
    img = _page_image(pdf_path, page_index, dpi)
    W, H = img.size
    px_per_pt = dpi / PT_PER_IN
    tw, th = W / cols, H / rows
    ox, oy = int(tw * overlap / 2), int(th * overlap / 2)
    out_dir.mkdir(parents=True, exist_ok=True)
    tiles: list[TileInfo] = []
    for r in range(rows):
        for c in range(cols):
            x0 = max(0, int(c * tw) - ox)
            y0 = max(0, int(r * th) - oy)
            x1 = min(W, int((c + 1) * tw) + ox)
            y1 = min(H, int((r + 1) * th) + oy)
            crop = img.crop((x0, y0, x1, y1))
            p = out_dir / f"{pdf_path.stem}-p{page_index + 1}-tile-r{r}c{c}.png"
            crop.save(p)
            tiles.append(TileInfo(path=str(p), col=c, row=r, bbox_pt=[x0 / px_per_pt, y0 / px_per_pt, x1 / px_per_pt, y1 / px_per_pt],
                                  px_w=x1 - x0, px_h=y1 - y0, dpi=dpi))
    (out_dir / f"{pdf_path.stem}-p{page_index + 1}-tiles.json").write_text(json.dumps([asdict(t) for t in tiles], indent=2), encoding="utf-8")
    return tiles


def render_zoom(pdf_path: Path, page_index: int, bbox_pt: BBox, out_dir: Path, dpi: int = 300, pad_pt: float = 24.0, name: str | None = None) -> Path:
    img = _page_image(pdf_path, page_index, dpi)
    k = dpi / PT_PER_IN
    x0, top, x1, bottom = bbox_pt
    box = (max(0, int((x0 - pad_pt) * k)), max(0, int((top - pad_pt) * k)), min(img.width, int((x1 + pad_pt) * k)), min(img.height, int((bottom + pad_pt) * k)))
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / (name or f"{pdf_path.stem}-p{page_index + 1}-zoom-{int(x0)}-{int(top)}.png")
    img.crop(box).save(out)
    return out


def overlay_markers(png_path: Path, markers: list[tuple[float, float, str]], bbox_pt: BBox, dpi: int, out_path: Path,
                    box_pt: float = 14.0) -> Path:
    """Draw numbered boxes (Set-of-Mark) at PDF-point positions onto a rendered tile/overview.

    markers: (x_pt, top_pt, label). bbox_pt: the PDF-point bbox the image covers (tile or full page).
    """
    from PIL import Image, ImageDraw

    img = Image.open(png_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    k = dpi / PT_PER_IN
    x_off, y_off = bbox_pt[0], bbox_pt[1]
    for x_pt, top_pt, label in markers:
        if not (bbox_pt[0] <= x_pt <= bbox_pt[2] and bbox_pt[1] <= top_pt <= bbox_pt[3]):
            continue
        cx, cy = (x_pt - x_off) * k, (top_pt - y_off) * k
        s = box_pt * k
        draw.rectangle([cx - s, cy - s, cx + s, cy + s], outline=(220, 30, 30), width=max(2, int(k * 0.8)))
        tw = 7 * len(label) * max(1, k / 2)
        draw.rectangle([cx + s, cy - s - 14 * k / 2, cx + s + tw + 6, cy - s], fill=(220, 30, 30))
        draw.text((cx + s + 3, cy - s - 14 * k / 2 + 1), label, fill=(255, 255, 255))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    return out_path
