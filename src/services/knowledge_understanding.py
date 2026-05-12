"""Governed AI-assisted knowledge understanding candidates.

The current implementation is deterministic and stdlib-only. It models the
bounded service contract that future AI calls must preserve: extraction may
propose structured candidates, but candidates and drafts are intermediate run
artifacts and cannot publish canonical wiki truth.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import re
from typing import Any, Mapping

from src.contracts import CandidateDraft, KnowledgeCandidate, KnowledgeCandidateType, SourceDocument
from src.services.openai_client import OpenAIClientError, OpenAIResponsesClient
from src.services.wiki_draft import slugify

_EXPLICIT_PREFIXES = {
    "entity": KnowledgeCandidateType.ENTITY,
    "process": KnowledgeCandidateType.PROCESS,
    "metric": KnowledgeCandidateType.METRIC,
    "decision": KnowledgeCandidateType.DECISION,
    "concept": KnowledgeCandidateType.CONCEPT,
    "contradiction": KnowledgeCandidateType.CONTRADICTION,
}
_METRIC_TERMS = ("metric", "kpi", "rate", "count", "total", "revenue", "cost", "margin", "%", "$")
_PROCESS_TERMS = ("process", "workflow", "stage", "step", "procedure", "handoff")
_DECISION_TERMS = ("decision", "decided", "approved", "rejected", "deferred")
_CONTRADICTION_TERMS = ("contradiction", "conflict", "disagrees", "inconsistent", "however", "but ")
_ENTITY_TERMS = ("team", "system", "service", "owner", "application", "data asset")


@dataclass(frozen=True)
class KnowledgeUnderstandingResult:
    candidates: tuple[KnowledgeCandidate, ...]
    provider: str
    fallback_used: bool = False
    warning: str = ""


def understand_knowledge(
    documents: tuple[SourceDocument, ...],
    *,
    settings: object | None = None,
    ai_client: object | None = None,
    min_relevance: float = 0.35,
) -> KnowledgeUnderstandingResult:
    """Extract candidates with configured AI first, then deterministic fallback."""
    if _ai_enabled(settings):
        model = str(getattr(settings, "ai_model", "gpt-4o"))
        client = ai_client or OpenAIResponsesClient(
            api_key=str(getattr(settings, "openai_api_key", "")),
            model=model,
            timeout_seconds=float(getattr(settings, "ai_timeout_seconds", 30.0)),
        )
        try:
            candidates = _extract_with_ai(documents, client=client, model=model, min_relevance=min_relevance)
            return KnowledgeUnderstandingResult(candidates, provider=f"openai:{model}")
        except (OpenAIClientError, ValueError, TypeError, KeyError) as exc:
            fallback = extract_knowledge_candidates(documents, min_relevance=min_relevance)
            return KnowledgeUnderstandingResult(fallback, provider="deterministic", fallback_used=True, warning=str(exc))
    return KnowledgeUnderstandingResult(extract_knowledge_candidates(documents, min_relevance=min_relevance), provider="deterministic")


def extract_knowledge_candidates(documents: tuple[SourceDocument, ...], *, min_relevance: float = 0.35) -> tuple[KnowledgeCandidate, ...]:
    """Extract filtered proposal candidates from parsed source documents."""
    candidates: list[KnowledgeCandidate] = []
    sequence = 1
    for document in documents:
        source_ref = str(document.metadata.get("relative_path", document.source_document_id))
        for line in _candidate_lines(document.text):
            candidate_type = _classify(line)
            relevance = _relevance_score(line, candidate_type)
            if relevance < min_relevance:
                continue
            confidence = _confidence_score(line, candidate_type)
            title = _title_for(line, candidate_type)
            candidates.append(KnowledgeCandidate(
                candidate_id=f"candidate-{sequence}",
                run_id=document.run_id,
                source_document_id=document.source_document_id,
                source_ref=source_ref,
                candidate_type=candidate_type,
                title=title,
                excerpt=line[:320],
                relevance_score=relevance,
                confidence_score=confidence,
                rationale=f"{candidate_type.value} candidate extracted from source evidence with deterministic relevance and confidence scoring.",
                target_slug=f"candidates/{slugify(title)}",
            ))
            sequence += 1
    return tuple(candidates)


def build_candidate_drafts(candidates: tuple[KnowledgeCandidate, ...]) -> tuple[CandidateDraft, ...]:
    """Build non-publishable draft support artifacts for candidate review."""
    drafts: list[CandidateDraft] = []
    for candidate in candidates:
        markdown = "\n".join([
            f"# Candidate: {candidate.title}",
            "",
            f"- Type: `{candidate.candidate_type.value}`",
            f"- Proposal only: `true`",
            f"- Source: `{candidate.source_ref}`",
            f"- Relevance: `{candidate.relevance_score:.2f}`",
            f"- Confidence: `{candidate.confidence_score:.2f}`",
            "",
            "## Extracted Evidence",
            candidate.excerpt,
            "",
            "## Governance Boundary",
            "This draft is an inspectable intermediate artifact. It is not canonical wiki truth and is not publishable without deterministic validation, Knowledge Manager review, and approval.",
            "",
        ])
        drafts.append(CandidateDraft(
            draft_id=f"draft-{candidate.candidate_id}",
            run_id=candidate.run_id,
            candidate_ids=(candidate.candidate_id,),
            title=candidate.title,
            markdown=markdown,
        ))
    return tuple(drafts)


def render_candidates_json(candidates: tuple[KnowledgeCandidate, ...]) -> str:
    payload = []
    for candidate in candidates:
        item = asdict(candidate)
        item["candidate_type"] = candidate.candidate_type.value
        item["is_proposal"] = candidate.is_proposal
        payload.append(item)
    return json.dumps({"knowledge_candidates": payload}, indent=2, sort_keys=True) + "\n"


def render_understanding_metadata(result: KnowledgeUnderstandingResult) -> str:
    return json.dumps(
        {
            "provider": result.provider,
            "fallback_used": result.fallback_used,
            "warning": result.warning,
            "candidate_count": len(result.candidates),
            "proposal_only": True,
        },
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_candidate_review_markdown(candidates: tuple[KnowledgeCandidate, ...], drafts: tuple[CandidateDraft, ...]) -> str:
    lines = [
        "# Knowledge Understanding Candidates",
        "",
        "These AI-assisted understanding outputs are proposal-only run artifacts. They do not modify `/wiki` and must be reviewed before any finalized knowledge is published.",
        "",
        "| Candidate | Type | Relevance | Confidence | Source | Draft |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    drafts_by_candidate = {draft.candidate_ids[0]: draft.draft_id for draft in drafts}
    for candidate in candidates:
        lines.append(
            f"| `{candidate.candidate_id}` | `{candidate.candidate_type.value}` | `{candidate.relevance_score:.2f}` | `{candidate.confidence_score:.2f}` | `{candidate.source_ref}` | `{drafts_by_candidate.get(candidate.candidate_id, '')}` |"
        )
    lines.append("")
    return "\n".join(lines)


def _candidate_lines(text: str) -> tuple[str, ...]:
    lines = [line.strip("-* \t") for line in text.splitlines()]
    return tuple(line for line in lines if len(line) >= 12)


def _classify(line: str) -> KnowledgeCandidateType:
    lowered = line.casefold()
    prefix = lowered.split(":", 1)[0].strip()
    if prefix in _EXPLICIT_PREFIXES:
        return _EXPLICIT_PREFIXES[prefix]
    if any(term in lowered for term in _CONTRADICTION_TERMS):
        return KnowledgeCandidateType.CONTRADICTION
    if any(term in lowered for term in _METRIC_TERMS) or re.search(r"\b\d+(?:\.\d+)?%?\b", lowered):
        return KnowledgeCandidateType.METRIC
    if any(term in lowered for term in _DECISION_TERMS):
        return KnowledgeCandidateType.DECISION
    if any(term in lowered for term in _PROCESS_TERMS):
        return KnowledgeCandidateType.PROCESS
    if any(term in lowered for term in _ENTITY_TERMS):
        return KnowledgeCandidateType.ENTITY
    return KnowledgeCandidateType.CONCEPT


def _relevance_score(line: str, candidate_type: KnowledgeCandidateType) -> float:
    base = {
        KnowledgeCandidateType.CONTRADICTION: 0.85,
        KnowledgeCandidateType.METRIC: 0.78,
        KnowledgeCandidateType.DECISION: 0.74,
        KnowledgeCandidateType.PROCESS: 0.68,
        KnowledgeCandidateType.ENTITY: 0.62,
        KnowledgeCandidateType.CONCEPT: 0.48,
    }[candidate_type]
    if ":" in line:
        base += 0.08
    if len(line) > 80:
        base += 0.04
    return min(base, 0.99)


def _confidence_score(line: str, candidate_type: KnowledgeCandidateType) -> float:
    base = 0.56 if candidate_type is KnowledgeCandidateType.CONCEPT else 0.68
    if ":" in line:
        base += 0.12
    if re.search(r"\b(source|because|approved|defined|measured|owner)\b", line, re.IGNORECASE):
        base += 0.08
    if candidate_type is KnowledgeCandidateType.CONTRADICTION:
        base -= 0.08
    return max(0.05, min(base, 0.95))


def _title_for(line: str, candidate_type: KnowledgeCandidateType) -> str:
    body = line.split(":", 1)[1].strip() if ":" in line else line
    words = re.findall(r"[A-Za-z0-9%$]+", body)[:8]
    title = " ".join(words) or candidate_type.value.title()
    return title[:80]


def _ai_enabled(settings: object | None) -> bool:
    return bool(settings and getattr(settings, "ai_enabled", False) and getattr(settings, "openai_api_key", ""))


def _extract_with_ai(
    documents: tuple[SourceDocument, ...],
    *,
    client: object,
    model: str,
    min_relevance: float,
) -> tuple[KnowledgeCandidate, ...]:
    candidates: list[KnowledgeCandidate] = []
    sequence = 1
    instructions = (
        "Extract governed KMS knowledge candidates from the source text. "
        "Return only JSON with a 'candidates' array. Each item must include "
        "candidate_type, title, excerpt, relevance_score, confidence_score, and rationale. "
        "candidate_type must be one of entity, process, metric, decision, concept, contradiction. "
        "Outputs are proposal-only and must not claim to publish or approve wiki truth."
    )
    for document in documents:
        payload = _source_payload(document)
        response = client.create_json_response(instructions=instructions, user_input=json.dumps(payload, sort_keys=True))
        for item in response.get("candidates", []):
            candidate = _candidate_from_ai_item(
                item,
                document=document,
                sequence=sequence,
                model=model,
            )
            if candidate.relevance_score >= min_relevance:
                candidates.append(candidate)
                sequence += 1
    return tuple(candidates)


def _source_payload(document: SourceDocument) -> Mapping[str, str]:
    return {
        "source_document_id": document.source_document_id,
        "source_ref": str(document.metadata.get("relative_path", document.source_document_id)),
        "title": document.title,
        "text": document.text[:12000],
    }


def _candidate_from_ai_item(item: Any, *, document: SourceDocument, sequence: int, model: str) -> KnowledgeCandidate:
    if not isinstance(item, Mapping):
        raise ValueError("candidate item must be an object")
    candidate_type = KnowledgeCandidateType(str(item["candidate_type"]).casefold())
    title = str(item["title"]).strip()
    excerpt = str(item["excerpt"]).strip()
    source_ref = str(document.metadata.get("relative_path", document.source_document_id))
    relevance = float(item["relevance_score"])
    confidence = float(item["confidence_score"])
    rationale = str(item.get("rationale", f"AI-assisted extraction using {model}.")).strip()
    return KnowledgeCandidate(
        candidate_id=f"candidate-{sequence}",
        run_id=document.run_id,
        source_document_id=document.source_document_id,
        source_ref=source_ref,
        candidate_type=candidate_type,
        title=title,
        excerpt=excerpt[:320],
        relevance_score=relevance,
        confidence_score=confidence,
        rationale=f"AI-assisted extraction using {model}: {rationale}",
        target_slug=f"candidates/{slugify(title)}",
    )


__all__ = [
    "build_candidate_drafts",
    "extract_knowledge_candidates",
    "KnowledgeUnderstandingResult",
    "render_candidate_review_markdown",
    "render_candidates_json",
    "render_understanding_metadata",
    "understand_knowledge",
]
