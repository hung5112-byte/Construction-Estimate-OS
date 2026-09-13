"""Multi-provider LLM abstraction (stub — full impl in Phase 4)."""
from __future__ import annotations
import asyncio
import inspect
import os
import shutil
from typing import Any, Protocol, runtime_checkable


async def _wrap_with_timeout(coro: Any, timeout: float) -> Any:
    """Wrap a coroutine with an asyncio timeout. Raises asyncio.TimeoutError on expiry."""
    return await asyncio.wait_for(coro, timeout=timeout)


@runtime_checkable
class LLMProvider(Protocol):
    name: str

    def complete(self, messages: list[dict], model: str | None = None) -> str:
        ...


class ClaudeProvider:
    name = "claude"

    def __init__(self, api_key: str | None = None, default_model: str = "claude-sonnet-4-6"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.default_model = default_model

    def complete(self, messages: list[dict], model: str | None = None) -> str:
        from anthropic import Anthropic

        from core.llm.usage_log import log_usage
        client = Anthropic(api_key=self.api_key)
        # Anthropic Messages API rejects role="system" inside messages — it must be
        # the top-level `system` parameter (OpenAI-compatible providers accept both).
        system_parts = [str(m.get("content", "")) for m in messages if m.get("role") == "system"]
        conv = [m for m in messages if m.get("role") != "system"]
        kwargs: dict = {
            "model": model or self.default_model,
            "max_tokens": 4096,
            "messages": conv,
        }
        if system_parts:
            kwargs["system"] = "\n\n".join(system_parts)
        resp = client.messages.create(**kwargs)
        usage = getattr(resp, "usage", None)
        if usage is not None:
            log_usage(
                self.name,
                model or self.default_model,
                getattr(usage, "input_tokens", 0),
                getattr(usage, "output_tokens", 0),
            )
        return resp.content[0].text

    async def acomplete(self, messages: list[dict], model: str | None = None) -> str:
        import asyncio
        return await asyncio.to_thread(self.complete, messages, model)


class ClaudeCLIProvider:
    """LLM provider that shells out to headless Claude Code (`claude -p`).

    Bills the user's Claude subscription (Max/Pro) instead of the Anthropic
    API — the robust subscription path for CLI + MCP + any tab (MCP sampling
    is Desktop-only; the Code tab doesn't support it).

    Invocation contract (Claude Code CLI ≥2.1):
    - prompt via STDIN (never argv — prompts exceed arg limits)
    - `--system-prompt <text>` for the system message (replaces the CLI's
      default agentic prompt — this is a pure LLM call); folded into stdin
      when it exceeds _MAX_SYSTEM_ARG (argv safety)
    - `--tools ""` disables every built-in tool; `--no-session-persistence`
      keeps runs off disk; `--output-format json` yields result text + usage
    - subprocess cwd is a temp dir so the CLI never loads a project's
      CLAUDE.md or trips a folder-trust prompt
    - the child env is SCRUBBED of ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN —
      otherwise the CLI itself may bill the API instead of the subscription,
      the exact thing this provider eliminates

    Temperature: accepted nowhere — the CLI does not expose a temperature
    knob; BaseAgent temperatures are ignored on this provider (documented
    engine-wide behavior: providers only ever receive messages + model).
    """
    name = "claude-cli"

    #: env vars that would silently re-route billing to the API — always removed
    SCRUBBED_ENV_VARS = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")
    #: above this size the system prompt moves from argv into stdin
    _MAX_SYSTEM_ARG = 100_000
    #: pass-6 default (replay 5 crashed a heavy Synthesizer call at 300s —
    #: subscription latency runs 60-85s on heavy calls and the Max plan
    #: rate-limits across concurrent sessions, so full-context calls can queue)
    DEFAULT_TIMEOUT_SECONDS = 900.0
    #: short pause before the single timeout retry
    RETRY_BACKOFF_SECONDS = 5.0

    def __init__(
        self,
        default_model: str = "claude-sonnet-4-6",
        timeout_seconds: float | None = None,
        claude_bin: str | None = None,
    ):
        """
        timeout_seconds: per-call cap. Resolution: explicit arg →
            BD_OS_LLM_TIMEOUT_SECONDS env → 900s default (claude-cli only;
            other providers keep their own defaults). One retry on timeout,
            then a rich error (elapsed / model / prompt size).
        claude_bin: explicit binary path; else env BD_OS_CLAUDE_BIN; else
            `claude` on PATH. Missing binary fails loudly at startup.
        """
        self.default_model = default_model
        if timeout_seconds is None:
            env_timeout = os.getenv("BD_OS_LLM_TIMEOUT_SECONDS", "").strip()
            timeout_seconds = (
                float(env_timeout) if env_timeout else self.DEFAULT_TIMEOUT_SECONDS
            )
        self.timeout_seconds = float(timeout_seconds)
        resolved = (
            claude_bin
            or os.getenv("BD_OS_CLAUDE_BIN")
            or shutil.which("claude")
        )
        # Absolutize: complete() runs the subprocess from a temp-dir cwd, so a
        # relative path (e.g. .tools/node_modules/.bin/claude) would not resolve.
        resolved = os.path.abspath(resolved) if resolved else None
        if not resolved or not os.path.exists(resolved):
            raise RuntimeError(
                "claude-cli provider selected but the `claude` binary was not "
                "found. Install Claude Code (npm install -g "
                "@anthropic-ai/claude-code) or point BD_OS_CLAUDE_BIN at the "
                "binary, then log in once with `claude /login` so headless "
                "runs can use the subscription."
            )
        self.claude_bin = resolved

    # ── public API ───────────────────────────────────────────────────────────

    def complete(self, messages: list[dict], model: str | None = None) -> str:
        import subprocess
        import tempfile
        import time as _time

        system_prompt, prompt = self._render(messages)
        argv = [
            self.claude_bin,
            "-p",
            "--output-format", "json",
            "--tools", "",
            "--no-session-persistence",
            "--model", model or self.default_model,
        ]
        if system_prompt and len(system_prompt) <= self._MAX_SYSTEM_ARG:
            argv += ["--system-prompt", system_prompt]
        elif system_prompt:
            prompt = (
                f"## SYSTEM INSTRUCTIONS (follow these for this reply)\n"
                f"{system_prompt}\n\n## REQUEST\n{prompt}"
            )
        prompt_chars = len(prompt) + len(system_prompt or "")

        env = os.environ.copy()
        for var in self.SCRUBBED_ENV_VARS:
            env.pop(var, None)

        # Retry ONCE on timeout with a short backoff (replay 5: a heavy
        # Synthesizer call died on a single hard cap mid-meeting). Two
        # consecutive timeouts raise with the full picture — no infinite patience.
        proc = None
        wall_seconds = 0.0
        for attempt in (1, 2):
            t0 = _time.monotonic()
            try:
                proc = subprocess.run(
                    argv,
                    input=prompt,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout_seconds,
                    env=env,
                    cwd=tempfile.gettempdir(),
                )
                wall_seconds = _time.monotonic() - t0
                break
            except subprocess.TimeoutExpired as e:
                elapsed = _time.monotonic() - t0
                from core.llm.usage_log import log_llm_event
                if attempt == 1:
                    log_llm_event(
                        self.name, "llm:retry",
                        reason="timeout",
                        attempt=attempt,
                        elapsed_seconds=round(elapsed, 1),
                        timeout_seconds=self.timeout_seconds,
                        model=model or self.default_model,
                        prompt_chars=prompt_chars,
                        backoff_seconds=self.RETRY_BACKOFF_SECONDS,
                    )
                    _time.sleep(self.RETRY_BACKOFF_SECONDS)
                    continue
                raise RuntimeError(
                    f"claude -p timed out on both attempts: {elapsed:.0f}s "
                    f"elapsed (cap {self.timeout_seconds:.0f}s per attempt) · "
                    f"model={model or self.default_model} · "
                    f"prompt={prompt_chars} chars (~{prompt_chars // 4} tokens). "
                    "Raise BD_OS_LLM_TIMEOUT_SECONDS (or llm.timeout_seconds in "
                    ".bd-os.yaml) or reduce the call's context."
                ) from e

        if proc.returncode != 0:
            # The CLI exits nonzero for error results too — surface the JSON
            # `result` field ("Not logged in · Please run /login", ...) rather
            # than a raw payload tail.
            detail = (proc.stderr or "").strip()
            try:
                import json as _json
                data = _json.loads(proc.stdout)
                detail = str(data.get("result", "")) or detail
            except (ValueError, TypeError):
                detail = detail or (proc.stdout or "").strip()[-500:]
            raise RuntimeError(
                f"claude -p exited {proc.returncode}: {detail[:500]}"
            )
        return self._parse_and_log(
            proc.stdout, messages, model,
            wall_seconds=wall_seconds, prompt_chars=prompt_chars,
        )

    async def acomplete(self, messages: list[dict], model: str | None = None) -> str:
        return await asyncio.to_thread(self.complete, messages, model)

    # ── internals ────────────────────────────────────────────────────────────

    @staticmethod
    def _render(messages: list[dict]) -> tuple[str, str]:
        """(system_prompt, stdin_prompt). Single user turn → raw content;
        multi-turn conversations are serialized with role headers."""
        system_parts = [
            str(m.get("content", "")) for m in messages if m.get("role") == "system"
        ]
        conv = [m for m in messages if m.get("role") != "system"]
        if len(conv) == 1:
            prompt = str(conv[0].get("content", ""))
        else:
            prompt = "\n\n".join(
                f"{str(m.get('role', 'user')).capitalize()}: {m.get('content', '')}"
                for m in conv
            )
        return "\n\n".join(system_parts), prompt

    def _parse_and_log(
        self,
        stdout: str,
        messages: list[dict],
        model: str | None,
        wall_seconds: float = 0.0,
        prompt_chars: int = 0,
    ) -> str:
        """Extract result text + usage from `--output-format json`; fall back
        to plain-text parsing if the JSON shape surprises.

        Every call logs its latency profile (pass 6): wall_seconds measured
        around the subprocess, duration_ms/duration_api_ms from the CLI's own
        JSON, and prompt_chars — enough to compute the subscription's real
        p50/p95 by call type from .bd-usage.jsonl.
        """
        import json as _json

        from core.llm.usage_log import estimate_tokens, log_usage

        text: str
        input_tokens: int
        output_tokens: int
        estimated = False
        extra: dict = {
            "wall_seconds": round(wall_seconds, 2),
            "prompt_chars": prompt_chars,
        }
        try:
            data = _json.loads(stdout)
            if not isinstance(data, dict):
                raise ValueError("not a JSON object")
            if data.get("is_error"):
                # e.g. "Not logged in · Please run /login" — fail loudly, the
                # run must never silently continue on an errored completion.
                raise RuntimeError(
                    f"claude -p returned an error result: "
                    f"{str(data.get('result', ''))[:300]}"
                )
            text = str(data.get("result", ""))
            usage = data.get("usage") or {}
            input_tokens = int(usage.get("input_tokens", 0)) + int(
                usage.get("cache_read_input_tokens", 0)
            ) + int(usage.get("cache_creation_input_tokens", 0))
            output_tokens = int(usage.get("output_tokens", 0))
            if "duration_ms" in data:
                extra["duration_ms"] = int(data["duration_ms"])
            if "duration_api_ms" in data:
                extra["duration_api_ms"] = int(data["duration_api_ms"])
            if input_tokens == 0 and output_tokens == 0:
                estimated = True
                input_tokens = estimate_tokens(
                    " ".join(str(m.get("content", "")) for m in messages)
                )
                output_tokens = estimate_tokens(text)
        except (ValueError, _json.JSONDecodeError):
            # plain-text fallback (--output-format surprises / older CLIs)
            text = stdout.strip()
            estimated = True
            input_tokens = estimate_tokens(
                " ".join(str(m.get("content", "")) for m in messages)
            )
            output_tokens = estimate_tokens(text)

        log_usage(
            self.name,
            model or self.default_model,
            input_tokens,
            output_tokens,
            estimated=estimated,
            extra=extra,
        )
        return text


class MCPSamplingProvider:
    """LLM provider routing complete() through the MCP sampling protocol.

    Lets bd-business-os run inside a Claude Desktop / Code session,
    using the subscription instead of an API key.

    Spec: https://modelcontextprotocol.io/docs/concepts/sampling

    Requires: an instance with a `create_message` method (async or sync) — typically
    `mcp.server.session.ServerSession` accessed via `server.request_context.session`.

    Real MCP SDK API (mcp>=1.0.0):
        await session.create_message(
            messages=[SamplingMessage(role=..., content=TextContent(...))],
            max_tokens=4096,
            model_preferences=ModelPreferences(hints=[ModelHint(name=...)]),
        ) -> CreateMessageResult(content=TextContent(text=...), ...)
    """
    name = "mcp-sampling"

    def __init__(
        self,
        mcp_server: Any,
        default_model: str = "claude-sonnet-4-6",
        max_retries: int = 4,
        timeout_seconds: float = 120.0,
        retry_initial_delay: float = 1.0,
        rate_limit_initial_delay: float = 15.0,
    ):
        """
        mcp_server: object exposing `create_message(...)` — real MCP `ServerSession`
                    or a duck-typed compatible object (mock-friendly for testing).
        max_retries: retries for transient errors (rate limit, timeout, network)
        timeout_seconds: hard timeout for each sampling call
        retry_initial_delay: backoff delay (sec) for transient errors (timeout/network);
                             doubles each retry
        rate_limit_initial_delay: backoff delay (sec) for a rate limit (429); doubles each
                                  retry. Anthropic's reset window is ~60s → needs a longer wait.
                                  Default 15s → 30s → 60s → 120s = total ~225s, enough to clear
                                  one reset window.
        """
        self.server = mcp_server
        self.default_model = default_model
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds
        self.retry_initial_delay = retry_initial_delay
        self.rate_limit_initial_delay = rate_limit_initial_delay

    @staticmethod
    def _is_rate_limit(exc: BaseException) -> bool:
        """429 / rate limit specifically — needs a longer backoff than other transients."""
        name = type(exc).__name__.lower()
        msg = str(exc).lower()
        return "ratelimit" in name or "429" in msg or "rate limit" in msg

    @classmethod
    def _is_retryable(cls, exc: BaseException) -> bool:
        """Decide which exceptions should be retried (rate limit / timeout / transient network).

        Identified by class name or message — covers Anthropic, MCP, asyncio, httpx.
        """
        if cls._is_rate_limit(exc):
            return True
        name = type(exc).__name__.lower()
        msg = str(exc).lower()
        if "timeout" in name or "timeout" in msg or "timed out" in msg:
            return True
        if "connection" in name or "connection" in msg:
            return True
        if "overloaded" in msg or "503" in msg or "502" in msg:
            return True
        return False

    def _initial_delay_for(self, exc: BaseException) -> float:
        """Pick initial backoff: longer for 429, shorter for other transients."""
        return self.rate_limit_initial_delay if self._is_rate_limit(exc) else self.retry_initial_delay

    def complete(self, messages: list[dict], model: str | None = None) -> str:
        """Send a sampling request via MCP with retry-with-backoff + timeout.

        An MCP SamplingMessage only accepts role 'user'/'assistant' — the system message
        is split into the `system_prompt` kwarg. Retry for rate limit/timeout/network errors.
        Backoff for a 429 is longer (15s base) than for a transient (1s base) — Anthropic's
        rate limit resets ~60s, so wait long enough to clear the reset window.
        """
        last_exc: BaseException | None = None
        delay: float | None = None  # set per error type in the exception handler

        for attempt in range(self.max_retries + 1):
            try:
                return self._do_complete(messages, model)
            except Exception as e:  # noqa: BLE001
                last_exc = e
                if attempt >= self.max_retries or not self._is_retryable(e):
                    raise
                if delay is None:
                    delay = self._initial_delay_for(e)
                import time
                time.sleep(delay)
                delay *= 2  # exponential backoff

        # Unreachable — but Python static analysis happier with explicit raise
        raise last_exc or RuntimeError("MCPSamplingProvider.complete failed")

    def _do_complete(self, messages: list[dict], model: str | None) -> str:
        """One attempt — no retry, with timeout."""
        system_prompt, conv_messages = self._split_system(messages)
        sampling_messages, model_prefs = self._build_request_payload(
            conv_messages, model
        )

        kwargs: dict[str, Any] = {
            "messages": sampling_messages,
            "model_preferences": model_prefs,
            "max_tokens": 4096,
        }
        if system_prompt:
            kwargs["system_prompt"] = system_prompt

        result = self.server.create_message(**kwargs)

        # ServerSession.create_message is async — auto-await with timeout.
        if inspect.isawaitable(result):
            result = self._run_sync_with_timeout(result, self.timeout_seconds)

        text = self._extract_text(result)
        self._log_estimated(messages, text, model)
        return text

    async def acomplete(self, messages: list[dict], model: str | None = None) -> str:
        """Async version — used in async MCP tool functions to avoid a deadlock.

        FastMCP calls a sync tool directly on the event loop, so complete() deadlocks
        when it tries to run create_message() in a new ThreadPoolExecutor. acomplete() awaits
        create_message() directly on the current event loop — no threading.
        Backoff for a 429 is longer (15s base) than for a transient (1s base).
        """
        last_exc: BaseException | None = None
        delay: float | None = None

        for attempt in range(self.max_retries + 1):
            try:
                return await self._do_acomplete(messages, model)
            except Exception as e:  # noqa: BLE001
                last_exc = e
                if attempt >= self.max_retries or not self._is_retryable(e):
                    raise
                if delay is None:
                    delay = self._initial_delay_for(e)
                import asyncio
                await asyncio.sleep(delay)
                delay *= 2

        raise last_exc or RuntimeError("MCPSamplingProvider.acomplete failed")

    async def _do_acomplete(self, messages: list[dict], model: str | None) -> str:
        """One async attempt — await create_message() directly."""
        system_prompt, conv_messages = self._split_system(messages)
        sampling_messages, model_prefs = self._build_request_payload(conv_messages, model)

        kwargs: dict[str, Any] = {
            "messages": sampling_messages,
            "model_preferences": model_prefs,
            "max_tokens": 4096,
        }
        if system_prompt:
            kwargs["system_prompt"] = system_prompt

        result = self.server.create_message(**kwargs)
        if inspect.isawaitable(result):
            result = await result
        text = self._extract_text(result)
        self._log_estimated(messages, text, model)
        return text

    def _log_estimated(self, messages: list[dict], completion: str, model: str | None) -> None:
        """MCP sampling returns no usage data — log chars/4 estimates instead."""
        from core.llm.usage_log import estimate_tokens, log_usage
        prompt_chars = sum(len(str(m.get("content", ""))) for m in messages)
        log_usage(
            self.name,
            model or self.default_model,
            estimate_tokens(" " * prompt_chars),
            estimate_tokens(completion),
            estimated=True,
        )

    @staticmethod
    def _run_sync_with_timeout(coro: Any, timeout: float) -> Any:
        """Run a coroutine synchronously with a hard timeout."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(asyncio.run, _wrap_with_timeout(coro, timeout))
                    return future.result()
        except RuntimeError:
            pass
        return asyncio.run(_wrap_with_timeout(coro, timeout))

    @staticmethod
    def _split_system(messages: list[dict]) -> tuple[str, list[dict]]:
        """Split messages with role='system' into a system_prompt string + the rest.

        If there are multiple system messages → join with "\n\n". Ensures conv_messages
        contains only user/assistant.
        """
        system_parts: list[str] = []
        rest: list[dict] = []
        for m in messages:
            if m.get("role") == "system":
                system_parts.append(str(m.get("content", "")))
            else:
                rest.append(m)
        return "\n\n".join(system_parts), rest

    def _build_request_payload(
        self, messages: list[dict], model: str | None
    ) -> tuple[Any, Any]:
        """Build request payload using MCP types when available, else raw dict.

        Returns (sampling_messages, model_preferences). Falls back to plain
        dicts/strings if mcp.types import fails — keeps unit tests w/ MagicMock
        servers working without the real SDK.
        """
        model_name = model or self.default_model
        try:
            from mcp.types import (
                ModelHint,
                ModelPreferences,
                SamplingMessage,
                TextContent,
            )
            sampling_msgs = [
                SamplingMessage(
                    role=m["role"],
                    content=TextContent(type="text", text=str(m["content"])),
                )
                for m in messages
            ]
            prefs = ModelPreferences(hints=[ModelHint(name=model_name)])
            return sampling_msgs, prefs
        except Exception:
            # Fallback used in tests with mock server.
            return messages, {"hints": [{"name": model_name}]}

    @staticmethod
    def _run_sync(coro: Any) -> Any:
        """Run coroutine to completion from sync context."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Inside an active loop — schedule and wait via new loop.
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    return pool.submit(asyncio.run, coro).result()
        except RuntimeError:
            pass
        return asyncio.run(coro)

    @staticmethod
    def _extract_text(result: Any) -> str:
        """Pull text from MCP CreateMessageResult or dict response shape."""
        content = result.content if hasattr(result, "content") else result["content"]

        # MCP SDK returns single TextContent (not list). Tests use list shape.
        if isinstance(content, list):
            first = content[0]
            return first.text if hasattr(first, "text") else first["text"]
        if hasattr(content, "text"):
            return content.text
        if isinstance(content, dict):
            return content["text"]
        return str(content)


def get_default_provider() -> LLMProvider:
    """Pick provider based on env vars.

    BD_OS_LLM_PROVIDER ∈ {claude-cli, anthropic-api, mcp-sampling} overrides
    the key-presence heuristic (2026-07-05 ruling: runs move onto the Claude
    subscription via headless `claude -p`). Unset → existing behavior
    unchanged (ClaudeProvider / API).
    """
    choice = os.getenv("BD_OS_LLM_PROVIDER", "").strip().lower()
    if choice == "claude-cli":
        from core.utils.config import load_config
        return ClaudeCLIProvider(
            timeout_seconds=load_config().llm.timeout_seconds,  # None → env → 900s
        )
    if choice == "anthropic-api":
        return ClaudeProvider()
    if choice == "mcp-sampling":
        raise RuntimeError(
            "BD_OS_LLM_PROVIDER=mcp-sampling requires a live MCP session — it "
            "is only valid inside the MCP server (ce-os-mcp), not the CLI."
        )
    if choice:
        raise RuntimeError(
            f"Unknown BD_OS_LLM_PROVIDER '{choice}'. "
            "Valid: claude-cli | anthropic-api | mcp-sampling."
        )
    return ClaudeProvider()
