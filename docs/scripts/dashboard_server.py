"""Live "good morning" division dashboard on localhost — demo edition.

Executive morning briefing from real vault data: a one-line state-of-the-division,
KPI tiles with trend arrows, a value-vs-cost ROI banner, a hero alert, "needs your
approval", "risks & alerts", and "recent activity". Click any item to read the
underlying document. Optional present/kiosk mode + branding for a projector, print
to PDF, and a guarded live "Approve → execute" action.

Read-only by default. The /doc endpoint is sandboxed to vault .md files. The live
approve action is OFF unless started with --enable-actions (demo mode).

Usage:
    python docs/scripts/dashboard_server.py
    python docs/scripts/dashboard_server.py --company "Acme Devices" --logo assets/logo.png
    python docs/scripts/dashboard_server.py --enable-actions     # demo: live approve
Open http://127.0.0.1:8787/  (add ?present=1 for projector mode). Stdlib only.
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HIST = Path("/tmp/bd-dashboard-history.json")
VENDOR = Path(__file__).resolve().parent / "vendor"   # locally-served Chart.js + D3 (offline-proof)

# --------------------------------------------------------------------------- #
# Markdown helpers                                                              #
# --------------------------------------------------------------------------- #

_WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_CODE = re.compile(r"`([^`]+)`")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def txt(s: str) -> str:
    s = s or ""
    s = _WIKILINK.sub(lambda m: m.group(1).replace("\\|", "|").split("|")[-1].strip(), s)
    s = _LINK.sub(lambda m: m.group(1), s)
    s = _BOLD.sub(r"\1", s)
    s = _CODE.sub(r"\1", s)
    return html.escape(s.strip())


def strip_frontmatter(md: str) -> str:
    if md.startswith("---"):
        parts = md.split("\n")
        if parts and parts[0].strip() == "---":
            for j in range(1, len(parts)):
                if parts[j].strip() == "---":
                    return "\n".join(parts[j + 1:])
    return md


def _is_sep(line: str) -> bool:
    return bool(re.match(r"^\s*>?\s*\|?[\s:|-]+\|?\s*$", line)) and "-" in line


def _row(line: str) -> list[str]:
    line = re.sub(r"^\s*>\s?", "", line.strip())
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    line = re.sub(r"\[\[[^\]]*\]\]", lambda m: m.group(0).replace("|", "\x00"), line)
    return [c.strip().replace("\x00", "|") for c in re.split(r"(?<!\\)\|", line)]


def _tables(md: str):
    lines = md.split("\n")
    out, i, n = [], 0, len(lines)
    while i < n:
        cur = lines[i].strip()
        is_row = cur.startswith("|") or (cur.startswith(">") and "|" in cur)
        if is_row and i + 1 < n and _is_sep(lines[i + 1]):
            headers = _row(lines[i])
            i += 2
            rows = []
            while i < n and ("|" in lines[i]) and lines[i].strip().startswith(("|", ">")):
                if not _is_sep(lines[i]):
                    rows.append(_row(lines[i]))
                i += 1
            out.append((headers, rows))
        else:
            i += 1
    return out


def _section(md: str, key: str) -> str:
    grab, buf = False, []
    for ln in md.split("\n"):
        if re.match(r"^#{1,6}\s", ln):
            grab = key.lower() in ln.lower()
            continue
        if grab:
            buf.append(ln)
    return "\n".join(buf)


def _task_cell(cell: str):
    m = _WIKILINK.search(cell)
    if not m:
        return txt(cell), ""
    inner = m.group(1).replace("\\|", "|")
    path, _, title = inner.partition("|")
    parts = path.split("/")
    folder = parts[1] if len(parts) >= 2 and parts[0] == "02-Tasks" else ""
    return html.escape((title or path).strip()), folder


# --------------------------------------------------------------------------- #
# Full markdown -> HTML for the click-through document modal                    #
# --------------------------------------------------------------------------- #


def _inline(text, vault):
    text = html.escape(text)

    def wl(m):
        inner = m.group(1).replace("\\|", "|")
        path, _, alias = inner.partition("|")
        label = (alias or path.split("/")[-1]).strip()
        rel = path.strip()
        if "/" in rel:
            if not rel.lower().endswith(".md"):
                rel += ".md"
            if (vault / rel).is_file():
                return f'<a class="dl" data-doc="{html.escape(rel)}">{html.escape(label)}</a>'
        return html.escape(label)

    def lk(m):
        label, url = m.group(1), m.group(2)
        if url.lower().endswith(".md") and (vault / url).is_file():
            return f'<a class="dl" data-doc="{html.escape(url)}">{html.escape(label)}</a>'
        if url.startswith(("http://", "https://")):
            return f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(label)}</a>'
        return html.escape(label)

    text = _WIKILINK.sub(wl, text)
    text = _LINK.sub(lk, text)
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _CODE.sub(r"<code>\1</code>", text)
    return text


def md_to_html(md, vault):
    lines = strip_frontmatter(md).split("\n")
    out, i, n = [], 0, len(lines)
    while i < n:
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if re.match(r"^---+$", s):
            out.append("<hr/>")
            i += 1
            continue
        h = re.match(r"^(#{1,6})\s+(.*)$", s)
        if h:
            lv = min(len(h.group(1)), 6)
            out.append(f"<h{lv}>{_inline(h.group(2), vault)}</h{lv}>")
            i += 1
            continue
        if s.startswith(">"):
            blk = []
            while i < n and lines[i].strip().startswith(">"):
                blk.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            cm = re.match(r"^\[!(\w+)\]\s*(.*)$", blk[0].strip()) if blk else None
            inner = md_to_html("\n".join(blk[1:] if cm else blk), vault)
            cls = "callout " + (cm.group(1).lower() if cm else "note")
            ttl = f'<div class="co-t">{_inline(cm.group(2), vault)}</div>' if cm and cm.group(2) else ""
            out.append(f'<div class="{cls}">{ttl}{inner}</div>')
            continue
        if s.startswith("|") and i + 1 < n and _is_sep(lines[i + 1]):
            hd = _row(lines[i])
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                if not _is_sep(lines[i]):
                    rows.append(_row(lines[i]))
                i += 1
            th = "".join(f"<th>{_inline(c, vault)}</th>" for c in hd)
            tb = "".join("<tr>" + "".join(f"<td>{_inline(c, vault)}</td>" for c in r) + "</tr>" for r in rows)
            out.append(f'<div class="tw"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>')
            continue
        if re.match(r"^[-*]\s+", s):
            its = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                its.append(_inline(re.sub(r"^\s*[-*]\s+", "", lines[i]), vault))
                i += 1
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in its) + "</ul>")
            continue
        para = [s]
        i += 1
        while i < n and lines[i].strip() and not re.match(r"^(#{1,6}\s|>|\||[-*]\s|---+$)", lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{_inline(' '.join(para), vault)}</p>")
    return "\n".join(out)


def best_doc(vault, folder):
    if not folder:
        return ""
    for name in ("07-decision-report.md", "08-execution-plan.md", "00-brief.md"):
        if (vault / "02-Tasks" / folder / name).is_file():
            return f"02-Tasks/{folder}/{name}"
    return ""


def plan_is_valid(vault, tdir):
    """True if the task already has an execution plan whose template table references a real catalog slug.
    When valid, the live action runs execute only (deterministic) and skips the LLM approve step."""
    pf = tdir / "08-execution-plan.md"
    if not pf.is_file():
        return False
    try:
        t = pf.read_text(encoding="utf-8")
    except OSError:
        return False
    if "templates to create" not in t.lower():
        return False
    for headers, rows in _tables(t):
        if "template" in " ".join(headers).lower():
            for r in rows:
                if len(r) >= 2 and (vault / "docs" / "templates-us" / r[1].strip() / (r[0].strip() + ".md")).is_file():
                    return True
    return False


# --------------------------------------------------------------------------- #
# Extract structured data                                                       #
# --------------------------------------------------------------------------- #


def parse_meta(md):
    def g(pat):
        m = re.search(pat, md)
        return m.group(1) if m else None
    return {
        "generated": g(r"[Gg]enerated\s+\*\*(.+?)\*\*") or g(r"generated:\s*(.+)"),
        "agents": g(r"Agents:\s*\*\*(\d+)\*\*"),
        "departments": g(r"in\s*\*\*(\d+)\s*departments"),
        "tasks": g(r"Tasks:\s*\*\*(\d+)\*\*"),
        "calls": g(r"LLM calls logged:\s*\*\*(\d+)\*\*"),
        "cost": g(r"[Tt]otal logged cost\s*≈?\s*\$([\d.]+)"),
    }


def parse_pending(md):
    sec = _section(md, "needs action") or md
    out = []
    for headers, rows in _tables(sec):
        joined = " ".join(headers).lower()
        if "task" in joined and ("waiting" in joined or "next" in joined):
            for r in rows:
                if not r or not r[0]:
                    continue
                title, folder = _task_cell(r[0])
                out.append({"title": title, "folder": folder,
                            "stage": txt(r[1]) if len(r) > 1 else "",
                            "next": txt(r[2]) if len(r) > 2 else ""})
            break
    return out


def parse_pipeline(md):
    sec = _section(md, "pipeline") or md
    out = []
    for headers, rows in _tables(sec):
        joined = " ".join(headers).lower()
        if "task" in joined and "stage" in joined:
            for r in rows:
                if not r or not r[0]:
                    continue
                title, folder = _task_cell(r[0])
                out.append({"title": title, "folder": folder,
                            "stage": txt(r[1]) if len(r) > 1 else "",
                            "tokens": txt(r[2]) if len(r) > 2 else ""})
            break
    return out


_SEV = {"🔴": ("red", 3), "🟠": ("amber", 2), "🟡": ("amber", 1), "🟢": ("green", 0)}
RATES = {"claude": (3.0, 15.0), "mcp-sampling": (0.0, 0.0)}


def read_risks(vault):
    risks = []
    proj = vault / "04-Projects"
    if not proj.exists():
        return risks
    seen = set()
    files = set(proj.glob("*/01-PM/risk-register.md")) | set(proj.glob("*/*/risk-register.md"))
    for rf in sorted(files):
        try:
            md = rf.read_text(encoding="utf-8")
        except OSError:
            continue
        project = rf.parts[rf.parts.index("04-Projects") + 1].replace("Project-", "")
        rel = str(rf.relative_to(vault))
        for headers, rows in _tables(md):
            hl = [h.lower() for h in headers]
            if "risk" not in " ".join(hl) or "score" not in " ".join(hl):
                continue
            ix = {k: next((j for j, h in enumerate(hl) if k in h), None) for k in ("id", "risk", "score", "owner", "status")}
            pix = next((j for j, h in enumerate(headers) if h.strip().lower() == "p"), None)
            iix = next((j for j, h in enumerate(headers) if h.strip().lower() == "i"), None)
            for r in rows:
                def cell(k):
                    j = ix[k]
                    return r[j] if j is not None and j < len(r) else ""

                def intcol(j):
                    if j is None or j >= len(r):
                        return 0
                    d = re.sub(r"[^\d]", "", r[j])
                    return int(d) if d else 0
                sev = next((v for s, v in _SEV.items() if s in cell("score")), None)
                status = cell("status").lower()
                if not sev or "closed" in status or "retired" in status:
                    continue
                rid = txt(cell("id"))
                if (project, rid) in seen:
                    continue
                seen.add((project, rid))
                num = re.sub(r"[^\d]", "", cell("score"))
                risks.append({"sev": sev[0], "rank": sev[1], "score": int(num) if num else 0,
                              "id": rid, "text": txt(cell("risk")), "owner": txt(cell("owner")),
                              "status": txt(cell("status")), "project": html.escape(project), "file": rel,
                              "p": intcol(pix), "i": intcol(iix)})
    risks.sort(key=lambda x: (x["rank"], x["score"]), reverse=True)
    return risks


def risk_health(risks):
    return {"red": sum(1 for r in risks if r["sev"] == "red"),
            "amber": sum(1 for r in risks if r["sev"] == "amber"),
            "green": sum(1 for r in risks if r["sev"] == "green")}


def risk_points(risks):
    out = []
    for r in risks:
        if r["p"] and r["i"]:
            out.append({"x": r["p"], "y": r["i"], "sev": r["sev"], "id": r["id"],
                        "label": _short(re.sub(r"\*\*", "", r["text"]), 48), "file": r["file"]})
    return out


def pipeline_progress(pipeline):
    total = len(pipeline)
    done = sum(1 for p in pipeline if "done" in p["stage"].lower())
    return {"done": done, "total": total, "pct": round(done / total * 100) if total else 0}


def parse_targets(vault):
    out = []
    proj = vault / "04-Projects"
    if proj.exists():
        for cw in sorted(proj.glob("*/05-BOM-Cost/cost-walk.md")):
            try:
                t = cw.read_text(encoding="utf-8")
            except OSError:
                continue
            sop = cur = tgt = None
            for ln in t.split("\n"):
                if not ln.strip().startswith("|") or "$" not in ln:
                    continue  # only the cost-trajectory table rows, not prose
                m = re.search(r"\$(\d+\.?\d*)", ln)
                if not m:
                    continue
                v = float(m.group(1))
                if "SOP" in ln:
                    sop = v
                elif "Current" in ln:
                    cur = v
                elif "Target" in ln:
                    tgt = v
            if sop and cur and tgt and sop > tgt:
                pct = round((sop - cur) / (sop - tgt) * 100)
                out.append({"pct": max(0, min(100, pct)), "label": "BOM cost-down", "detail": f"${cur:.2f} → ${tgt:.0f}"})
                break
    pm = vault / "00-Brain" / "products.md"
    if pm.is_file():
        m = re.search(r"AFR\s*(\d+\.?\d*)%\s*→\s*(?:target\s*)?(\d+\.?\d*)%", pm.read_text(encoding="utf-8"))
        if m:
            cur, tgt = float(m.group(1)), float(m.group(2))
            if cur > 0:
                out.append({"pct": round(min(100, tgt / cur * 100)), "label": "Field AFR", "detail": f"{cur}% → {tgt}%"})
    return out


def agent_network(md):
    nodes, links, cur, inseg = [], [], None, False
    for ln in md.split("\n"):
        if re.match(r"^##\s+\S", ln):          # level-2 heading (## ...), not ###
            inseg = "agents" in ln.lower()
            cur = None
            continue
        if not inseg:
            continue
        h = re.match(r"^###\s+\[\[[^|\]]*\|([^\]]+)\]\]", ln)
        if h:
            name = h.group(1).strip()
            mm = re.search(r"meetings:\s*(\d+)", ln)
            cur = "d:" + name
            nodes.append({"id": cur, "label": name, "type": "dept", "activity": int(mm.group(1)) if mm else 0})
            continue
        if cur and ln.strip().startswith("|") and not _is_sep(ln):
            cells = _row(ln)
            if not cells or cells[0].lower().startswith("agent"):
                continue
            am = _WIKILINK.search(cells[0])
            if not am:
                continue
            aname = am.group(1).replace("\\|", "|").split("|")[-1].strip()
            ment = re.sub(r"[^\d]", "", cells[2]) if len(cells) >= 3 else ""
            aid = "a:" + cur + ":" + aname
            nodes.append({"id": aid, "label": aname, "type": "agent", "activity": int(ment) if ment else 0})
            links.append({"source": cur, "target": aid})
    return {"nodes": nodes, "links": links}


def spend_series(vault):
    f = vault / ".bd-usage.jsonl"
    if not f.is_file():
        return []
    cum, out = 0.0, []
    try:
        lines = f.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    for ln in lines:
        try:
            r = json.loads(ln)
        except Exception:
            continue
        ri, ro = RATES.get(r.get("provider", "?"), (0.0, 0.0))
        cum += r.get("prompt_tokens", 0) / 1e6 * ri + r.get("completion_tokens", 0) / 1e6 * ro
        out.append(round(cum, 4))
    return out[-40:]


def read_activity(vault, pipeline):
    by = {p["folder"]: p for p in pipeline if p["folder"]}
    root = vault / "02-Tasks"
    if not root.exists():
        return []
    items = []
    for d in root.glob("*/"):
        if not d.is_dir():
            continue
        try:
            mt = max((f.stat().st_mtime for f in d.iterdir() if f.is_file()), default=d.stat().st_mtime)
        except OSError:
            continue
        info = by.get(d.name, {})
        items.append({"mtime": mt, "title": info.get("title", d.name), "stage": info.get("stage", ""), "folder": d.name})
    items.sort(key=lambda x: x["mtime"], reverse=True)
    return items[:6]


def trends(cur):
    """Append a snapshot to /tmp history (never the vault); return deltas vs the prior distinct snapshot."""
    try:
        hist = json.loads(HIST.read_text())
    except Exception:
        hist = []
    keys = ("tasks", "pending", "high")
    if not hist or any(hist[-1].get(k) != cur.get(k) for k in keys + ("cost",)):
        hist.append({**cur, "ts": time.time()})
        hist = hist[-60:]
        try:
            HIST.write_text(json.dumps(hist))
        except Exception:
            pass
    base = hist[-2] if len(hist) >= 2 else None
    return {k: ((cur.get(k) or 0) - (base.get(k) or 0)) if base else 0 for k in keys}


# --------------------------------------------------------------------------- #
# Render                                                                        #
# --------------------------------------------------------------------------- #


def _num(s):
    return s if s not in (None, "") else "—"


def _short(s, n=46):
    s = s or ""
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def _risk_label(r):
    t = re.split(r"\s[—-]\s|\(", r["text"])[0].strip()
    return _short(t, 30)


def _stage_phrase(stage):
    s = stage.lower()
    if "done" in s:
        return "green", "completed — outputs rendered"
    if "stop 2" in s or "execution plan" in s:
        return "amber", "execution plan ready — awaiting approval"
    if "stop 1" in s or "decision report" in s:
        return "amber", "decision report ready — awaiting approval"
    if "clarification" in s:
        return "amber", "needs clarification answered"
    if "meeting" in s:
        return "blue", "meeting in progress"
    if "routed" in s:
        return "blue", "routed — ready for meeting"
    return "blue", txt(stage) or "updated"


def _doc_attr(path):
    return f' data-doc="{html.escape(path)}" class="clk"' if path else ""


def _arrow(delta, up="red", down="green"):
    if not delta:
        return ""
    if delta > 0:
        return f'<span class="dl dl-{up}">▲{delta}</span>'
    return f'<span class="dl dl-{down}">▼{abs(delta)}</span>'


def render_content(md, vault, owner, division, company, logo, rate, hours, actions):
    meta = parse_meta(md)
    pending = parse_pending(md)
    pipeline = parse_pipeline(md)
    risks = read_risks(vault)
    activity = read_activity(vault, pipeline)
    high = [r for r in risks if r["sev"] == "red"]
    n_tasks = int(meta["tasks"] or 0)
    tr = trends({"tasks": n_tasks, "pending": len(pending), "high": len(high), "cost": meta["cost"] or "0"})

    data = {"health": risk_health(risks), "pipeline": pipeline_progress(pipeline),
            "targets": parse_targets(vault), "riskPoints": risk_points(risks),
            "network": agent_network(md), "spark": spend_series(vault)}

    now = datetime.now()
    greet = "Good morning" if now.hour < 12 else ("Good afternoon" if now.hour < 18 else "Good evening")
    when = now.strftime("%A, %B %-d · %-I:%M %p")

    brand = ""
    if logo:
        brand += f'<img src="{logo}" alt="" style="height:30px;border-radius:6px"/>'
    if company:
        brand += f'<span class="co">{html.escape(company)}</span>'
    head = (
        '<div class="hdr">'
        f'<div><h1>{greet}, {html.escape(owner)}</h1>'
        f'<p class="sub">{html.escape(when)} · here\'s where your division stands</p></div>'
        f'<div class="hdr-r"><div class="brand">{brand}<span class="live"><span class="ld"></span>live</span>'
        f'<button class="btn" id="exportbtn" onclick="window.print()">Export PDF</button></div>'
        f'<p class="div">{html.escape(division)}</p></div></div>'
    )

    # exec one-liner — rule-based state of the division
    bits = []
    if high:
        names = ", ".join(_risk_label(r) for r in high[:2])
        bits.append(f"{len(high)} high risk{'s' if len(high) != 1 else ''} open ({names})")
    if pending:
        bits.append(f"{len(pending)} decision{'s' if len(pending) != 1 else ''} await your sign-off")
    lead = "All programs tracking — " + "; ".join(bits) + "." if bits else "All clear — no high risks or pending decisions."
    summary = f'<div class="summary">{html.escape(lead)}</div>'
    gov = ('<div class="gov"><span class="gv">✓ AI proposes, you approve</span>'
           '<span class="gv">✓ every claim cited to a source</span>'
           '<span class="gv">✓ cert boundaries protected</span>'
           '<span class="gv">✓ 2 mandatory sign-off gates</span></div>')

    def kpi(color, val, label, arrow="", count=None, prefix="", dec=0, extra=""):
        cnt = f' data-count="{count}" data-prefix="{html.escape(prefix)}" data-dec="{dec}"' if count is not None else ""
        return (f'<div class="kpi"><div class="kpi-top"><span class="sq sq-{color}"></span>'
                f'<span class="kpi-v"{cnt}>{html.escape(str(val))}</span>{arrow}</div>'
                f'<div class="kpi-l">{html.escape(label)}</div>{extra}</div>')
    spark = '<div class="sparkwrap"><canvas id="spark"></canvas></div>' if data["spark"] else ""
    kpis = ('<div class="kpis">'
            + kpi("blue", _num(meta["tasks"]), "active tasks", _arrow(tr["tasks"], "blue", "gray"), count=n_tasks)
            + kpi("amber", len(pending), "need approval", _arrow(tr["pending"], "amber", "green"), count=len(pending))
            + kpi("red", len(high), "high risks open", _arrow(tr["high"], "red", "green"), count=len(high))
            + kpi("gray", ("$" + meta["cost"]) if meta["cost"] else "—", "compute cost",
                  count=(float(meta["cost"]) if meta["cost"] else None), prefix="$", dec=2, extra=spark)
            + "</div>")

    def gauge_card(cid, center_id, label, sub):
        return (f'<div class="gz"><div class="gz-c"><canvas id="{cid}"></canvas>'
                f'<div class="gz-center" id="{center_id}"></div></div>'
                f'<div class="gz-l">{html.escape(label)}</div><div class="gz-sub">{html.escape(sub) or "&nbsp;"}</div></div>')
    gz = '<div class="gauges">'
    gz += gauge_card("healthDonut", "healthCenter", "risk health", f'{data["health"]["red"]} high · {data["health"]["amber"]} med')
    gz += gauge_card("pipeGauge", "pipeCenter", "pipeline done", f'{data["pipeline"]["done"]}/{data["pipeline"]["total"]} tasks')
    for idx, t in enumerate(data["targets"]):
        gz += gauge_card(f"tg{idx}", f"tgc{idx}", t["label"], t["detail"])
    gz += "</div>"

    # ROI band — value / revenue framing
    ah = round(n_tasks * hours)
    days = round(ah / 8, 1)
    val = round(n_tasks * hours * rate)
    roi = (f'<div class="roi"><span class="roi-ic">↳</span>'
           f'<span><b>{n_tasks} cross-functional decisions</b> · ≈ {ah} analyst-hours (~{days} analyst-days, ~${val:,} of loaded labor) '
           f'— <b>compressed to minutes</b>, for <b>${meta["cost"] or "0"}</b> in compute</span></div>')

    if high:
        h = high[0]
        hero = (
            f'<div class="hero hero-red"{_doc_attr(h["file"])}>'
            '<span class="sq sq-red hero-sq"></span><div class="hero-body">'
            f'<div class="pills"><span class="pill pill-red">High risk · {h["id"]}</span>'
            f'<span class="pill pill-gray">{h["project"]} · {h["status"]}</span></div>'
            f'<h3>{h["text"]}</h3>'
            f'<p class="hero-sub">Owner: {h["owner"] or "—"}. Top open red-rated risk across your projects — click to read the full register and mitigation.</p>'
            f'<div class="btns"><button class="btn" data-doc="{html.escape(h["file"])}">Open risk register</button></div>'
            "</div></div>")
    elif pending:
        p = pending[0]
        doc = best_doc(vault, p["folder"])
        hero = (
            f'<div class="hero hero-amber"{_doc_attr(doc)}><span class="sq sq-amber hero-sq"></span><div class="hero-body">'
            f'<div class="pills"><span class="pill pill-amber">{html.escape(p["stage"])}</span></div>'
            f'<h3>{p["title"]}</h3><p class="hero-sub">{html.escape(p["next"])}</p>'
            f'<div class="btns"><button class="btn" data-doc="{html.escape(doc)}">Open report</button></div></div></div>')
    else:
        hero = ('<div class="hero hero-green"><span class="sq sq-green hero-sq"></span><div class="hero-body">'
                '<div class="pills"><span class="pill pill-green">All clear</span></div>'
                '<h3>No high risks or pending approvals</h3>'
                '<p class="hero-sub">Every task has cleared its stops and no red-rated risks are open.</p></div></div>')

    if pending:
        items = ""
        for p in pending:
            doc = best_doc(vault, p["folder"])
            approve_btn = (f'<button class="btn btn-go" data-approve="{html.escape(p["folder"])}">Approve →</button>'
                           if actions and p["folder"] else '<button class="btn">Approve</button>')
            items += (
                f'<div class="item"{_doc_attr(doc)}><span class="sq sq-blue"></span><div class="item-b">'
                f'<div class="item-t">{p["title"]}</div>'
                f'<div class="meta">{html.escape(p["stage"])}</div>'
                f'<div class="btns"><button class="btn" data-doc="{html.escape(doc)}">Open report</button>{approve_btn}</div></div></div>')
        approvals = f'<div class="card"><div class="sec-h">Needs your approval</div>{items}</div>'
    else:
        approvals = '<div class="card"><div class="sec-h">Needs your approval</div><p class="empty">Nothing waiting — all stops cleared.</p></div>'

    rl = ""
    for r in risks[:5]:
        rl += (f'<div class="risk"{_doc_attr(r["file"])}><span class="dot dot-{r["sev"]}"></span>'
               f'<span>{r["text"]} <span class="risk-meta">· {r["project"]} {r["id"]}</span></span></div>')
    risks_inner = rl or '<p class="empty">No open risks.</p>'
    risks_card = f'<div class="card"><div class="sec-h">Risks &amp; alerts</div>{risks_inner}</div>'

    al = ""
    for a in activity:
        color, phrase = _stage_phrase(a["stage"])
        t = datetime.fromtimestamp(a["mtime"])
        wa = t.strftime("%-I:%M %p") if t.date() == now.date() else t.strftime("%b %-d")
        doc = best_doc(vault, a["folder"])
        al += (f'<div class="tline"{_doc_attr(doc)}><span class="tt">{wa}</span>'
               f'<span><span class="dot dot-{color} dot-sm"></span>{html.escape(_short(a["title"]))} — {html.escape(phrase)}</span></div>')
    activity_inner = al or '<p class="empty">No recent task activity.</p>'
    activity_card = f'<div class="card"><div class="sec-h">Recent activity</div>{activity_inner}</div>'

    board = ('<div class="board">'
             '<div class="card"><div class="sec-h">Risk matrix — probability × impact</div>'
             '<div class="chart-h"><canvas id="riskMatrix"></canvas></div>'
             '<div class="chart-leg"><span><i class="lg lg-red"></i>high</span><span><i class="lg lg-amber"></i>medium</span>'
             '<span><i class="lg lg-green"></i>low</span><span class="chart-tip">click a bubble to open the risk</span></div></div>'
             '<div class="card"><div class="sec-h">Division at work — agents by activity</div>'
             '<div id="network" class="net"></div></div></div>')
    html_out = (head + summary + gov + kpis + roi + gz + hero
                + '<div class="cols"><div class="col">' + approvals + "</div>"
                + '<div class="col">' + risks_card + activity_card + "</div></div>"
                + board)
    return html_out, data


PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Division dashboard — morning briefing</title>
<style>
:root{--bg:#1b1a17;--card:#25241f;--tile:#211f1a;--bd:rgba(255,255,255,.10);--bd2:rgba(255,255,255,.18);
--t1:#ECEAE2;--t2:#A8A49A;--t3:#76726A;
--blue:#8FBDEE;--blue-b:rgba(55,138,221,.6);--blue-bg:rgba(55,138,221,.14);
--amber:#F4C879;--amber-b:rgba(239,159,39,.6);--amber-bg:rgba(239,159,39,.14);
--red:#F09A9A;--red-b:rgba(226,75,74,.6);--red-bg:rgba(226,75,74,.15);
--green:#A6CE6A;--green-bg:rgba(99,153,34,.15);--gray-b:rgba(255,255,255,.22);}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--t1);
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.5;}
.wrap{max-width:1040px;margin:0 auto;padding:22px 22px 56px;}
.hdr{display:flex;justify-content:space-between;align-items:flex-start;gap:14px;flex-wrap:wrap;margin-bottom:12px;}
h1{margin:0;font-size:26px;font-weight:600;} .sub{margin:5px 0 0;font-size:14px;color:var(--t2);}
.hdr-r{text-align:right;} .div{margin:8px 0 0;font-size:13px;color:var(--t3);}
.brand{display:flex;align-items:center;gap:10px;justify-content:flex-end;}
.co{font-size:14px;font-weight:600;color:var(--t1);}
.live{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:var(--green);}
.ld{width:7px;height:7px;border-radius:50%;background:var(--green);animation:p 1.8s ease-in-out infinite;}
@keyframes p{0%,100%{opacity:1}50%{opacity:.35}}
.summary{font-size:16px;color:var(--t1);background:var(--card);border:.5px solid var(--bd);border-left:3px solid var(--blue-b);
border-radius:10px;padding:11px 16px;margin:0 0 12px;}
.gov{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 16px;}
.gov .gv{font-size:12px;color:var(--green);background:var(--green-bg);border:.5px solid rgba(99,153,34,.35);border-radius:8px;padding:4px 10px;}
body.present .gov .gv{font-size:13px;}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:13px;margin-bottom:13px;}
.kpi{background:var(--tile);border-radius:11px;padding:14px 16px;}
.kpi-top{display:flex;align-items:center;gap:11px;} .kpi-v{font-size:25px;font-weight:600;}
.kpi-l{font-size:13px;color:var(--t2);margin-top:7px;}
.dl{font-size:12px;font-weight:600;margin-left:2px;} .dl-red{color:var(--red);} .dl-green{color:var(--green);}
.dl-amber{color:var(--amber);} .dl-blue{color:var(--blue);} .dl-gray{color:var(--t3);}
.sq{width:30px;height:30px;border-radius:8px;flex:none;}
.sq-blue{background:var(--blue-bg);border:1.5px solid var(--blue-b);}
.sq-amber{background:var(--amber-bg);border:1.5px solid var(--amber-b);}
.sq-red{background:var(--red-bg);border:1.5px solid var(--red-b);}
.sq-green{background:var(--green-bg);border:1.5px solid rgba(99,153,34,.6);}
.sq-gray{background:rgba(255,255,255,.06);border:1.5px solid var(--gray-b);}
.roi{display:flex;align-items:center;gap:10px;background:var(--green-bg);border:.5px solid rgba(99,153,34,.4);
border-radius:11px;padding:11px 16px;margin-bottom:16px;font-size:14px;color:var(--t1);}
.roi b{color:var(--green);font-weight:600;} .roi-ic{color:var(--green);font-size:18px;}
.card{background:var(--card);border:.5px solid var(--bd);border-radius:13px;padding:16px 19px;}
.sec-h{font-size:16px;font-weight:600;margin:0 0 6px;}
.hero{display:flex;gap:13px;background:var(--card);border-radius:13px;padding:17px 19px;margin-bottom:16px;}
.hero-red{border:2px solid var(--red-b);} .hero-amber{border:2px solid var(--amber-b);} .hero-green{border:.5px solid var(--bd);}
.hero-sq{width:38px;height:38px;} .hero-body{flex:1;min-width:0;}
.pills{display:flex;gap:8px;flex-wrap:wrap;} .pill{font-size:11px;font-weight:500;padding:3px 9px;border-radius:8px;}
.pill-red{color:var(--red);background:var(--red-bg);} .pill-amber{color:var(--amber);background:var(--amber-bg);}
.pill-green{color:var(--green);background:var(--green-bg);} .pill-gray{color:var(--t2);background:rgba(255,255,255,.07);}
.hero h3{margin:9px 0 5px;font-size:16px;font-weight:600;} .hero-sub{margin:0;font-size:13px;color:var(--t2);line-height:1.55;}
.btns{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;}
.btn{font-size:12px;padding:5px 13px;border-radius:8px;border:.5px solid var(--bd2);background:transparent;color:var(--t1);cursor:pointer;}
.btn:hover{background:rgba(255,255,255,.06);} .btn-go{border-color:var(--green);color:var(--green);}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:start;}
.col{display:flex;flex-direction:column;gap:16px;}
.item{display:flex;gap:12px;padding:13px 0;border-top:.5px solid var(--bd);border-radius:8px;}
.item:first-of-type{border-top:none;} .item-b{flex:1;min-width:0;} .item-t{font-size:14px;font-weight:500;}
.meta{font-size:12px;color:var(--t2);margin-top:3px;}
.risk{display:flex;gap:10px;padding:7px 0;font-size:13px;border-radius:8px;}
.risk+.risk{border-top:.5px solid var(--bd);} .risk-meta{color:var(--t3);font-size:12px;}
.dot{width:9px;height:9px;border-radius:50%;flex:none;margin-top:5px;}
.dot-sm{width:7px;height:7px;display:inline-block;margin:0 7px 1px 0;vertical-align:middle;}
.dot-red{background:var(--red);} .dot-amber{background:var(--amber);} .dot-green{background:var(--green);} .dot-blue{background:var(--blue);}
.tline{display:flex;gap:11px;padding:5px 0;font-size:13px;border-radius:8px;}
.tt{color:var(--t3);flex:none;min-width:62px;font-variant-numeric:tabular-nums;}
.empty{color:var(--t3);font-size:13px;margin:6px 0 0;}
.clk{cursor:pointer;} .clk:hover{background:rgba(255,255,255,.04);}
.foot{margin-top:26px;font-size:12px;color:var(--t3);}
.gauges{display:grid;grid-template-columns:repeat(4,1fr);gap:13px;margin-bottom:16px;}
.gz{background:var(--tile);border-radius:11px;padding:12px 12px 10px;text-align:center;}
.gz-c{position:relative;height:92px;} .gz-c canvas{max-height:92px;}
.gz-center{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:21px;font-weight:600;color:var(--t1);}
.gz-l{font-size:12.5px;color:var(--t2);margin-top:8px;font-weight:500;} .gz-sub{font-size:11px;color:var(--t3);margin-top:2px;}
.sparkwrap{height:24px;margin-top:8px;position:relative;}
.board{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px;align-items:start;}
.chart-h{position:relative;height:300px;}
.chart-leg{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--t2);margin-top:10px;align-items:center;}
.chart-leg .lg{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:-1px;}
.lg-red{background:var(--red);} .lg-amber{background:var(--amber);} .lg-green{background:var(--green);} .chart-tip{margin-left:auto;color:var(--t3);}
.net{height:320px;} .net circle.hot{animation:hot 1.7s ease-in-out infinite;}
@keyframes hot{0%,100%{opacity:1}50%{opacity:.45}}
body.present .gz-c{height:120px} body.present .gz-c canvas{max-height:120px} body.present .chart-h{height:360px} body.present .net{height:380px}
#ov{position:fixed;inset:0;background:rgba(0,0,0,.6);display:none;z-index:50;} #ov.on{display:block;overflow:auto;}
#panel{background:var(--card);border:.5px solid var(--bd2);border-radius:14px;max-width:840px;width:calc(100% - 32px);margin:36px auto;}
#ph{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:14px 20px;border-bottom:.5px solid var(--bd);position:sticky;top:0;background:var(--card);border-radius:14px 14px 0 0;}
#pt{margin:0;font-size:16px;font-weight:600;}
#x{cursor:pointer;border:.5px solid var(--bd2);background:transparent;color:var(--t1);border-radius:8px;padding:5px 12px;font-size:13px;}
#pb{padding:18px 24px 28px;font-size:14px;line-height:1.65;}
#pb h1{font-size:21px} #pb h2{font-size:17px;margin-top:22px} #pb h3{font-size:15px}
#pb table{border-collapse:collapse;width:100%;font-size:12.5px;margin:10px 0}
#pb th,#pb td{border:.5px solid var(--bd);padding:7px 10px;text-align:left;vertical-align:top}
#pb th{background:rgba(255,255,255,.05)} #pb code{background:rgba(255,255,255,.07);padding:1px 5px;border-radius:5px}
#pb a.dl,#pb a{color:var(--blue);cursor:pointer} #pb ul{padding-left:20px} #pb li{margin:4px 0}
#pb .callout{border:.5px solid var(--bd);border-radius:10px;padding:10px 14px;margin:12px 0;background:rgba(255,255,255,.03)}
#pb .co-t{font-weight:600;margin-bottom:6px} #pb hr{border:0;border-top:.5px solid var(--bd);margin:18px 0}
.spin{display:inline-block;width:16px;height:16px;border:2px solid var(--bd2);border-top-color:var(--green);border-radius:50%;animation:sp 1s linear infinite;vertical-align:-3px;margin-right:8px}
@keyframes sp{to{transform:rotate(360deg)}}
body.present{font-size:18px} body.present .wrap{max-width:1280px;padding:34px 34px 60px}
body.present h1{font-size:34px} body.present .kpi-v{font-size:34px} body.present .summary{font-size:19px}
body.present .sec-h{font-size:19px} body.present .hero h3{font-size:21px} body.present .roi{font-size:16px}
@media print{body{background:#fff;color:#111}.live,.btn,#exportbtn,.foot,#ov,.brand{display:none!important}
.card,.kpi,.hero,.summary{border:1px solid #ccc!important;background:#fff!important}
.summary,.item-t,.kpi-v,.hero h3,.sec-h,h1{color:#111!important}
.sub,.div,.meta,.kpi-l,.risk-meta,.hero-sub,.tt{color:#555!important}
.roi{background:#eef6ea!important;color:#1a3a1a!important}.roi b{color:#1a3a1a!important}}
@media(max-width:720px){.kpis{grid-template-columns:repeat(2,1fr)}.cols{grid-template-columns:1fr}}
</style></head><body class="__BODYCLASS__">
<main class="wrap">
<div id="content">__CONTENT__</div>
<div class="foot" id="foot">read-only · click any item to open its document · generated __GENERATED__</div>
</main>
<div id="ov"><div id="panel"><div id="ph"><h2 id="pt">Document</h2><button id="x" onclick="closeDoc()">Close ✕</button></div><div id="pb"></div></div></div>
<script src="/lib/chart.umd.min.js"></script>
<script src="/lib/d3.min.js"></script>
<script>
var POLL=__POLL_MS__, PRESENT=__PRESENT__, lastM="__MTIME__", DASH=__DATA__;
var CH={},C={red:'#E24B4A',amber:'#EF9F27',green:'#639922',blue:'#378ADD',t2:'#A8A49A',grid:'rgba(255,255,255,.08)',track:'rgba(255,255,255,.07)'};
function modalOpen(){return document.getElementById('ov').classList.contains('on');}
function mk(id,cfg){var el=document.getElementById(id);if(!el||!window.Chart)return;if(CH[id]){CH[id].destroy();}CH[id]=new Chart(el,cfg);}
function ring(id,pct,color){pct=Math.max(0,Math.min(100,Math.round(pct)));mk(id,{type:'doughnut',data:{datasets:[{data:[pct,100-pct],backgroundColor:[color,C.track],borderWidth:0}]},options:{cutout:'74%',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{enabled:false}},animation:{duration:PRESENT?900:0}}});}
function setTx(id,t){var e=document.getElementById(id);if(e)e.textContent=t;}
var LC={};
function animateCounters(){document.querySelectorAll('.kpi-v[data-count]').forEach(function(el){
var tgt=parseFloat(el.getAttribute('data-count')),dec=parseInt(el.getAttribute('data-dec')||'0'),pre=el.getAttribute('data-prefix')||'';
var lab=el.parentNode.parentNode.querySelector('.kpi-l');var key=pre+'|'+(lab?lab.textContent:'');
function show(v){el.textContent=pre+v.toFixed(dec);}
if(LC[key]===tgt){show(tgt);return;}var from=LC[key]||0;LC[key]=tgt;var t0=performance.now();
function step(t){var k=Math.min(1,(t-t0)/700);show(from+(tgt-from)*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(step);}requestAnimationFrame(step);});}
function buildNetwork(d){var wrap=document.getElementById('network');if(!wrap||!window.d3||!d.network||!d.network.nodes.length)return;
wrap.innerHTML='';var W=wrap.clientWidth||520,H=wrap.clientHeight||320,pal=['#7F77DD','#1D9E75','#D85A30','#378ADD','#D4537E','#BA7517'],di=0,dc={};
var nodes=d.network.nodes.map(function(n){return Object.assign({},n);}),links=d.network.links.map(function(l){return Object.assign({},l);});
nodes.forEach(function(n){if(n.type==='dept'){dc[n.id]=pal[di++%pal.length];}});
var svg=d3.select(wrap).append('svg').attr('width','100%').attr('height',H).attr('viewBox','0 0 '+W+' '+H);
var sim=d3.forceSimulation(nodes).force('link',d3.forceLink(links).id(function(n){return n.id;}).distance(38).strength(.45)).force('charge',d3.forceManyBody().strength(-85)).force('center',d3.forceCenter(W/2,H/2)).force('collide',d3.forceCollide(13));
var link=svg.append('g').attr('stroke','rgba(255,255,255,.10)').selectAll('line').data(links).join('line');
var node=svg.append('g').selectAll('circle').data(nodes).join('circle').attr('r',function(n){return n.type==='dept'?Math.min(20,9+Math.sqrt(n.activity||0)*1.6):Math.min(12,4+Math.sqrt(n.activity||0));}).attr('fill',function(n){return n.type==='dept'?dc[n.id]:'rgba(236,234,226,.30)';}).attr('stroke',function(n){return n.type==='dept'?'rgba(255,255,255,.25)':'none';}).attr('class',function(n){return (n.activity||0)>50?'hot':'';});
node.append('title').text(function(n){return n.label+' · '+(n.activity||0)+' active';});
var lab=svg.append('g').selectAll('text').data(nodes.filter(function(n){return n.type==='dept';})).join('text').text(function(n){return n.label;}).attr('font-size',10).attr('fill','#ECEAE2').attr('text-anchor','middle');
sim.on('tick',function(){link.attr('x1',function(l){return l.source.x;}).attr('y1',function(l){return l.source.y;}).attr('x2',function(l){return l.target.x;}).attr('y2',function(l){return l.target.y;});
node.attr('cx',function(n){return n.x=Math.max(12,Math.min(W-12,n.x));}).attr('cy',function(n){return n.y=Math.max(12,Math.min(H-12,n.y));});
lab.attr('x',function(n){return n.x;}).attr('y',function(n){return n.y-14;});});}
function renderVisuals(d){if(!d)return;try{
mk('healthDonut',{type:'doughnut',data:{labels:['high','medium','low'],datasets:[{data:[d.health.red,d.health.amber,d.health.green],backgroundColor:[C.red,C.amber,C.green],borderWidth:0}]},options:{cutout:'66%',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},animation:{duration:PRESENT?900:0}}});
setTx('healthCenter',d.health.red+d.health.amber+d.health.green);
ring('pipeGauge',d.pipeline.pct,C.green);setTx('pipeCenter',d.pipeline.pct+'%');
(d.targets||[]).forEach(function(t,i){ring('tg'+i,t.pct,C.blue);setTx('tgc'+i,t.pct+'%');});
if(d.riskPoints&&d.riskPoints.length){mk('riskMatrix',{type:'bubble',data:{datasets:[{data:d.riskPoints.map(function(p){return{x:p.x,y:p.y,r:9};}),backgroundColor:d.riskPoints.map(function(p){return p.sev==='red'?C.red:p.sev==='amber'?C.amber:C.green;})}]},options:{responsive:true,maintainAspectRatio:false,onClick:function(e,els){if(els.length){var p=d.riskPoints[els[0].index];if(p&&p.file)openDoc(p.file);}},plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){var p=d.riskPoints[c.dataIndex];return p.id+' · '+p.label;}}}},scales:{x:{min:.5,max:5.5,title:{display:true,text:'probability →',color:C.t2},ticks:{stepSize:1,color:C.t2},grid:{color:C.grid}},y:{min:.5,max:5.5,title:{display:true,text:'impact →',color:C.t2},ticks:{stepSize:1,color:C.t2},grid:{color:C.grid}}}}});}
if(d.spark&&d.spark.length){mk('spark',{type:'line',data:{labels:d.spark.map(function(_,i){return i;}),datasets:[{data:d.spark,borderColor:C.green,borderWidth:1.5,pointRadius:0,tension:.35}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{enabled:false}},scales:{x:{display:false},y:{display:false}},animation:false}});}
animateCounters();buildNetwork(d);}catch(e){}}
async function poll(){try{var r=await fetch('/fragment?t='+Date.now());if(!r.ok)return;var j=await r.json();
if(j.mtime!==lastM && !modalOpen()){document.getElementById('content').innerHTML=j.html;lastM=j.mtime;renderVisuals(j.data);}
document.getElementById('foot').textContent='live · updated '+new Date().toLocaleTimeString();}catch(e){}}
if(!PRESENT)setInterval(poll,POLL);
function showPanel(t,h){document.getElementById('pt').textContent=t;document.getElementById('pb').innerHTML=h;var ov=document.getElementById('ov');ov.classList.add('on');ov.scrollTop=0;}
async function openDoc(p){if(!p)return;try{var r=await fetch('/doc?path='+encodeURIComponent(p));var j=await r.json();showPanel(j.title||'Document',j.error?('<p>'+j.error+'</p>'):j.html);}catch(e){}}
function closeDoc(){document.getElementById('ov').classList.remove('on');}
var APMSG=['Reviewing the decision report and execution plan…','Drafting the engineering change order…','Drafting the supplier qualification report…','Drafting the first-article inspection report…','Formatting and filing the documents…'];
var EMBEDDED=(function(){try{return window.self!==window.top;}catch(e){return true;}})();
function askApprove(){
/* confirm() is suppressed inside a sandboxed iframe (e.g. the Obsidian embed): without allow-modals it
   silently returns false, which would abort the approve. When embedded, the explicit button click IS the
   confirmation, so skip the dialog. Top-level (the standalone demo window) still gets the confirm. */
if(EMBEDDED)return true;
try{return window.confirm('Approve this decision and draft the documents live? The agents write each one — about a minute.');}
catch(e){return true;}}
async function runApprove(folder){if(askApprove()===false)return;
var mi=0;function tick(){showPanel('Drafting documents…','<p><span class="spin"></span>'+APMSG[Math.min(mi,APMSG.length-1)]+'</p><p style="color:var(--t3);font-size:12px">the agents are writing each document from the approved decision</p>');mi++;}
tick();var iv=setInterval(tick,12000);
try{var r=await fetch('/action/approve?folder='+encodeURIComponent(folder),{method:'POST'});var j=await r.json();clearInterval(iv);
if(j.error){showPanel('Action','<p>'+j.error+'</p>');return;}
var h='<p>';j.steps.forEach(function(s){h+=(s.ok?'✓':'✗')+' '+s.cmd+'<br/>';});h+='</p>';
if(j.outputs&&j.outputs.length){h+='<p><b>Documents generated:</b></p><ul>';j.outputs.forEach(function(o){h+='<li>'+o+'</li>';});h+='</ul>';
h+='<p><button class="btn btn-go" data-reveal="'+folder+'">Open documents in Finder ↗</button></p>';}
if(j.plan){h+='<p><a class="dl" data-doc="'+j.plan+'">Open the execution plan →</a></p>';}
showPanel('Approved — documents ready',h);}catch(e){clearInterval(iv);showPanel('Action','<p>Action failed.</p>');}}
async function revealDocs(folder){try{await fetch('/action/reveal?folder='+encodeURIComponent(folder),{method:'POST'});}catch(e){}}
document.addEventListener('click',function(e){var ap=e.target.closest('[data-approve]');if(ap){e.preventDefault();e.stopPropagation();runApprove(ap.getAttribute('data-approve'));return;}
var rv=e.target.closest('[data-reveal]');if(rv){e.preventDefault();e.stopPropagation();revealDocs(rv.getAttribute('data-reveal'));return;}
if(e.target.closest('#panel')&&!e.target.closest('[data-doc]'))return;var t=e.target.closest('[data-doc]');if(t){e.preventDefault();e.stopPropagation();openDoc(t.getAttribute('data-doc'));return;}
if(e.target.id==='ov')closeDoc();});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeDoc();});
window.addEventListener('load',function(){renderVisuals(DASH);});
</script>
</body></html>"""


