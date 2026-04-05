from __future__ import annotations

import difflib
import logging
import os
import tempfile
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import Body, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from kms_domain import WikiPageRevision

from kms_config import RuntimeConfig
from kms_api.db.factory import create_metadata_store
from kms_api.governance.service import GovernedWikiPublicationService, PolicyValidationService
from kms_api.infopedia import InfopediaProjectionService
from kms_api.orchestration import OrchestrationRequest, RunOrchestrationService
from kms_api.services.metadata_service import MetadataService
from kms_api.wiki.models import WikiDraftResult
from kms_api.wiki.service import WikiRevisionWriter

logger = logging.getLogger(__name__)


class KmiRuntime:
    def __init__(self, *, runtime_config: RuntimeConfig | None = None, wiki_root: Path | None = None) -> None:
        self.runtime_config = runtime_config
        self.store = create_metadata_store(runtime_config, use_memory=runtime_config is None)
        self.metadata = MetadataService(self.store)
        if wiki_root is not None:
            self.wiki_root = wiki_root
        elif runtime_config is not None:
            self.wiki_root = Path(runtime_config.wiki_path).expanduser()
        else:
            self.wiki_root = Path(tempfile.mkdtemp(prefix="kms-kmi-wiki-"))
        self.validator = PolicyValidationService(self.store)
        self.infopedia = InfopediaProjectionService(self.store, self.wiki_root)
        self.publisher = GovernedWikiPublicationService(
            self.validator,
            WikiRevisionWriter(self.store, wiki_root=self.wiki_root, publish_enabled=True),
            post_publish_hook=self.refresh_projections,
        )
        self.orchestrator = RunOrchestrationService(
            self.store,
            wiki_root=self.wiki_root,
            timestamp_provider=_timestamp_provider,
            post_publish_hook=self.refresh_projections,
        )

    def seed_demo_data(self) -> None:
        demo_source_root = _repo_root() / "tests/fixtures/source_intake/customer-revenue"
        if not demo_source_root.exists():
            return
        if self.store.list_runs():
            return

        self.orchestrator.orchestrate(
            OrchestrationRequest(
                source_root_path=str(demo_source_root),
                initiated_by="knowledge-manager",
                domain_hint="customer-revenue",
                run_notes="Seeded demo run for KMI dashboard.",
            )
        )
        self.orchestrator.orchestrate(
            OrchestrationRequest(
                source_root_path=str(demo_source_root),
                initiated_by="knowledge-manager-review",
                domain_hint="customer-revenue",
                run_notes="Seeded demo run with approval and finalization.",
                approval_decision="approved",
                approval_reviewer_id="knowledge-manager",
                approval_reason="Seeded demo finalization.",
            )
        )

    def refresh_projections(self) -> None:
        try:
            result = self.infopedia.refresh()
            logger.info(
                "projection_refresh_completed wiki_nodes=%s operational_docs=%s wiki_docs=%s stale_pages=%s",
                result.wiki_node_count,
                result.operational_doc_count,
                result.wiki_doc_count,
                result.stale_page_count,
            )
        except Exception:
            logger.exception("projection_refresh_failed")
            return None


