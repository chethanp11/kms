"""Explicit run state transition helpers."""

from __future__ import annotations

from dataclasses import replace

from src.contracts import MaintenanceRun, RunState, ValidationError

_ALLOWED = {
    RunState.CREATED: {RunState.IN_PROGRESS, RunState.BLOCKED, RunState.FAILED},
    RunState.IN_PROGRESS: {RunState.COMPLETED, RunState.BLOCKED, RunState.FAILED},
    RunState.BLOCKED: {RunState.IN_PROGRESS, RunState.FAILED},
    RunState.FAILED: set(),
    RunState.COMPLETED: set(),
}


def transition_run(run: MaintenanceRun, target: RunState, *, reason: str = "") -> MaintenanceRun:
    if target not in _ALLOWED[run.state]:
        raise ValidationError(f"invalid run transition: {run.state.value} -> {target.value}")
    return replace(run, state=target, blocked_reason=reason if target is RunState.BLOCKED else run.blocked_reason)


__all__ = ["transition_run"]
