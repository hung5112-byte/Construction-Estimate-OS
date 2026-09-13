"""ClaudeCLIProvider — headless `claude -p` on the Claude subscription.

All subprocess interaction is mocked (no real CLI in the suite). Covers the
2026-07-05 pass-5 ruling: provider selection matrix, stdin delivery (never
argv), the billing-critical env scrub, json/text output parsing, missing
binary startup error, and usage-log integration.
"""
from __future__ import annotations

import json
import os
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from core.llm.providers import (
    ClaudeCLIProvider,
    ClaudeProvider,
    MCPSamplingProvider,
    get_default_provider,
)

OK_RESULT = json.dumps({
    "type": "result", "subtype": "success", "is_error": False,
    "result": "OK", "total_cost_usd": 0.0021,
    "usage": {"input_tokens": 10, "output_tokens": 2,
              "cache_read_input_tokens": 5, "cache_creation_input_tokens": 3},
})


def _provider(**kwargs) -> ClaudeCLIProvider:
    kwargs.setdefault("claude_bin", "/bin/echo")  # exists; never actually run
    return ClaudeCLIProvider(**kwargs)


def _run_capture(provider, messages, model=None, stdout=OK_RESULT, returncode=0):
    captured = {}

    def fake_run(argv, **kwargs):
        captured["argv"] = argv
        captured.update(kwargs)
        return SimpleNamespace(returncode=returncode, stdout=stdout, stderr="")

    with patch("subprocess.run", side_effect=fake_run), \
         patch("core.llm.usage_log.log_usage") as log:
        captured["result"] = provider.complete(messages, model=model)
        captured["log_usage"] = log
    return captured


class TestInvocationContract:
    def test_prompt_travels_via_stdin_never_argv(self):
        big_prompt = "analyze this brief " * 5000  # ~95KB — would blow argv
        cap = _run_capture(_provider(), [{"role": "user", "content": big_prompt}])
        assert cap["input"] == big_prompt
        assert all(big_prompt not in str(a) for a in cap["argv"])

    def test_flags_headless_json_no_tools_no_session(self):
        cap = _run_capture(_provider(), [{"role": "user", "content": "hi"}])
        argv = cap["argv"]
        assert "-p" in argv
        assert argv[argv.index("--output-format") + 1] == "json"
        assert argv[argv.index("--tools") + 1] == ""
        assert "--no-session-persistence" in argv

    def test_model_mapping_default_and_override(self):
        provider = _provider(default_model="claude-sonnet-4-6")
        cap = _run_capture(provider, [{"role": "user", "content": "hi"}])
        assert cap["argv"][cap["argv"].index("--model") + 1] == "claude-sonnet-4-6"
        cap = _run_capture(provider, [{"role": "user", "content": "hi"}],
                           model="claude-haiku-4-5")
        assert cap["argv"][cap["argv"].index("--model") + 1] == "claude-haiku-4-5"

    def test_system_prompt_via_flag(self):
        cap = _run_capture(_provider(), [
            {"role": "system", "content": "You are the CRITIC."},
            {"role": "user", "content": "judge this"},
        ])
        argv = cap["argv"]
        assert argv[argv.index("--system-prompt") + 1] == "You are the CRITIC."
        assert cap["input"] == "judge this"

    def test_oversized_system_prompt_folds_into_stdin(self):
        huge = "rule " * 30_000  # ~150KB > _MAX_SYSTEM_ARG
        cap = _run_capture(_provider(), [
            {"role": "system", "content": huge},
            {"role": "user", "content": "go"},
        ])
        assert "--system-prompt" not in cap["argv"]
        assert "SYSTEM INSTRUCTIONS" in cap["input"]
        assert huge[:500] in cap["input"] and cap["input"].endswith("go")

    def test_multi_turn_conversation_serialized_with_role_headers(self):
        cap = _run_capture(_provider(), [
            {"role": "user", "content": "first"},
            {"role": "assistant", "content": "reply"},
            {"role": "user", "content": "second"},
        ])
        assert "User: first" in cap["input"]
        assert "Assistant: reply" in cap["input"]

    def test_cwd_is_a_neutral_temp_dir_not_the_vault(self):
        import tempfile
        cap = _run_capture(_provider(), [{"role": "user", "content": "hi"}])
        assert cap["cwd"] == tempfile.gettempdir()

    def test_timeout_is_configurable_and_passed(self):
        cap = _run_capture(_provider(timeout_seconds=42.0),
                           [{"role": "user", "content": "hi"}])
        assert cap["timeout"] == 42.0