def create_app(*, seed_demo_data: bool = True, runtime_config: RuntimeConfig | None = None) -> FastAPI:
    app = FastAPI(title="KMS API")
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    runtime = KmiRuntime(runtime_config=runtime_config)
    app.state.kmi_runtime = runtime
    if seed_demo_data:
        runtime.seed_demo_data()

    @app.get("/health")
    async def health() -> Dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/search")
    async def search(
        q: str = Query(default=""),
        scope: str = Query(default="operational"),
        domain: Optional[str] = Query(default=None),
        page_type: Optional[str] = Query(default=None),
        freshness: Optional[str] = Query(default=None),
        confidence: Optional[str] = Query(default=None),
        status: Optional[str] = Query(default=None),
    ) -> Dict[str, Any]:
        return runtime.infopedia.search(
            query=q,
            domain=domain,
            page_type=page_type,
            freshness=freshness,
            confidence=confidence,
            status=status,
            scope=scope,
        )

    @app.get("/api/runs")
    async def list_runs() -> Dict[str, Any]:
        runs = sorted(runtime.store.list_runs(), key=lambda run: run.created_at, reverse=True)
        return {
            "items": [_run_summary(run, runtime) for run in runs],
            "summary": _dashboard_summary(runtime),
        }

    @app.post("/api/runs")
    async def create_run(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
        source_path = str(payload.get("source_path", "")).strip()
        if not source_path:
            raise HTTPException(status_code=400, detail="source_path is required")
        request = OrchestrationRequest(
            source_root_path=source_path,
            initiated_by=str(payload.get("initiated_by", "knowledge-manager")),
            domain_hint=(str(payload["domain_hint"]).strip() if payload.get("domain_hint") else None),
            run_notes=(str(payload["run_notes"]).strip() if payload.get("run_notes") else None),
            approval_decision=payload.get("approval_decision"),
            approval_reviewer_id=(str(payload["approval_reviewer_id"]).strip() if payload.get("approval_reviewer_id") else None),
            approval_reason=(str(payload["approval_reason"]).strip() if payload.get("approval_reason") else None),
        )
        result = runtime.orchestrator.orchestrate(request)
        return _run_detail(result.run_id, runtime)

    @app.get("/api/runs/{run_id}")
    async def get_run(run_id: str) -> Dict[str, Any]:
        return _run_detail(run_id, runtime)

    @app.get("/api/runs/{run_id}/artifacts")
    async def get_run_artifacts(run_id: str) -> Dict[str, Any]:
        detail = _run_detail(run_id, runtime)
        return {
            "run": detail["run"],
            "artifacts": detail["artifacts"],
            "revisions": detail["revisions"],
            "source_files": detail["source_files"],
            "source_documents": detail["source_documents"],
            "source_notes": detail["source_notes"],
            "approvals": detail["approvals"],
            "contradictions": detail["contradictions"],
            "qa_reports": detail["qa_reports"],
            "lint_findings": detail["lint_findings"],
        }

    @app.get("/api/reviews/{revision_id}/diff")
    async def get_review_diff(revision_id: str) -> Dict[str, Any]:
        revision = _find_revision(runtime.store, revision_id)
        return _diff_payload(revision, runtime)

    @app.post("/api/approvals/{revision_id}")
    async def submit_approval(revision_id: str, payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
        revision = _find_revision(runtime.store, revision_id)
        decision = str(payload.get("decision", "")).strip()
        if decision not in {"approved", "rejected", "deferred", "escalated"}:
            raise HTTPException(status_code=400, detail="decision must be approved, rejected, deferred, or escalated")
        policy_version = str(payload.get("policy_version", "governance.v1")).strip()
        reviewer_id = str(payload.get("reviewer_id", "knowledge-manager")).strip()
        reason = str(payload.get("reason")).strip() if payload.get("reason") else None
        finalize = bool(payload.get("finalize", False))

        approval = runtime.validator.record_approval(
            revision_id=revision_id,
            decision=decision,  # type: ignore[arg-type]
            policy_version=policy_version,
            reviewer_id=reviewer_id,
            reason=reason,
        )

        finalized = False
        governance = None
        if finalize and decision == "approved":
            draft_result = _draft_result_from_revision(revision)
            governance = runtime.publisher.publish_revision(revision.run_id, draft_result, revision)
            finalized = True

        return {
            "approval": _serialize(approval),
            "governance": _serialize(governance) if governance is not None else None,
            "finalized": finalized,
            "revision": _serialize(revision),
        }

    @app.get("/api/wiki/pages/{slug}")
    async def get_wiki_page(slug: str) -> Dict[str, Any]:
        page = runtime.store.get_wiki_page_by_slug(slug)
        if page is None:
            raise HTTPException(status_code=404, detail="Wiki page not found")
        content = _read_wiki_content(runtime.wiki_root, page.current_revision_id, runtime.store)
        return {
            "page": _serialize(page),
            "content": content,
            "revisions": [_serialize(revision) for revision in runtime.store.list_wiki_page_revisions(page.page_id)],
            "approvals": [_serialize(approval) for approval in runtime.store.list_approvals()],
            "contradictions": [_serialize(record) for record in runtime.store.list_contradictions(page_id=page.page_id)],
        }

    @app.get("/api/contradictions/{contradiction_id}")
    async def get_contradiction(contradiction_id: str) -> Dict[str, Any]:
        records = [record for record in runtime.store.list_contradictions() if record.contradiction_id == contradiction_id]
        if not records:
            raise HTTPException(status_code=404, detail="Contradiction not found")
        record = records[0]
        return {
            "contradiction": _serialize(record),
            "run": _run_summary(runtime.store.get_run(record.run_id), runtime) if runtime.store.get_run(record.run_id) else None,
            "revision": _serialize(_find_revision(runtime.store, record.revision_id)) if record.revision_id else None,
        }

    @app.get("/api/health/findings")
    async def get_health_findings() -> Dict[str, Any]:
        lint_findings = runtime.store.list_lint_findings()
        contradictions = runtime.store.list_contradictions()
        pages = runtime.store.list_wiki_pages()
        open_questions = [record for record in contradictions if record.status != "resolved"]
        stale_pages = [page for page in pages if page.freshness_status != "current"]
        return {
            "generated_at": _timestamp_provider(),
            "items": {
                "lint_findings": [_serialize(item) for item in lint_findings],
                "contradictions": [_serialize(item) for item in contradictions],
                "open_questions": [_serialize(item) for item in open_questions],
                "stale_pages": [_serialize(item) for item in stale_pages],
            },
            "summary": {
                "lint_finding_count": len(lint_findings),
                "contradiction_count": len(contradictions),
                "open_question_count": len(open_questions),
                "stale_page_count": len(stale_pages),
            },
        }

    @app.get("/api/infopedia/tree")
    async def get_infopedia_tree(domain: Optional[str] = Query(default=None)) -> Dict[str, Any]:
        return runtime.infopedia.tree(domain=domain)

    @app.get("/api/infopedia/search")
    async def search_infopedia(
        q: str = Query(default=""),
        domain: Optional[str] = Query(default=None),
        page_type: Optional[str] = Query(default=None),
        freshness: Optional[str] = Query(default=None),
        confidence: Optional[str] = Query(default=None),
        status: Optional[str] = Query(default=None),
    ) -> Dict[str, Any]:
        return runtime.infopedia.search(
            query=q,
            domain=domain,
            page_type=page_type,
            freshness=freshness,
            confidence=confidence,
            status=status,
        )

    @app.get("/api/infopedia/pages/{slug}")
    async def get_infopedia_page(slug: str) -> Dict[str, Any]:
        try:
            return runtime.infopedia.page(slug)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Infopedia page not found") from exc

    return app


def _run_detail(run_id: str, runtime: KmiRuntime) -> Dict[str, Any]:
    run = runtime.store.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    run_events = runtime.store.list_run_events(run_id)
    revisions = runtime.store.list_wiki_page_revisions()
    run_revisions = [revision for revision in revisions if revision.run_id == run_id]
    return {
        "run": _run_summary(run, runtime),
        "source_files": [_serialize(item) for item in runtime.store.list_source_files(run_id)],
        "source_documents": [_serialize(item) for item in runtime.store.list_source_documents(run_id)],
        "source_notes": [_serialize(item) for item in runtime.store.list_source_notes(run_id)],
        "artifacts": [_serialize(item) for item in runtime.store.list_intake_artifacts(run_id)],
        "impact_records": [_serialize(item) for item in runtime.store.list_impact_records(run_id)],
        "revisions": [_serialize(item) for item in run_revisions],
        "approvals": [_serialize(item) for item in runtime.store.list_approvals()],
        "contradictions": [_serialize(item) for item in runtime.store.list_contradictions(run_id=run_id)],
        "qa_reports": [_serialize(item) for item in runtime.store.list_qa_reports(run_id=run_id)],
        "lint_findings": [_serialize(item) for item in runtime.store.list_lint_findings(run_id=run_id)],
        "run_events": [_serialize(item) for item in run_events],
    }


def _run_summary(run: Any, runtime: KmiRuntime) -> Dict[str, Any]:
    if run is None:
        return {}
    revisions = [revision for revision in runtime.store.list_wiki_page_revisions() if revision.run_id == run.run_id]
    open_contradictions = [
        item for item in runtime.store.list_contradictions(run_id=run.run_id) if item.status != "resolved"
    ]
    pending_approvals = [revision for revision in revisions if revision.status in {"staged", "review_required"}]
    return {
        "run_id": run.run_id,
        "status": run.status,
        "source_path": run.source_path,
        "domain_hint": run.domain_hint,
        "run_notes": run.run_notes,
        "created_at": run.created_at,
        "started_at": run.started_at,
        "completed_at": run.completed_at,
        "created_by": run.created_by,
        "current_stage": run.current_stage,
        "revision_count": len(revisions),
        "pending_approvals": len(pending_approvals),
        "contradiction_count": len(open_contradictions),
        "lint_count": len(runtime.store.list_lint_findings(run_id=run.run_id)),
        "qa_count": len(runtime.store.list_qa_reports(run_id=run.run_id)),
        "artifact_count": len(runtime.store.list_intake_artifacts(run_id=run.run_id)),
        "source_file_count": len(runtime.store.list_source_files(run_id=run.run_id)),
        "source_document_count": len(runtime.store.list_source_documents(run_id=run.run_id)),
        "source_note_count": len(runtime.store.list_source_notes(run_id=run.run_id)),
    }


def _dashboard_summary(runtime: KmiRuntime) -> Dict[str, Any]:
    runs = runtime.store.list_runs()
    revisions = runtime.store.list_wiki_page_revisions()
    contradictions = runtime.store.list_contradictions()
    lint_findings = runtime.store.list_lint_findings()
    return {
        "run_count": len(runs),
        "blocked_runs": len([run for run in runs if run.status == "blocked"]),
        "in_progress_runs": len([run for run in runs if run.status == "in_progress"]),
        "completed_runs": len([run for run in runs if run.status == "completed"]),
        "pending_approvals": len([rev for rev in revisions if rev.status in {"staged", "review_required"}]),
        "open_contradictions": len([item for item in contradictions if item.status != "resolved"]),
        "lint_findings": len(lint_findings),
    }


def _diff_payload(revision: WikiPageRevision, runtime: KmiRuntime) -> Dict[str, Any]:
    draft = _draft_result_from_revision(revision)
    current_markdown = _read_wiki_content(runtime.wiki_root, revision.revision_id, runtime.store)
    before = ""
    if revision.change_type == "update":
        page = next((page for page in runtime.store.list_wiki_pages() if page.page_id == revision.page_id), None)
        if page is not None:
            before = _read_wiki_content(runtime.wiki_root, page.current_revision_id, runtime.store)
    after = draft.content_markdown
    diff = "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile="before.md",
            tofile="after.md",
        )
    )
    qa_reports = runtime.store.list_qa_reports(revision_id=revision.revision_id)
    approvals = runtime.store.list_approvals(revision.revision_id)
    contradictions = runtime.store.list_contradictions(revision_id=revision.revision_id)
    return {
        "revision": _serialize(revision),
        "page": _serialize(next(page for page in runtime.store.list_wiki_pages() if page.page_id == revision.page_id)),
        "current_markdown": current_markdown,
        "before_markdown": before,
        "after_markdown": after,
        "diff": diff,
        "source_trace_ids": list(revision.source_trace_ids),
        "rule_findings": _serialize(qa_reports[-1]) if qa_reports else None,
        "approvals": [_serialize(item) for item in approvals],
        "contradictions": [_serialize(item) for item in contradictions],
    }


