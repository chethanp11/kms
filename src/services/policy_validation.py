"""Policy validation service for page candidates."""

from __future__ import annotations

from src.contracts import GateResult, KnowledgePage, PolicyFinding, QAReport

_REQUIRED_SECTIONS: tuple[tuple[str, str], ...] = (
    ("kms.schema.title.required", "title"),
    ("kms.schema.page_type.required", "page_type"),
    ("kms.content.summary.required", "## Summary"),
    ("kms.source_trace.section.required", "## Source Trace"),
)


def validate_page(page: KnowledgePage, *, revision_id: str = "", policy_version: str = "policy.example.v1") -> QAReport:
    findings: list[PolicyFinding] = []
    if not page.title.strip():
        findings.append(PolicyFinding("kms.schema.title.required", "error", "Page title is required."))
    if not page.page_type.strip():
        findings.append(PolicyFinding("kms.schema.page_type.required", "error", "Page type is required."))
    if "## Summary" not in page.body:
        findings.append(PolicyFinding("kms.content.summary.required", "error", "Page must include a Summary section."))
    if "## Source Trace" not in page.body:
        findings.append(PolicyFinding("kms.source_trace.section.required", "error", "Page must include a Source Trace section."))
    if not page.source_refs:
        findings.append(PolicyFinding("kms.source_refs.required", "error", "Page metadata must retain at least one source reference."))
    for source_ref in page.source_refs:
        if source_ref not in page.body:
            findings.append(PolicyFinding("kms.source_trace.coverage.required", "error", f"Source reference must appear in page body: {source_ref}"))
    result = GateResult.PASS if not findings else GateResult.BLOCK
    checked = ", ".join(rule_id for rule_id, _ in _REQUIRED_SECTIONS)
    return QAReport(
        result=result,
        findings=tuple(findings),
        qa_report_id=f"qa-{revision_id}" if revision_id else "",
        revision_id=revision_id,
        policy_version=policy_version,
        summary=f"Evaluated executable rules: {checked}, kms.source_refs.required, kms.source_trace.coverage.required.",
    )


__all__ = ["validate_page"]
