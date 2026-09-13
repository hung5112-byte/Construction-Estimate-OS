"""MCP server wrapping construction-estimate-os FlowController as MCP tools.

When running in Claude Desktop / Code, every LLM call routes through MCP sampling
(MCPSamplingProvider) — using the user's subscription, no ANTHROPIC_API_KEY needed.

Run:
    python -m core.mcp_server          # stdio transport
    ce-os-mcp                          # via console_script (after install)

Tools registered (9):
    bd_run         — Stage 1: brief → router → gap → clarify (PAUSE)
    bd_resume      — Stage 2: resume after Department Head answers clarification
    bd_meeting     — Stage 3: research + meeting → 07-decision-report.md (Stop 1)
    bd_approve     — Stage 4: Department Head approves → 08-execution-plan.md (Stop 2)
    bd_execute     — Stage 5: render .docx/.xlsx into 03-Outputs/
    bd_draft       — Single LLM call for boilerplate (SOP, ECO form, RMA letter, policy...) — fast path
    bd_status      — inspect vault (Brain summary + tasks)
    bd_onboard     — run onboard wizard creating new vault scaffold
    bd_upgrade     — refresh existing vault with enriched prompts + aliases
"""
from __future__ import annotations
import os
import re
from pathlib import Path

from mcp.server.fastmcp import Context, FastMCP

from core.brain.reader import BrainReader
from core.llm.providers import MCPSamplingProvider
from core.obsidian.vault import ObsidianVault
from core.onboard import onboard_vault
from core.orchestrator.flow_controller import FlowController
from core.upgrade import upgrade_vault


mcp = FastMCP("construction-estimate-os")


def _pick_llm(ctx: Context):
    """Choose the LLM provider based on env vars.

    BD_OS_LLM_PROVIDER ∈ {claude-cli, anthropic-api, mcp-sampling} overrides
    the heuristic (2026-07-05 ruling: runs move onto the Claude subscription
    via headless `claude -p` — works in every tab, unlike MCP sampling).

    Unset → existing heuristic unchanged:
    - ANTHROPIC_API_KEY set → ClaudeProvider
    - Not set → MCPSamplingProvider (subscription via Claude Desktop; the
      Claude Code tab does NOT support sampling → 'Method not found').
    """
    choice = os.getenv("BD_OS_LLM_PROVIDER", "").strip().lower()
    if choice == "claude-cli":
        from core.llm.providers import ClaudeCLIProvider
        from core.utils.config import load_config
        return ClaudeCLIProvider(
            timeout_seconds=load_config().llm.timeout_seconds,  # None → env → 900s
        )
    if choice == "anthropic-api":
        from core.llm.providers import ClaudeProvider
        return ClaudeProvider()
    if choice == "mcp-sampling":
        return MCPSamplingProvider(ctx.session)

    if os.getenv("ANTHROPIC_API_KEY"):
        from core.llm.providers import ClaudeProvider
        return ClaudeProvider()
    return MCPSamplingProvider(ctx.session)


def _make_fc(vault_root: str, ctx: Context) -> FlowController:
    """Build FlowController bound to current MCP request session.

    Load vault/.env (ANTHROPIC_API_KEY, TAVILY_API_KEY, ...) into os.environ
    before picking the LLM provider (priority: Anthropic API > MCP sampling).
    """
    from core.utils.config import apply_vault_env_to_os
    apply_vault_env_to_os(Path(vault_root))

    llm = _pick_llm(ctx)
    return FlowController(vault_root=Path(vault_root), llm=llm)


def _vault_root_from_task(task_folder: Path) -> Path:
    """Task folders live at <vault>/02-Tasks/<slug>/ — climb 2 levels."""
    return task_folder.parent.parent


