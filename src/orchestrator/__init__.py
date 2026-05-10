"""Run orchestration scaffold."""

from __future__ import annotations

from dataclasses import dataclass, replace

from src.contracts import MaintenanceRun, RunState, SourceBundle


@dataclass(frozen=True)
class RunSummary:
    run: MaintenanceRun
    source_count: int
    warning_count: int


def summarize_intake(run: MaintenanceRun, bundle: SourceBundle) -> RunSummary:
    state = RunState.COMPLETED if not bundle.warnings else RunState.BLOCKED
    updated_run = replace(run, state=state, summary_counts={"source_files": len(bundle.files), "warnings": len(bundle.warnings)})
    return RunSummary(run=updated_run, source_count=len(bundle.files), warning_count=len(bundle.warnings))


__all__ = ["RunSummary", "summarize_intake"]