class Handler(BaseHTTPRequestHandler):
    dash_file = Path("00-Dashboard.md")
    vault = Path(".")
    owner = "Brian"
    division = "Hardware engineering & supply chain division"
    company = ""
    logo = ""
    rate = 75.0
    hours = 6.0
    actions = False
    poll_ms = 8000

    def log_message(self, *a):
        pass

    def _read(self):
        p = self.dash_file
        if not p.exists():
            return None, "0", None
        md = p.read_text(encoding="utf-8")  # READ ONLY
        return md, str(p.stat().st_mtime), parse_meta(md).get("generated")

    def _content(self, md):
        if md is None:
            return f'<div class="card">Source not found: {html.escape(str(self.dash_file))}. Run agent_dashboard.py first.</div>', {}
        return render_content(md, self.vault, self.owner, self.division, self.company,
                              self.logo, self.rate, self.hours, self.actions)

    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        path = u.path
        if path in ("/", "/index.html"):
            md, mtime, gen = self._read()
            present = "present" in parse_qs(u.query)
            content, data = self._content(md)
            djson = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
            page = (PAGE.replace("__CONTENT__", content)
                    .replace("__BODYCLASS__", "present" if present else "")
                    .replace("__DATA__", djson)
                    .replace("__PRESENT__", "true" if present else "false")
                    .replace("__GENERATED__", html.escape(gen or "—"))
                    .replace("__MTIME__", mtime).replace("__POLL_MS__", str(self.poll_ms)))
            self._send(200, page)
        elif path == "/fragment":
            md, mtime, gen = self._read()
            content, data = self._content(md)
            self._send(200, json.dumps({"html": content, "mtime": mtime, "data": data}, ensure_ascii=False), "application/json")
        elif path == "/doc":
            rel = parse_qs(u.query).get("path", [""])[0]
            try:
                target = (self.vault / rel).resolve()
            except (OSError, ValueError):
                target = None
            if (not target or not str(target).startswith(str(self.vault) + "/")
                    or target.suffix.lower() != ".md" or not target.is_file()):
                self._send(404, json.dumps({"error": "Document not found or outside the vault."}), "application/json")
                return
            doc = target.read_text(encoding="utf-8")  # READ ONLY
            m = re.search(r"^#\s+(.+)$", doc, re.M)
            title = html.escape((m.group(1).strip() if m else target.stem))
            self._send(200, json.dumps({"title": title, "html": md_to_html(doc, self.vault)}), "application/json")
        elif path.startswith("/lib/"):
            name = path[len("/lib/"):]
            f = (VENDOR / name).resolve()
            if name in ("chart.umd.min.js", "d3.min.js") and str(f).startswith(str(VENDOR) + "/") and f.is_file():
                self._send(200, f.read_text(encoding="utf-8"), "application/javascript; charset=utf-8")
            else:
                self._send(404, "not found", "text/plain")
        elif path == "/health":
            self._send(200, "ok", "text/plain")
        else:
            self._send(404, "not found", "text/plain")

    def do_POST(self):
        u = urlparse(self.path)
        if not self.actions:
            self._send(403, json.dumps({"error": "Live actions are disabled. Start the server with --enable-actions (demo mode)."}), "application/json")
            return
        if u.path == "/action/approve":
            folder = parse_qs(u.query).get("folder", [""])[0]
            tdir = (self.vault / "02-Tasks" / folder).resolve()
            if (not str(tdir).startswith(str(self.vault / "02-Tasks") + "/")
                    or not (tdir / "07-decision-report.md").is_file()):
                self._send(404, json.dumps({"error": "Task not ready — no decision report to approve."}), "application/json")
                return
            bdos = self.vault / ".venv" / "bin" / "bd-os"
            base = [str(bdos)] if bdos.exists() else [sys.executable, "-m", "core.cli"]
            # Pre-staged tasks already have a valid plan -> render deterministically (no LLM).
            cmds = ("execute",) if plan_is_valid(self.vault, tdir) else ("approve", "execute")
            steps = []
            for cmd in cmds:
                try:
                    r = subprocess.run(base + [cmd, str(tdir)], cwd=str(self.vault),
                                       capture_output=True, text=True, timeout=240)
                    steps.append({"cmd": cmd, "ok": r.returncode == 0,
                                  "out": (r.stdout or r.stderr or "")[-400:]})
                    if r.returncode != 0:
                        break
                except Exception as e:  # noqa: BLE001
                    steps.append({"cmd": cmd, "ok": False, "out": str(e)})
                    break
            outdir = self.vault / "03-Outputs" / folder
            outs = sorted(f.name for f in outdir.glob("*.docx")) if outdir.exists() else []
            plan = f"02-Tasks/{folder}/08-execution-plan.md"
            self._send(200, json.dumps({"steps": steps, "outputs": outs,
                                        "plan": plan if (self.vault / plan).is_file() else ""}), "application/json")
        elif u.path == "/action/reveal":
            folder = parse_qs(u.query).get("folder", [""])[0]
            outdir = (self.vault / "03-Outputs" / folder).resolve()
            if str(outdir).startswith(str(self.vault / "03-Outputs") + "/") and outdir.is_dir():
                try:
                    subprocess.Popen(["open", str(outdir)])
                except Exception:  # noqa: BLE001
                    pass
                self._send(200, json.dumps({"ok": True}), "application/json")
            else:
                self._send(404, json.dumps({"error": "No outputs to reveal yet."}), "application/json")
        else:
            self._send(404, "not found", "text/plain")


