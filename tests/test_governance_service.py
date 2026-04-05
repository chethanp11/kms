from __future__ import annotations

import json
from pathlib import Path

import pytest

from kms_api.db.metadata_store import InMemoryMetadataStore
from kms_api.governance.loader import GovernanceRuleLoader
from kms_api.governance.service import (
    GovernedWikiPublicationService,
    GovernanceBlockedError,
    PolicyValidationService,
)
from kms_api.wiki.models import WikiDraftInput
from kms_api.wiki.service import WikiDraftService, WikiRevisionWriter
from kms_domain import ContradictionRecord


FIXTURES = Path("tests/fixtures/wiki")


def load_json_fixture(name: str) -> dict[str, object]:
    return json.loads((FIXTURES / "drafts" / f"{name}.json").read_text(encoding="utf-8"))


def build_draft(name: str) -> WikiDraftInput:
    payload = load_json_fixture(name)
    payload = dict(payload)
    payload.pop("expected_slug")
    payload.pop("expected_path")
    return WikiDraftInput(**payload)


def build_draft_result(name: str):
    return WikiDraftService().build_draft(build_draft(name))


def test_rule_loader_reads_governance_yaml() -> None:
    loaded = GovernanceRuleLoader(Path("rules")).load()
    rule_ids = {rule.rule_id for rule in loaded.rules}

    assert "rule.page_requires_common_sections" in rule_ids
    assert "rule.source_trace_requires_references" in rule_ids
    assert "rule.new_canonical_metric_requires_approval" in rule_ids
    assert all(rule.description and rule.condition and rule.action for rule in loaded.rules)


def test_validation_blocks_missing_source_trace() -> None:
    store = InMemoryMetadataStore()
    validator = PolicyValidationService(store)
    draft = build_draft("metric-net-revenue-retention")
    draft.section_content["Source Trace"] = []

    decision = validator.validate_draft_input("run_20260405_001", draft)

    assert decision.status == "blocked"
    assert decision.publish_allowed is False
    assert decision.source_trace_status == "partial"
    assert any(
        finding.rule_id == "gate.source_trace_section_required" for finding in decision.rule_findings
    )

    reports = store.list_qa_reports("run_20260405_001")
    assert len(reports) == 1
    assert reports[0].status == "fail"
    assert reports[0].revision_id is None


def test_contradiction_gate_blocks_publish() -> None:
    store = InMemoryMetadataStore()
    validator = PolicyValidationService(store)
    draft_result = build_draft_result("metric-net-revenue-retention")
    writer = WikiRevisionWriter(store, publish_enabled=False)
    writer.write_revision("run_20260405_002", draft_result)
    revision = store.list_wiki_page_revisions()[0]

    store.record_contradiction(
        ContradictionRecord(
            contradiction_id="contradiction_001",
            run_id="run_20260405_002",
            severity="error",
            status="open",
            conflicting_claims=["claim a", "claim b"],
            source_refs=["raw:/sources/reports/nrr.csv"],
            created_at="2026-04-05T09:12:44Z",
            revision_id=revision.revision_id,
            page_id=revision.page_id,
        )
    )

    decision = validator.validate_revision("run_20260405_002", draft_result, revision)

    assert decision.status == "blocked"
    assert decision.publish_allowed is False
    assert decision.contradiction_status == "blocked"
    assert any(finding.rule_id == "gate.contradiction_high" for finding in decision.rule_findings)


def test_approval_gate_allows_publish_after_review(tmp_path: Path) -> None:
    store = InMemoryMetadataStore()
    validator = PolicyValidationService(store)
    draft_result = build_draft_result("metric-net-revenue-retention")
    staging_writer = WikiRevisionWriter(store, publish_enabled=False)
    staging_writer.write_revision("run_20260405_003", draft_result)
    revision = store.list_wiki_page_revisions()[0]

    initial = validator.validate_revision("run_20260405_003", draft_result, revision)
    assert initial.status == "review_required"
    assert initial.approval_required is True
    assert initial.publish_allowed is False

    approval = validator.approve_revision(
        revision.revision_id,
        policy_version="governance.v1",
        reviewer_id="knowledge-manager",
    )
    assert approval.decision == "approved"

    approved = validator.validate_revision("run_20260405_003", draft_result, revision)
    assert approved.status == "pass"
    assert approved.publish_allowed is True

    publish_writer = WikiRevisionWriter(
        store,
        wiki_root=tmp_path / "wiki",
        publish_enabled=True,
    )
    published = GovernedWikiPublicationService(validator, publish_writer).publish_revision(
        "run_20260405_003",
        draft_result,
        revision,
    )

    assert published.publish_allowed is True
    assert (tmp_path / "wiki" / draft_result.path).exists()
    assert store.list_wiki_page_revisions()[0].status == "finalized"


def test_governed_publication_blocks_without_approval(tmp_path: Path) -> None:
    store = InMemoryMetadataStore()
    validator = PolicyValidationService(store)
    draft_result = build_draft_result("metric-net-revenue-retention")
    staging_writer = WikiRevisionWriter(store, publish_enabled=False)
    staging_writer.write_revision("run_20260405_005", draft_result)
    revision = store.list_wiki_page_revisions()[0]

    publication_service = GovernedWikiPublicationService(
        validator,
        WikiRevisionWriter(store, wiki_root=tmp_path / "wiki", publish_enabled=True),
    )

    with pytest.raises(GovernanceBlockedError):
        publication_service.publish_revision("run_20260405_005", draft_result, revision)

    assert not (tmp_path / "wiki").exists()


def test_writer_refuses_publish_without_governance_result(tmp_path: Path) -> None:
    store = InMemoryMetadataStore()
    draft_result = build_draft_result("metric-net-revenue-retention")
    writer = WikiRevisionWriter(store, wiki_root=tmp_path / "wiki", publish_enabled=True)

    with pytest.raises(PermissionError):
        writer.write_revision("run_20260405_004", draft_result)

    assert store.list_wiki_pages() == []
    assert store.list_wiki_page_revisions() == []
    assert not (tmp_path / "wiki").exists()