class TestEnvScrub:
    """CRITICAL: the child env must never carry API-billing credentials —
    otherwise the CLI bills the API instead of the subscription, the exact
    thing this provider exists to eliminate."""

    def test_anthropic_api_key_is_scrubbed_from_the_subprocess_env(self, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-would-bill-the-api")
        monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "tok-would-bill-the-api")
        monkeypatch.setenv("TAVILY_API_KEY", "tvly-needed-for-research")
        cap = _run_capture(_provider(), [{"role": "user", "content": "hi"}])
        child_env = cap["env"]
        assert "ANTHROPIC_API_KEY" not in child_env
        assert "ANTHROPIC_AUTH_TOKEN" not in child_env
        # everything else passes through untouched
        assert child_env.get("TAVILY_API_KEY") == "tvly-needed-for-research"
        # ...and the parent process env is NOT mutated
        assert os.environ["ANTHROPIC_API_KEY"] == "sk-ant-would-bill-the-api"


class TestOutputParsing:
    def test_json_result_text_and_usage_logged(self):
        cap = _run_capture(_provider(), [{"role": "user", "content": "hi"}])
        assert cap["result"] == "OK"
        log = cap["log_usage"]
        log.assert_called_once()
        args, kwargs = log.call_args
        assert args[0] == "claude-cli"
        assert args[2] == 18  # input 10 + cache_read 5 + cache_creation 3
        assert args[3] == 2
        assert kwargs.get("estimated", False) is False

    def test_plain_text_fallback_when_output_is_not_json(self):
        cap = _run_capture(_provider(), [{"role": "user", "content": "hi"}],
                           stdout="just plain text\n")
        assert cap["result"] == "just plain text"
        args, kwargs = cap["log_usage"].call_args
        assert kwargs.get("estimated") is True

    def test_is_error_result_raises_loudly(self):
        err = json.dumps({"type": "result", "is_error": True,
                          "result": "Not logged in · Please run /login",
                          "usage": {}})
        with pytest.raises(RuntimeError, match="Not logged in"):
            _run_capture(_provider(), [{"role": "user", "content": "hi"}],
                         stdout=err)

    def test_nonzero_exit_raises_with_stderr(self):
        def fake_run(argv, **kwargs):
            return SimpleNamespace(returncode=1, stdout="", stderr="boom")
        with patch("subprocess.run", side_effect=fake_run):
            with pytest.raises(RuntimeError, match="exited 1.*boom"):
                _provider().complete([{"role": "user", "content": "hi"}])

    async def test_acomplete_wraps_complete(self):
        provider = _provider()
        with patch.object(provider, "complete", return_value="async-ok") as c:
            out = await provider.acomplete([{"role": "user", "content": "hi"}])
        assert out == "async-ok"
        c.assert_called_once()


class TestBinaryResolution:
    def test_missing_binary_fails_loudly_at_startup(self, monkeypatch):
        monkeypatch.delenv("BD_OS_CLAUDE_BIN", raising=False)
        with patch("shutil.which", return_value=None):
            with pytest.raises(RuntimeError, match="binary was not.*found|not "):
                ClaudeCLIProvider()

    def test_env_override_wins(self, monkeypatch):
        monkeypatch.setenv("BD_OS_CLAUDE_BIN", "/bin/echo")
        with patch("shutil.which", return_value=None):
            provider = ClaudeCLIProvider()
        assert provider.claude_bin == "/bin/echo"


