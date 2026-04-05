from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import logging
from pathlib import Path
from typing import Callable

from kms_domain import (
    ApprovalRecord,
    ContradictionRecord,
    ImpactRecord,
    LintFinding,
    MetadataStore,
    Run,
    RunEvent,
    SourceNote,
    WikiPageRevision,
)

from kms_api.governance.service import GovernedWikiPublicationService, PolicyValidationService
from kms_api.intake.service import IntakeRequest, SourceIntakeService, make_stable_id
from kms_api.services.metadata_service import MetadataService
from kms_api.wiki.models import WikiDraftInput, WikiDraftResult
from kms_api.wiki.service import WikiDraftService, WikiRevisionWriter, source_note_to_draft_input

from .agents import AgentSpec, BoundedAgentRunner
from .catalog import load_orchestration_catalog
from .models import OrchestrationRequest, OrchestrationResult, OrchestrationStageResult

TimestampProvider = Callable[[], str]

logger = logging.getLogger(__name__)

_AGENT_CATALOG = load_orchestration_catalog()
AGENT_SPECS = _AGENT_CATALOG.agent_specs()


@dataclass(frozen=True)
class _DraftCandidate:
    source_note: SourceNote
    page_type: str
    impact_id: str
    draft_input: WikiDraftInput


class RunLintService:
    def __init__(
        self,
        metadata: MetadataService,
        wiki_root: Path,
        timestamp_provider: TimestampProvider,
    ) -> None:
        self._metadata = metadata
        self._wiki_root = wiki_root
        self._timestamp_provider = timestamp_provider

    def lint_revision(self, run_id: str, revision: WikiPageRevision, draft: WikiDraftResult) -> list[LintFinding]:
        findings: list[LintFinding] = []
        file_path = self._wiki_root / Path(draft.path)
        if not file_path.exists():
            findings.append(
                LintFinding(
                    lint_finding_id=_make_lint_id(run_id, revision.revision_id, "missing-file"),
                    run_id=run_id,
                    severity="error",
                    code="lint.file_missing",
                    message=f"Expected finalized wiki file was not written: {draft.path}",
                    created_at=self._timestamp_provider(),
                    page_id=revision.page_id,
                    revision_id=revision.revision_id,
                )
            )
        if findings:
            for finding in findings:
                self._metadata.record_lint_finding(finding)
        return findings


