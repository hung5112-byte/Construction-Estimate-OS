"""Round 1 — each department states its perspective (in parallel).

P1.1: load the per-agent enriched system prompt from
<departments_root>/<dept>/agents/<default_speaker>.md via AgentLoader.
Fall back to the generic PERSPECTIVE_PROMPT if the file is missing.

V2 (intra-department round): when `intra_department=True`, every TEAM agent in
the department first gives a short take, then the MANAGER (default_speaker)
synthesizes those takes into the department perspective — mirroring a real org
where the manager speaks for the department in cross-functional meetings.
Team takes are returned in `team_inputs` for traceability (written into
04-meeting-r1-perspectives.md with wikilinks).
"""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from core.agents.department import DepartmentLoader
from core.agents.agent_loader import AgentLoader
from core.agents.base_agent import BaseAgent
from core.meeting.debate_state import MeetingState


PERSPECTIVE_PROMPT = """You are the {dept_name} department in the company.

Read the brief + Brain context. State YOUR DEPARTMENT'S PERSPECTIVE:
- What does your department care about in this brief?
- Opportunities / risks from your department's angle?
- Relevant Brain numbers (cite specifically)?
- A short recommendation

Plain English. Define any jargon. Cite the Brain for every claim.
Keep it under 400 words — this is round 1.
"""

# Stance appended after the agent system_prompt when using enriched prompts
_STANCE_SUFFIX = """
## YOUR TASK IN THIS MEETING (Round 1)
State your department's perspective:
- What does your department care about in this brief?
- Opportunities / risks from your department's angle?
- Relevant Brain numbers (cite specifically)?
- A short recommendation

Plain English. Define any jargon. Cite the Brain for every claim.
Keep it under 400 words — this is round 1.
"""

# Stance for a TEAM agent in the intra-department round — short input to the manager
_TEAM_SUFFIX = """
## YOUR TASK IN THIS MEETING (Round 1 — team input)
Give YOUR TEAM'S take on this brief for your manager:
- The 1-3 things your team must flag (risk, dependency, opportunity)
- Relevant Brain numbers (cite specifically)
- Your team's one-line recommendation

Plain English. Be specific, not exhaustive. HARD LIMIT: 150 words.
"""

# Stance for the MANAGER synthesizing team inputs into the department perspective
_MANAGER_SUFFIX = """
## YOUR TASK IN THIS MEETING (Round 1 — synthesize your department)
Your teams' inputs are provided under ADDITIONAL CONTEXT. As the manager:
- Weigh and reconcile your teams' takes (call out disagreements honestly)
- State YOUR DEPARTMENT'S position: concerns, opportunities, risks
- Cite the Brain for every number; credit a team when you use its point (e.g. "per the EE team")
- End with a short recommendation

Plain English. Define any jargon. Keep it under 400 words — this is round 1.
"""