@mcp.tool()
async def bd_run(brief: str, vault: str, ctx: Context) -> dict:
    """Stage 1: brief → router → gap → clarification (PAUSE).

    ⏱️ Duration: 20-50s (2-3 LLM calls). Run directly in the Claude Code tab.
    (The Cowork tab has a 60s timeout — switch to the Code tab if it fails.)

    Returns task_folder path + stage. If stage == PAUSE_CLARIFICATION,
    Department Head needs to answer questions in 03-clarification.md before bd_resume.
    """
    fc = _make_fc(vault, ctx)
    result = await fc.arun(brief)
    return {
        "stage": result.stage.value,
        "task_folder": str(result.task_folder),
        "message": result.message,
    }


@mcp.tool()
def bd_resume(task_folder: str, ctx: Context) -> dict:
    """Stage 2: resume after Department Head answers 03-clarification.md.

    Validates all questions answered, writes 03-clarification-answered.md.
    """
    folder = Path(task_folder)
    fc = _make_fc(str(_vault_root_from_task(folder)), ctx)
    result = fc.resume_after_clarification(folder)
    return {
        "stage": result.stage.value,
        "task_folder": str(result.task_folder),
        "message": result.message,
    }


@mcp.tool()
def bd_meeting(
    task_folder: str,
    ctx: Context,
    departments: list[str] | None = None,
) -> dict:
    """Stage 3: research + meeting (Pro/Con + Perspective) + synthesizer.

    ⏱️ Duration: 60-180s (7+ sequential LLM calls). Run in the Claude Code tab
    (10-minute timeout). Do NOT run in the Cowork tab (60s hard cap — will fail).

    Auto-extracts departments from 01-routing.md if not provided.
    Output: 07-decision-report.md (Stop 1).
    """
    folder = Path(task_folder)
    fc = _make_fc(str(_vault_root_from_task(folder)), ctx)

    if not departments:
        routing_path = folder / "01-routing.md"
        if not routing_path.exists():
            return {
                "stage": "ERROR",
                "task_folder": str(folder),
                "message": "01-routing.md not found — run bd_run first",
            }
        m = re.search(r"\*\*Departments:\*\*\s*(.+)", routing_path.read_text(encoding="utf-8"))
        if not m:
            return {
                "stage": "ERROR",
                "task_folder": str(folder),
                "message": "Cannot parse Departments from 01-routing.md",
            }
        departments = [d.strip() for d in m.group(1).split(",") if d.strip()]

    result = fc.run_meeting(folder, departments=departments)
    return {
        "stage": result.stage.value,
        "task_folder": str(result.task_folder),
        "message": result.message,
    }


@mcp.tool()
def bd_approve(task_folder: str, ctx: Context) -> dict:
    """Stage 4: Department Head approves decision report → 08-execution-plan.md (Stop 2)."""
    folder = Path(task_folder)
    fc = _make_fc(str(_vault_root_from_task(folder)), ctx)
    result = fc.approve_decision(folder)
    return {
        "stage": result.stage.value,
        "task_folder": str(result.task_folder),
        "message": result.message,
    }


@mcp.tool()
def bd_execute(task_folder: str, ctx: Context) -> dict:
    """Stage 5: render outputs (.docx/.xlsx) into vault/03-Outputs/<task>/."""
    folder = Path(task_folder)
    fc = _make_fc(str(_vault_root_from_task(folder)), ctx)
    result = fc.execute(folder)
    return {
        "stage": result.stage.value,
        "task_folder": str(result.task_folder),
        "message": result.message,
    }


@mcp.tool()
def bd_ingest(path: str, vault: str, label: str = "internal") -> dict:
    """Ingest a document or folder (docx/pptx/pdf/xlsx/csv/txt) into searchable memory.

    Creates a citable shadow card (.md) next to each binary — provenance,
    extraction confidence, anti-poisoning screening — then refreshes the vault
    search index so agents can find and cite the content immediately.
    ⏱️ seconds per document; first embedding run may add ~1-2s model init.
    """
    from core.ingest.pipeline import ingest_paths
    from core.retrieval.indexer import VaultIndexer

    vault_path = Path(vault)
    src = Path(path)
    if not src.exists():
        return {"ok": False, "message": f"Path not found: {src}"}
    if label not in ("public", "internal", "restricted"):
        return {"ok": False, "message": "label must be public, internal, or restricted"}
    results = ingest_paths(vault_path, [src], label=label)
    ingested = [r for r in results if r.status == "ingested"]
    if ingested:
        VaultIndexer(vault_path).build()
    return {
        "ok": True,
        "ingested": [{"source": r.source, "card": r.card, "confidence": r.confidence,
                      "quarantined": r.quarantined} for r in ingested],
        "skipped_unchanged": sum(r.status == "skipped-unchanged" for r in results),
        "unsupported": [r.source for r in results if r.status == "unsupported"],
        "failed": [{"source": r.source, "error": r.error}
                   for r in results if r.status == "failed"],
    }


