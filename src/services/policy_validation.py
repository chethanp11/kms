"""Policy validation service for page candidates."""

from __future__ import annotations

from src.contracts import GateResult, KnowledgePage, PolicyFinding, QAReport


def validate_page(page: KnowledgePage, *, revision_id: str = "", policy_version: str = "policy.example.v1") -> QAReport:
    findings: list[PolicyFinding] = []
    if "## Source Trace" not in page.body:
        findings.append(PolicyFinding("kms.source_trace.required", "error", "Page must include a Source Trace section."))
    if not page.source_refs:
        findings.append(PolicyFinding("kms.source_refs.required", "error", "Page metadata must retain at least one source reference."))
    result = GateResult.PASS if not findings else GateResult.BLOCK
    return QAReport(result=result, findings=tuple(findings), qa_report_id=f"qa-{revision_id}" if revision_id else "", revision_id=revision_id, policy_version=policy_version)


__all__ = ["validate_page"]
