from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable

from kms_domain import (
    IntakeArtifact,
    MetadataStore,
    SourceNote,
    WikiPage,
    WikiPageRevision,
)

from kms_api.governance.models import GovernanceDecision
from .conventions import canonical_page_path, canonical_page_type_folder, resolve_page_slug
from .models import WikiDraftInput, WikiDraftResult, WikiRevisionWriteResult
from .templates import TemplateCatalog, render_frontmatter, render_template

TimestampProvider = Callable[[], str]


def default_timestamp_provider() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_stable_id(prefix: str, *parts: str) -> str:
    import hashlib

    digest = hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


class WikiDraftService:
    def __init__(
        self,
        templates_root: Path | None = None,
        existing_slugs: Iterable[str] | None = None,
    ) -> None:
        self._templates_root = templates_root or Path("templates/wiki")
        self._catalog = TemplateCatalog.load(self._templates_root)
        self._existing_slugs = set(existing_slugs or [])

    def build_draft(
        self,
        request: WikiDraftInput,
        *,
        existing_slugs: Iterable[str] | None = None,
    ) -> WikiDraftResult:
        if not request.title.strip():
            raise ValueError("Wiki draft title is required")
        if not request.domain.strip():
            raise ValueError("Wiki draft domain is required")
        if not request.last_updated.strip():
            raise ValueError("Wiki draft last_updated is required")
        if not request.source_refs:
            raise ValueError("Wiki draft source_refs must not be empty")
        if not request.owners:
            raise ValueError("Wiki draft owners must not be empty")

        blueprint = self._catalog.blueprint_for(request.page_type)
        expected_folder = canonical_page_type_folder(request.page_type)
        if blueprint.folder != expected_folder:
            raise ValueError(
                f"Blueprint folder {blueprint.folder} does not match canonical folder {expected_folder}"
            )
        unknown_sections = set(request.section_content) - set(blueprint.body_sections)
        if unknown_sections:
            raise ValueError(
                f"Unsupported section(s) for {request.page_type}: {sorted(unknown_sections)}"
            )

        template_text = self._catalog.template_text(request.page_type)
        for section_name in blueprint.body_sections:
            placeholder = f"{{{{section:{section_name}}}}}"
            if placeholder not in template_text:
                raise ValueError(
                    f"Template {blueprint.template_file} is missing placeholder {placeholder}"
                )

        slug_registry = self._existing_slugs if existing_slugs is None else set(existing_slugs)
        slug = resolve_page_slug(
            title=request.title,
            page_type=request.page_type,
            domain=request.domain,
            identity_key=request.identity_key,
            existing_slugs=slug_registry,
        )
        path = canonical_page_path(request.page_type, request.domain, slug)

        frontmatter = {
            "title": request.title,
            "slug": slug,
            "type": request.page_type,
            "domain": request.domain,
            "status": request.status,
            "source_refs": request.source_refs,
            "last_updated": request.last_updated,
            "confidence": request.confidence,
            "review_required": request.review_required,
            "related": request.related,
            "tags": request.tags,
            "owners": request.owners,
        }

        rendered = render_template(
            template_text,
            context={
                "frontmatter": render_frontmatter(self._catalog.frontmatter_order, frontmatter),
                "title": request.title,
                "slug": slug,
                "type": request.page_type,
                "domain": request.domain,
                "status": request.status,
                "last_updated": request.last_updated,
                "confidence": request.confidence,
                "review_required": "true" if request.review_required else "false",
            },
            section_content=request.section_content,
        )
        return WikiDraftResult(
            title=request.title,
            slug=slug,
            page_type=request.page_type,
            domain=request.domain,
            path=str(path),
            content_markdown=rendered.rstrip() + "\n",
            frontmatter=frontmatter,
            template_file=blueprint.template_file,
            section_content=dict(request.section_content),
        )