class TestProviderSelection:
    """BD_OS_LLM_PROVIDER matrix; unset → existing behavior byte-for-byte."""

    def test_unset_returns_claude_provider_unchanged(self, monkeypatch):
        monkeypatch.delenv("BD_OS_LLM_PROVIDER", raising=False)
        assert isinstance(get_default_provider(), ClaudeProvider)

    def test_claude_cli_selected(self, monkeypatch):
        monkeypatch.setenv("BD_OS_LLM_PROVIDER", "claude-cli")
        monkeypatch.setenv("BD_OS_CLAUDE_BIN", "/bin/echo")
        assert isinstance(get_default_provider(), ClaudeCLIProvider)

    def test_anthropic_api_selected(self, monkeypatch):
        monkeypatch.setenv("BD_OS_LLM_PROVIDER", "anthropic-api")
        assert isinstance(get_default_provider(), ClaudeProvider)

    def test_mcp_sampling_invalid_outside_the_mcp_server(self, monkeypatch):
        monkeypatch.setenv("BD_OS_LLM_PROVIDER", "mcp-sampling")
        with pytest.raises(RuntimeError, match="MCP session"):
            get_default_provider()

    def test_unknown_value_fails_loudly(self, monkeypatch):
        monkeypatch.setenv("BD_OS_LLM_PROVIDER", "gpt-something")
        with pytest.raises(RuntimeError, match="Unknown BD_OS_LLM_PROVIDER"):
            get_default_provider()

    def test_claude_cli_selected_but_binary_missing_is_a_clear_startup_error(
        self, monkeypatch
    ):
        monkeypatch.setenv("BD_OS_LLM_PROVIDER", "claude-cli")
        monkeypatch.delenv("BD_OS_CLAUDE_BIN", raising=False)
        with patch("shutil.which", return_value=None):
            with pytest.raises(RuntimeError, match="claude"):
                get_default_provider()


class TestMcpServerPickLlm:
    """The MCP server's picker honors the same env var."""

    def _ctx(self):
        return SimpleNamespace(session=MagicMock())

    def test_claude_cli_selected(self, monkeypatch):
        from core.mcp_server import _pick_llm
        monkeypatch.setenv("BD_OS_LLM_PROVIDER", "claude-cli")
        monkeypatch.setenv("BD_OS_CLAUDE_BIN", "/bin/echo")
        assert isinstance(_pick_llm(self._ctx()), ClaudeCLIProvider)

    def test_mcp_sampling_selected(self, monkeypatch):
        from core.mcp_server import _pick_llm
        monkeypatch.setenv("BD_OS_LLM_PROVIDER", "mcp-sampling")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-ignored-by-override")
        assert isinstance(_pick_llm(self._ctx()), MCPSamplingProvider)

    def test_unset_with_key_keeps_api_heuristic(self, monkeypatch):
        from core.mcp_server import _pick_llm
        monkeypatch.delenv("BD_OS_LLM_PROVIDER", raising=False)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-x")
        assert isinstance(_pick_llm(self._ctx()), ClaudeProvider)

    def test_unset_without_key_keeps_sampling_fallback(self, monkeypatch):
        from core.mcp_server import _pick_llm
        monkeypatch.delenv("BD_OS_LLM_PROVIDER", raising=False)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        assert isinstance(_pick_llm(self._ctx()), MCPSamplingProvider)


# ── Pass 6: meeting-proof timeout / retry / latency profile ─────────────────
# Replay 5 crashed mid-meeting: subprocess.TimeoutExpired on a heavy
# full-context Synthesizer call at the hard 300s cap (subscription latency
# runs 60-85s on heavy calls; Max-plan rate limits queue concurrent sessions).


class TestTimeoutConfiguration:
    def test_default_is_900s_for_claude_cli(self, monkeypatch):
        monkeypatch.delenv("BD_OS_LLM_TIMEOUT_SECONDS", raising=False)
        assert _provider().timeout_seconds == 900.0

    def test_env_var_overrides_default(self, monkeypatch):
        monkeypatch.setenv("BD_OS_LLM_TIMEOUT_SECONDS", "1234")
        assert _provider().timeout_seconds == 1234.0

    def test_explicit_arg_beats_env(self, monkeypatch):
        monkeypatch.setenv("BD_OS_LLM_TIMEOUT_SECONDS", "1234")
        assert _provider(timeout_seconds=42.0).timeout_seconds == 42.0

    def test_config_knob_flows_through_get_default_provider(self, monkeypatch):
        from core.utils import config as config_mod
        monkeypatch.setenv("BD_OS_LLM_PROVIDER", "claude-cli")
        monkeypatch.setenv("BD_OS_CLAUDE_BIN", "/bin/echo")
        monkeypatch.delenv("BD_OS_LLM_TIMEOUT_SECONDS", raising=False)
        cfg = config_mod.Config()
        cfg.llm.timeout_seconds = 600.0
        monkeypatch.setattr(config_mod, "load_config", lambda *a, **k: cfg)
        provider = get_default_provider()
        assert provider.timeout_seconds == 600.0

    def test_config_none_falls_back_to_env_then_default(self, monkeypatch):
        monkeypatch.delenv("BD_OS_LLM_TIMEOUT_SECONDS", raising=False)
        assert ClaudeCLIProvider(
            timeout_seconds=None, claude_bin="/bin/echo").timeout_seconds == 900.0