def main():
    here = Path(__file__).resolve()
    repo_root = here.parents[2]
    ap = argparse.ArgumentParser(description="Live interactive morning dashboard (demo edition)")
    ap.add_argument("--vault", type=Path, default=repo_root)
    ap.add_argument("--file", type=Path, default=None)
    ap.add_argument("--owner", default="Brian")
    ap.add_argument("--division", default="Hardware engineering & supply chain division")
    ap.add_argument("--company", default="")
    ap.add_argument("--logo", default="", help="Path to a logo image (inlined as data URI)")
    ap.add_argument("--analyst-rate", type=float, default=75.0, help="Loaded $/hr for the ROI banner")
    ap.add_argument("--hours-per-task", type=float, default=6.0, help="Analyst-hours equivalent per decision")
    ap.add_argument("--enable-actions", action="store_true", help="Enable the live Approve→execute action (demo)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--poll", type=int, default=8)
    args = ap.parse_args()

    Handler.vault = args.vault.resolve()
    Handler.dash_file = (args.file or (args.vault / "00-Dashboard.md")).resolve()
    Handler.owner = args.owner
    Handler.division = args.division
    Handler.company = args.company
    Handler.rate = args.analyst_rate
    Handler.hours = args.hours_per_task
    Handler.actions = args.enable_actions
    Handler.poll_ms = max(2, args.poll) * 1000

    if args.logo:
        lp = Path(args.logo)
        if not lp.is_absolute():
            lp = Handler.vault / args.logo
        if lp.is_file():
            mime = "image/png" if lp.suffix.lower() == ".png" else "image/jpeg" if lp.suffix.lower() in (".jpg", ".jpeg") else "image/svg+xml" if lp.suffix.lower() == ".svg" else "image/png"
            Handler.logo = f"data:{mime};base64," + base64.b64encode(lp.read_bytes()).decode()

    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    url = f"http://{args.host}:{args.port}/"
    print("Morning dashboard (demo edition):")
    print(f"  source : {Handler.dash_file}  {'(found)' if Handler.dash_file.exists() else '(MISSING — run agent_dashboard.py)'}")
    print(f"  url    : {url}   (present mode: {url}?present=1)")
    print(f"  actions: {'ENABLED (live approve)' if Handler.actions else 'disabled (read-only)'}")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
