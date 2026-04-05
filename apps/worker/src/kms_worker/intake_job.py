from __future__ import annotations

from kms_api.db.factory import create_metadata_store
from kms_api.intake import SourceIntakeService
from kms_api.intake.service import IntakeRequest
from kms_config import load_runtime_config


def run_intake_job(source_root_path: str, initiated_by: str = "worker") -> object:
    runtime_config = load_runtime_config()
    store = create_metadata_store(runtime_config)
    service = SourceIntakeService(store)
    return service.start_intake(
        IntakeRequest(
            source_root_path=source_root_path,
            initiated_by=initiated_by,
        )
    )