class RunOrchestrationService:
    def __init__(
        self,
        store: MetadataStore,
        *,
        wiki_root: Path | None = None,
        templates_root: Path | None = None,
        timestamp_provider: TimestampProvider | None = None,
        post_publish_hook: Callable[[], None] | None = None,
    ) -> None:
        self._store = store
        self._metadata = MetadataService(store)
        self._timestamp_provider = timestamp_provider or _default_timestamp_provider
        self._intake = SourceIntakeService(store, timestamp_provider=self._timestamp_provider)
        self._drafts = WikiDraftService(templates_root=templates_root)
        self._validator = PolicyValidationService(store, timestamp_provider=self._timestamp_provider)
        self._staging_writer = WikiRevisionWriter(
            store,
            wiki_root=wiki_root,
            timestamp_provider=self._timestamp_provider,
            publish_enabled=False,
        )
        self._publisher = GovernedWikiPublicationService(
            self._validator,
            WikiRevisionWriter(
                store,
                wiki_root=wiki_root,
                timestamp_provider=self._timestamp_provider,
                publish_enabled=True,
            ),
            post_publish_hook=post_publish_hook,
        )
        self._lint = RunLintService(
            self._metadata,
            wiki_root=wiki_root or Path("wiki"),
            timestamp_provider=self._timestamp_provider,
        )
        self._agents = BoundedAgentRunner(self._metadata, self._timestamp_provider)

    def orchestrate(self, request: OrchestrationRequest) -> OrchestrationResult:
        source_root = Path(request.source_root_path).expanduser().resolve()
        run_id = make_stable_id("run", str(source_root), request.initiated_by, request.domain_hint or "")
        logger.info("run_orchestration_started run_id=%s source_root=%s", run_id, source_root)
        existing_run = self._metadata.get_run(run_id)
        run = self._ensure_run(run_id, source_root, request)
        run_events: list[RunEvent] = []
        stage_results: list[OrchestrationStageResult] = []
        revision_ids: list[str] = []
        lint_finding_ids: list[str] = []

        if run.current_stage is None:
            run.current_stage = "source_intake"
            run.status = "in_progress"
            self._store.create_run(run)

        intake_event = self._record_event(
            run_id,
            kind="run_created" if existing_run is None else "run_resumed",
            stage="source_intake",
            status="in_progress",
            message=f"Orchestration started for {source_root}.",
        )
        run_events.append(intake_event)

        intake_result = self._agents.run(
            AGENT_SPECS["source_intake"],
            run_id=run_id,
            input_summary=f"source_root={source_root}",
            handler=lambda: self._intake.start_intake(
                IntakeRequest(
                    source_root_path=str(source_root),
                    initiated_by=request.initiated_by,
                    domain_hint=request.domain_hint,
                    run_notes=request.run_notes,
                )
            ),
        )
        stage_results.append(
            OrchestrationStageResult(
                stage="source_intake",
                status="completed",
                message=f"Discovered {intake_result.total_files} files.",
                agent_name=AGENT_SPECS["source_intake"].agent_name,
                details={
                    "total_files": str(intake_result.total_files),
                    "supported_files": str(intake_result.supported_files),
                    "unsupported_files": str(intake_result.unsupported_files),
                },
            )
        )
        run_events.append(
            self._record_event(
                run_id,
                kind="stage_completed",
                stage="source_intake",
                status="completed",
                message=f"Source intake completed with {intake_result.supported_files} supported files.",
                agent_name=AGENT_SPECS["source_intake"].agent_name,
            )
        )

        run = self._set_run_state(run_id, status="in_progress", current_stage="source_analysis")

        candidates = self._agents.run(
            AGENT_SPECS["source_analysis"],
            run_id=run_id,
            input_summary=f"{len(self._metadata.list_source_notes(run_id))} source notes",
            handler=lambda: [note.source_note_id for note in self._metadata.list_source_notes(run_id)],
        )
        run_events.append(
            self._record_event(
                run_id,
                kind="stage_completed",
                stage="source_analysis",
                status="in_progress",
                message=f"Source analysis inspected {len(candidates)} source note(s).",
                agent_name=AGENT_SPECS["source_analysis"].agent_name,
            )
        )
        stage_results.append(
            OrchestrationStageResult(
                stage="source_analysis",
                status="completed",
                message=f"Inspected {len(candidates)} source note(s).",
                agent_name=AGENT_SPECS["source_analysis"].agent_name,
                details={"source_note_count": str(len(candidates))},
            )
        )

        candidates = self._agents.run(
            AGENT_SPECS["wiki_impact"],
            run_id=run_id,
            input_summary=f"{len(candidates)} source note(s)",
            handler=lambda: self._analyze_source_notes(run_id, request.domain_hint or "general"),
        )
        run_events.append(
            self._record_event(
                run_id,
                kind="stage_completed",
                stage="wiki_impact",
                status="in_progress",
                message=f"Wiki impact analysis prepared {len(candidates)} candidate page(s).",
                agent_name=AGENT_SPECS["wiki_impact"].agent_name,
            )
        )
        stage_results.append(
            OrchestrationStageResult(
                stage="wiki_impact",
                status="completed",
                message=f"Prepared {len(candidates)} candidate page(s).",
                agent_name=AGENT_SPECS["wiki_impact"].agent_name,
                details={"candidate_count": str(len(candidates))},
            )
        )

        for candidate in candidates:
            draft_result = self._agents.run(
                AGENT_SPECS["wiki_curator"],
                run_id=run_id,
                input_summary=f"{candidate.source_note.source_note_id}:{candidate.page_type}",
                handler=lambda candidate=candidate: self._drafts.build_draft(candidate.draft_input),
            )
            revision_write = self._staging_writer.write_revision(run_id, draft_result)
            revision = self._store_revision_lookup(run_id, revision_write.revision_id)
            revision_ids.append(revision_write.revision_id)
            self._record_impact_target(run_id, candidate.impact_id, revision.page_id)
            stage_results.append(
                OrchestrationStageResult(
                    stage="wiki_curator",
                    status="completed",
                    message=f"Staged {draft_result.page_type} revision {revision_write.revision_id}.",
                    agent_name=AGENT_SPECS["wiki_curator"].agent_name,
                    revision_id=revision_write.revision_id,
                    page_id=revision.page_id,
                )
            )
            run_events.append(
                self._record_event(
                    run_id,
                    kind="stage_completed",
                    stage="wiki_curator",
                    status="in_progress",
                    message=f"Curated draft for {draft_result.slug}.",
                    agent_name=AGENT_SPECS["wiki_curator"].agent_name,
                    details={"slug": draft_result.slug, "page_type": draft_result.page_type},
                )
            )

            validation = self._agents.run(
                AGENT_SPECS["policy_qa"],
                run_id=run_id,
                input_summary=f"{revision.revision_id}:{draft_result.page_type}",
                handler=lambda revision=revision, draft_result=draft_result: self._validator.validate_revision(
                    run_id,
                    draft_result,
                    revision,
                ),
                revision_id=revision.revision_id,
                page_id=revision.page_id,
            )
            run_events.append(
                self._record_event(
                    run_id,
                    kind="stage_completed" if validation.status != "blocked" else "stage_blocked",
                    stage="policy_qa",
                    status="blocked" if validation.status == "blocked" else "in_progress",
                    message=validation.messages[0] if validation.messages else "Validation completed.",
                    agent_name=AGENT_SPECS["policy_qa"].agent_name,
                    details={"qa_report_id": validation.qa_report_id, "status": validation.status},
                )
            )
            stage_results.append(
                OrchestrationStageResult(
                    stage="policy_qa",
                    status="blocked" if validation.status == "blocked" else "completed",
                    message=validation.messages[0] if validation.messages else "Validation completed.",
                    agent_name=AGENT_SPECS["policy_qa"].agent_name,
                    revision_id=revision.revision_id,
                    page_id=revision.page_id,
                    details={
                        "qa_report_id": validation.qa_report_id,
                        "approval_required": str(validation.approval_required),
                        "source_trace_status": validation.source_trace_status,
                        "contradiction_status": validation.contradiction_status,
                    },
                )
            )

            if validation.status == "blocked":
                self._set_run_state(run_id, status="blocked", current_stage="policy_qa")
                blocked_reason = validation.messages[0] if validation.messages else "Validation blocked publication."
                logger.info("run_orchestration_blocked run_id=%s stage=policy_qa reason=%s", run_id, blocked_reason)
                run_events.append(
                    self._record_event(
                        run_id,
                        kind="run_blocked",
                        stage="policy_qa",
                        status="blocked",
                        message=blocked_reason,
                        agent_name=AGENT_SPECS["policy_qa"].agent_name,
                    )
                )
                return self._finalize_result(
                    run_id,
                    run_status="blocked",
                    current_stage="policy_qa",
                    stage_results=stage_results,
                    run_events=run_events,
                    revision_ids=revision_ids,
                    lint_finding_ids=lint_finding_ids,
                    blocked_reason=blocked_reason,
                )

            contradiction_record = self._build_contradiction_record(run_id, candidate, revision, validation)
            if contradiction_record is not None:
                self._store.record_contradiction(contradiction_record)
                run_events.append(
                    self._record_event(
                        run_id,
                        kind="stage_completed",
                        stage="contradiction_review",
                        status="in_progress",
                        message=f"Recorded contradiction review for {candidate.source_note.title}.",
                        agent_name=AGENT_SPECS["contradiction_review"].agent_name,
                        details={"contradiction_id": contradiction_record.contradiction_id},
                    )
                )
                stage_results.append(
                    OrchestrationStageResult(
                        stage="contradiction_review",
                        status="completed",
                        message=f"Recorded contradiction review for {candidate.source_note.title}.",
                        agent_name=AGENT_SPECS["contradiction_review"].agent_name,
                        revision_id=revision.revision_id,
                        page_id=revision.page_id,
                        details={"contradiction_id": contradiction_record.contradiction_id},
                    )
                )

            if validation.approval_required and validation.status != "pass":
                if request.approval_decision is None:
                    run = self._set_run_state(run_id, status="blocked", current_stage="approval")
                    blocked_reason = "Approval required before finalization."
                    logger.info("run_orchestration_blocked run_id=%s stage=approval reason=%s", run_id, blocked_reason)
                    run_events.append(
                        self._record_event(
                            run_id,
                            kind="stage_blocked",
                            stage="approval",
                            status="blocked",
                            message=blocked_reason,
                            agent_name=AGENT_SPECS["approval"].agent_name,
                        )
                    )
                    stage_results.append(
                        OrchestrationStageResult(
                            stage="approval",
                            status="blocked",
                            message=blocked_reason,
                            agent_name=AGENT_SPECS["approval"].agent_name,
                            revision_id=revision.revision_id,
                            page_id=revision.page_id,
                        )
                    )
                    return self._finalize_result(
                        run_id,
                        run_status="blocked",
                        current_stage="approval",
                        stage_results=stage_results,
                        run_events=run_events,
                        revision_ids=revision_ids,
                        lint_finding_ids=lint_finding_ids,
                        blocked_reason=blocked_reason,
                    )

                approval_record = self._agents.run(
                    AGENT_SPECS["approval"],
                    run_id=run_id,
                    input_summary=f"{revision.revision_id}:{request.approval_decision}",
                    handler=lambda: self._record_approval(
                        revision.revision_id,
                        request.policy_version,
                        request.approval_reviewer_id or request.initiated_by,
                        request.approval_reason,
                        request.approval_decision or "deferred",
                    ),
                    revision_id=revision.revision_id,
                    page_id=revision.page_id,
                )
                run_events.append(
                    self._record_event(
                        run_id,
                        kind="stage_completed",
                        stage="approval",
                        status="in_progress",
                        message=f"Approval decision recorded as {approval_record.decision}.",
                        agent_name=AGENT_SPECS["approval"].agent_name,
                        details={"approval_id": approval_record.approval_id},
                    )
                )
                stage_results.append(
                    OrchestrationStageResult(
                        stage="approval",
                        status="completed",
                        message=f"Approval decision recorded as {approval_record.decision}.",
                        agent_name=AGENT_SPECS["approval"].agent_name,
                        revision_id=revision.revision_id,
                        page_id=revision.page_id,
                        details={"approval_id": approval_record.approval_id},
                    )
                )
                validation = self._validator.validate_revision(run_id, draft_result, revision)

            if not validation.publish_allowed:
                run = self._set_run_state(run_id, status="blocked", current_stage="approval")
                blocked_reason = validation.messages[0] if validation.messages else "Validation blocked publication."
                logger.info("run_orchestration_blocked run_id=%s stage=approval reason=%s", run_id, blocked_reason)
                run_events.append(
                    self._record_event(
                        run_id,
                        kind="run_blocked",
                        stage="approval",
                        status="blocked",
                        message=blocked_reason,
                        agent_name=AGENT_SPECS["approval"].agent_name,
                    )
                )
                return self._finalize_result(
                    run_id,
                    run_status="blocked",
                    current_stage="approval",
                    stage_results=stage_results,
                    run_events=run_events,
                    revision_ids=revision_ids,
                    lint_finding_ids=lint_finding_ids,
                    blocked_reason=blocked_reason,
                )

            publish_result = self._agents.run(
                AGENT_SPECS["publisher"],
                run_id=run_id,
                input_summary=f"{revision.revision_id}:{draft_result.slug}",
                handler=lambda revision=revision, draft_result=draft_result, validation=validation: self._publisher.publish_revision(
                    run_id,
                    draft_result,
                    revision,
                ),
                revision_id=revision.revision_id,
                page_id=revision.page_id,
            )
            run_events.append(
                self._record_event(
                    run_id,
                    kind="stage_completed",
                    stage="publisher",
                    status="in_progress",
                    message=f"Published revision {publish_result.revision_id}.",
                    agent_name=AGENT_SPECS["publisher"].agent_name,
                    details={"path": draft_result.path},
                )
            )
            stage_results.append(
                OrchestrationStageResult(
                    stage="publisher",
                    status="completed",
                    message=f"Published revision {publish_result.revision_id}.",
                    agent_name=AGENT_SPECS["publisher"].agent_name,
                    revision_id=publish_result.revision_id,
                    page_id=publish_result.page_id,
                    details={"path": draft_result.path},
                )
            )

            lint_findings = self._agents.run(
                AGENT_SPECS["lint"],
                run_id=run_id,
                input_summary=f"{publish_result.revision_id}:{draft_result.path}",
                handler=lambda revision=revision, draft_result=draft_result: self._lint.lint_revision(
                    run_id,
                    revision,
                    draft_result,
                ),
                revision_id=revision.revision_id,
                page_id=revision.page_id,
            )
            lint_finding_ids.extend([finding.lint_finding_id for finding in lint_findings])
            run_events.append(
                self._record_event(
                    run_id,
                    kind="stage_completed",
                    stage="lint",
                    status="in_progress",
                    message=f"Lint completed with {len(lint_findings)} findings.",
                    agent_name=AGENT_SPECS["lint"].agent_name,
                    details={"finding_count": str(len(lint_findings))},
                )
            )
            stage_results.append(
                OrchestrationStageResult(
                    stage="lint",
                    status="completed",
                    message=f"Lint completed with {len(lint_findings)} findings.",
                    agent_name=AGENT_SPECS["lint"].agent_name,
                    revision_id=revision.revision_id,
                    page_id=revision.page_id,
                    details={"finding_count": str(len(lint_findings))},
                )
            )

        run = self._set_run_state(run_id, status="completed", current_stage="completed")
        run.completed_at = self._timestamp_provider()
        self._store.create_run(run)
        logger.info("run_orchestration_completed run_id=%s", run_id)
        run_events.append(
            self._record_event(
                run_id,
                kind="run_completed",
                stage="completed",
                status="completed",
                message=f"Run {run_id} completed successfully.",
            )
        )
        return self._finalize_result(
            run_id,
            run_status="completed",
            current_stage="completed",
            stage_results=stage_results,
            run_events=run_events,
            revision_ids=revision_ids,
            lint_finding_ids=lint_finding_ids,
            blocked_reason=None,
        )

    def _analyze_source_notes(self, run_id: str, domain: str) -> list[_DraftCandidate]:
        candidates: list[_DraftCandidate] = []
        for source_note in self._metadata.list_source_notes(run_id):
            page_type = _choose_page_type(source_note)
            draft_input = _build_draft_input(source_note, domain, page_type)
            impact_id = make_stable_id("impact", run_id, source_note.source_note_id, page_type)
            impact = ImpactRecord(
                impact_id=impact_id,
                run_id=run_id,
                source_document_id=source_note.source_document_id,
                impact_type=f"candidate:{page_type}",
                summary=f"{source_note.title} maps to {page_type} output.",
                created_at=self._timestamp_provider(),
            )
            self._metadata.record_impact(impact)
            candidates.append(
                _DraftCandidate(
                    source_note=source_note,
                    page_type=page_type,
                    impact_id=impact_id,
                    draft_input=draft_input,
                )
            )
        return candidates

    def _build_contradiction_record(
        self,
        run_id: str,
        candidate: _DraftCandidate,
        revision: WikiPageRevision,
        validation,
    ) -> ContradictionRecord | None:
        if validation.contradiction_status == "clear" and not candidate.source_note.review_required:
            return None
        return ContradictionRecord(
            contradiction_id=make_stable_id(
                "contradiction",
                run_id,
                revision.revision_id,
                candidate.source_note.source_note_id,
            ),
            run_id=run_id,
            severity="warning" if validation.contradiction_status != "blocked" else "error",
            status="reviewing" if validation.contradiction_status == "clear" else "open",
            conflicting_claims=[
                candidate.source_note.summary,
                "Source intake marked the candidate for human review.",
            ],
            source_refs=list(candidate.source_note.source_refs),
            created_at=self._timestamp_provider(),
            page_id=revision.page_id,
            revision_id=revision.revision_id,
        )

    def _record_approval(
        self,
        revision_id: str,
        policy_version: str,
        reviewer_id: str,
        reason: str | None,
        decision: str,
    ) -> ApprovalRecord:
        if decision == "approved":
            return self._validator.record_approval(
                revision_id,
                decision="approved",
                policy_version=policy_version,
                reviewer_id=reviewer_id,
                reason=reason,
            )
        if decision == "rejected":
            return self._validator.reject_revision(
                revision_id,
                policy_version=policy_version,
                reviewer_id=reviewer_id,
                reason=reason,
            )
        return self._validator.record_approval(
            revision_id,
            decision=decision,  # type: ignore[arg-type]
            policy_version=policy_version,
            reviewer_id=reviewer_id,
            reason=reason,
        )

    def _record_impact_target(self, run_id: str, impact_id: str, page_id: str) -> None:
        impact_records = self._metadata.list_impact_records(run_id)
        for impact in impact_records:
            if impact.impact_id == impact_id:
                impact.target_page_id = page_id
                self._metadata.record_impact(impact)
                return

    def _record_event(
        self,
        run_id: str,
        *,
        kind: str,
        stage: str,
        status: str,
        message: str,
        agent_name: str | None = None,
        details: dict[str, str] | None = None,
    ) -> RunEvent:
        event = RunEvent(
            event_id=make_stable_id("event", run_id, kind, stage, message, str(len(message))),
            run_id=run_id,
            kind=kind,  # type: ignore[arg-type]
            stage=stage,
            status=status,  # type: ignore[arg-type]
            message=message,
            created_at=self._timestamp_provider(),
            agent_name=agent_name,
            details=details or {},
        )
        return self._metadata.record_run_event(event)

    def _ensure_run(self, run_id: str, source_root: Path, request: OrchestrationRequest) -> Run:
        existing = self._metadata.get_run(run_id)
        if existing is not None:
            return existing
        run = Run(
            run_id=run_id,
            status="created",
            source_path=str(source_root),
            created_at=self._timestamp_provider(),
            domain_hint=request.domain_hint,
            run_notes=request.run_notes,
            created_by=request.initiated_by,
            current_stage="source_intake",
        )
        self._store.create_run(run)
        return run

    def _set_run_state(self, run_id: str, *, status: str, current_stage: str) -> Run:
        run = self._metadata.get_run(run_id)
        if run is None:
            raise KeyError(f"Run {run_id} not found")
        run.status = status  # type: ignore[assignment]
        run.current_stage = current_stage
        if status != "completed":
            run.completed_at = None
        self._store.create_run(run)
        return run

    def _store_revision_lookup(self, run_id: str, revision_id: str) -> WikiPageRevision:
        for revision in self._metadata.list_wiki_page_revisions():
            if revision.revision_id == revision_id and revision.run_id == run_id:
                return revision
        raise KeyError(f"Revision {revision_id} not found for run {run_id}")

    def _finalize_result(
        self,
        run_id: str,
        *,
        run_status: str,
        current_stage: str | None,
        stage_results: list[OrchestrationStageResult],
        run_events: list[RunEvent],
        revision_ids: list[str],
        lint_finding_ids: list[str],
        blocked_reason: str | None,
    ) -> OrchestrationResult:
        run = self._metadata.get_run(run_id)
        if run is None:
            raise KeyError(f"Run {run_id} not found")
        return OrchestrationResult(
            run_id=run_id,
            run_status=run_status,
            current_stage=current_stage,
            stage_results=stage_results,
            run_events=run_events,
            agent_executions=self._metadata.list_agent_executions(run_id),
            revision_ids=revision_ids,
            lint_finding_ids=lint_finding_ids,
            blocked_reason=blocked_reason,
        )


