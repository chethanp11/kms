"""Observable event contracts for early scaffold validation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    subject_id: str
    message: str
    created_at: str


def audit_event(event_type: str, subject_id: str, message: str) -> AuditEvent:
    return AuditEvent(event_type=event_type, subject_id=subject_id, message=message, created_at=datetime.now(timezone.utc).isoformat())


__all__ = ["AuditEvent", "audit_event"]