class PerspectivesCollector:
    def __init__(
        self,
        departments_root: Path,
        llm,
        max_parallel: int = 5,
        vault_root: Path | None = None,
        intra_department: bool = False,
    ):
        """
        departments_root: path to the departments folder (vault/01-Departments or repo/departments).
        vault_root: optional, used to find agent .md files if departments_root has no agents/.
                    If None, look for agent .md directly under departments_root/<dept>/agents/.
        intra_department: when True, run the team round before the manager synthesis
                    (costs roughly one LLM call per team agent extra, per department).
        """
        self.departments_root = Path(departments_root)
        self.loader = DepartmentLoader(self.departments_root)
        self.agent_loader = AgentLoader()
        self.llm = llm
        self.max_parallel = max_parallel
        # vault_root lets us find agents in the vault when departments_root is a repo path
        self.vault_root = Path(vault_root) if vault_root else None
        self.intra_department = intra_department

    def collect(self, state: MeetingState) -> dict:
        results: dict[str, str] = {}
        team_inputs: dict[str, dict[str, str]] = {}
        with ThreadPoolExecutor(max_workers=self.max_parallel) as executor:
            futures = {
                executor.submit(self._speak_dept, dept_code, state): dept_code
                for dept_code in state["departments"]
            }
            for fut in futures:
                dept_code = futures[fut]
                try:
                    perspective, takes = fut.result()
                    results[dept_code] = perspective
                    if takes:
                        team_inputs[dept_code] = takes
                except Exception as e:
                    results[dept_code] = f"[ERROR] {e}"

        return {"perspectives": results, "team_inputs": team_inputs}

    def _resolve_agent_path(self, dept_code: str, agent_id: str) -> Path | None:
        """Find the agent .md file. Try in priority order:
        1. <departments_root>/<dept_code>/agents/<agent_id>.md
        2. <vault_root>/01-Departments/<dept_code>/agents/<agent_id>.md  (if vault_root set)
        """
        candidates = [
            self.departments_root / dept_code / "agents" / f"{agent_id}.md",
        ]
        if self.vault_root:
            candidates.append(
                self.vault_root / "01-Departments" / dept_code / "agents" / f"{agent_id}.md"
            )
        for p in candidates:
            if p.exists():
                return p
        return None

    def _speak_dept(self, dept_code: str, state: MeetingState) -> tuple[str, dict[str, str]]:
        """Produce the department perspective.

        Returns (perspective, team_takes). team_takes is {} when the intra round
        is off or the department has no team agents besides the manager.
        """
        try:
            dept = self.loader.load(dept_code)
        except FileNotFoundError:
            return f"[Department {dept_code} does not exist in the vault]", {}

        manager_id = dept.default_speaker
        team_ids = [a for a in (dept.agents or []) if a != manager_id]

        if not self.intra_department or not manager_id or not team_ids:
            # Single-speaker mode (legacy behavior)
            system_prompt = self._load_system_prompt(dept_code, dept, manager_id, _STANCE_SUFFIX)
            return self._call(dept, dept_code, system_prompt, state), {}

        # Intra-department round: each team speaks briefly, then the manager synthesizes
        takes: dict[str, str] = {}
        for team_id in team_ids:
            team_prompt = self._load_system_prompt(dept_code, dept, team_id, _TEAM_SUFFIX)
            try:
                takes[team_id] = self._call(dept, dept_code, team_prompt, state)
            except Exception as e:  # one team failing must not sink the department
                takes[team_id] = f"[ERROR] {e}"

        manager_prompt = self._load_system_prompt(dept_code, dept, manager_id, _MANAGER_SUFFIX)
        teams_block = "\n\n".join(
            f"### Input from [[{team_id}]]\n{text}" for team_id, text in takes.items()
        )
        synthesis = self._call(
            dept, dept_code, manager_prompt, state,
            extra_context=f"## YOUR TEAMS' INPUTS\n\n{teams_block}",
        )
        return synthesis, takes

    def _call(self, dept, dept_code: str, system_prompt: str, state: MeetingState,
              extra_context: str = "") -> str:
        agent = BaseAgent(
            name_vn=dept.name_vn,
            role=dept_code,
            system_prompt=system_prompt,
            llm=self.llm,
            department=dept_code,
            temperature=0.5,
        )
        return agent.speak(
            brief=state["brief"],
            brain_context=state["brain_context"],
            history=[],
            extra_context=extra_context,
        )

    def _load_system_prompt(self, dept_code: str, dept, agent_id: str | None,
                            suffix: str) -> str:
        """Load the enriched prompt for `agent_id` + stance suffix.

        Falls back to the generic PERSPECTIVE_PROMPT when the agent file is
        missing, empty, or unparsable.
        """
        if not agent_id:
            return PERSPECTIVE_PROMPT.format(dept_name=dept.name_vn)

        agent_path = self._resolve_agent_path(dept_code, agent_id)
        if agent_path is None:
            return PERSPECTIVE_PROMPT.format(dept_name=dept.name_vn)

        try:
            agent_def = self.agent_loader.load(agent_path)
            body = agent_def.system_prompt
            if not body:
                return PERSPECTIVE_PROMPT.format(dept_name=dept.name_vn)
            return body + suffix
        except Exception:
            # Any parse error falls back gracefully
            return PERSPECTIVE_PROMPT.format(dept_name=dept.name_vn)

    # Backward-compat shim: older tests/utilities used this name for the
    # single-speaker prompt loader.
    def _load_agent_system_prompt(self, dept_code: str, dept) -> str:
        return self._load_system_prompt(dept_code, dept, dept.default_speaker, _STANCE_SUFFIX)
