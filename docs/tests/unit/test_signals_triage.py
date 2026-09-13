import json
from datetime import datetime

from core.signals.prefilter import PrefilterVerdict
from core.signals.rules import SignalRules
from core.signals.schema import Event, Severity
from core.signals.triage import triage

RULES = SignalRules.model_validate({
    "departments": ["Quality & Reliability", "Service Operations"],
})
EVENT = Event(source="email", external_id="1", sender="ops@factory.com",
              subject="Line down", body="SMT line 2 halted since 06:00.",
              received_at=datetime(2026, 7, 1))
PASSED = PrefilterVerdict(True, "critical keyword hit", ["line down"], [])


class FakeLLM:
    def __init__(self, reply):
        self.reply = reply
        self.messages = None

    def complete(self, messages, model=None):
        self.messages = messages
        if isinstance(self.reply, Exception):
            raise self.reply
        return self.reply


def test_valid_llm_reply_is_parsed():
    llm = FakeLLM(json.dumps({
        "severity": "critical",
        "departments": ["quality & reliability", "Legal"],  # Legal is unknown
        "summary": "Production line stopped at the contract manufacturer.",
        "rationale": "Output halted, revenue at risk today.",
    }))
    r = triage(EVENT, PASSED, RULES, llm=llm)
    assert r.severity == Severity.CRITICAL
    assert r.departments == ["Quality & Reliability"]  # unknown filtered, case fixed
    assert r.triaged_by == "llm"


def test_json_inside_prose_is_extracted():
    llm = FakeLLM('Here is my verdict:\n{"severity": "routine", "departments": [], '
                  '"summary": "FYI note.", "rationale": "No action."}')
    r = triage(EVENT, PASSED, RULES, llm=llm)
    assert r.severity == Severity.ROUTINE


def test_unparseable_reply_falls_back_to_keywords():
    r = triage(EVENT, PASSED, RULES, llm=FakeLLM("I cannot classify this."))
    assert r.triaged_by == "prefilter-fallback"
    assert r.severity == Severity.CRITICAL  # critical keyword matched in prefilter


def test_llm_exception_falls_back():
    r = triage(EVENT, PASSED, RULES, llm=FakeLLM(RuntimeError("api down")))
    assert r.triaged_by == "prefilter-fallback"


def test_no_llm_and_no_critical_keyword_needs_review():
    verdict = PrefilterVerdict(True, "high keyword hit", [], ["shortage"])
    r = triage(EVENT, verdict, RULES, llm=None)
    assert r.severity == Severity.REVIEW


def test_message_body_is_wrapped_as_untrusted_data():
    llm = FakeLLM(json.dumps({"severity": "routine", "departments": [],
                              "summary": "x", "rationale": "y"}))
    triage(EVENT, PASSED, RULES, llm=llm)
    user_msg = llm.messages[1]["content"]
    assert "UNTRUSTED MESSAGE" in user_msg
    assert EVENT.body in user_msg
