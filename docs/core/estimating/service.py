"""Estimate Service — the HTTP face of the pipeline for a company-OS app (contract v1).

Starlette (already a dependency via mcp) + uvicorn. Loopback by default
set CE_SERVICE_TOKEN to require an
`X-Api-Key` header. Every handler is a thin wrapper over `core.estimating.pipeline`
nothing is computed here.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route

from core.estimating import CONTRACT_VERSION, engine_version, pipeline
from core.estimating.rfi import EstimateQuestion, auto_assume_all


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _envelope(folder: Path | None, **payload) -> JSONResponse:
    return JSONResponse({"engine_version": engine_version(), "contract_version": CONTRACT_VERSION, "folder": folder.name if folder else None} | payload)


def _error(status: int, message: str) -> JSONResponse:
    return JSONResponse({"error": message, "contract_version": CONTRACT_VERSION}, status_code=status)


class _TokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        token = os.getenv("CE_SERVICE_TOKEN", "")
        if token and request.url.path != "/health" and request.headers.get("x-api-key") != token:
            return _error(401, "missing or invalid X-Api-Key")
        return await call_next(request)


def apply_answer_payload(folder: Path, payload: dict) -> list[EstimateQuestion]:
    """`{auto_assume: true}` or `{answers: [{match, answer?, assumption?}]}` (match = question text prefix)."""
    if payload.get("auto_assume"):
        return auto_assume_all(folder)
    js = folder / "05-questions.json"
    qs = [EstimateQuestion(**d) for d in _load(js)]
    for a in payload.get("answers") or []:
        m = str(a.get("match", "")).strip().lower()
        for q in qs:
            if m and q.text.lower().startswith(m):
                if a.get("assumption"):
                    q.assumption = str(a["assumption"])
                if a.get("answer"):
                    q.answer = str(a["answer"])
    js.write_text(json.dumps([q.to_dict() for q in qs], indent=2), encoding="utf-8")
    return qs


def create_app(vault_root: Path) -> Starlette:
    vault_root = Path(vault_root).resolve()
    estimates = vault_root / pipeline.ESTIMATES_DIR

    def folder_of(request: Request) -> Path | None:
        f = estimates / request.path_params["id"]
        return f if f.is_dir() and f.resolve().parent == estimates.resolve() else None

    async def health(request: Request):
        from core.estimating.playbooks import list_playbooks

        return _envelope(None, vault=str(vault_root), playbooks=sorted(list_playbooks()))

    async def intake(request: Request):
        body = await request.json()
        try:
            folder = pipeline.intake(vault_root, Path(body["package_dir"]), body["name"], body["building_type"], body.get("city", "Dallas"),
                                     int(body.get("aace_class") or 2), body.get("gross_sf"), render=bool(body.get("render", False)))
        except (KeyError, FileNotFoundError, ValueError) as e:
            return _error(400, f"{type(e).__name__}: {e}")
        return _envelope(folder, profile=_load(folder / "00-project-profile.json"), sheet_register=_load(folder / "01-sheet-register.json"),
                         spec_sections=_load(folder / "02-spec-index.json").get("sections", []), division_01=_load(folder / "02-division-01.json"))

    async def takeoff(request: Request):
        folder = folder_of(request)
        if not folder:
            return _error(404, "unknown estimate")
        body = await request.json() if await request.body() else {}
        if body.get("reader_lines"):
            tmp = folder / "readers" / "service-lines.json"
            tmp.parent.mkdir(exist_ok=True)
            tmp.write_text(json.dumps(body["reader_lines"]), encoding="utf-8")
            led = pipeline.merge_reader_lines(folder, tmp)
            checks = _load(folder / "03-takeoff-checks.json") if (folder / "03-takeoff-checks.json").exists() else []
        else:
            led, checks = pipeline.seed_takeoff(folder)
        return _envelope(folder, ledger=_load(folder / "04-takeoff-ledger.json"), checks=checks, discrepancies=_load(folder / "04-discrepancies.json"))

    async def rfi(request: Request):
        folder = folder_of(request)
        if not folder:
            return _error(404, "unknown estimate")
        pipeline.rfi(folder)
        return _envelope(folder, questions=_load(folder / "05-questions.json"))

    async def answers(request: Request):
        folder = folder_of(request)
        if not folder:
            return _error(404, "unknown estimate")
        body = await request.json() if await request.body() else {}
        qs = apply_answer_payload(folder, body)
        open_crit = sum(1 for q in qs if q.severity == "CRITICAL" and not q.answer and not q.assumption)
        return _envelope(folder, questions=[q.to_dict() for q in qs], open_critical=open_crit)

    async def price(request: Request):
        folder = folder_of(request)
        if not folder:
            return _error(404, "unknown estimate")
        est = pipeline.price(folder, vault_root)
        return _envelope(folder, **est)

    async def review(request: Request):
        folder = folder_of(request)
        if not folder:
            return _error(404, "unknown estimate")
        gates, verdict = pipeline.review(folder)
        return _envelope(folder, verdict=verdict, gates=gates, client_findings=_load(folder / "09-client-safe-findings.json"))

    async def report(request: Request):
        folder = folder_of(request)
        if not folder:
            return _error(404, "unknown estimate")
        out = pipeline.report(folder)
        return _envelope(folder, report_md=out.read_text(encoding="utf-8"), proposal_md=(folder / "09-proposal-draft.md").read_text(encoding="utf-8"),
                         client_findings=_load(folder / "09-client-safe-findings.json"))

    async def approve(request: Request):
        folder = folder_of(request)
        if not folder:
            return _error(404, "unknown estimate")
        outs = pipeline.approve(folder, vault_root)
        return _envelope(folder, outputs=[str(o) for o in outs])

    async def rom(request: Request):
        body = await request.json()
        try:
            folder = pipeline.rom(vault_root, body)
        except (KeyError, ValueError) as e:
            return _error(400, f"{type(e).__name__}: {e}")
        est = _load(folder / "06-estimate.json")
        sc = _load(folder / "07-review-scorecard.json")
        return _envelope(folder, profile=_load(folder / "00-project-profile.json"), three_point=est["meta"]["three_point"], aace_class=est["meta"]["aace_class"],
                         accuracy_band=est["meta"]["accuracy_band"], verdict=sc["verdict"], gates=sc["gates"], questions=_load(folder / "05-questions.json"),
                         summary_by_division=est["summary_by_division"], risks=_load(folder / "06-risks.json"),
                         proposal_md=(folder / "09-proposal-draft.md").read_text(encoding="utf-8"), client_findings=_load(folder / "09-client-safe-findings.json"))

    async def file(request: Request):
        folder = folder_of(request)
        name = request.path_params["name"]
        if not folder or "/" in name or name.startswith(".") or not (folder / name).is_file():
            return _error(404, "unknown file")
        p = folder / name
        if p.suffix == ".json":
            return JSONResponse(_load(p))
        return PlainTextResponse(p.read_text(encoding="utf-8"))

    routes = [
        Route("/health", health), Route("/estimates/intake", intake, methods=["POST"]), Route("/estimates/rom", rom, methods=["POST"]),
        Route("/estimates/{id}/takeoff", takeoff, methods=["POST"]), Route("/estimates/{id}/rfi", rfi, methods=["POST"]),
        Route("/estimates/{id}/answers", answers, methods=["POST"]), Route("/estimates/{id}/price", price, methods=["POST"]),
        Route("/estimates/{id}/review", review, methods=["POST"]), Route("/estimates/{id}/report", report, methods=["POST"]),
        Route("/estimates/{id}/approve", approve, methods=["POST"]), Route("/estimates/{id}/files/{name}", file),
    ]
    return Starlette(routes=routes, middleware=[Middleware(_TokenMiddleware)])


def serve(vault_root: Path, host: str = "127.0.0.1", port: int = 8801) -> None:
    import uvicorn

    uvicorn.run(create_app(vault_root), host=host, port=port, log_level="info")
