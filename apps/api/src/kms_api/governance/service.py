from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import logging
from pathlib import Path
from typing import Any, Callable

from kms_domain import (
    ApprovalRecord,
    ApprovalDecision,
    ContradictionRecord,
    MetadataStore,
    QAReport,
    WikiPageRevision,
)

from kms_api.wiki.models import WikiDraftInput, WikiDraftResult
from kms_api.wiki.service import WikiRevisionWriter

from .loader import GovernanceRuleLoader
from .models import (
    ContradictionStatus,
    GovernanceDecision,
    GovernanceRule,
    GovernanceStatus,
    RuleFinding,
    SourceTraceStatus,
)

TimestampProvider = Callable[[], str]

logger = logging.getLogger(__name__)


def default_timestamp_provider() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_stable_id(prefix: str, *parts: str) -> str:
    import hashlib

    digest = hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


class GovernanceBlockedError(RuntimeError):
    def __init__(self, decision: GovernanceDecision) -> None:
        super().__init__("Governance blocked publish")
        self.decision = decision


@dataclass(frozen=True)
class _Context:
    draft: WikiDraftInput
    draft_result: WikiDraftResult | None
    revision: WikiPageRevision | None
    page_id: str | None
    page_sections: list[str]
    non_empty_sections: list[str]
    source_refs: list[str]
    source_trace_lines: list[str]
    contradiction_max_severity: str
    contradictions: list[ContradictionRecord]
    approval_record: ApprovalRecord | None
    change_type: str


