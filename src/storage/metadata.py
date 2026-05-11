"""Deterministic in-memory metadata store for KMS runtime state."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.contracts import ApprovalRecord, ContradictionRecord, LintFinding, MaintenanceRun, QAReport, WikiPageRevision


@dataclass
class MetadataStore:
    runs: dict[str, MaintenanceRun] = field(default_factory=dict)
    revisions: dict[str, WikiPageRevision] = field(default_factory=dict)
    approvals: dict[str, ApprovalRecord] = field(default_factory=dict)
    qa_reports: dict[str, QAReport] = field(default_factory=dict)
    contradictions: dict[str, ContradictionRecord] = field(default_factory=dict)
    lint_findings: dict[str, LintFinding] = field(default_factory=dict)
    events: list[object] = field(default_factory=list)

    def save_run(self, run: MaintenanceRun) -> MaintenanceRun:
        self.runs[run.run_id] = run
        return run

    def get_run(self, run_id: str) -> MaintenanceRun | None:
        return self.runs.get(run_id)

    def save_revision(self, revision: WikiPageRevision) -> WikiPageRevision:
        self.revisions[revision.revision_id] = revision
        return revision

    def save_approval(self, approval: ApprovalRecord) -> ApprovalRecord:
        self.approvals[approval.revision_id] = approval
        return approval

    def approval_for_revision(self, revision_id: str) -> ApprovalRecord | None:
        return self.approvals.get(revision_id)

    def save_qa_report(self, report: QAReport) -> QAReport:
        key = report.qa_report_id or report.revision_id or f"qa-{len(self.qa_reports)+1}"
        self.qa_reports[key] = report
        return report


__all__ = ["MetadataStore"]
