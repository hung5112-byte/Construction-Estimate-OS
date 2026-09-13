"""BaseAgent — foundation for every agent (department member, debater, ...)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


class LLM(Protocol):
    def complete(self, messages: list[dict], model: str | None = None) -> str:
        ...


@dataclass
class BaseAgent:
    name_local: str
    role: str
    system_prompt: str
    llm: LLM
    department: str = ""
    expertise: list[str] = field(default_factory=list)
    required_refs: list[str] = field(default_factory=list)
    required_tools: list[str] = field(default_factory=list)
    model_override: str | None = None
    temperature: float = 0.7

    def build_messages(
        self,
        brief: str,
        brain_context: dict,
        history: list[str],
        extra_context: str = "",
        request: str | None = None,
    ) -> list[dict]:
        """Compose messages for an LLM call.

        P2.7: Filter the Brain context by `required_refs` to save tokens.
        E.g. CFO required_refs=["strategy","finance","laws"] → pass only 3 sections
        instead of dumping the full brain (8 sections). If required_refs is empty → full dump.

        `request` overrides the default debate-agent REQUEST line — document
        writers (e.g. the Synthesizer) need their own task framing, not "state
        your perspective" (live-replay lesson 2026-07-05: the default line
        nudged the Synthesizer away from machine-checked format tokens).
        """
        # ADR-004 §5 (judge-only, anti-fabrication): episodic decisions never
        # ride the Brain dump into debaters — Step 3 injects them into the
        # Synthesizer alone via meeting state, bounded and scored.
        brain_context = {k: v for k, v in brain_context.items() if k != "decisions"}
        filtered_brain = self._filter_brain(brain_context)
        sys_parts = [
            self.system_prompt,
            "",
            "## BUSINESS DATA (Brain context):",
            f"```yaml\n{self._format_brain(filtered_brain)}\n```",
        ]
        if extra_context:
            sys_parts.append("\n## ADDITIONAL CONTEXT:\n" + extra_context)

        user_parts = [f"## TASK\n{brief}"]
        if history:
            user_parts.append("\n## PRIOR TRANSCRIPT\n" + "\n".join(history))
        user_parts.append(
            "\n## REQUEST\n"
            + (request or "State your perspective (in plain English, citing the Brain).")
        )

        return [
            {"role": "system", "content": "\n".join(sys_parts)},
            {"role": "user", "content": "\n".join(user_parts)},
        ]

    def _filter_brain(self, ctx: dict) -> dict:
        """Slice the Brain context by required_refs (P2.7).

        BrainContext top-level keys: strategy, products, budget, headcount,
        laws, decisions, state, glossary. required_refs use the key name (e.g.
        ["strategy","laws"]) or a filename stem (e.g. "strategy.md" → "strategy").
        """
        if not self.required_refs:
            return ctx
        wanted: set[str] = set()
        for ref in self.required_refs:
            stem = ref.replace(".md", "").strip().lower()
            wanted.add(stem)
        # Aliases — accept "decisions-log" or "decisions"; "finance" → "budget"
        alias_map = {
            "decisions-log": "decisions",
            "finance": "budget",
            "people": "headcount",
        }
        for k, v in alias_map.items():
            if k in wanted:
                wanted.add(v)
        if not wanted:
            return ctx
        filtered = {k: v for k, v in ctx.items() if k in wanted}
        # Always include glossary (small, useful for terms)
        if "glossary" in ctx:
            filtered.setdefault("glossary", ctx["glossary"])
        return filtered if filtered else ctx

    @staticmethod
    def _format_brain(ctx: dict) -> str:
        import yaml

        return yaml.safe_dump(ctx, allow_unicode=True, sort_keys=False, width=120)

    def speak(
        self,
        brief: str,
        brain_context: dict,
        history: list[str],
        extra_context: str = "",
        request: str | None = None,
    ) -> str:
        messages = self.build_messages(
            brief, brain_context, history, extra_context, request=request
        )
        return self.llm.complete(messages, model=self.model_override)
