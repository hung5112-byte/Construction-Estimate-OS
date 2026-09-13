from core.agents.base_agent import BaseAgent
from unittest.mock import MagicMock


def test_base_agent_speak_calls_llm():
    mock_llm = MagicMock()
    mock_llm.complete.return_value = "I agree with option A because..."

    agent = BaseAgent(
        name_local="Test Agent",
        role="tester",
        system_prompt="You are a test specialist.",
        llm=mock_llm,
    )

    response = agent.speak(
        brief="Test brief",
        brain_context={"strategy": "..."},
        history=[],
    )

    assert "agree" in response
    mock_llm.complete.assert_called_once()


def test_base_agent_includes_brain_in_prompt():
    mock_llm = MagicMock()
    mock_llm.complete.return_value = "ok"

    agent = BaseAgent(name_local="A", role="r", system_prompt="sys", llm=mock_llm)
    agent.speak(brief="b", brain_context={"strategy": "US"}, history=[])

    # Verify brain_context is injected
    call_args = mock_llm.complete.call_args
    messages = call_args[0][0] if call_args[0] else call_args.kwargs["messages"]
    full_text = str(messages)
    assert "US" in full_text
