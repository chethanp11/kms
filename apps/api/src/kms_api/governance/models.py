from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

RuleSeverity = Literal["error", "warning"]
RuleAction = Literal["block_publish", "escalate_review", "log_only"]
GovernanceStatus = Literal["pass", "review_required", "blocked"]
SourceTraceStatus = Literal["missing", "partial", "complete"]
ContradictionStatus = Literal["clear", "review_required", "blocked"]


@dataclass(frozen=True)
class GovernanceRule:
    rule_id: str
    description: str
    scope_page_types: tuple[str, ...]
    severity: RuleSeverity
    condition: dict[str, Any]
    action: RuleAction
    source_file: str


@dataclass(frozen=True)
class RuleFinding:
    rule_id: str
    severity: RuleSeverity
    action: RuleAction
    message: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class GovernanceDecision:
    run_id: str
    revision_id: str | None
    page_id: str | None
    status: GovernanceStatus
    publish_allowed: bool
    approval_required: bool
    source_trace_status: SourceTraceStatus
    contradiction_status: ContradictionStatus
    qa_report_id: str
    rule_findings: list[RuleFinding] = field(default_factory=list)
    messages: list[str] = field(default_factory=list)
    revision_status: Literal["staged", "review_required", "approved", "rejected", "finalized"] = "staged"


@dataclass
class GovernanceValidationResult:
    rule_findings: list[RuleFinding]
    source_trace_status: SourceTraceStatus
    contradiction_status: ContradictionStatus
    approval_required: bool
    approval_record_id: str | None
    blocked: bool
    review_required: bool
    messages: list[str] = field(default_factory=list)
