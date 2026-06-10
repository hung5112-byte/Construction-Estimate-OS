"""Multi-provider LLM abstraction (stub — full impl in Phase 4)."""
from __future__ import annotations
import asyncio
import inspect
import os
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
        client = Anthropic(api_key=self.api_key)
        resp = client.messages.create(
            model=model or self.default_model,
            max_tokens=4096,
            messages=messages,
        )
        return resp.content[0].text

    async def acomplete(self, messages: list[dict], model: str | None = None) -> str:
        import asyncio
        return await asyncio.to_thread(self.complete, messages, model)


class MCPSamplingProvider:
    """LLM provider routing complete() through the MCP sampling protocol.

    Lets vn-business-os run inside a Claude Desktop / Code session,
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

        return self._extract_text(result)

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
        return self._extract_text(result)

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


class DeepSeekProvider:
    """LLM provider for DeepSeek API (OpenAI-compatible).

    Endpoint: https://api.deepseek.com (OpenAI-compat) or /anthropic
    Models: deepseek-v4-pro (default, premium), deepseek-v4-flash (~6x cheaper).
    ~10x cheaper than Claude, good for small businesses.
    """
    name = "deepseek"

    def __init__(
        self,
        api_key: str | None = None,
        default_model: str = "deepseek-v4-pro",
        base_url: str = "https://api.deepseek.com",
    ):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.default_model = default_model
        self.base_url = base_url

    def complete(self, messages: list[dict], model: str | None = None) -> str:
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        # DeepSeek v4-pro has thinking mode ON by default (slow + token-heavy).
        # Turn it off via extra_body for 3-5x faster responses on meeting nodes.
        resp = client.chat.completions.create(
            model=model or self.default_model,
            messages=messages,
            max_tokens=4096,
            extra_body={"thinking": {"type": "disabled"}},
        )
        return resp.choices[0].message.content or ""

    async def acomplete(self, messages: list[dict], model: str | None = None) -> str:
        return await asyncio.to_thread(self.complete, messages, model)


def get_default_provider() -> LLMProvider:
    """Pick provider based on env vars (priority: DeepSeek > Anthropic).

    DeepSeek is preferred because it's ~10x cheaper — good for small businesses.
    Set DEEPSEEK_API_KEY in vault/.env or os.environ to use DeepSeek.
    Falls back to Anthropic if only ANTHROPIC_API_KEY is set.
    """
    if os.getenv("DEEPSEEK_API_KEY"):
        return DeepSeekProvider()
    return ClaudeProvider()
