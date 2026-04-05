from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from kms_domain import AgentExecutionRecord, RunEvent

OrchestrationStage = Literal[
    "source_intake",
    "source_analysis",
    "wiki_impact",
    "wiki_curator",
    "policy_qa",
    "contradiction_review",
    "approval",
    "publisher",
    "lint",
]


@dataclass(frozen=True)
class OrchestrationRequest:
    source_root_path: str
    initiated_by: str
    domain_hint: str | None = None
    run_notes: str | None = None
    policy_version: str = "governance.v1"
    approval_decision: Literal["approved", "rejected", "deferred", "escalated"] | None = None
    approval_reviewer_id: str | None = None
    approval_reason: str | None = None


@dataclass(frozen=True)
class OrchestrationStageResult:
    stage: OrchestrationStage
    status: Literal["completed", "blocked", "failed"]
    message: str
    agent_name: str | None = None
    revision_id: str | None = None
    page_id: str | None = None
    details: dict[str, str] = field(default_factory=dict)


@dataclass
class OrchestrationResult:
    run_id: str
    run_status: str
    current_stage: str | None
    stage_results: list[OrchestrationStageResult] = field(default_factory=list)
    run_events: list[RunEvent] = field(default_factory=list)
    agent_executions: list[AgentExecutionRecord] = field(default_factory=list)
    revision_ids: list[str] = field(default_factory=list)
    lint_finding_ids: list[str] = field(default_factory=list)
    blocked_reason: str | None = None
