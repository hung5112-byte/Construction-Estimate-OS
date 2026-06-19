"""Live, READ-ONLY web dashboard that visualizes 00-Dashboard.md on localhost.

This server NEVER writes to the vault. It opens 00-Dashboard.md in read mode on
every request, renders it as a styled visual dashboard, and auto-refreshes the page
when the file's modification time changes (e.g. after agent_dashboard.py regenerates
it). Information-only — no control mutates any file.

Design system (via ui-ux-pro-max): "Data-Dense Dashboard" style, "Real-Time /
Operations" pattern, Analytics palette (#1E40AF data + #D97706 amber accent,
full light/dark), Fira Code/Fira Sans typography with tabular numerals, token
usage as a sorted AAA bar chart with always-visible value labels.

Usage:
    python docs/scripts/dashboard_server.py                       # vault = repo root, port 8787
    python docs/scripts/dashboard_server.py --port 9000 --poll 5
    python docs/scripts/dashboard_server.py --vault "C:/path/to/vault"
    python docs/scripts/dashboard_server.py --file  "C:/path/to/00-Dashboard.md"

Open the printed URL (default http://127.0.0.1:8787/). Stop with Ctrl+C.
Dependencies: Python 3.11+ standard library only. Fonts load from Google Fonts
when online and fall back to system fonts (font-display: swap) when offline.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# --------------------------------------------------------------------------- #
# Inline SVG icon set (Lucide-style, stroke=currentColor) — no emoji as icons   #
# --------------------------------------------------------------------------- #

ICONS = {
    "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "refresh": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/>'
    '<path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M3 21v-5h5"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>'
    '<path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/>'
    '<rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/>',
    "clipboard": '<rect x="8" y="2" width="8" height="4" rx="1"/>'
    '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>'
    '<path d="M9 12h6"/><path d="M9 16h6"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "dollar": '<line x1="12" y1="2" x2="12" y2="22"/>'
    '<path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    "barchart": '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/>'
    '<line x1="6" y1="20" x2="6" y2="16"/>',
    "alert": '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>'
    '<line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    "workflow": '<rect x="3" y="3" width="8" height="8" rx="2"/><path d="M7 11v4a2 2 0 0 0 2 2h4"/>'
    '<rect x="13" y="13" width="8" height="8" rx="2"/>',
    "cpu": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/>'
    '<path d="M9 2v2"/><path d="M15 2v2"/><path d="M9 20v2"/><path d="M15 20v2"/>'
    '<path d="M2 9h2"/><path d="M2 15h2"/><path d="M20 9h2"/><path d="M20 15h2"/>',
}


def icon(name: str, cls: str = "ic", size: int = 18) -> str:
    inner = ICONS.get(name, ICONS["activity"])
    return (
        f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true">{inner}</svg>'
    )


def heading_icon(text: str) -> tuple[str, str]:
    """Pick an icon by heading keyword and strip a leading emoji/symbol run."""
    low = text.lower()
    name = "activity"
    if "needs action" in low:
        name = "alert"
    elif "pipeline" in low:
        name = "workflow"
    elif "token" in low:
        name = "barchart"
    elif "agent" in low:
        name = "cpu"
    clean = re.sub(r"^[^\w(]+", "", text).strip() or text
    return name, clean


# --------------------------------------------------------------------------- #
# Markdown -> HTML (minimal GFM subset: enough to faithfully render the file)  #
# --------------------------------------------------------------------------- #

_WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_CODE = re.compile(r"`([^`]+)`")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _wikilink_repl(m: re.Match) -> str:
    inner = m.group(1).replace("\\|", "|")
    if "|" in inner:
        return inner.split("|")[-1].strip()
    seg = inner.split("/")[-1]
    return seg[:-3].strip() if seg.endswith(".md") else seg.strip()


def clean_inline(text: str) -> str:
    text = html.escape(text)
    text = _WIKILINK.sub(_wikilink_repl, text)
    text = _LINK.sub(lambda m: m.group(1), text)
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _CODE.sub(r"<code>\1</code>", text)
    return text


def _is_table_sep(line: str) -> bool:
    return bool(re.match(r"^\s*\|?[\s:|-]+\|?\s*$", line)) and "-" in line


def _split_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    # Protect pipes inside [[wikilinks]] (escaped or not) so they aren't
    # mistaken for column delimiters, then restore them after the split.
    line = re.sub(r"\[\[[^\]]*\]\]", lambda m: m.group(0).replace("|", "\x00"), line)
    return [c.strip().replace("\x00", "|") for c in re.split(r"(?<!\\)\|", line)]


def render_blocks(lines: list[str]) -> str:
    out: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if re.match(r"^---+$", stripped):
            out.append("<hr/>")
            i += 1
            continue

        h = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if h:
            level = len(h.group(1))
            if level <= 2:
                name, clean = heading_icon(h.group(2))
                out.append(
                    f'<h{level} class="sec"><span class="sec-ic">{icon(name, "ic", 18)}</span>'
                    f"<span>{clean_inline(clean)}</span></h{level}>"
                )
            else:
                out.append(f'<h{level} class="sub">{clean_inline(h.group(2))}</h{level}>')
            i += 1
            continue

        if stripped.startswith(">"):
            block: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                block.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            kind, title = "note", ""
            if block:
                cm = re.match(r"^\[!(\w+)\]\s*(.*)$", block[0].strip())
                if cm:
                    kind = cm.group(1).lower()
                    title = cm.group(2).strip()
                    block = block[1:]
            body = render_blocks(block)
            ic = icon("alert", "ic", 16) if kind in ("warning", "danger", "caution") else ""
            title_html = (
                f'<div class="cw-title">{ic}<span>{clean_inline(title)}</span></div>' if title else ""
            )
            out.append(f'<div class="cw cw-{html.escape(kind)}">{title_html}{body}</div>')
            continue

        if stripped.startswith("|") and i + 1 < n and _is_table_sep(lines[i + 1]):
            headers = _split_row(lines[i])
            i += 2
            rows: list[list[str]] = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(_split_row(lines[i]))
                i += 1
            thead = "".join(f"<th>{clean_inline(c)}</th>" for c in headers)
            tbody = ""
            for r in rows:
                tbody += "<tr>" + "".join(f"<td>{clean_inline(c)}</td>" for c in r) + "</tr>"
            out.append(
                f'<div class="tw"><table><thead><tr>{thead}</tr></thead>'
                f"<tbody>{tbody}</tbody></table></div>"
            )
            continue

        if re.match(r"^[-*]\s+", stripped):
            items = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(clean_inline(re.sub(r"^\s*[-*]\s+", "", lines[i])))
                i += 1
            out.append("<ul>" + "".join(f"<li>{it}</li>" for it in items) + "</ul>")
            continue

        para = [stripped]
        i += 1
        while i < n and lines[i].strip() and not re.match(
            r"^(#{1,6}\s|>|\||[-*]\s|---+$)", lines[i].strip()
        ):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{clean_inline(' '.join(para))}</p>")

    return "\n".join(out)


def strip_frontmatter(md: str) -> str:
    if md.startswith("---"):
        parts = md.split("\n")
        if parts and parts[0].strip() == "---":
            for j in range(1, len(parts)):
                if parts[j].strip() == "---":
                    return "\n".join(parts[j + 1 :])
    return md


# --------------------------------------------------------------------------- #
# Structured parse for the KPI hero strip + token bar chart                      #
# --------------------------------------------------------------------------- #


def find_tables(md: str):
    lines = md.split("\n")
    tables, i, n = [], 0, len(lines)
    while i < n:
        if lines[i].strip().startswith("|") and i + 1 < n and _is_table_sep(lines[i + 1]):
            headers = _split_row(lines[i])
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(_split_row(lines[i]))
                i += 1
            tables.append((headers, rows))
        else:
            i += 1
    return tables


def _num(s: str) -> int:
    digits = re.sub(r"[^\d]", "", s or "")
    return int(digits) if digits else 0


def parse_hero(md: str) -> dict:
    def grab(pat):
        m = re.search(pat, md)
        return m.group(1) if m else None

    hero = {
        "generated": grab(r"[Gg]enerated\s+\*\*(.+?)\*\*"),
        "agents": grab(r"Agents:\s*\*\*(\d+)\*\*"),
        "departments": grab(r"in\s*\*\*(\d+)\s*departments"),
        "tasks": grab(r"Tasks:\s*\*\*(\d+)\*\*"),
        "calls": grab(r"LLM calls logged:\s*\*\*(\d+)\*\*"),
        "total_cost": grab(r"[Tt]otal logged cost\s*≈?\s*\$([\d.]+)"),
        "tokens": [],
    }
    for headers, rows in find_tables(md):
        joined = " ".join(headers).lower()
        if "cost" in joined and ("calls" in joined or "model" in joined or "provider" in joined):
            today_idx = next((k for k, h in enumerate(headers) if "today" in h.lower()), None)
            cost_idx = next((k for k, h in enumerate(headers) if "cost" in h.lower()), None)
            calls_idx = next((k for k, h in enumerate(headers) if "call" in h.lower()), None)
            for r in rows:
                if not r or not r[0]:
                    continue
                hero["tokens"].append(
                    {
                        "label": r[0],
                        "today": _num(r[today_idx]) if today_idx is not None and today_idx < len(r) else 0,
                        "calls": r[calls_idx] if calls_idx is not None and calls_idx < len(r) else "",
                        "cost": r[cost_idx] if cost_idx is not None and cost_idx < len(r) else "",
                    }
                )
            break
    hero["tokens"].sort(key=lambda t: t["today"], reverse=True)  # AAA: sort descending
    return hero


def render_hero(hero: dict) -> str:
    def card(ic, label, value, accent=False):
        v = value if value not in (None, "") else "—"
        cls = "kpi kpi-accent" if accent else "kpi"
        return (
            f'<div class="{cls}"><div class="kpi-top"><span class="kpi-ic">{icon(ic, "ic", 16)}</span>'
            f'<span class="kpi-l">{html.escape(label)}</span></div>'
            f'<div class="kpi-v">{html.escape(str(v))}</div></div>'
        )

    cards = (
        card("users", "Agents", hero["agents"])
        + card("grid", "Departments", hero["departments"])
        + card("clipboard", "Tasks", hero["tasks"])
        + card("zap", "LLM calls", hero["calls"])
        + card("dollar", "Logged cost", ("$" + hero["total_cost"]) if hero["total_cost"] else None, True)
    )
    hero_html = f'<section class="hero" aria-label="Key metrics">{cards}</section>'

    toks = [t for t in hero["tokens"] if t["today"] > 0]
    if not toks:
        return hero_html
    total = sum(t["today"] for t in toks)
    mx = max(t["today"] for t in toks)
    top = toks[0]
    rows = ""
    for t in toks:
        w = max(2, round(t["today"] / mx * 100))
        meta = " · ".join(x for x in [(t["calls"] + " calls") if t["calls"] else "", t["cost"]] if x)
        rows += (
            '<div class="bar-row"><div class="bar-top">'
            f'<span class="bar-lbl">{clean_inline(t["label"])}</span>'
            f'<span class="bar-num">{t["today"]:,} tok</span></div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{w}%"></div></div>'
            + (f'<div class="bar-meta">{clean_inline(meta)}</div>' if meta else "")
            + "</div>"
        )
    aria = f"Tokens used today by model. Total {total:,}. Highest: {top['label']} at {top['today']:,}."
    return (
        hero_html
        + '<section class="bars" role="img" aria-label="' + html.escape(aria) + '">'
        '<div class="bars-h"><span class="bars-ic">' + icon("barchart", "ic", 16) + "</span>"
        '<span>Tokens used today</span>'
        f'<span class="bars-total">{total:,} total</span></div>' + rows + "</section>"
    )


def build_content(md: str) -> str:
    hero = parse_hero(md)
    body = render_blocks(strip_frontmatter(md).split("\n"))
    return render_hero(hero) + '<div class="doc">' + body + "</div>"


# --------------------------------------------------------------------------- #
# Page shell (CSS/JS are a plain string; placeholders filled via .replace)      #
# --------------------------------------------------------------------------- #

PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Division Dashboard — live</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Fira+Sans:wght@300;400;500;600;700&display=swap');
:root{
  --bg:#F8FAFC; --surface:#FFFFFF; --surface2:#F1F5F9; --text:#0F172A; --text2:#475569; --text3:#64748B;
  --border:#E2E8F0; --border2:#CBD5E1; --primary:#1E40AF; --primary2:#2563EB; --primary-bg:#EFF4FE;
  --accent:#B45309; --accent-bg:#FEF3C7; --accent-line:#F59E0B;
  --danger:#B91C1C; --danger-bg:#FEF2F2; --ok:#15803D; --ok-bg:#DCFCE7; --ring:#1E40AF;
  --font-sans:'Fira Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  --font-mono:'Fira Code',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --z-header:20;
}
@media (prefers-color-scheme:dark){:root{
  --bg:#0B1220; --surface:#111A2E; --surface2:#16223B; --text:#E2E8F0; --text2:#94A3B8; --text3:#8597AD;
  --border:#1E293B; --border2:#334155; --primary:#60A5FA; --primary2:#3B82F6; --primary-bg:#16223B;
  --accent:#FBBF24; --accent-bg:#2A2410; --accent-line:#B7791F;
  --danger:#F87171; --danger-bg:#2A1414; --ok:#34D399; --ok-bg:#0F2A1E; --ring:#60A5FA;
}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font-sans);
  font-size:15px;line-height:1.6;-webkit-font-smoothing:antialiased;}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px 64px;}
header.top{position:sticky;top:0;z-index:var(--z-header);background:color-mix(in srgb,var(--bg) 88%,transparent);
  backdrop-filter:saturate(1.2) blur(8px);border-bottom:1px solid var(--border);
  padding:12px 24px;margin:0 -24px 22px;display:flex;align-items:center;gap:14px;flex-wrap:wrap;}
.brand{display:flex;align-items:center;gap:11px;}
.brand-mark{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;
  background:var(--primary);color:#fff;}
.brand h1{font-size:17px;font-weight:600;margin:0;line-height:1.15;letter-spacing:-.2px;}
.brand .sub{font-size:12px;color:var(--text3);}
.spacer{flex:1}
.live{display:inline-flex;align-items:center;gap:7px;font-size:12px;font-weight:500;color:var(--ok);
  background:var(--ok-bg);padding:4px 11px;border-radius:999px;}
.dot{width:8px;height:8px;border-radius:50%;background:var(--ok);animation:pulse 1.8s ease-in-out infinite;}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.82)}}
.status{font-size:12px;color:var(--text3);font-variant-numeric:tabular-nums;min-width:150px;text-align:right;}
button.rf{display:inline-flex;align-items:center;gap:7px;font:inherit;font-size:13px;font-weight:500;
  background:var(--surface);color:var(--text);border:1px solid var(--border2);border-radius:9px;
  padding:7px 13px;cursor:pointer;transition:background .18s ease,border-color .18s ease;}
button.rf:hover{background:var(--surface2);border-color:var(--primary2);}
button.rf:active{transform:scale(.98)}
button.rf .ic.spin{animation:spin 1s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
a:focus-visible,button:focus-visible{outline:2px solid var(--ring);outline-offset:2px;border-radius:6px;}
.ic{display:block}
.hero{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));gap:13px;margin-bottom:14px;}
.kpi{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:15px 17px;
  transition:border-color .18s ease,transform .18s ease;}
.kpi:hover{border-color:var(--border2);transform:translateY(-1px);}
.kpi-top{display:flex;align-items:center;gap:8px;margin-bottom:9px;color:var(--text3);}
.kpi-ic{display:grid;place-items:center;width:26px;height:26px;border-radius:7px;
  background:var(--primary-bg);color:var(--primary);}
.kpi-l{font-size:12.5px;font-weight:500;color:var(--text2);}
.kpi-v{font-family:var(--font-mono);font-size:28px;font-weight:600;letter-spacing:-1px;
  font-variant-numeric:tabular-nums;color:var(--text);}
.kpi-accent .kpi-ic{background:var(--accent-bg);color:var(--accent);}
.kpi-accent .kpi-v{color:var(--accent);}
.bars{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:16px 18px;margin-bottom:24px;}
.bars-h{display:flex;align-items:center;gap:9px;font-size:13px;font-weight:500;color:var(--text2);margin-bottom:14px;}
.bars-ic{display:grid;place-items:center;width:24px;height:24px;border-radius:7px;background:var(--primary-bg);color:var(--primary);}
.bars-total{margin-left:auto;font-family:var(--font-mono);font-size:12px;color:var(--text3);font-variant-numeric:tabular-nums;}
.bar-row{margin-bottom:13px}.bar-row:last-child{margin-bottom:0}
.bar-top{display:flex;justify-content:space-between;align-items:baseline;font-size:13px;margin-bottom:6px;gap:10px;}
.bar-lbl{color:var(--text)}.bar-lbl code{font-family:var(--font-mono);font-size:12px;background:var(--surface2);padding:1px 6px;border-radius:5px;}
.bar-num{font-family:var(--font-mono);color:var(--text2);font-variant-numeric:tabular-nums;white-space:nowrap;}
.bar-track{height:10px;background:var(--surface2);border-radius:6px;overflow:hidden;}
.bar-fill{height:100%;background:var(--primary);border-radius:6px;transition:width .5s cubic-bezier(.4,0,.2,1);}
.bar-meta{font-size:12px;color:var(--text3);margin-top:5px;font-family:var(--font-mono);}
.doc h1.sec{font-size:21px}.doc h2.sec{font-size:17px;margin-top:34px;padding-top:24px;border-top:1px solid var(--border);}
.doc .sec{display:flex;align-items:center;gap:10px;font-weight:600;letter-spacing:-.2px;}
.doc .sec:first-child{margin-top:0;padding-top:0;border-top:0;}
.sec-ic{display:grid;place-items:center;width:30px;height:30px;border-radius:8px;background:var(--primary-bg);color:var(--primary);flex:none;}
.doc h2.sec .sec-ic{width:27px;height:27px}
.doc h3.sub{font-size:14.5px;font-weight:600;margin:24px 0 6px;padding-left:11px;
  border-left:3px solid var(--primary2);line-height:1.4;}
.tw{overflow-x:auto;margin:13px 0;border:1px solid var(--border);border-radius:11px;}
table{border-collapse:collapse;width:100%;font-size:13.5px;}
th,td{text-align:left;padding:9px 13px;border-bottom:1px solid var(--border);vertical-align:top;
  font-variant-numeric:tabular-nums;}
th{color:var(--text2);font-weight:600;background:var(--surface2);white-space:nowrap;position:sticky;top:0;}
tbody tr{transition:background .15s ease}
tbody tr:hover{background:var(--surface2)}
tbody tr:last-child td{border-bottom:0}
code{font-family:var(--font-mono);background:var(--surface2);padding:1.5px 6px;border-radius:5px;font-size:12.5px;}
ul{padding-left:20px;margin:10px 0}li{margin:4px 0}
hr{border:0;border-top:1px solid var(--border);margin:26px 0}
.cw{border:1px solid var(--border);border-radius:12px;padding:14px 16px;margin:16px 0;background:var(--surface);}
.cw-warning,.cw-danger,.cw-caution{background:var(--accent-bg);border-color:var(--accent-line);}
.cw-title{display:flex;align-items:center;gap:8px;font-weight:600;margin-bottom:8px;color:var(--text);}
.cw-warning .cw-title,.cw-danger .cw-title{color:var(--accent);}
.cw .tw{border:0;margin:6px 0 0}.cw table{background:transparent}
.cw-note{background:var(--surface2);border-color:var(--border);color:var(--text2);font-size:13.5px;}
.foot{margin-top:34px;padding-top:18px;border-top:1px solid var(--border);
  font-size:12px;color:var(--text3);display:flex;gap:8px;flex-wrap:wrap;align-items:center;}
.foot code{font-size:11.5px}
.err{background:var(--danger-bg);color:var(--danger);padding:16px;border-radius:12px;border:1px solid var(--danger);}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0;}
@media (max-width:640px){.wrap{padding:0 16px 48px}header.top{margin:0 -16px 18px;padding:12px 16px}
  .status{display:none}.brand h1{font-size:16px}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style></head><body>
<header class="top">
  <div class="brand">
    <span class="brand-mark">__BRANDICON__</span>
    <div><h1>Division Dashboard</h1><div class="sub">live · read-only view</div></div>
  </div>
  <span class="spacer"></span>
  <span class="live"><span class="dot"></span>LIVE</span>
  <span class="status" id="status" aria-live="polite">checking…</span>
  <button class="rf" id="refresh" aria-label="Refresh now">__RFICON__<span>Refresh</span></button>
</header>
<main class="wrap">
  <h2 class="sr-only">Live read-only dashboard rendered from 00-Dashboard.md, auto-refreshing when the file changes.</h2>
  <div id="content">__CONTENT__</div>
  <div class="foot">__FOOTICON__<span>Source <code>__SRCFILE__</code> · generated __GENERATED__ · information-only, the file is never modified.</span></div>
</main>
<script>
var POLL=__POLL_MS__, lastM="__MTIME__";
var statusEl=document.getElementById('status'), btn=document.getElementById('refresh');
function fmt(d){return d.toLocaleTimeString();}
function setStatus(t){statusEl.textContent=t;}
function busy(on){var s=btn.querySelector('.ic');if(s){s.classList.toggle('spin',on);}}
async function poll(force){
  busy(true);
  try{
    var r=await fetch('/fragment?t='+Date.now());
    if(!r.ok) throw new Error(r.status);
    var j=await r.json();
    if(force || j.mtime!==lastM){
      document.getElementById('content').innerHTML=j.html; lastM=j.mtime; flash();
    }
    setStatus('updated '+fmt(new Date())+' · every '+(POLL/1000)+'s');
  }catch(e){ setStatus('source unavailable — retrying…'); }
  finally{ busy(false); }
}
function flash(){var c=document.getElementById('content');
  c.style.transition='none';c.style.opacity='.4';
  requestAnimationFrame(function(){c.style.transition='opacity .45s ease';c.style.opacity='1';});}
btn.addEventListener('click',function(){poll(true);});
setInterval(poll,POLL); setStatus('auto-refresh every '+(POLL/1000)+'s');
</script>
</body></html>"""


