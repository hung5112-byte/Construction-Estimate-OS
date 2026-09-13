"""Orchestrate the whole flow: brief → router → gap → clarify (Stop pre) →
   research → meeting → synthesizer (Stop 1) → execution (Stop 2)."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional
import re

from core.brain.reader import BrainReader
from core.brain.gap_analyzer import GapAnalyzer
from core.clarifier.question_generator import QuestionGenerator
from core.clarifier.clarification_io import (
    write_clarification, read_answers,
)
from core.obsidian.vault import ObsidianVault
from core.orchestrator.router import Router
from core.utils.config import load_config
from core.paths import data_root, templates_root


class FlowStage(str, Enum):
    PAUSE_CLARIFICATION = "PAUSE_CLARIFICATION"
    PAUSE_DECISION_REPORT = "PAUSE_DECISION_REPORT"
    PAUSE_EXECUTE = "PAUSE_EXECUTE"
    DONE = "DONE"
    ERROR = "ERROR"


@dataclass
class FlowResult:
    stage: FlowStage
    task_folder: Path
    message: str = ""
    error: Optional[str] = None


def _slugify(brief: str, max_len: int = 50) -> str:
    """Slugify accented text → ASCII kebab-case.

    P2.6: use unicodedata.normalize NFKD to strip diacritics (e.g. "Café" → "cafe").
    A plain \\w+ regex keeps Unicode accents → an accented folder name on Windows
    can cause path edge cases; normalizing to ASCII is safer.
    """
    import unicodedata
    # NFKD decompose: "ü" → "u" + combining mark; then drop the combining marks
    decomposed = unicodedata.normalize("NFKD", brief.lower())
    ascii_only = "".join(c for c in decomposed if not unicodedata.combining(c))
    # Special case: "đ" does not decompose under NFKD → manual replace
    ascii_only = ascii_only.replace("đ", "d").replace("Đ", "d")
    # Strip non-alphanumeric (keep space + dash to convert)
    s = re.sub(r"[^a-z0-9\s-]", "", ascii_only)
    s = re.sub(r"\s+", "-", s.strip())[:max_len]
    return s.strip("-") or "task"


class FlowController:
    def __init__(self, vault_root: Path, llm):
        self.vault = ObsidianVault(vault_root)
        self.llm = llm
        # Vault-level .bd-os.yaml takes priority; load_config falls back to ~/.bd-os.yaml
        self.config = load_config(self.vault.root / ".bd-os.yaml")

    def run(self, brief: str) -> FlowResult:
        """Stage 1: brief → router → gap → clarification (PAUSE)."""
        # 1. Create task folder
        task_folder = self.vault.create_task_folder(_slugify(brief))
        (task_folder / "00-brief.md").write_text(
            f"---\ntype: brief\n---\n# Brief\n\n{brief}\n", encoding="utf-8",
        )

        # 2. Read Brain
        brain = BrainReader(self.vault.root).load()

        # 3. Router classify
        rules_path = Path(__file__).parent / "classifier_rules.yaml"
        router = Router(self.llm, rules_path=rules_path)
        classification = router.classify(brief, brain)

        (task_folder / "01-routing.md").write_text(
            f"---\ntype: routing\n---\n# Task classification\n\n"
            f"- **Class:** {classification.class_.value}\n"
            f"- **Departments:** {', '.join(classification.departments)}\n"
            f"- **Reasoning:** {classification.reasoning}\n",
            encoding="utf-8",
        )

        # 4. Context dump
        (task_folder / "02-context.md").write_text(
            "---\ntype: context\n---\n# Brain context loaded\n\n"
            f"```yaml\n{brain.model_dump_json(indent=2)}\n```\n",
            encoding="utf-8",
        )

        # 5. Gap analysis
        analyzer = GapAnalyzer(self.llm)
        gaps = analyzer.analyze(brief, brain)

        if not gaps:
            return FlowResult(
                stage=FlowStage.PAUSE_DECISION_REPORT,
                task_folder=task_folder,
                message="No gaps — ready to run the meeting.",
            )

        # 6. Generate questions
        qg = QuestionGenerator(self.llm)
        questions = qg.generate(gaps, brain.model_dump(), brief)

        if not questions:
            return FlowResult(
                stage=FlowStage.PAUSE_DECISION_REPORT,
                task_folder=task_folder,
                message="Gaps exist but none are CRITICAL/WARN, skipping clarification.",
            )

        # 7. Write clarification + PAUSE
        clarification_path = task_folder / "03-clarification.md"
        write_clarification(clarification_path, questions)

        return FlowResult(
            stage=FlowStage.PAUSE_CLARIFICATION,
            task_folder=task_folder,
            message=f"Please answer {len(questions)} question(s) in {clarification_path.name}",
        )

    async def arun(self, brief: str) -> FlowResult:
        """Async version of run() — used in async MCP tools to avoid a deadlock.

        FastMCP calls a sync tool directly on the event loop, so llm.complete() deadlocks.
        arun() uses acomplete() → await create_message() directly, no threading.
        """
        task_folder = self.vault.create_task_folder(_slugify(brief))
        (task_folder / "00-brief.md").write_text(
            f"---\ntype: brief\n---\n# Brief\n\n{brief}\n", encoding="utf-8",
        )

        brain = BrainReader(self.vault.root).load()

        rules_path = Path(__file__).parent / "classifier_rules.yaml"
        router = Router(self.llm, rules_path=rules_path)
        classification = await router.aclassify(brief, brain)

        (task_folder / "01-routing.md").write_text(
            f"---\ntype: routing\n---\n# Task classification\n\n"
            f"- **Class:** {classification.class_.value}\n"
            f"- **Departments:** {', '.join(classification.departments)}\n"
            f"- **Reasoning:** {classification.reasoning}\n",
            encoding="utf-8",
        )

        (task_folder / "02-context.md").write_text(
            "---\ntype: context\n---\n# Brain context loaded\n\n"
            f"```yaml\n{brain.model_dump_json(indent=2)}\n```\n",
            encoding="utf-8",
        )

        analyzer = GapAnalyzer(self.llm)
        gaps = await analyzer.aanalyze(brief, brain)

        if not gaps:
            return FlowResult(
                stage=FlowStage.PAUSE_DECISION_REPORT,
                task_folder=task_folder,
                message="No gaps — ready to run the meeting.",
            )

        qg = QuestionGenerator(self.llm)
        questions = await qg.agenerate(gaps, brain.model_dump(), brief)

        if not questions:
            return FlowResult(
                stage=FlowStage.PAUSE_DECISION_REPORT,
                task_folder=task_folder,
                message="Gaps exist but none are CRITICAL/WARN, skipping clarification.",
            )

        clarification_path = task_folder / "03-clarification.md"
        write_clarification(clarification_path, questions)

        return FlowResult(
            stage=FlowStage.PAUSE_CLARIFICATION,
            task_folder=task_folder,
            message=f"Please answer {len(questions)} question(s) in {clarification_path.name}",
        )

    def resume_after_clarification(self, task_folder: Path) -> FlowResult:
        """Stage 2: read answers → continue the flow (research+meeting)."""
        clarification_path = task_folder / "03-clarification.md"
        if not clarification_path.exists():
            return FlowResult(
                stage=FlowStage.ERROR, task_folder=task_folder,
                error="03-clarification.md not found",
            )

        answers = read_answers(clarification_path)
        unanswered = [a for a in answers if a.choice is None and not a.free_text_answer]
        if unanswered:
            return FlowResult(
                stage=FlowStage.PAUSE_CLARIFICATION,
                task_folder=task_folder,
                message=f"{len(unanswered)} question(s) still unanswered",
            )

        # Save normalized answers
        (task_folder / "03-clarification-answered.md").write_text(
            "---\ntype: answers\n---\n"
            + "\n".join(f"- Q: {a.question_text}\n  A: {a.choice or a.free_text_answer}"
                       for a in answers),
            encoding="utf-8",
        )

        # Phase 4-5 wires research + meeting here
        return FlowResult(
            stage=FlowStage.PAUSE_DECISION_REPORT,
            task_folder=task_folder,
            message="Answers recorded. Ready for research + meeting.",
        )

    def run_meeting(self, task_folder: Path, departments: list[str]) -> FlowResult:
        """Stage 3: research → meeting → synthesizer → citation-validate → STOP 1.

        P1.6: translator_mode controls how far TranslatorPipeline applies:
          "off"              — no simplification
          "final_only"       — only final decision report (default, preserves old behavior)
          "all_intermediate" — also applies to each perspective output before they enter state
        P1.8: CitationValidator runs after report written, appends warning section if flags found.
        """
        from core.brain.reader import BrainReader
        from core.orchestrator.research_phase import ResearchPhase
        from core.orchestrator.perspectives_collector import PerspectivesCollector
        from core.orchestrator.citation_validator import CitationValidator
        from core.meeting.meeting_graph import MeetingGraph
        from core.meeting.debate_state import new_meeting_state
        from core.translator.pipeline import TranslatorPipeline
        from core.obsidian.git_sync import GitSync

        brief = self._read_brief(task_folder)
        brain = BrainReader(self.vault.root).load()

        # 1. Research phase (RULE 5) — cache per-vault (P2.3)
        research = ResearchPhase(self.llm, vault_root=self.vault.root)
        findings = research.run(
            brief=brief,
            brain_summary=brain.model_dump_json()[:3000],
            task_folder=task_folder,
        )

        # 2. Translator pipeline — created once, shared across pipeline
        # P1.6: translator_mode from config (default "final_only" preserves old behavior)
        translator_mode = getattr(self.config, "translator_mode", "final_only")
        glossary_path = self.vault.root / "00-Brain" / "glossary.md"
        translator = TranslatorPipeline(self.llm, vault_glossary_path=glossary_path)

        # 3. Meeting graph
        # P0.3 fix: use vault/01-Departments so BYOT + pack depts are picked up.
        # Fallback to repo/departments/ if vault path absent (test fixtures, CI).
        vault_depts = self.vault.root / "01-Departments"
        repo_depts = Path(__file__).parent.parent.parent / "departments"
        departments_root = vault_depts if vault_depts.exists() else repo_depts
        collector = PerspectivesCollector(
            departments_root=departments_root,
            llm=self.llm,
            vault_root=self.vault.root,
            # V2: team round + manager synthesis (see MeetingConfig for cost notes)
            intra_department=bool(
                getattr(self.config.meeting, "intra_department_round", False)
            ),
        )

        # P1.6: wrap collector with translator when all_intermediate mode
        if translator_mode == "all_intermediate":
            collector_fn = _make_translating_collector(collector.collect, translator)
        else:
            collector_fn = collector.collect

        # P1.4: opt-in checkpointer. Default off due to SqliteSaver compat issues.
        # When the user sets `meeting.use_checkpointer=true` in .bd-os.yaml, try to init.
        # If it fails (LangGraph version mismatch, SQLite locked, ...), log + fall back.
        use_cp = bool(getattr(self.config.meeting, "use_checkpointer", False))
        cp_setting: Any = False
        if use_cp:
            try:
                from core.meeting.checkpointer import make_checkpointer
                cp_setting = make_checkpointer()
            except Exception as e:  # noqa: BLE001
                self._log_warning(f"Checkpointer init failed, fallback off: {e}")
                cp_setting = False

        graph = MeetingGraph(
            llm=self.llm,
            perspectives_collector=collector_fn,
            checkpointer=cp_setting,
        )

        state = new_meeting_state(
            brief=brief,
            departments=departments,
            brain_context=brain.model_dump(),
            max_rounds=self.config.meeting.max_debate_rounds,
            task_id=task_folder.name,
        )
        state["research_findings"] = findings

        # Judge-only episodic memory (ADR-004 §5, Step 3): assemble the bounded
        # "PAST DECISIONS" block from the ledger; consumed only by the
        # Synthesizer node. Best-effort — memory must never block a meeting.
        try:
            from core.critic.telemetry import emit_memory_injection
            from core.meeting.memory_injection import assemble_memory_context

            mem = assemble_memory_context(self.vault.root, topic=brief)
            if mem is not None:
                state["memory_context"] = mem.block
                # Persisted per-task so the critic judge and revision rounds see
                # the same block (excluded from the vault_search index — this is
                # ledger-derived, judge-only content).
                (task_folder / "03c-memory-context.md").write_text(
                    mem.block, encoding="utf-8"
                )
                emit_memory_injection(task_folder, mem.items, total_chars=len(mem.block))
        except Exception as e:  # noqa: BLE001
            self._log_warning(f"Memory injection skipped: {e}")

        final_state = graph.build().invoke(state)

        # 4. Write intermediate meeting outputs to vault
        self._write_meeting_outputs(task_folder, final_state)

        # 5. Translator pipeline on final_report (RULE 4)
        # "off" — skip; "final_only" / "all_intermediate" — always translate final report
        # (in all_intermediate mode intermediates were already translated, final still needs it)
        if translator_mode == "off":
            translated_report = final_state["final_report"]
        else:
            translated_report = translator.apply(final_state["final_report"])

        report_text = f"---\ntype: decision_report\nstop: 1\n---\n{translated_report}"
        decision_path = task_folder / "07-decision-report.md"

        # 6. Critic loop (Pass A) — evaluator-optimizer gate before Stop 1.
        # Tier awareness (ADR-003 Addendum B): mandatory at COMPLEX/STRATEGIC
        # (≙ T2+), skippable at SIMPLE (≙ T0/T1) — read from 01-routing.md via
        # the critic.apply_to_classes config knob. When the critic is skipped,
        # the legacy P1.8 warning-section path is preserved unchanged.
        from core.critic.loop import CriticLoop
        from core.critic.models import CriticError

        critic_cfg = getattr(self.config, "critic", None)
        critic_loop = None
        if critic_cfg is not None and critic_cfg.enabled:
            critic_loop = CriticLoop(
                llm=self.llm,
                config=critic_cfg,
                vault_root=self.vault.root,
                primary_model=self.config.llm.primary,
            )

        flag_msg = ""
        if critic_loop is not None and critic_loop.should_run(task_folder):
            synthesizer = graph.synthesizer

            def _revise(revision_md: str, prior_draft: str) -> str:
                # Same PAST DECISIONS block as the drafting turn (ADR-004 §5):
                # a repair round must see what memory-derived claims rest on.
                revised = synthesizer.revise(
                    prior_draft, revision_md,
                    memory_block=state.get("memory_context") or "",
                )
                # The translator is deliberately SKIPPED on revision rounds
                # (2026-07-05 ruling, replay 4): revisions edit already-
                # simplified text, and the LLM editor is a structure hazard —
                # even with preservation mandates it stripped machine markers
                # live. The critic loop assembles the structural skeleton in
                # code after this hook regardless.
                if not revised.strip().startswith("---"):
                    revised = f"---\ntype: decision_report\nstop: 1\n---\n{revised}"
                return revised

            try:
                outcome = critic_loop.run_pass_a(task_folder, report_text, _revise)
            except CriticError as e:
                # Structural failure — OpenAI ladder `raise`: engine error, not a retry.
                return FlowResult(
                    stage=FlowStage.ERROR, task_folder=task_folder,
                    error=f"Critic structural failure: {e}",
                )
            banner_msg = " THRESHOLD-NOT-MET banner attached —" if outcome.banner else ""
            flag_msg = (
                f" | Critic: {outcome.verdict} after {outcome.rounds_used} round(s)."
                f"{banner_msg} Scorecard: {outcome.scorecard_path.name}."
            )
        else:
            decision_path.write_text(report_text, encoding="utf-8")
            # P1.8: legacy citation warning — only when the critic is skipped.
            validator = CitationValidator()
            flags = validator.validate(decision_path)
            if flags:
                flag_msg = f" | {len(flags)} claim(s) missing a citation were flagged."

        # 7. Auto-commit (best-effort, log on failure)
        try:
            GitSync(self.vault.root).commit(
                f"feat(task): {task_folder.name} — decision report ready (Stop 1)"
            )
        except Exception as e:
            self._log_warning(f"Git commit failed (Stop 1): {e}")

        return FlowResult(
            stage=FlowStage.PAUSE_DECISION_REPORT,
            task_folder=task_folder,
            message=f"Decision report ready at {decision_path.name}. Department Head to review + approve.{flag_msg}",
        )

    def _log_warning(self, message: str) -> None:
        """Log a warning to <vault>/.bd-business-os.log instead of swallowing it.

        The Department Head can read this file to see why a git commit failed, etc.
        """
        from datetime import datetime
        log_path = self.vault.root / ".bd-business-os.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] WARN: {message}\n"
        try:
            with log_path.open("a", encoding="utf-8") as f:
                f.write(line)
        except Exception:
            pass  # a logging failure must not break the flow

    def _read_brief(self, task_folder: Path) -> str:
        brief_md = (task_folder / "00-brief.md").read_text(encoding="utf-8")
        parts = brief_md.split("---", 2)
        return (parts[2] if len(parts) >= 3 else brief_md).strip()

    def _write_meeting_outputs(self, task_folder: Path, state):
        team_inputs = state.get("team_inputs") or {}
        sections = []
        for dept, p in state["perspectives"].items():
            block = [f"## [[01-Departments/{dept}/index|{dept}]]"]
            takes = team_inputs.get(dept) or {}
            if takes:
                block.append("\n### Team inputs\n")
                for team_id, text in takes.items():
                    block.append(f"#### [[{team_id}]]\n\n{text}\n")
                block.append("### Department synthesis\n")
            block.append(p)
            sections.append("\n".join(block))
        perspectives_md = "\n\n".join(sections)
        (task_folder / "04-meeting-r1-perspectives.md").write_text(
            f"---\ntype: meeting_r1\n---\n# Round 1 — Perspectives\n\n{perspectives_md}",
            encoding="utf-8",
        )

        debate_md = "\n\n".join(state["pro_con_debate"]["history"])
        (task_folder / "05-meeting-r2-debate.md").write_text(
            f"---\ntype: meeting_r2\n---\n# Round 2 — Pro/Con Debate\n\n{debate_md}",
            encoding="utf-8",
        )

        perspective_md = "\n\n".join(state["perspective_debate"]["history"])
        (task_folder / "06-meeting-r3-perspectives.md").write_text(
            f"---\ntype: meeting_r3\n---\n# Round 3 — Perspective Debate\n\n{perspective_md}",
            encoding="utf-8",
        )

    def approve_decision(self, task_folder: Path, decision: str = "approve") -> FlowResult:
        """Stage 4: Department Head approves the decision report → generate a structured execution plan (P0.2)."""
        from core.translator.pipeline import TranslatorPipeline
        from core.orchestrator.execution_planner import generate_execution_plan

        # translator_mode "off" applies to the plan path too — the simplify step
        # sends the whole plan as one LLM call, same failure mode as the report
        if getattr(self.config, "translator_mode", "final_only") == "off":
            translator = None
        else:
            glossary_path = self.vault.root / "00-Brain" / "glossary.md"
            translator = TranslatorPipeline(self.llm, vault_glossary_path=glossary_path)

        try:
            plan_path = generate_execution_plan(
                task_folder=task_folder,
                llm=self.llm,
                translator=translator,
                templates_root=templates_root(),
            )
        except FileNotFoundError as exc:
            return FlowResult(
                stage=FlowStage.ERROR,
                task_folder=task_folder,
                error=str(exc),
            )
        except Exception as exc:
            return FlowResult(
                stage=FlowStage.ERROR,
                task_folder=task_folder,
                error=f"Error generating the execution plan: {exc}",
            )

        # Critic Pass B — report↔plan consistency before Stop 2 (critic-draft
        # §2 R6). Same tier awareness as Pass A; max 1 fix round by design.
        from core.critic.loop import CriticLoop
        from core.critic.models import CriticError

        critic_cfg = getattr(self.config, "critic", None)
        pass_b_msg = ""
        if (
            critic_cfg is not None
            and critic_cfg.enabled
            and critic_cfg.plan_pass.enabled
        ):
            critic_loop = CriticLoop(
                llm=self.llm,
                config=critic_cfg,
                vault_root=self.vault.root,
                primary_model=self.config.llm.primary,
            )
            if critic_loop.should_run(task_folder):
                from core.critic.pass_b import run_pass_b

                def _replan(revision_md: str, prior_plan: str) -> str:
                    new_path = generate_execution_plan(
                        task_folder=task_folder,
                        llm=self.llm,
                        translator=translator,
                        templates_root=templates_root(),
                        revision_context=(
                            f"PREVIOUS PLAN (did not clear the critic):\n\n{prior_plan}\n\n"
                            f"CRITIC REVISION INSTRUCTION:\n\n{revision_md}"
                        ),
                    )
                    return new_path.read_text(encoding="utf-8")

                try:
                    outcome = run_pass_b(
                        task_folder=task_folder,
                        llm=self.llm,
                        config=critic_cfg,
                        vault_root=self.vault.root,
                        replan_fn=_replan,
                        primary_model=self.config.llm.primary,
                    )
                except CriticError as e:
                    return FlowResult(
                        stage=FlowStage.ERROR, task_folder=task_folder,
                        error=f"Critic Pass B structural failure: {e}",
                    )
                banner_msg = " THRESHOLD-NOT-MET banner attached —" if outcome.banner else ""
                pass_b_msg = (
                    f" | Critic Pass B: {outcome.verdict}.{banner_msg} "
                    "Scorecard: 08b-critic-scorecard.md."
                )

        return FlowResult(
            stage=FlowStage.PAUSE_EXECUTE,
            task_folder=task_folder,
            message=f"Execution plan ready at {plan_path.name}. Run 'execute' to generate documents.{pass_b_msg}",
        )

    def execute(self, task_folder: Path) -> FlowResult:
        """Stage 5: render docs from execution plan → 03-Outputs/ (P0.1)."""
        from core.orchestrator.document_executor import execute_documents
        from core.brain.reader import BrainReader

        repo_root = data_root()

        # Load brain context for template substitutions (best-effort)
        brain_context: dict | None = None
        try:
            brain = BrainReader(self.vault.root).load()
            brain_context = brain.model_dump()
        except Exception:
            pass  # brain unavailable — substitutions will use task metadata only

        try:
            result = execute_documents(
                task_folder=task_folder,
                vault_root=self.vault.root,
                repo_root=repo_root,
                llm=self.llm,
                brain_context=brain_context,
            )
        except FileNotFoundError as exc:
            return FlowResult(
                stage=FlowStage.ERROR,
                task_folder=task_folder,
                error=str(exc),
            )
        except Exception as exc:
            return FlowResult(
                stage=FlowStage.ERROR,
                task_folder=task_folder,
                error=f"Error rendering documents: {exc}",
            )

        # ADR-004 §1: a successful execute IS the Stop-2 approval — append to
        # the episodic ledger only now, after rendering succeeded (an execute
        # on an unapproved/broken folder errors out above and records nothing).
        # Idempotent; a ledger problem must never block the DONE result.
        try:
            from core.brain.ledger import record_approved_decision

            record_approved_decision(self.vault.root, task_folder)
        except Exception as e:  # noqa: BLE001
            self._log_warning(f"Decision-ledger append failed: {e}")

        generated = result["generated"]
        skipped = result["skipped"]

        parts = [f"Created {len(generated)} document(s) in 03-Outputs/{task_folder.name}/"]
        if generated:
            parts.append("Documents: " + ", ".join(Path(g).name for g in generated))
        if skipped:
            parts.append(f"Skipped {len(skipped)} template(s) not found: " + "; ".join(skipped))

        return FlowResult(
            stage=FlowStage.DONE,
            task_folder=task_folder,
            message=" | ".join(parts),
        )


def _make_translating_collector(collect_fn, translator) -> Callable:
    """Wrap the collector to translate each perspective output (P1.6 all_intermediate mode).

    Only used when translator_mode = 'all_intermediate'.
    The translator calls the LLM, so it adds cost — the Department Head must opt in via .bd-os.yaml:
        translator_mode: all_intermediate
    Avoid double-translation: the final report is still translated later by flow_controller,
    but perspective inputs into the Synthesizer will already be simplified → cleaner synthesis.
    A translator error must not break the flow — fall back to raw text.
    """
    def _wrapped(state):
        result = collect_fn(state)
        perspectives = result.get("perspectives", {})
        translated = {}
        for dept_code, text in perspectives.items():
            # Do not translate error/placeholder markers
            if isinstance(text, str) and (
                text.startswith("[ERROR]") or text.startswith("[Department")
            ):
                translated[dept_code] = text
            else:
                try:
                    translated[dept_code] = translator.apply(text)
                except Exception:
                    # Translator failure must not break meeting flow
                    translated[dept_code] = text
        return {"perspectives": translated}

    return _wrapped