@mcp.tool()
def bd_outcome(
    task_folder: str,
    outcome: str,
    quality: float,
    reflection: str = "",
) -> dict:
    """Record the real-world outcome of an approved decision (ADR-004 episodic loop).

    Call when the Department Head reports how a past decision actually played out.
    Flips the decision-ledger entry pending→resolved and writes outcome.md in the
    task folder. quality ∈ [0,1] (1 = the decision worked exactly as intended).
    reflection: 2-4 sentences — was the call right (cite the outcome), which part
    of the thesis held/failed, one concrete lesson. Compose it from the Department
    Head's words; leave empty rather than inventing one.
    """
    from core.brain.ledger import DecisionLedger, ledger_path, write_outcome_note

    folder = Path(task_folder)
    if not 0.0 <= quality <= 1.0:
        return {"ok": False, "message": "quality must be between 0 and 1"}
    if not folder.exists():
        return {"ok": False, "message": f"Task folder not found: {folder}"}
    vault_root = _vault_root_from_task(folder)
    ledger = DecisionLedger(ledger_path(vault_root))
    if not ledger.resolve(folder.name, outcome=outcome, quality=quality, reflection=reflection):
        return {
            "ok": False,
            "message": f"No ledger entry for '{folder.name}' — was this task approved via bd_execute?",
        }
    note = write_outcome_note(folder, outcome=outcome, quality=quality)
    return {
        "ok": True,
        "message": f"Outcome recorded: ledger entry resolved (quality {quality}), {note.name} written.",
    }


@mcp.tool()
async def bd_draft(
    brief: str,
    vault: str,
    ctx: Context,
    doc_type: str = "document",
) -> dict:
    """Fast path: draft one boilerplate document in a single LLM call (no debate).

    ⏱️ Duration: 10-30s (1 LLM call). Works in both the Code tab and the Cowork tab
    (short docs). Long docs (a full SOP set) should run in the Code tab.

    Use for: simple SOPs, ECO forms, RMA disposition letters, work instructions,
    checklists, supplier letters, policies...
    Do NOT use for: strategic decisions or high-risk docs
    (use bd_run → bd_meeting → bd_approve → bd_execute for those).

    Trade-off: fast (~10-30s instead of the 1-3 minutes of bd_run+bd_meeting)
    but it does NOT go through multi-perspective review.

    Args:
        brief: The specific request (e.g. "RMA disposition letter for customer X,
               20 units, out-of-warranty repair quote").
        vault: Vault path.
        doc_type: Document type (e.g. "SOP", "ECO form", "RMA letter", "checklist").

    Returns dict {task_folder, draft_path, message}.
    """
    from core.orchestrator.draft import adraft_document
    from core.utils.config import apply_vault_env_to_os

    vault_path = Path(vault)
    apply_vault_env_to_os(vault_path)

    llm = _pick_llm(ctx)
    return await adraft_document(
        brief=brief,
        vault_root=vault_path,
        llm=llm,
        doc_type=doc_type,
    )