class PolicyValidationService:
    def __init__(
        self,
        store: MetadataStore,
        rules_root: Path | None = None,
        timestamp_provider: TimestampProvider | None = None,
    ) -> None:
        self._store = store
        self._loader = GovernanceRuleLoader(rules_root)
        self._rules = self._loader.load().rules
        self._timestamp_provider = timestamp_provider or default_timestamp_provider

    def validate_draft_input(
        self,
        run_id: str,
        draft: WikiDraftInput,
    ) -> GovernanceDecision:
        context = self._build_context(run_id=run_id, draft=draft, draft_result=None, revision=None)
        return self._evaluate(run_id, context)

    def validate_revision(
        self,
        run_id: str,
        draft_result: WikiDraftResult,
        revision: WikiPageRevision,
    ) -> GovernanceDecision:
        draft = _draft_input_from_result(draft_result)
        context = self._build_context(
            run_id=run_id,
            draft=draft,
            draft_result=draft_result,
            revision=revision,
        )
        return self._evaluate(run_id, context)

    def record_approval(
        self,
        revision_id: str,
        decision: ApprovalDecision,
        policy_version: str,
        reviewed_at: str | None = None,
        reviewer_id: str | None = None,
        reason: str | None = None,
        override_requested: bool = False,
    ) -> ApprovalRecord:
        approval = ApprovalRecord(
            approval_id=make_stable_id("approval", revision_id, policy_version, decision),
            revision_id=revision_id,
            decision=decision,
            policy_version=policy_version,
            reviewed_at=reviewed_at or self._timestamp_provider(),
            reviewer_id=reviewer_id,
            reason=reason,
            override_requested=override_requested,
        )
        self._store.record_approval(approval)
        revisions = self._store.list_wiki_page_revisions()
        for revision in revisions:
            if revision.revision_id == revision_id:
                revision.status = (
                    "approved"
                    if decision == "approved"
                    else "rejected"
                    if decision == "rejected"
                    else "review_required"
                )
                self._store.upsert_wiki_page_revision(revision)
                break
        return approval

    def record_contradiction(self, record: ContradictionRecord) -> ContradictionRecord:
        return self._store.record_contradiction(record)

    def approve_revision(self, revision_id: str, policy_version: str, reviewer_id: str) -> ApprovalRecord:
        return self.record_approval(
            revision_id=revision_id,
            decision="approved",
            policy_version=policy_version,
            reviewer_id=reviewer_id,
        )

    def reject_revision(self, revision_id: str, policy_version: str, reviewer_id: str, reason: str) -> ApprovalRecord:
        return self.record_approval(
            revision_id=revision_id,
            decision="rejected",
            policy_version=policy_version,
            reviewer_id=reviewer_id,
            reason=reason,
        )

    def _build_context(
        self,
        *,
        run_id: str,
        draft: WikiDraftInput,
        draft_result: WikiDraftResult | None,
        revision: WikiPageRevision | None,
    ) -> _Context:
        page_sections = list(draft.section_content.keys())
        non_empty_sections = [
            section_name
            for section_name, value in draft.section_content.items()
            if _is_present(value)
        ]
        source_refs = list(draft.source_refs)
        source_trace_lines = _as_list(draft.section_content.get("Source Trace"))
        existing_page = None
        if draft_result is not None:
            existing_page = self._store.get_wiki_page_by_slug(draft_result.slug)
        change_type = revision.change_type if revision is not None else "create"
        contradictions = self._store.list_contradictions(
            run_id=run_id,
            page_id=existing_page.page_id if existing_page is not None else None,
            revision_id=revision.revision_id if revision is not None else None,
        )
        approval_record = None
        if revision is not None:
            approvals = self._store.list_approvals(revision.revision_id)
            approval_record = approvals[-1] if approvals else None
        return _Context(
            draft=draft,
            draft_result=draft_result,
            revision=revision,
            page_id=existing_page.page_id if existing_page is not None else None,
            page_sections=page_sections,
            non_empty_sections=non_empty_sections,
            source_refs=source_refs,
            source_trace_lines=source_trace_lines,
            contradiction_max_severity=_max_contradiction_severity(contradictions),
            contradictions=contradictions,
            approval_record=approval_record,
            change_type=change_type,
        )

    def _evaluate(self, run_id: str, context: _Context) -> GovernanceDecision:
        findings: list[RuleFinding] = []
        if not context.draft.title.strip():
            findings.append(
                RuleFinding(
                    rule_id="gate.title_required",
                    severity="error",
                    action="block_publish",
                    message="Wiki draft title is required.",
                )
            )
        if not context.draft.domain.strip():
            findings.append(
                RuleFinding(
                    rule_id="gate.domain_required",
                    severity="error",
                    action="block_publish",
                    message="Wiki draft domain is required.",
                )
            )
        if not context.draft.last_updated.strip():
            findings.append(
                RuleFinding(
                    rule_id="gate.last_updated_required",
                    severity="error",
                    action="block_publish",
                    message="Wiki draft last_updated is required.",
                )
            )
        if not context.draft.owners:
            findings.append(
                RuleFinding(
                    rule_id="gate.owners_required",
                    severity="error",
                    action="block_publish",
                    message="Wiki draft owners must not be empty.",
                )
            )
        if not context.source_refs:
            findings.append(
                RuleFinding(
                    rule_id="gate.source_refs_required",
                    severity="error",
                    action="block_publish",
                    message="Finalized pages require at least one source reference.",
                )
            )
        if "Source Trace" not in context.non_empty_sections:
            findings.append(
                RuleFinding(
                    rule_id="gate.source_trace_section_required",
                    severity="error",
                    action="block_publish",
                    message="Source Trace section must be populated before publication.",
                )
            )

        if context.contradiction_max_severity == "error":
            findings.append(
                RuleFinding(
                    rule_id="gate.contradiction_high",
                    severity="error",
                    action="block_publish",
                    message="High-severity contradiction blocks publication.",
                )
            )
        elif context.contradiction_max_severity == "warning":
            findings.append(
                RuleFinding(
                    rule_id="gate.contradiction_medium",
                    severity="warning",
                    action="escalate_review",
                    message="Medium-severity contradiction requires human review.",
                )
            )

        for rule in self._rules:
            finding = self._evaluate_rule(rule, context)
            if finding is not None:
                findings.append(finding)

        approval_required = _requires_approval(context, findings)
        approval_record = context.approval_record
        approval_granted = approval_record is not None and approval_record.decision == "approved"
        approval_rejected = approval_record is not None and approval_record.decision == "rejected"

        blocked = any(finding.action == "block_publish" for finding in findings) or approval_rejected
        review_required = approval_required and not approval_granted
        if blocked:
            status: GovernanceStatus = "blocked"
        elif review_required:
            status = "review_required"
        else:
            status = "pass"

        contradiction_status: ContradictionStatus = "clear"
        if context.contradiction_max_severity == "warning":
            contradiction_status = "review_required"
        elif context.contradiction_max_severity == "error":
            contradiction_status = "blocked"

        qa_status = "pass"
        if blocked:
            qa_status = "fail"
        elif review_required:
            qa_status = "warn"

        qa_report = QAReport(
            qa_report_id=make_stable_id(
                "qa",
                run_id,
                context.revision.revision_id if context.revision is not None else "draft",
                context.draft.page_type,
                context.draft_result.slug if context.draft_result is not None else context.draft.title,
            ),
            run_id=run_id,
            status=qa_status,  # type: ignore[arg-type]
            rule_ids=[finding.rule_id for finding in findings],
            summary=_summarize_findings(findings, approval_required, approval_granted, blocked),
            created_at=self._timestamp_provider(),
            revision_id=context.revision.revision_id if context.revision is not None else None,
        )
        self._store.record_qa_report(qa_report)

        if context.revision is not None:
            context.revision.status = (
                "rejected" if blocked else "review_required" if review_required else "approved"
            )
            self._store.upsert_wiki_page_revision(context.revision)

        run = self._store.get_run(run_id)
        if run is not None and blocked:
            run.status = "blocked"
            run.current_stage = "governance_blocked"
            self._store.create_run(run)

        return GovernanceDecision(
            run_id=run_id,
            revision_id=context.revision.revision_id if context.revision is not None else None,
            page_id=context.page_id,
            status=status,
            publish_allowed=not blocked and (not approval_required or approval_granted),
            approval_required=approval_required,
            source_trace_status=_source_trace_status(context),
            contradiction_status=contradiction_status,
            qa_report_id=qa_report.qa_report_id,
            rule_findings=findings,
            messages=[qa_report.summary],
            revision_status=context.revision.status if context.revision is not None else "staged",
        )

    def _evaluate_rule(
        self,
        rule: GovernanceRule,
        context: _Context,
    ) -> RuleFinding | None:
        if rule.scope_page_types and context.draft.page_type not in rule.scope_page_types:
            return None
        condition_result = _evaluate_condition(rule.condition, _build_rule_context(context))
        if rule.action == "block_publish":
            if rule.rule_id in _REQUIREMENT_BLOCK_RULE_IDS:
                if condition_result:
                    return None
            else:
                if not condition_result:
                    return None
            message = f"{rule.description} Publish blocked."
        elif rule.action == "escalate_review":
            if rule.rule_id in _TRIGGER_REVIEW_RULE_IDS:
                if not condition_result:
                    return None
            else:
                if condition_result:
                    return None
            message = f"{rule.description} Review required."
        else:
            if not condition_result:
                return None
            message = rule.description
        return RuleFinding(
            rule_id=rule.rule_id,
            severity=rule.severity,
            action=rule.action,
            message=message,
            details={"source_file": rule.source_file},
        )


