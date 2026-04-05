from __future__ import annotations

from kms_api.db.metadata_store import InMemoryMetadataStore
from kms_api.intake import SourceIntakeService
from kms_api.intake.service import IntakeRequest


def run_intake_job(source_root_path: str, initiated_by: str = "worker") -> object:
    store = InMemoryMetadataStore()
    service = SourceIntakeService(store)
    return service.start_intake(
        IntakeRequest(
            source_root_path=source_root_path,
            initiated_by=initiated_by,
        )
    )