def _default_timestamp_provider() -> str:
    return datetime.now(timezone.utc).isoformat()


def _choose_page_type(source_note: SourceNote) -> str:
    title = f"{source_note.title} {source_note.summary}".lower()
    if "metric" in title or "retention" in title:
        return "metric"
    if "data" in title or "fact" in title:
        return "data-asset"
    if "process" in title or "workflow" in title:
        return "process"
    return "open-question" if source_note.review_required else "source-note"


def _build_draft_input(source_note: SourceNote, domain: str, page_type: str) -> WikiDraftInput:
    if page_type == "source-note":
        return source_note_to_draft_input(source_note, domain=domain)
    if page_type == "open-question":
        return WikiDraftInput(
            title=f"{source_note.title} Open Question",
            page_type="open-question",
            domain=domain,
            section_content={
                "Summary": source_note.summary,
                "Current Understanding": source_note.summary,
                "Question": f"What remains unresolved about {source_note.title}?",
                "Conflicting Evidence": [
                    f"Source note summary: {source_note.summary}",
                    *[f"Source trace: {ref}" for ref in source_note.source_refs],
                ],
                "Why Unresolved": "The intake output still requires human review.",
                "Required Review": "Knowledge Manager approval required before finalization.",
                "Source Trace": [f"Source reference: {ref}" for ref in source_note.source_refs],
            },
            source_refs=list(source_note.source_refs),
            related=[],
            tags=["open-question", "orchestration"],
            owners=["knowledge-manager:unassigned"],
            last_updated=source_note.created_at,
            confidence="provisional",
            review_required=True,
            status="review_required",
            identity_key=source_note.source_note_id,
        )
    if page_type == "metric":
        return WikiDraftInput(
            title=source_note.title,
            page_type="metric",
            domain=domain,
            section_content={
                "Summary": source_note.summary,
                "Current Understanding": source_note.summary,
                "Business Definition": source_note.summary,
                "Formula": "Derived from governed source notes and downstream review.",
                "Grain / Scope": "Run-level draft candidate.",
                "Valid Segmentations": [f"Source signal: {signal}" for signal in source_note.extracted_signals],
                "Approved Sources": [f"Source reference: {ref}" for ref in source_note.source_refs],
                "Common Pitfalls": ["Review required before final publication."],
                "Related Metrics": [],
                "Source Trace": [f"Source reference: {ref}" for ref in source_note.source_refs],
            },
            source_refs=list(source_note.source_refs),
            related=[],
            tags=["metric", "orchestration"],
            owners=["knowledge-manager:unassigned"],
            last_updated=source_note.created_at,
            confidence="provisional",
            review_required=True,
            status="review_required",
            identity_key=source_note.source_note_id,
        )
    return WikiDraftInput(
        title=source_note.title,
        page_type="data-asset",
        domain=domain,
        section_content={
            "Summary": source_note.summary,
            "Current Understanding": source_note.summary,
            "Purpose": "Derived governed candidate page.",
            "Source System": "Unknown pending review.",
            "Grain": "Unknown pending review.",
            "Key Fields": [f"Signal: {signal}" for signal in source_note.extracted_signals],
            "Join Keys": [],
            "Refresh Cadence": "Unknown pending review.",
            "Known Issues": ["Review required before final publication."],
            "Downstream Usage": [],
            "Source Trace": [f"Source reference: {ref}" for ref in source_note.source_refs],
        },
        source_refs=list(source_note.source_refs),
        related=[],
        tags=["data-asset", "orchestration"],
        owners=["knowledge-manager:unassigned"],
        last_updated=source_note.created_at,
        confidence="provisional",
        review_required=True,
        status="review_required",
        identity_key=source_note.source_note_id,
    )


def _make_lint_id(run_id: str, revision_id: str, suffix: str) -> str:
    return make_stable_id("lint", run_id, revision_id, suffix)
