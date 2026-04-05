from __future__ import annotations

import json
from pathlib import Path

import pytest

from kms_api.db.metadata_store import InMemoryMetadataStore
from kms_api.wiki.conventions import canonical_page_path, resolve_page_slug, slugify
from kms_api.wiki.models import WikiDraftInput
from kms_api.wiki.service import (
    WikiDraftService,
    WikiRevisionWriter,
    source_note_to_draft_input,
)
from kms_domain import SourceNote


FIXTURES = Path("tests/fixtures/wiki")


def load_json_fixture(name: str) -> dict[str, object]:
    return json.loads((FIXTURES / "drafts" / f"{name}.json").read_text(encoding="utf-8"))


def load_expected_markdown(name: str) -> str:
    return (FIXTURES / "expected" / f"{name}.md").read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "page_type,domain,title,expected_path",
    [
        ("metric", "customer-revenue-analytics", "Net Revenue Retention", "metrics/customer-revenue-analytics/net-revenue-retention.md"),
        ("data-asset", "customer-revenue-analytics", "Sales Orders Fact", "data-assets/customer-revenue-analytics/sales-orders-fact.md"),
        ("source-note", "customer-revenue-analytics", "Net Revenue Retention Source Note", "source-notes/customer-revenue-analytics/net-revenue-retention-source-note.md"),
        ("open-question", "customer-revenue-analytics", "Net Revenue Retention Clarification", "open-questions/customer-revenue-analytics/net-revenue-retention-clarification.md"),
    ],
)
def test_canonical_page_path_uses_type_folders(page_type: str, domain: str, title: str, expected_path: str) -> None:
    slug = slugify(title)
    assert str(canonical_page_path(page_type, domain, slug)) == expected_path


def test_slug_collision_resolves_deterministically() -> None:
    slug = resolve_page_slug(
        title="Net Revenue Retention",
        page_type="metric",
        domain="customer-revenue-analytics",
        identity_key="metric:customer-revenue-analytics:nrr-v2",
        existing_slugs={"net-revenue-retention"},
    )

    assert slug.startswith("net-revenue-retention-")
    assert slug != "net-revenue-retention"


@pytest.mark.parametrize(
    "fixture_name",
    [
        "metric-net-revenue-retention",
        "data-asset-sales-orders-fact",
        "source-note-net-revenue-retention",
        "open-question-net-revenue-retention",
    ],
)
def test_wiki_draft_service_renders_expected_markdown(fixture_name: str) -> None:
    payload = load_json_fixture(fixture_name)
    draft_payload = dict(payload)
    expected_slug = draft_payload.pop("expected_slug")
    expected_path = draft_payload.pop("expected_path")
    draft = WikiDraftService().build_draft(WikiDraftInput(**draft_payload))

    assert draft.content_markdown == load_expected_markdown(fixture_name)
    assert draft.path == expected_path
    assert draft.slug == expected_slug


def test_source_note_adapter_uses_intake_outputs() -> None:
    source_note = SourceNote(
        source_note_id="note_123",
        run_id="run_123",
        source_document_id="doc_123",
        title="Net Revenue Retention Source Note",
        slug="source-notes/net-revenue-retention",
        summary="NRR improved to 118% for enterprise accounts in Q4.",
        source_refs=["/sources/reports/q4-revenue-ops-review.md"],
        extracted_signals=["NRR", "enterprise accounts", "Q4 improvement"],
        review_required=True,
        created_at="2026-04-05T09:12:44Z",
    )

    draft_input = source_note_to_draft_input(
        source_note,
        domain="customer-revenue-analytics",
        source_details="Parsed from the intake source note and attached raw note.",
        current_understanding="The note suggests the metric should be reconciled against monthly close.",
        related=["metric/customer-revenue-analytics/net-revenue-retention"],
        tags=["source-note", "revenue"],
        owners=["knowledge-manager:revenue-ops"],
        identity_key="source-note:customer-revenue-analytics:net-revenue-retention",
    )

    assert draft_input.page_type == "source-note"
    assert draft_input.section_content["Extracted Signals"] == ["NRR", "enterprise accounts", "Q4 improvement"]
    assert draft_input.section_content["Source Trace"] == [
        "Source reference: /sources/reports/q4-revenue-ops-review.md"
    ]


def test_revision_writer_stages_without_wiki_write(tmp_path: Path) -> None:
    payload = load_json_fixture("metric-net-revenue-retention")
    draft_payload = dict(payload)
    draft_payload.pop("expected_slug")
    draft_payload.pop("expected_path")
    draft = WikiDraftService().build_draft(WikiDraftInput(**draft_payload))
    store = InMemoryMetadataStore()
    writer = WikiRevisionWriter(store, wiki_root=tmp_path / "wiki", publish_enabled=False)

    result = writer.write_revision("run_20260405_001", draft)

    assert result.written_to_wiki is False
    assert result.page_status == "draft"
    assert not (tmp_path / "wiki").exists()

    pages = store.list_wiki_pages()
    assert len(pages) == 1
    assert pages[0].slug == draft.slug
    assert pages[0].status == "draft"

    revisions = store.list_wiki_page_revisions()
    assert len(revisions) == 1
    assert revisions[0].revision_id == result.revision_id
    assert revisions[0].status == "staged"