class GovernedWikiPublicationService:
    def __init__(
        self,
        validator: PolicyValidationService,
        writer: WikiRevisionWriter,
        post_publish_hook: Callable[[], None] | None = None,
    ) -> None:
        self._validator = validator
        self._writer = writer
        self._post_publish_hook = post_publish_hook

    def publish_revision(
        self,
        run_id: str,
        draft_result: WikiDraftResult,
        revision: WikiPageRevision,
    ) -> GovernanceDecision:
        logger.info(
            "publish_revision_started run_id=%s revision_id=%s slug=%s",
            run_id,
            revision.revision_id,
            draft_result.slug,
        )
        decision = self._validator.validate_revision(run_id, draft_result, revision)
        if not decision.publish_allowed:
            logger.info(
                "publish_revision_blocked run_id=%s revision_id=%s status=%s",
                run_id,
                revision.revision_id,
                decision.status,
            )
            raise GovernanceBlockedError(decision)
        self._writer.write_revision(run_id, draft_result, governance_result=decision)
        if self._post_publish_hook is not None:
            self._post_publish_hook()
        logger.info("publish_revision_completed run_id=%s revision_id=%s", run_id, revision.revision_id)
        return decision


def _draft_input_from_result(draft_result: WikiDraftResult) -> WikiDraftInput:
    return WikiDraftInput(
        title=draft_result.title,
        page_type=draft_result.page_type,
        domain=draft_result.domain,
        section_content=dict(draft_result.section_content),
        source_refs=list(draft_result.frontmatter["source_refs"]),  # type: ignore[index]
        related=list(draft_result.frontmatter["related"]),  # type: ignore[index]
        tags=list(draft_result.frontmatter["tags"]),  # type: ignore[index]
        owners=list(draft_result.frontmatter["owners"]),  # type: ignore[index]
        last_updated=str(draft_result.frontmatter["last_updated"]),
        confidence=draft_result.frontmatter["confidence"],  # type: ignore[assignment]
        review_required=bool(draft_result.frontmatter["review_required"]),
        status=draft_result.frontmatter["status"],  # type: ignore[assignment]
        identity_key=draft_result.slug,
    )