def source_note_to_draft_input(
    source_note: SourceNote,
    *,
    domain: str,
    source_details: str | None = None,
    current_understanding: str | None = None,
    related: list[str] | None = None,
    tags: list[str] | None = None,
    owners: list[str] | None = None,
    identity_key: str | None = None,
) -> WikiDraftInput:
    extracted_signals = source_note.extracted_signals
    summary = source_note.summary
    sections: dict[str, str | list[str]] = {
        "Summary": summary,
        "Current Understanding": current_understanding or summary,
        "Source Details": source_details or "Derived from intake source-note output.",
        "Extracted Signals": extracted_signals,
        "Candidate Entities": [],
        "Candidate Metrics": [],
        "Candidate Processes": [],
        "Candidate Impacts": [],
        "Source Trace": [f"Source reference: {source_ref}" for source_ref in source_note.source_refs],
    }
    return WikiDraftInput(
        title=source_note.title,
        page_type="source-note",
        domain=domain,
        section_content=sections,
        source_refs=list(source_note.source_refs),
        related=related or [],
        tags=tags or ["source-note"],
        owners=owners or ["knowledge-manager:unassigned"],
        last_updated=source_note.created_at,
        confidence="medium",
        review_required=source_note.review_required,
        status="finalized",
        identity_key=identity_key or source_note.source_note_id,
    )


class WikiRevisionWriter:
    def __init__(
        self,
        store: MetadataStore,
        wiki_root: Path | None = None,
        *,
        timestamp_provider: TimestampProvider | None = None,
        publish_enabled: bool = False,
    ) -> None:
        self._store = store
        self._wiki_root = wiki_root or Path("wiki")
        self._timestamp_provider = timestamp_provider or default_timestamp_provider
        self._publish_enabled = publish_enabled

    def write_revision(
        self,
        run_id: str,
        draft: WikiDraftResult,
        governance_result: GovernanceDecision | None = None,
    ) -> WikiRevisionWriteResult:
        page_id = make_stable_id("page", draft.page_type, draft.domain, draft.slug)
        revision_id = make_stable_id(
            "rev",
            run_id,
            draft.page_type,
            draft.domain,
            draft.slug,
            draft.content_markdown,
        )
        existing_page = self._store.get_wiki_page_by_slug(draft.slug)
        change_type = "create" if existing_page is None else "update"

        if self._publish_enabled:
            if governance_result is None:
                raise PermissionError("Governed wiki publication requires a validation decision")
            if not governance_result.publish_allowed:
                raise PermissionError("Governed wiki publication was blocked by validation")
            if governance_result.run_id != run_id or governance_result.revision_id != revision_id:
                raise PermissionError("Governed wiki publication decision does not match the target revision")

        page_status: str = "finalized" if self._publish_enabled else "draft"
        page = WikiPage(
            page_id=page_id,
            slug=draft.slug,
            title=draft.title,
            page_type=draft.page_type,
            status=page_status,  # type: ignore[arg-type]
            freshness_status="current" if self._publish_enabled else "missing",
            confidence_status=_map_confidence_to_page_status(str(draft.frontmatter["confidence"])),
            updated_at=self._timestamp_provider(),
            current_revision_id=revision_id,
        )
        self._store.upsert_wiki_page(page)

        revision = WikiPageRevision(
            revision_id=revision_id,
            page_id=page_id,
            run_id=run_id,
            status="staged" if not self._publish_enabled else "finalized",
            change_type=change_type,
            section_changes=list(draft.section_content),
            source_trace_ids=list(draft.frontmatter["source_refs"]),
            diff_summary=f"Rendered {draft.page_type} page from governed draft input.",
            created_at=self._timestamp_provider(),
            finalized_at=self._timestamp_provider() if self._publish_enabled else None,
            draft_title=draft.title,
            draft_slug=draft.slug,
            draft_page_type=draft.page_type,
            draft_domain=draft.domain,
            draft_path=draft.path,
            draft_markdown=draft.content_markdown,
            draft_frontmatter=dict(draft.frontmatter),
            draft_sections=dict(draft.section_content),
        )
        self._store.upsert_wiki_page_revision(revision)

        if self._publish_enabled:
            relative_path = Path(draft.path)
            file_path = self._wiki_root / relative_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(draft.content_markdown, encoding="utf-8")
            self._store.record_intake_artifact(
                IntakeArtifact(
                    artifact_id=make_stable_id("artifact", run_id, revision_id, "wiki"),
                    run_id=run_id,
                    artifact_type="wiki_publish",
                    status="created",
                    path=str(relative_path),
                    summary=f"Published {draft.title}",
                    created_at=self._timestamp_provider(),
                )
            )

        return WikiRevisionWriteResult(
            page_id=page_id,
            revision_id=revision_id,
            path=draft.path,
            written_to_wiki=self._publish_enabled,
            change_type=change_type,  # type: ignore[arg-type]
            page_status=page_status,  # type: ignore[arg-type]
        )


def _map_confidence_to_page_status(confidence: str) -> str:
    if confidence == "high":
        return "high"
    if confidence == "low":
        return "low"
    return "medium"