@mcp.tool()
def bd_status(vault: str = "") -> dict:
    """Inspect vault — Brain summary + active depts + tasks + tool availability.

    ⚡ Duration: <1s (no LLM call). Works in any tab (Code / Cowork / Chat).

    Vault resolution: if not passed, read from the env var BD_OS_DEFAULT_VAULT
    (set on Windows via: setx BD_OS_DEFAULT_VAULT "F:\\vaults\\<CompanyName>").

    Live research tools (web/law/local/competitor) only run with a
    TAVILY_API_KEY. bd_status reports which tools are ready vs. skipped so the Department Head
    knows whether the decision report rests on real research or just Brain + LLM knowledge.
    """
    # Fallback: if no vault is passed, read from env BD_OS_DEFAULT_VAULT
    if not vault:
        vault = os.environ.get("BD_OS_DEFAULT_VAULT", "")
        if not vault:
            return {
                "error": (
                    "Vault path not found. How to fix: "
                    "(1) Pass the vault argument vault='F:\\vaults\\<CompanyName>', OR "
                    "(2) Set the env var: setx BD_OS_DEFAULT_VAULT 'F:\\vaults\\<CompanyName>' "
                    "then restart Claude Desktop (quit completely, then reopen)."
                ),
            }
    vault_path = Path(vault)

    # Apply vault/.env to os.environ before checking tool availability
    from core.utils.config import apply_vault_env_to_os
    apply_vault_env_to_os(vault_path)

    try:
        brain = BrainReader(vault_path).load()
    except FileNotFoundError as e:
        return {"error": str(e), "vault": vault}

    vault_obj = ObsidianVault(vault_path)
    tasks = vault_obj.list_tasks()

    from core.orchestrator.research_phase import (
        list_available_tools, list_skipped_tools,
    )

    # P2.5: Report installed packs + compliance refs (PackLoader integration)
    packs_info: list[dict] = []
    try:
        from core.agents.pack_loader import PackLoader
        # Read the vault's .bd-os.yaml to know which packs are installed
        cfg_path = vault_path / ".bd-os.yaml"
        installed_codes: list[str] = []
        if cfg_path.exists():
            import yaml
            cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
            installed_codes = cfg.get("packs", []) or []
        repo = Path(__file__).parent.parent
        loader = PackLoader(repo / "packs")
        for code in installed_codes:
            try:
                pack = loader.load(code)
                packs_info.append({
                    "code": pack.code,
                    "name": pack.name,
                    "version": pack.version,
                    "compliance_refs": pack.compliance_refs,
                })
            except FileNotFoundError:
                pass
    except Exception:  # noqa: BLE001
        pass

    workflow_rules = """📋 OPERATING GUIDE (Claude reads this before handling a task):

🎯 Recommended environment: the Claude Code tab (10-minute timeout, can call every MCP tool).

✅ Every MCP tool is directly callable:
   - bd_status, obsidian_* — instant (<1s)
   - bd_draft — 10-30s (1 LLM call, drafts boilerplate)
   - bd_run — 20-50s (router + clarification)
   - bd_resume — <10s (resume after the Department Head answers clarification)
   - bd_meeting — 60-180s (multi-department debate, 7+ LLM calls)
   - bd_approve — 10-30s
   - bd_execute — 10-30s (render docx/xlsx)

⚠️ Notes by tab:
   - 🟢 Claude Code tab: call every tool directly, no timeout worries
   - 🟡 Cowork tab: only bd_status / bd_draft / obsidian_* work (60s cap)
     → Heavy tasks (bd_run, bd_meeting) will fail. If the user is in Cowork and needs a
        heavy task, tell them to switch to the Code tab (click "</> Code" at the top of Claude Desktop).

🔄 Standard workflow for a task that produces a .docx deliverable:
   1. bd_draft(brief, vault, doc_type)  — fast path for a simple SOP/ECO form/RMA letter
   OR the full pipeline for a strategic decision:
   1. bd_run(brief, vault) → returns task_folder + may PAUSE_CLARIFICATION
   2. (if PAUSE) the Department Head answers 03-clarification.md → bd_resume(task_folder)
   3. bd_meeting(task_folder) → 07-decision-report.md (Stop 1 — Department Head approves)
   4. bd_approve(task_folder) → 08-execution-plan.md (Stop 2 — Department Head approves)
   5. bd_execute(task_folder) → .docx/.xlsx files in 03-Outputs/

After each step, report the task_folder + a summary of the new files. Wait for Department Head confirmation
at Stop 1 / Stop 2 before running the next stage.

For details, see README-USER.md in the repo (Part 3 — Daily use).
"""

    return {
        "vault": str(vault_path),
        "icp": brain.strategy.icp[:200],
        "vision": brain.strategy.vision[:200],
        "products": len(brain.products),
        "active_departments": brain.headcount.active_departments,
        "state": brain.state,
        "active_tasks": [t.name for t in tasks],
        "critic": _critic_status(tasks),
        "tools_live": list_available_tools(vault_root=vault_path),
        "tools_skipped": list_skipped_tools(vault_root=vault_path),
        "packs": packs_info,
        "_workflow_rules": workflow_rules,
    }


