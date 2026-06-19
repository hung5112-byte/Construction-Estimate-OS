"""Load config from .vncoderc or vncode-config.yaml."""
from __future__ import annotations
from pathlib import Path
from typing import Literal, Optional
import os
import yaml
from pydantic import BaseModel, Field


class MeetingConfig(BaseModel):
    # Defaults tuned for MCP sampling latency: each LLM call ~10-30s via Claude Desktop.
    # Lite defaults (0/1/3) run ~1-2 minutes, enough for most operational decisions.
    # The manager opts into a deeper debate via .vncoderc when needed (old 2/3/5 → strategic decisions).
    max_perspective_rounds: int = 0
    max_debate_rounds: int = 1
    max_perspective_debate_rounds: int = 1
    total_max: int = 3
    use_checkpointer: bool = False
    # V2 intra-department round: every team agent gives a short take, then the
    # department manager synthesizes them into the department perspective.
    # Cost: ~1 extra LLM call per team agent per participating department
    # (a 5-department meeting goes from ~5 to ~29 round-1 calls). Turn off via
    # .vncoderc (`meeting: {intra_department_round: false}`) for quick tasks.
    intra_department_round: bool = True


class LLMConfig(BaseModel):
    primary: str = "claude-sonnet-4-6"
    secondary: str = "gemini-2-5-pro"
    max_retries: int = 3
    max_tokens_per_task: int = 100_000
    max_cost_usd_per_task: float = 2.0


# translator_mode controls how far the TranslatorPipeline is applied:
#   "off"              — do not simplify any output
#   "final_only"       — apply only to the final decision report (default, preserves old behavior)
#   "all_intermediate" — apply to every output: perspectives, pro/con, final report
TranslatorMode = Literal["off", "final_only", "all_intermediate"]


class Config(BaseModel):
    vault_path: Optional[str] = None
    meeting: MeetingConfig = Field(default_factory=MeetingConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    # P1.6: translator scope — default "final_only" preserves old behavior
    translator_mode: TranslatorMode = "final_only"


KNOWN_API_KEYS = [
    "TAVILY_API_KEY",
    "ANTHROPIC_API_KEY",
    "DEEPSEEK_API_KEY",
    "GOOGLE_API_KEY",
    "OPENAI_API_KEY",
    "BRAVE_API_KEY",
]


def load_config(path: Optional[Path] = None) -> Config:
    """Load config from path, ~/.vncoderc, or return defaults."""
    candidates = ([path] if path else []) + [Path.home() / ".vncoderc"]
    for p in candidates:
        if p and p.exists():
            try:
                return Config(**yaml.safe_load(p.read_text(encoding="utf-8")))
            except Exception:
                pass  # malformed config — fall through to defaults
    return Config()


def load_vault_env(vault_path: Path) -> dict[str, str]:
    """Read <vault>/.env → dict (only *_API_KEY keys); does not inject into os.environ."""
    env_path = Path(vault_path) / ".env"
    if not env_path.exists():
        return {}
    result: dict[str, str] = {}
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k.endswith("_API_KEY") or k in KNOWN_API_KEYS:
            result[k] = v
    return result


def save_vault_env(vault_path: Path, keys: dict[str, str]) -> Path:
    """Save API keys to <vault>/.env (merge with existing keys). Ensures .gitignore.

    Args:
        vault_path: Vault directory
        keys: Dict {KEY_NAME: value}. Empty values are skipped.
    """
    vault = Path(vault_path)
    env_path = vault / ".env"
    existing = load_vault_env(vault) if env_path.exists() else {}
    existing.update({k: v for k, v in keys.items() if v})

    lines = ["# VN Business OS — API keys (do NOT commit this file)"]
    for k in KNOWN_API_KEYS:
        if k in existing:
            lines.append(f"{k}={existing[k]}")
    for k in sorted(existing):
        if k not in KNOWN_API_KEYS:
            lines.append(f"{k}={existing[k]}")
    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    gitignore = vault / ".gitignore"
    ignore_lines = (
        gitignore.read_text(encoding="utf-8").splitlines() if gitignore.exists() else []
    )
    if ".env" not in {ln.strip() for ln in ignore_lines}:
        ignore_lines.append(".env")
        gitignore.write_text("\n".join(ignore_lines) + "\n", encoding="utf-8")

    return env_path


def apply_vault_env_to_os(vault_path: Path) -> dict[str, str]:
    """Load vault/.env and set into os.environ (only if not already set). Returns keys applied.

    Also exports BD_OS_ACTIVE_VAULT so downstream code that never sees the vault
    argument (e.g. the LLM usage log) can resolve the active vault.
    """
    os.environ["BD_OS_ACTIVE_VAULT"] = str(Path(vault_path))
    keys = load_vault_env(vault_path)
    for k, v in keys.items():
        if v and not os.environ.get(k):
            os.environ[k] = v
    return keys
