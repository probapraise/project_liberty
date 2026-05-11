"""Policy engine scaffold.

Stage 2 will implement deterministic allow/intervention decisions. Stage 1 keeps
this module importable so scripts and tests have a stable target.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyDecision:
    action: str
    reason: str
    risk_level: str = "green"


def evaluate_stage1() -> PolicyDecision:
    return PolicyDecision(
        action="log_only",
        reason="Stage 1 placeholder: real activity policy starts in Stage 2.",
    )
