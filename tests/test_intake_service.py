from pathlib import Path

from kms_api.db.metadata_store import InMemoryMetadataStore
from kms_api.intake.service import IntakeRequest, SourceIntakeService


def test_source_intake_discovers_parses_and_records_artifacts() -> None:
    fixture_root = Path("tests/fixtures/source_intake/customer-revenue").resolve()
    store = InMemoryMetadataStore()
    service = SourceIntakeService(store, timestamp_provider=lambda: "2026-04-05T09:12:44Z")

    result = service.start_intake(
        IntakeRequest(
            source_root_path=str(fixture_root),
            initiated_by="knowledge-manager",
            domain_hint="customer-revenue",
            run_notes="monthly refresh",
        )
    )

    assert result.total_files == 4
    assert result.supported_files == 3
    assert result.unsupported_files == 1
    assert result.parsed_documents == 3
    assert result.source_notes == 3
    assert result.status == "completed_with_warnings"

    runs = store.list_runs()
    assert len(runs) == 1
    assert runs[0].status == "completed_with_warnings"
    assert runs[0].current_stage == "handoff"

    source_files = store.list_source_files(result.run_id)
    assert len(source_files) == 4
    assert {source_file.parse_status for source_file in source_files} == {"parsed", "unsupported"}

    source_documents = store.list_source_documents(result.run_id)
    assert len(source_documents) == 3
    assert any("Net Revenue Retention" in document.summary for document in source_documents)

    source_notes = store.list_source_notes(result.run_id)
    assert len(source_notes) == 3
    assert all(note.review_required for note in source_notes)

    artifacts = store.list_intake_artifacts(result.run_id)
    assert len(artifacts) == 11
    assert {artifact.artifact_type for artifact in artifacts} == {
        "source_registry",
        "parse_output",
        "source_note",
        "intake_summary",
    }
