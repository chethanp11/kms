"""Deterministic in-memory metadata store for KMS runtime state."""

from __future__ import annotations

from dataclasses import dataclass, field, replace

from src.contracts import ApprovalRecord, CandidateDraft, CandidateReviewStatus, ContradictionRecord, KnowledgeCandidate, LintFinding, MaintenanceRun, QAReport, WikiPageRevision
from src.observability import AuditEvent, audit_event


@dataclass
class MetadataStore:
    runs: dict[str, MaintenanceRun] = field(default_factory=dict)
    revisions: dict[str, WikiPageRevision] = field(default_factory=dict)
    approvals: dict[str, ApprovalRecord] = field(default_factory=dict)
    qa_reports: dict[str, QAReport] = field(default_factory=dict)
    contradictions: dict[str, ContradictionRecord] = field(default_factory=dict)
    knowledge_candidates: dict[str, KnowledgeCandidate] = field(default_factory=dict)
    candidate_drafts: dict[str, CandidateDraft] = field(default_factory=dict)
    approved_candidate_ids: set[str] = field(default_factory=set)
    rejected_candidate_ids: set[str] = field(default_factory=set)
    archived_candidate_ids: set[str] = field(default_factory=set)
    lint_findings: dict[str, LintFinding] = field(default_factory=dict)
    events: list[AuditEvent] = field(default_factory=list)

    def record_event(self, event_type: str, subject_id: str, message: str) -> AuditEvent:
        event = audit_event(event_type, subject_id, message)
        self.events.append(event)
        return event

    def save_run(self, run: MaintenanceRun) -> MaintenanceRun:
        self.runs[run.run_id] = run
        self.record_event("run.saved", run.run_id, f"Run state saved as {run.state.value}.")
        return run

    def get_run(self, run_id: str) -> MaintenanceRun | None:
        return self.runs.get(run_id)

    def save_revision(self, revision: WikiPageRevision) -> WikiPageRevision:
        self.revisions[revision.revision_id] = revision
        self.record_event("revision.saved", revision.revision_id, f"Revision {revision.status.value} for run {revision.run_id}.")
        return revision

    def save_approval(self, approval: ApprovalRecord) -> ApprovalRecord:
        self.approvals[approval.revision_id] = approval
        self.record_event("approval.saved", approval.revision_id, f"Approval decision {approval.decision.value} by {approval.reviewer_id}.")
        return approval

    def approval_for_revision(self, revision_id: str) -> ApprovalRecord | None:
        return self.approvals.get(revision_id)

    def save_qa_report(self, report: QAReport) -> QAReport:
        key = report.qa_report_id or report.revision_id or f"qa-{len(self.qa_reports)+1}"
        self.qa_reports[key] = report
        self.record_event("policy.evaluated", report.revision_id or key, f"Policy result {report.result.value} with {len(report.findings)} findings.")
        return report

    def save_knowledge_candidate(self, candidate: KnowledgeCandidate) -> KnowledgeCandidate:
        self.knowledge_candidates[candidate.candidate_id] = candidate
        self.approved_candidate_ids.discard(candidate.candidate_id)
        self.rejected_candidate_ids.discard(candidate.candidate_id)
        self.archived_candidate_ids.discard(candidate.candidate_id)
        self.record_event("candidate.created", candidate.candidate_id, f"{candidate.candidate_type.value} candidate from {candidate.source_ref}.")
        return candidate

    def save_candidate_draft(self, draft: CandidateDraft) -> CandidateDraft:
        self.candidate_drafts[draft.draft_id] = draft
        return draft

    def approve_candidate(self, candidate_id: str) -> None:
        candidate = self.knowledge_candidates[candidate_id]
        self.knowledge_candidates[candidate_id] = replace(candidate, review_status=CandidateReviewStatus.APPROVED, duplicate_rationale="")
        self.approved_candidate_ids.add(candidate_id)
        self.rejected_candidate_ids.discard(candidate_id)
        self.record_event("candidate.approved", candidate_id, "Candidate approved during KMI review.")

    def approve_candidate_with_mods(self, candidate_id: str, modification_text: str) -> None:
        candidate = self.knowledge_candidates[candidate_id]
        self.knowledge_candidates[candidate_id] = replace(candidate, review_status=CandidateReviewStatus.APPROVED_WITH_MODS, modification_text=modification_text.strip())
        self.approved_candidate_ids.add(candidate_id)
        self.rejected_candidate_ids.discard(candidate_id)
        self.record_event("candidate.approved_with_mods", candidate_id, "Candidate approved with reviewer modifications.")

    def reject_candidate(self, candidate_id: str, *, reason: str = "") -> None:
        candidate = self.knowledge_candidates[candidate_id]
        self.knowledge_candidates[candidate_id] = replace(candidate, review_status=CandidateReviewStatus.REJECTED, duplicate_rationale=reason or candidate.duplicate_rationale)
        self.rejected_candidate_ids.add(candidate_id)
        self.approved_candidate_ids.discard(candidate_id)
        self.record_event("candidate.rejected", candidate_id, reason or "Candidate rejected during KMI review.")

    def auto_reject_duplicate(self, candidate_id: str, *, duplicate_of: str, reason: str) -> None:
        candidate = self.knowledge_candidates[candidate_id]
        self.knowledge_candidates[candidate_id] = replace(
            candidate,
            review_status=CandidateReviewStatus.REJECTED,
            duplicate_of=duplicate_of,
            duplicate_rationale=reason,
        )
        self.rejected_candidate_ids.add(candidate_id)
        self.approved_candidate_ids.discard(candidate_id)
        self.record_event("candidate.auto_rejected_duplicate", candidate_id, reason)

    def archive_candidate(self, candidate_id: str) -> None:
        self.archived_candidate_ids.add(candidate_id)
        self.record_event("candidate.archived", candidate_id, "Candidate archived after publication.")

    def approved_candidates_for_run(self, run_id: str) -> tuple[KnowledgeCandidate, ...]:
        return tuple(
            candidate
            for candidate in self.knowledge_candidates.values()
            if candidate.run_id == run_id
            and candidate.candidate_id in self.approved_candidate_ids
            and candidate.candidate_id not in self.archived_candidate_ids
        )

    def candidates_for_run(self, run_id: str, *, include_archived: bool = True) -> tuple[KnowledgeCandidate, ...]:
        return tuple(
            candidate
            for candidate in self.knowledge_candidates.values()
            if candidate.run_id == run_id
            and (include_archived or candidate.candidate_id not in self.archived_candidate_ids)
        )


__all__ = ["MetadataStore"]
