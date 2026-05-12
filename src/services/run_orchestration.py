"""Run orchestration service for the working stdlib KMS slice."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

from src.config.settings import KMSSettings, default_settings
from src.contracts import ApprovalDecision, ChangeType, KnowledgeCandidate, KnowledgePage, MaintenanceRun, PageStatus, RevisionState, RunState, ValidationError, WikiPageRevision
from src.services.approval import create_approval
from src.services.contradiction import detect_contradictions
from src.services.infopedia_projection import build_tree
from src.services.knowledge_understanding import (
    build_candidate_drafts,
    render_candidate_review_markdown,
    render_candidates_json,
    render_understanding_metadata,
    understand_knowledge,
)
from src.services.lint import lint_wiki
from src.services.parsing import parse_source_bundle
from src.services.policy_validation import validate_page
from src.services.publisher import PublishSummary, publish_page
from src.services.search_index import rebuild_search_index
from src.services.source_analysis import analyze_sources
from src.services.source_discovery import discover_sources
from src.services.source_note import render_source_note
from src.services.wiki_draft import draft_pages
from src.services.wiki_draft import slugify
from src.storage import ArtifactStore, MetadataStore, SearchIndexStore, WikiStore


@dataclass(frozen=True)
class RuntimeResult:
    run: MaintenanceRun
    source_count: int
    page_count: int
    published: tuple[PublishSummary, ...]
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class CandidateWorkflowResult:
    run: MaintenanceRun
    candidates: tuple[KnowledgeCandidate, ...]
    provider: str
    fallback_used: bool = False
    warning: str = ""


@dataclass(frozen=True)
class CandidateApprovalResult:
    run_id: str
    approved_candidate_ids: tuple[str, ...]


@dataclass(frozen=True)
class CandidatePublishResult:
    run: MaintenanceRun
    published: tuple[PublishSummary, ...]


@dataclass
class KMSRuntime:
    settings: KMSSettings
    metadata: MetadataStore
    wiki: WikiStore
    artifacts: ArtifactStore
    search: SearchIndexStore

    @classmethod
    def create(cls, settings: KMSSettings | None = None) -> "KMSRuntime":
        resolved = settings or default_settings()
        resolved.ensure_directories()
        return cls(resolved, MetadataStore(), WikiStore(resolved.wiki_root), ArtifactStore(resolved.artifact_root), SearchIndexStore())

    def start_run(self, source_path: Path | str, *, run_id: str = "run-1", auto_approve: bool = False, reviewer_id: str = "knowledge-manager") -> RuntimeResult:
        run = self.metadata.save_run(MaintenanceRun(run_id=run_id, source_path=str(source_path), state=RunState.IN_PROGRESS))
        bundle = discover_sources(source_path)
        self.artifacts.write_text(run_id, "source-note.md", render_source_note(bundle))
        documents = parse_source_bundle(bundle, run_id=run_id)
        understanding = understand_knowledge(documents, settings=self.settings)
        candidates = understanding.candidates
        candidate_drafts = build_candidate_drafts(candidates)
        for candidate in candidates:
            self.metadata.save_knowledge_candidate(candidate)
        for draft in candidate_drafts:
            self.metadata.save_candidate_draft(draft)
            self.artifacts.write_text(run_id, f"candidate-drafts/{draft.draft_id}.md", draft.markdown)
        self.artifacts.write_text(run_id, "knowledge-candidates.json", render_candidates_json(candidates))
        self.artifacts.write_text(run_id, "knowledge-candidates-review.md", render_candidate_review_markdown(candidates, candidate_drafts))
        self.artifacts.write_text(run_id, "knowledge-understanding-metadata.json", render_understanding_metadata(understanding))
        contradictions = detect_contradictions(documents, run_id=run_id)
        for contradiction in contradictions:
            self.metadata.contradictions[contradiction.contradiction_id] = contradiction
        proposals = analyze_sources(documents)
        pages = draft_pages(proposals)
        published: list[PublishSummary] = []
        warnings = list(bundle.warnings)
        if contradictions:
            warnings.append("contradictions require review")
        for index, page in enumerate(pages, start=1):
            revision_id = f"revision-{index}"
            revision = WikiPageRevision(revision_id, page.page_id or f"page-{index}", run_id, RevisionState.REVIEW_REQUIRED, ChangeType.CREATE, ("summary", "source_trace"), page.source_refs, "Drafted source-note page.")
            self.metadata.save_revision(revision)
            qa = self.metadata.save_qa_report(validate_page(page, revision_id=revision_id, policy_version=self.settings.policy_version))
            approval = None
            if auto_approve and qa.can_publish and not contradictions:
                approval = self.metadata.save_approval(create_approval(revision_id, reviewer_id, ApprovalDecision.APPROVED, reason="auto-approved for deterministic local run"))
                published.append(publish_page(page, qa, approval, self.wiki))
        rebuild_search_index(self.wiki, self.search)
        for finding in lint_wiki(self.wiki):
            self.metadata.lint_findings[finding.lint_finding_id] = finding
        build_tree(self.wiki)
        final_state = RunState.COMPLETED if not warnings else RunState.BLOCKED
        run = replace(
            run,
            state=final_state,
            summary_counts={
                "source_files": len(bundle.files),
                "documents": len(documents),
                "knowledge_candidates": len(candidates),
                "candidate_drafts": len(candidate_drafts),
                "draft_pages": len(pages),
                "published_pages": len(published),
                "warnings": len(warnings),
            },
            blocked_reason="; ".join(warnings),
        )
        self.metadata.save_run(run)
        return RuntimeResult(run, len(bundle.files), len(pages), tuple(published), tuple(warnings))

    def create_candidates(self, source_path: Path | str, *, run_id: str = "run-1") -> CandidateWorkflowResult:
        run = self.metadata.save_run(MaintenanceRun(run_id=run_id, source_path=str(source_path), state=RunState.IN_PROGRESS))
        bundle = discover_sources(source_path)
        self.artifacts.write_text(run_id, "source-note.md", render_source_note(bundle))
        documents = parse_source_bundle(bundle, run_id=run_id)
        understanding = understand_knowledge(documents, settings=self.settings)
        candidates = understanding.candidates
        candidate_drafts = build_candidate_drafts(candidates)
        for candidate in candidates:
            self.metadata.save_knowledge_candidate(candidate)
        for draft in candidate_drafts:
            self.metadata.save_candidate_draft(draft)
            self.artifacts.write_text(run_id, f"candidate-drafts/{draft.draft_id}.md", draft.markdown)
        self.artifacts.write_text(run_id, "knowledge-candidates.json", render_candidates_json(candidates))
        self.artifacts.write_text(run_id, "knowledge-candidates-review.md", render_candidate_review_markdown(candidates, candidate_drafts))
        self.artifacts.write_text(run_id, "knowledge-understanding-metadata.json", render_understanding_metadata(understanding))
        run = replace(
            run,
            state=RunState.COMPLETED,
            summary_counts={
                "source_files": len(bundle.files),
                "documents": len(documents),
                "knowledge_candidates": len(candidates),
                "candidate_drafts": len(candidate_drafts),
                "approved_candidates": 0,
                "published_pages": 0,
                "warnings": 1 if understanding.warning else 0,
            },
            blocked_reason=understanding.warning,
        )
        self.metadata.save_run(run)
        return CandidateWorkflowResult(run, candidates, understanding.provider, understanding.fallback_used, understanding.warning)

    def approve_candidates(self, run_id: str, *, candidate_ids: tuple[str, ...] = (), approve_all: bool = False) -> CandidateApprovalResult:
        run = self.metadata.get_run(run_id)
        if run is None:
            raise ValidationError(f"run not found: {run_id}")
        run_candidates = self.metadata.candidates_for_run(run_id, include_archived=False)
        selected = run_candidates if approve_all else tuple(candidate for candidate in run_candidates if candidate.candidate_id in set(candidate_ids))
        if not selected:
            raise ValidationError("no candidates selected for approval")
        for candidate in selected:
            self.metadata.approve_candidate(candidate.candidate_id)
        approved_ids = tuple(candidate.candidate_id for candidate in self.metadata.approved_candidates_for_run(run_id))
        self.metadata.save_run(replace(run, summary_counts={**dict(run.summary_counts), "approved_candidates": len(approved_ids)}))
        return CandidateApprovalResult(run_id, approved_ids)

    def publish_approved_candidates(self, run_id: str, *, reviewer_id: str = "knowledge-manager") -> CandidatePublishResult:
        run = self.metadata.get_run(run_id)
        if run is None:
            raise ValidationError(f"run not found: {run_id}")
        approved = self.metadata.approved_candidates_for_run(run_id)
        if not approved:
            raise ValidationError("no approved candidates available to publish")
        published: list[PublishSummary] = []
        for index, candidate in enumerate(approved, start=1):
            page = _page_from_candidate(candidate)
            revision_id = f"{run_id}-candidate-revision-{index}"
            revision = WikiPageRevision(
                revision_id,
                page.page_id or f"page-{candidate.candidate_id}",
                run_id,
                RevisionState.REVIEW_REQUIRED,
                ChangeType.CREATE,
                ("candidate", "source_trace"),
                page.source_refs,
                f"Publish approved {candidate.candidate_type.value} candidate.",
            )
            self.metadata.save_revision(revision)
            qa = self.metadata.save_qa_report(validate_page(page, revision_id=revision_id, policy_version=self.settings.policy_version))
            approval = self.metadata.save_approval(create_approval(revision_id, reviewer_id, ApprovalDecision.APPROVED, reason="approved candidate publication"))
            published.append(publish_page(page, qa, approval, self.wiki))
            self.metadata.archive_candidate(candidate.candidate_id)
        rebuild_search_index(self.wiki, self.search)
        build_tree(self.wiki)
        updated = replace(
            run,
            state=RunState.COMPLETED,
            summary_counts={**dict(run.summary_counts), "approved_candidates": len(approved), "published_pages": len(published)},
            blocked_reason="",
        )
        self.metadata.save_run(updated)
        return CandidatePublishResult(updated, tuple(published))


def _page_from_candidate(candidate: KnowledgeCandidate) -> KnowledgePage:
    title = candidate.title
    slug = f"candidates/{slugify(title)}-{candidate.candidate_id}"
    body = "\n".join([
        "## Summary",
        candidate.excerpt,
        "",
        "## Candidate Type",
        candidate.candidate_type.value,
        "",
        "## Review Status",
        "Approved by Knowledge Manager through KMI candidate review.",
        "",
        "## Source Trace",
        f"- {candidate.source_ref}",
        "",
        "## Confidence",
        f"- Relevance: {candidate.relevance_score:.2f}",
        f"- Confidence: {candidate.confidence_score:.2f}",
        "",
        "## Rationale",
        candidate.rationale,
    ])
    return KnowledgePage(
        page_id=f"page-{candidate.candidate_id}",
        page_type=candidate.candidate_type.value,
        path=f"{slug}.md",
        title=title,
        body=body,
        status=PageStatus.FINALIZED,
        source_refs=(candidate.source_ref,),
        tags=(candidate.candidate_type.value,),
        metadata={"candidate_id": candidate.candidate_id, "source_ref": candidate.source_ref},
    )


__all__ = ["CandidateApprovalResult", "CandidatePublishResult", "CandidateWorkflowResult", "KMSRuntime", "RuntimeResult"]
