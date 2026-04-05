from __future__ import annotations

from kms_api.db.factory import create_metadata_store
from kms_api.orchestration import OrchestrationRequest, RunOrchestrationService
from kms_config import load_runtime_config


def run_orchestration_job(
    source_root_path: str,
    initiated_by: str = "worker",
    domain_hint: str | None = None,
    run_notes: str | None = None,
) -> object:
    runtime_config = load_runtime_config()
    store = create_metadata_store(runtime_config)
    service = RunOrchestrationService(store)
    return service.orchestrate(
        OrchestrationRequest(
            source_root_path=source_root_path,
            initiated_by=initiated_by,
            domain_hint=domain_hint,
            run_notes=run_notes,
        )
    )