def _critic_status(tasks: list[Path]) -> dict[str, str]:
    """Surface `CRITIC round N/M` per task while the loop runs (critic-draft §7)."""
    import json

    status: dict[str, str] = {}
    for t in tasks:
        state_path = t / "critic" / "state.json"
        if not state_path.exists():
            continue
        try:
            st = json.loads(state_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        verdict = st.get("final_verdict")
        if verdict:
            status[t.name] = f"CRITIC {verdict}"
        else:
            status[t.name] = f"CRITIC round {st.get('round', '?')}/{st.get('max_rounds', '?')}"
    return status


@mcp.tool()
def bd_onboard(
    vault: str,
    packs: list[str] | None = None,
    tavily_api_key: str = "",
    anthropic_api_key: str = "",
    google_api_key: str = "",
    openai_api_key: str = "",
) -> dict:
    """Create vault scaffold for a new division.

    Calls core.onboard.onboard_vault directly (no subprocess).

    Args:
        vault: Path where vault will be created
        packs: Optional list of pack codes (none ship by default; see packs/README.md)
        tavily_api_key: RECOMMENDED — enables the 4 search tools (law/competitor/web/local).
                        Get a free tier at https://tavily.com (1000 req/month free).
                        If left blank: search tools skip gracefully — the flow still runs
                        but the decision report rests entirely on Brain + LLM knowledge.
        anthropic_api_key: Optional fallback if not using MCP sampling
        google_api_key: Optional for the Gemini fallback
        openai_api_key: Optional for the GPT fallback

    Returns dict with steps, packs, warnings, next_steps, api_keys_saved.
    """
    keys = {
        "TAVILY_API_KEY": tavily_api_key,
        "ANTHROPIC_API_KEY": anthropic_api_key,
        "GOOGLE_API_KEY": google_api_key,
        "OPENAI_API_KEY": openai_api_key,
    }
    return onboard_vault(
        vault_path=vault,
        packs=packs or [],
        init_git=True,
        api_keys=keys,
    )


@mcp.tool()
def bd_upgrade(
    vault: str,
    refresh_agents: bool = True,
    refresh_dept_yaml: bool = True,
    refresh_brain_aliases: bool = True,
    regenerate_hubs: bool = False,
) -> dict:
    """Upgrade an existing vault to the new plugin version.

    Refreshes agent prompts, department YAML, Brain aliases. Does NOT touch
    Brain content (filled in by the Department Head), Tasks, or Outputs.

    Args:
        vault: Path to the existing vault
        refresh_agents: Overwrite agent .md files with the new enriched prompts
        refresh_dept_yaml: Overwrite department.yaml (aliases_local, routing rules)
        refresh_brain_aliases: Inject aliases into the frontmatter of Brain files
        regenerate_hubs: Delete old index.md + recreate (default NO)

    Returns dict with the count of refreshed files + warnings.
    """
    return upgrade_vault(
        vault_path=vault,
        refresh_agents=refresh_agents,
        refresh_dept_yaml=refresh_dept_yaml,
        refresh_brain_aliases=refresh_brain_aliases,
        regenerate_hubs=regenerate_hubs,
    )


def main() -> None:
    """Entry point — run MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
