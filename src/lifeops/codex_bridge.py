"""Codex bridge helpers.

PowerShell startup scripts perform the Stage 1 Codex CLI launch. Stage 2 will
add intervention prompt dispatch.
"""

from __future__ import annotations

from pathlib import Path


def read_prompt(path: Path) -> str:
    return path.read_text(encoding="utf-8")
