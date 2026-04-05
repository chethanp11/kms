from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TypeVar

from kms_domain import AgentExecutionRecord

from kms_api.services.metadata_service import MetadataService

TimestampProvider = Callable[[], str]
T = TypeVar("T")


@dataclass(frozen=True)
class AgentSpec:
    agent_name: str
    skill_name: str | None
    stage: str


class BoundedAgentRunner:
    def __init__(
        self,
        metadata: MetadataService,
        timestamp_provider: TimestampProvider,
    ) -> None:
        self._metadata = metadata
        self._timestamp_provider = timestamp_provider

    def run(
        self,
        spec: AgentSpec,
        *,
        run_id: str,
        input_summary: str,
        handler: Callable[[], T],
        revision_id: str | None = None,
        page_id: str | None = None,
        artifact_id: str | None = None,
    ) -> T:
        execution_id = _stable_id(
            "agent",
            run_id,
            spec.agent_name,
            spec.stage,
            input_summary,
        )
        record = AgentExecutionRecord(
            execution_id=execution_id,
            run_id=run_id,
            agent_name=spec.agent_name,
            stage=spec.stage,
            status="started",
            started_at=self._timestamp_provider(),
            skill_name=spec.skill_name,
            input_summary=input_summary,
            revision_id=revision_id,
            page_id=page_id,
            artifact_id=artifact_id,
        )
        self._metadata.record_agent_execution(record)

        try:
            result = handler()
        except Exception as exc:
            record.status = "failed"
            record.completed_at = self._timestamp_provider()
            record.output_summary = ""
            record.blocked_reason = str(exc)
            self._metadata.record_agent_execution(record)
            raise

        record.status = "completed"
        record.completed_at = self._timestamp_provider()
        record.output_summary = _summarize_result(result)
        self._metadata.record_agent_execution(record)
        return result


def _summarize_result(result: object) -> str:
    if result is None:
        return ""
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        keys = ", ".join(sorted(result))
        return f"dict[{keys}]"
    if isinstance(result, list):
        return f"list[{len(result)}]"
    return result.__class__.__name__


def _stable_id(prefix: str, *parts: str) -> str:
    import hashlib

    digest = hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"
