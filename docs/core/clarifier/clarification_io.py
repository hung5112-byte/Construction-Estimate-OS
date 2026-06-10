"""Write clarification.md for the Department Head + parse the answer when the Department Head ticks a checkbox."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import re
from core.clarifier.question_generator import Question


@dataclass
class AnsweredQuestion:
    question_text: str
    choice: Optional[str]
    free_text_answer: Optional[str] = None


def write_clarification(path: Path, questions: list[Question]) -> None:
    parts = ["---", "type: clarification", "answered: false", "---", ""]
    parts.append("# 🤖 Questions from the system (Brain-first)")
    parts.append("")
    parts.append("> Tick `[x]` for the Department Head's choice, or fill in free text. Save the file.")
    parts.append("")

    for i, q in enumerate(questions, 1):
        parts.append(f"## Q{i} [{q.severity.value}]")
        parts.append(f"_Cite: {q.citation}_")
        parts.append("")
        parts.append(q.text)
        parts.append("")
        if q.choices:
            for c in q.choices:
                parts.append(f"- [ ] {c}")
        if q.free_text:
            parts.append("")
            parts.append("**Answer:**")
            parts.append("```")
            parts.append("(fill in here)")
            parts.append("```")
        parts.append("")

    path.write_text("\n".join(parts), encoding="utf-8")


def read_answers(path: Path) -> list[AnsweredQuestion]:
    content = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    answers = []

    blocks = re.split(r"^## Q\d+", content, flags=re.MULTILINE)[1:]
    for block in blocks:
        # Find the checked choice
        checked = re.search(r"^-\s+\[x\]\s+(.+)$", block, re.MULTILINE | re.IGNORECASE)
        # Find free text
        free = re.search(r"```\n(.*?)\n```", block, re.DOTALL)
        free_text = None
        if free:
            txt = free.group(1).strip()
            if txt and txt != "(fill in here)":
                free_text = txt
        # Question text — first non-empty line ending with ?
        q_match = re.search(r"^(.+\?)\s*$", block, re.MULTILINE)
        question_text = q_match.group(1).strip() if q_match else "(unknown)"

        answers.append(AnsweredQuestion(
            question_text=question_text,
            choice=checked.group(1).strip() if checked else None,
            free_text_answer=free_text,
        ))

    return answers
