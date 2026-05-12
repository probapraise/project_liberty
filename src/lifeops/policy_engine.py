"""Policy engine scaffold.

Stage 2 will implement deterministic allow/intervention decisions. Stage 1 keeps
this module importable so scripts and tests have a stable target.
"""

from __future__ import annotations

from dataclasses import dataclass

from .app_scope import classify_monitored_process, is_monitored_process


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


def evaluate_process_scope(process_name: str | None) -> PolicyDecision:
    """Return the Stage 2 scope decision for a process name."""
    if not is_monitored_process(process_name):
        return PolicyDecision(
            action="ignore",
            reason="현재 감시 범위는 Chrome과 Steam으로 제한되어 있습니다.",
        )
    return PolicyDecision(
        action="log_only",
        reason=f"{classify_monitored_process(process_name)} scope candidate",
    )
