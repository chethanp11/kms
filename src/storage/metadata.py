"""Deterministic in-memory metadata store for KMS runtime state."""

from __future__ import annotations

from dataclasses import dataclass, field, replace

from src.contracts import ApprovalRecord, CandidateDraft, CandidateReviewStatus, ContradictionRecord, KnowledgeCandidate, LintFinding, MaintenanceRun, QAReport, WikiPageRevision


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

    def save_knowledge_candidate(self, candidate: KnowledgeCandidate) -> KnowledgeCandidate:
        self.knowledge_candidates[candidate.candidate_id] = candidate
        self.approved_candidate_ids.discard(candidate.candidate_id)
        self.rejected_candidate_ids.discard(candidate.candidate_id)
        self.archived_candidate_ids.discard(candidate.candidate_id)
        return candidate

    def save_candidate_draft(self, draft: CandidateDraft) -> CandidateDraft:
        self.candidate_drafts[draft.draft_id] = draft
        return draft

    def approve_candidate(self, candidate_id: str) -> None:
        candidate = self.knowledge_candidates[candidate_id]
        self.knowledge_candidates[candidate_id] = replace(candidate, review_status=CandidateReviewStatus.APPROVED, duplicate_rationale="")
        self.approved_candidate_ids.add(candidate_id)
        self.rejected_candidate_ids.discard(candidate_id)

    def approve_candidate_with_mods(self, candidate_id: str, modification_text: str) -> None:
        candidate = self.knowledge_candidates[candidate_id]
        self.knowledge_candidates[candidate_id] = replace(candidate, review_status=CandidateReviewStatus.APPROVED_WITH_MODS, modification_text=modification_text.strip())
        self.approved_candidate_ids.add(candidate_id)
        self.rejected_candidate_ids.discard(candidate_id)

    def reject_candidate(self, candidate_id: str, *, reason: str = "") -> None:
        candidate = self.knowledge_candidates[candidate_id]
        self.knowledge_candidates[candidate_id] = replace(candidate, review_status=CandidateReviewStatus.REJECTED, duplicate_rationale=reason or candidate.duplicate_rationale)
        self.rejected_candidate_ids.add(candidate_id)
        self.approved_candidate_ids.discard(candidate_id)

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

    def archive_candidate(self, candidate_id: str) -> None:
        self.archived_candidate_ids.add(candidate_id)

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
