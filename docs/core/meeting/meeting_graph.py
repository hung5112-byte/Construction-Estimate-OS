"""LangGraph orchestrator — the entire meeting flow.

Adapted from TradingAgents/graph/trading_graph.py with neutral naming.

Flow:
  perspectives → pro_con_loop → perspective_loop → synthesizer → END
"""
from __future__ import annotations
from typing import Callable
from langgraph.graph import StateGraph, END
from core.meeting.debate_state import MeetingState
from core.meeting.conditional_logic import next_pro_con_node, next_perspective_node
from core.meeting.synthesizer import Synthesizer
from core.meeting.checkpointer import make_checkpointer
from core.agents.pro_advocate import ProAdvocate
from core.agents.con_advocate import ConAdvocate
from core.agents.perspective_debators import (
    GrowthDebator, CautiousDebator, BalancedDebator,
)
from core.llm.activity_log import agent_span, log_activity


def _traced(fn, agent: str, stage: str):
    """Wrap a graph node with start/end/say activity records (best-effort).

    Zero semantic change: the node result passes through untouched; the records
    only feed the live activity log so visualizations can show whose turn it is
    and what was said.
    """
    def wrapped(state):
        task = state.get("task_id", "") if isinstance(state, dict) else ""
        with agent_span(agent, stage=stage, task=task):
            result = fn(state)
        _log_say(agent, stage, task, result)
        return result
    return wrapped


def _log_say(agent: str, stage: str, task: str, result) -> None:
    """Pull the utterance out of a node's state update; swallow any surprise."""
    try:
        text = ""
        if isinstance(result, dict):
            if isinstance(result.get("final_report"), str):
                text = result["final_report"]
            else:
                for key in ("pro_con_debate", "perspective_debate"):
                    part = result.get(key)
                    if isinstance(part, dict) and part.get("history"):
                        text = part["history"][-1]
                        break
        if text:
            log_activity(agent, "say", stage=stage, task=task, text=text)
    except Exception:  # noqa: BLE001 — telemetry never breaks the meeting
        pass


class MeetingGraph:
    """Build + run LangGraph meeting flow."""

    def __init__(
        self,
        llm,
        perspectives_collector: Callable[[MeetingState], dict],
        checkpointer=None,
    ):
        """
        perspectives_collector: function that takes state, returns {"perspectives": {...}}.
        Implemented in Phase 3 from DepartmentLoader.
        checkpointer: optional. If None, uses default SQLite checkpointer.
                      Pass False to disable checkpointing (useful for tests).
        """
        self.llm = llm
        self.perspectives_collector = perspectives_collector
        self.checkpointer = checkpointer
        self.pro = ProAdvocate(llm)
        self.con = ConAdvocate(llm)
        self.growth = GrowthDebator(llm)
        self.cautious = CautiousDebator(llm)
        self.balanced = BalancedDebator(llm)
        self.synthesizer = Synthesizer(llm)

    def build(self):
        graph = StateGraph(MeetingState)

        # perspectives traces per-department/per-team spans inside the collector
        graph.add_node("perspectives", self.perspectives_collector)
        graph.add_node("pro", _traced(self.pro.run, "pro-advocate", "meeting-r2"))
        graph.add_node("con", _traced(self.con.run, "con-advocate", "meeting-r2"))
        graph.add_node("growth", _traced(self.growth.run, "growth-debator", "meeting-r3"))
        graph.add_node("cautious", _traced(self.cautious.run, "cautious-debator", "meeting-r3"))
        graph.add_node("balanced", _traced(self.balanced.run, "balanced-debator", "meeting-r3"))
        graph.add_node("synthesizer", _traced(self.synthesizer.run, "synthesizer", "decision"))

        graph.set_entry_point("perspectives")
        graph.add_edge("perspectives", "pro")

        graph.add_conditional_edges("pro", next_pro_con_node, {
            "con": "con", "perspective_phase": "growth", "pro": "pro",
        })
        graph.add_conditional_edges("con", next_pro_con_node, {
            "pro": "pro", "perspective_phase": "growth", "con": "con",
        })
        graph.add_conditional_edges("growth", next_perspective_node, {
            "cautious": "cautious", "synthesizer": "synthesizer",
        })
        graph.add_conditional_edges("cautious", next_perspective_node, {
            "balanced": "balanced", "synthesizer": "synthesizer",
        })
        graph.add_conditional_edges("balanced", next_perspective_node, {
            "growth": "growth", "synthesizer": "synthesizer",
        })
        graph.add_edge("synthesizer", END)

        # checkpointer logic:
        #   None  → use default SQLite saver
        #   False → no checkpointer
        #   else  → use the provided one
        if self.checkpointer is False:
            return graph.compile()
        cp = self.checkpointer if self.checkpointer is not None else make_checkpointer()
        return graph.compile(checkpointer=cp)

    def invoke(self, state: MeetingState, config: dict | None = None) -> MeetingState:
        cfg = config or {"configurable": {"thread_id": state.get("task_id", "default")}}
        return self.build().invoke(state, config=cfg)