def _build_rule_context(context: _Context) -> dict[str, Any]:
    return {
        "frontmatter": {
            "title": context.draft.title,
            "slug": context.draft_result.slug if context.draft_result is not None else "",
            "type": context.draft.page_type,
            "domain": context.draft.domain,
            "status": context.draft.status,
            "source_refs": context.source_refs,
            "last_updated": context.draft.last_updated,
            "confidence": context.draft.confidence,
            "review_required": context.draft.review_required,
            "related": context.draft.related,
            "tags": context.draft.tags,
            "owners": context.draft.owners,
        },
        "page": {
            "title": context.draft.title,
            "type": context.draft.page_type,
            "sections": list(context.page_sections),
            "non_empty_sections": list(context.non_empty_sections),
            "change_type": context.change_type,
            "section_count": len(context.page_sections),
        },
        "revision": {
            "change_type": context.change_type,
            "status": context.revision.status if context.revision is not None else "staged",
        },
        "source_trace": {
            "count": len(context.source_refs),
            "lines": list(context.source_trace_lines),
        },
        "contradictions": {
            "count": len(context.contradictions),
            "max_severity": context.contradiction_max_severity,
            "severities": [record.severity for record in context.contradictions],
        },
        "approval": {
            "exists": context.approval_record is not None,
            "decision": context.approval_record.decision if context.approval_record else None,
            "reviewer_id": context.approval_record.reviewer_id if context.approval_record else None,
            "override_requested": (
                context.approval_record.override_requested if context.approval_record else False
            ),
        },
    }


def _evaluate_condition(condition: dict[str, Any], context: dict[str, Any]) -> bool:
    if "all" in condition:
        return all(_evaluate_condition(child, context) for child in condition["all"])
    if "any" in condition:
        return any(_evaluate_condition(child, context) for child in condition["any"])
    field_path = condition.get("field")
    operator = condition.get("operator")
    if field_path is None or operator is None:
        raise ValueError(f"Invalid rule condition: {condition}")
    current = _resolve_path(context, str(field_path))
    expected = condition.get("value")
    if operator == "exists":
        return _is_present(current)
    if operator == "min_items":
        return isinstance(current, list) and len(current) >= int(expected)
    if operator == "equals":
        return current == expected
    if operator == "not_equals":
        return current != expected
    if operator == "in":
        return current in _as_list(expected)
    if operator == "contains":
        return isinstance(current, list) and expected in current
    if operator == "contains_all":
        return isinstance(current, list) and all(item in current for item in _as_list(expected))
    if operator == "contains_any":
        return isinstance(current, list) and any(item in current for item in _as_list(expected))
    raise ValueError(f"Unsupported rule operator: {operator}")


def _resolve_path(context: dict[str, Any], path: str) -> Any:
    current: Any = context
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _is_present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return len(value) > 0
    if isinstance(value, dict):
        return len(value) > 0
    return True


def _max_contradiction_severity(records: list[ContradictionRecord]) -> str:
    severity_order = {"info": 0, "warning": 1, "error": 2}
    if not records:
        return "clear"
    return max(records, key=lambda record: severity_order[record.severity]).severity


def _source_trace_status(context: _Context) -> SourceTraceStatus:
    if not context.source_refs:
        return "missing"
    if not context.source_trace_lines:
        return "partial"
    return "complete"


def _requires_approval(context: _Context, findings: list[RuleFinding]) -> bool:
    if context.draft.review_required:
        return True
    if context.draft.confidence in {"low", "medium", "provisional"}:
        return True
    if context.draft.page_type in {"metric", "data-asset"} and context.change_type == "create":
        return True
    if any(finding.action == "escalate_review" for finding in findings):
        return True
    if context.contradiction_max_severity in {"warning", "error"}:
        return True
    return False


def _summarize_findings(
    findings: list[RuleFinding],
    approval_required: bool,
    approval_granted: bool,
    blocked: bool,
) -> str:
    if blocked:
        return "Validation blocked by policy, contradiction, or missing required source trace."
    if approval_required and not approval_granted:
        return "Validation requires human approval before finalization."
    if findings:
        return "Validation completed with policy findings."
    return "Validation passed without findings."


_REQUIREMENT_BLOCK_RULE_IDS = {
    "rule.page_requires_common_sections",
    "rule.source_trace_requires_references",
}

_TRIGGER_REVIEW_RULE_IDS = {
    "rule.review_required_flag_escalates",
    "rule.low_confidence_requires_review",
    "rule.new_canonical_metric_requires_approval",
    "rule.new_canonical_data_asset_requires_approval",
    "rule.contradiction_requires_review",
}