class TestTimeoutRetry:
    def _timeout_exc(self):
        import subprocess
        return subprocess.TimeoutExpired(cmd="claude", timeout=900)

    def test_retry_once_on_timeout_then_success(self, monkeypatch):
        provider = _provider()
        calls = []

        def fake_run(argv, **kwargs):
            calls.append(argv)
            if len(calls) == 1:
                raise self._timeout_exc()
            return SimpleNamespace(returncode=0, stdout=OK_RESULT, stderr="")

        with patch("subprocess.run", side_effect=fake_run), \
             patch("time.sleep") as sleep, \
             patch("core.llm.usage_log.log_llm_event") as event, \
             patch("core.llm.usage_log.log_usage"):
            out = provider.complete([{"role": "user", "content": "hi"}])

        assert out == "OK"
        assert len(calls) == 2  # one retry, no more
        sleep.assert_called_once_with(provider.RETRY_BACKOFF_SECONDS)
        # loud llm:retry event with the diagnostic fields
        event.assert_called_once()
        args, kwargs = event.call_args
        assert args[0] == "claude-cli" and args[1] == "llm:retry"
        assert kwargs["reason"] == "timeout"
        assert kwargs["timeout_seconds"] == provider.timeout_seconds
        assert kwargs["model"] == provider.default_model
        assert kwargs["prompt_chars"] == len("hi")

    def test_two_consecutive_timeouts_raise_rich_error(self):
        provider = _provider(timeout_seconds=7.0)
        prompt = "x" * 400

        with patch("subprocess.run", side_effect=self._timeout_exc()), \
             patch("time.sleep"), \
             patch("core.llm.usage_log.log_llm_event"):
            with pytest.raises(RuntimeError) as exc:
                provider.complete(
                    [{"role": "user", "content": prompt}],
                    model="claude-haiku-4-5",
                )
        msg = str(exc.value)
        assert "timed out on both attempts" in msg
        assert "cap 7s" in msg                    # the elapsed/cap time
        assert "claude-haiku-4-5" in msg          # the model
        assert "400 chars" in msg                 # the prompt size
        assert "BD_OS_LLM_TIMEOUT_SECONDS" in msg  # the operator's lever


class TestLatencyProfileLogging:
    def test_every_call_logs_duration_and_prompt_size(self):
        cli_json = json.dumps({
            "type": "result", "is_error": False, "result": "OK",
            "duration_ms": 83250, "duration_api_ms": 81000,
            "usage": {"input_tokens": 10, "output_tokens": 2},
        })
        cap = _run_capture(_provider(), [
            {"role": "system", "content": "sys"},
            {"role": "user", "content": "hello"},
        ], stdout=cli_json)
        _, kwargs = cap["log_usage"].call_args
        extra = kwargs["extra"]
        assert extra["duration_ms"] == 83250
        assert extra["duration_api_ms"] == 81000
        assert extra["prompt_chars"] == len("sys") + len("hello")
        assert extra["wall_seconds"] >= 0.0

    def test_plain_text_fallback_still_logs_the_profile(self):
        cap = _run_capture(_provider(), [{"role": "user", "content": "hi"}],
                           stdout="plain")
        _, kwargs = cap["log_usage"].call_args
        assert "wall_seconds" in kwargs["extra"]
        assert kwargs["extra"]["prompt_chars"] == len("hi")


class TestJudgeModelTier:
    """Pass-6 item 4: the judged rubrics' 5-sample majority runs on the haiku
    tier by default — true since pass 1 (judge_model='quick' → haiku); pinned
    here so it can never silently drift while synthesizer/debaters stay on the
    configured deep model (llm.primary)."""

    def test_default_judge_model_resolves_to_haiku(self):
        from core.critic.constants import MODEL_TIER_QUICK, resolve_judge_model
        from core.utils.config import CriticConfig
        assert CriticConfig().judge_model == "quick"
        assert resolve_judge_model("quick", "claude-sonnet-4-6") == MODEL_TIER_QUICK
        assert MODEL_TIER_QUICK == "claude-haiku-4-5"

    def test_critic_loop_uses_haiku_while_primary_stays_deep(self):
        from core.critic.loop import CriticLoop
        from core.utils.config import CriticConfig
        loop = CriticLoop(
            llm=MagicMock(), config=CriticConfig(), vault_root="/tmp",
            primary_model="claude-sonnet-4-6",
        )
        assert loop.judge_model == "claude-haiku-4-5"