def _draft_result_from_revision(revision: WikiPageRevision) -> WikiDraftResult:
    return WikiDraftResult(
        title=revision.draft_title,
        slug=revision.draft_slug,
        page_type=revision.draft_page_type,
        domain=revision.draft_domain,
        path=revision.draft_path,
        content_markdown=revision.draft_markdown,
        frontmatter=dict(revision.draft_frontmatter),
        template_file=f"{revision.draft_page_type}.md",
        section_content=dict(revision.draft_sections),
    )


def _read_wiki_content(wiki_root: Path, revision_id: str | None, store: InMemoryMetadataStore) -> str:
    if revision_id is None:
        return ""
    revision = next((item for item in store.list_wiki_page_revisions() if item.revision_id == revision_id), None)
    if revision is None:
        return ""
    content_path = wiki_root / revision.draft_path
    if content_path.exists():
        return content_path.read_text(encoding="utf-8")
    return revision.draft_markdown


def _find_revision(store: InMemoryMetadataStore, revision_id: str) -> WikiPageRevision:
    for revision in store.list_wiki_page_revisions():
        if revision.revision_id == revision_id:
            return revision
    raise HTTPException(status_code=404, detail="Revision not found")


def _serialize(value: Any) -> Any:
    if value is None:
        return None
    if is_dataclass(value):
        return {key: _serialize(item) for key, item in asdict(value).items()}
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items()}
    return value


def _timestamp_provider() -> str:
    return datetime.now(timezone.utc).isoformat()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


__all__ = ["create_app", "KmiRuntime"]