class Handler(BaseHTTPRequestHandler):
    dash_file: Path = Path("00-Dashboard.md")
    poll_ms: int = 8000

    def log_message(self, *a):
        pass

    def _read(self):
        p = self.dash_file
        if not p.exists():
            return None, "0", None
        md = p.read_text(encoding="utf-8")  # READ ONLY
        return md, str(p.stat().st_mtime), parse_hero(md).get("generated")

    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            md, mtime, gen = self._read()
            content = (
                build_content(md)
                if md is not None
                else f'<div class="err">Source file not found: {html.escape(str(self.dash_file))}</div>'
            )
            page = (
                PAGE.replace("__CONTENT__", content)
                .replace("__BRANDICON__", icon("activity", "ic", 19))
                .replace("__RFICON__", icon("refresh", "ic", 15))
                .replace("__FOOTICON__", icon("activity", "ic", 14))
                .replace("__SRCFILE__", html.escape(str(self.dash_file)))
                .replace("__GENERATED__", html.escape(gen or "—"))
                .replace("__MTIME__", mtime)
                .replace("__POLL_MS__", str(self.poll_ms))
            )
            self._send(200, page)
        elif path == "/fragment":
            md, mtime, gen = self._read()
            content = (
                build_content(md)
                if md is not None
                else f'<div class="err">Source file not found: {html.escape(str(self.dash_file))}</div>'
            )
            self._send(
                200,
                json.dumps({"html": content, "mtime": mtime, "generated": gen, "read_at": time.time()}),
                "application/json",
            )
        elif path == "/raw":
            md, _, _ = self._read()
            self._send(200, md or "", "text/plain; charset=utf-8")
        elif path == "/health":
            self._send(200, "ok", "text/plain")
        else:
            self._send(404, "not found", "text/plain")


def main():
    here = Path(__file__).resolve()
    repo_root = here.parents[2]
    ap = argparse.ArgumentParser(description="Live read-only dashboard for 00-Dashboard.md")
    ap.add_argument("--vault", type=Path, default=repo_root, help="Vault root (default: repo root)")
    ap.add_argument("--file", type=Path, default=None, help="Explicit path to the dashboard .md")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--poll", type=int, default=8, help="Browser auto-refresh interval (seconds)")
    args = ap.parse_args()

    dash_file = (args.file or (args.vault / "00-Dashboard.md")).resolve()
    Handler.dash_file = dash_file
    Handler.poll_ms = max(2, args.poll) * 1000

    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    url = f"http://{args.host}:{args.port}/"
    print("Live dashboard (read-only) serving:")
    print(f"  source : {dash_file}  {'(found)' if dash_file.exists() else '(MISSING)'}")
    print(f"  url    : {url}")
    print(f"  refresh: every {args.poll}s · the source file is never modified")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
