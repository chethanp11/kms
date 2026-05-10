"""Governance and policy-gate scaffold."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from src.contracts import ApprovalDecision, ApprovalRecord, KnowledgePage


class GateResult(str, Enum):
    PASS = "pass"
    REVIEW_REQUIRED = "review_required"
    BLOCK = "block"


@dataclass(frozen=True)
class PolicyFinding:
    rule_id: str
    severity: str
    message: str


@dataclass(frozen=True)
class QAReport:
    result: GateResult
    findings: tuple[PolicyFinding, ...] = ()

    @property
    def can_publish(self) -> bool:
        return self.result is GateResult.PASS


def validate_page_candidate(page: KnowledgePage) -> QAReport:
    """Run minimal fail-closed checks for a wiki page candidate."""

    findings: list[PolicyFinding] = []
    if "Source Trace" not in page.body:
        findings.append(PolicyFinding("kms.source_trace.required", "error", "Knowledge page body must include a Source Trace section."))
    if findings:
        return QAReport(GateResult.BLOCK, tuple(findings))
    return QAReport(GateResult.PASS)


def approval_allows_publication(record: ApprovalRecord) -> bool:
    return record.decision is ApprovalDecision.APPROVED


__all__ = ["GateResult", "PolicyFinding", "QAReport", "approval_allows_publication", "validate_page_candidate"]
