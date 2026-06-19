"""Single source of truth for bundled-data locations.

All packaged data — `templates-us/`, `departments/`, `packs/`, `vault-template/` —
lives under the repo's `docs/` folder (the `core` package is at `docs/core`).

These helpers resolve that folder ROBUSTLY: instead of counting `.parent` levels
from each caller (fragile — breaks if a module moves), they locate the data root by
searching upward for the `templates-us` directory. Use `templates_root()` everywhere
a default-template path is needed.
"""
from __future__ import annotations
from pathlib import Path

# Marker dirs that identify the bundled-data root (any one is sufficient).
_MARKERS = ("templates-us", "departments", "vault-template")


def data_root() -> Path:
    """Return the folder that holds templates-us/ departments/ packs/ vault-template/.

    In this repo that is `docs/`. Resolved by walking up from this file until a
    folder containing a marker dir is found, so it is invariant to where callers live.
    """
    here = Path(__file__).resolve().parent.parent  # docs/core -> docs
    for base in (here, *here.parents):
        if any((base / m).is_dir() for m in _MARKERS):
            return base
    return here


def templates_root() -> Path:
    """Absolute path to the default template library (`docs/templates-us`)."""
    return data_root() / "templates-us"
