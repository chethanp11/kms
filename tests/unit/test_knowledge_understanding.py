"""Unit coverage for TEST-021 governed knowledge understanding candidates."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import json
import os
import unittest
from unittest.mock import patch

from src.config.settings import KMSSettings
from src.contracts import KnowledgeCandidate, KnowledgeCandidateType, SourceDocument, ValidationError
from src.services.openai_client import OpenAIClientError
from src.services.knowledge_understanding import build_candidate_drafts, extract_knowledge_candidates, understand_knowledge
from src.services.run_orchestration import KMSRuntime


class KnowledgeUnderstandingTests(unittest.TestCase):
    def test_settings_load_local_env_placeholder_values_without_exposing_key_repr(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / ".env").write_text(
                "OPEN_AI_KEY=test-key\nKMS_AI_MODEL=gpt-4o\nKMS_AI_ENABLED=true\nKMS_AI_TIMEOUT_SECONDS=12\n",
                encoding="utf-8",
            )
            previous = Path.cwd()
            try:
                os.chdir(root)
                with patch.dict(os.environ, {}, clear=True):
                    settings = KMSSettings.from_env()
            finally:
                os.chdir(previous)

        self.assertTrue(settings.ai_enabled)
        self.assertEqual(settings.ai_model, "gpt-4o")
        self.assertEqual(settings.ai_timeout_seconds, 12.0)
        self.assertNotIn("test-key", repr(settings))

    def test_extracts_filtered_scored_candidate_types(self) -> None:
        document = SourceDocument(
            source_document_id="doc-1",
            source_file_id="source-1",
            run_id="run-021",
            title="Governance Notes",
            content_type="text/markdown",
            text="\n".join([
                "Entity: Revenue Operations team owns the metric glossary.",
                "Process: Monthly close workflow has review and approval steps.",
                "Metric: Gross margin rate is measured as 42%.",
                "Decision: The manager approved the canonical definition.",
                "Concept: Governed source trace keeps knowledge auditable.",
                "Contradiction: Source A says active but Source B disagrees.",
                "tiny",
            ]),
            metadata={"relative_path": "governance.md"},
        )

        candidates = extract_knowledge_candidates((document,), min_relevance=0.35)

        self.assertEqual({candidate.candidate_type for candidate in candidates}, set(KnowledgeCandidateType))
        self.assertTrue(all(candidate.is_proposal for candidate in candidates))
        self.assertTrue(all(candidate.source_ref == "governance.md" for candidate in candidates))
        self.assertTrue(all(0.35 <= candidate.relevance_score <= 1.0 for candidate in candidates))
        self.assertTrue(all(0.0 <= candidate.confidence_score <= 1.0 for candidate in candidates))

    def test_candidate_drafts_are_intermediate_and_not_publishable(self) -> None:
        candidate = KnowledgeCandidate(
            candidate_id="candidate-1",
            run_id="run-021",
            source_document_id="doc-1",
            source_ref="source.md",
            candidate_type=KnowledgeCandidateType.METRIC,
            title="Revenue Metric",
            excerpt="Metric: Revenue is approved source evidence.",
            relevance_score=0.9,
            confidence_score=0.8,
            rationale="test candidate",
        )

        draft = build_candidate_drafts((candidate,))[0]

        self.assertTrue(draft.is_intermediate_artifact)
        self.assertFalse(draft.publishable)
        self.assertIn("not canonical wiki truth", draft.markdown)

        with self.assertRaises(ValidationError):
            KnowledgeCandidate(
                candidate_id="candidate-bad",
                run_id="run-021",
                source_document_id="doc-1",
                source_ref="source.md",
                candidate_type=KnowledgeCandidateType.CONCEPT,
                title="Bad",
                excerpt="Bad",
                relevance_score=1.2,
                confidence_score=0.5,
                rationale="invalid relevance",
            )

    def test_run_writes_candidate_artifacts_without_publishing_candidate_drafts(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            (source / "ops.md").write_text(
                "Metric: Revenue rate is 42%.\nContradiction: One source says active but another source disagrees.",
                encoding="utf-8",
            )
            runtime = KMSRuntime.create(KMSSettings(raw_root=root / "raw", wiki_root=root / "wiki", artifact_root=root / "artifacts"))

            result = runtime.start_run(source, run_id="run-021", auto_approve=True)

            self.assertEqual(result.run.summary_counts["knowledge_candidates"], 2)
            self.assertEqual(result.run.summary_counts["candidate_drafts"], 2)
            artifact_names = runtime.artifacts.list_run_artifacts("run-021")
            self.assertIn("knowledge-candidates.json", artifact_names)
            self.assertIn("knowledge-candidates-review.md", artifact_names)
            self.assertIn("knowledge-understanding-metadata.json", artifact_names)
            self.assertIn("candidate-drafts/draft-candidate-1.md", artifact_names)
            candidate_payload = json.loads((root / "artifacts" / "run-021" / "knowledge-candidates.json").read_text(encoding="utf-8"))
            self.assertTrue(candidate_payload["knowledge_candidates"][0]["is_proposal"])
            self.assertFalse((root / "wiki" / "candidate-drafts" / "draft-candidate-1.md").exists())

    def test_uses_configured_openai_client_without_live_network(self) -> None:
        document = SourceDocument(
            source_document_id="doc-1",
            source_file_id="source-1",
            run_id="run-022",
            title="Metric Notes",
            content_type="text/markdown",
            text="Revenue definition source text.",
            metadata={"relative_path": "metric.md"},
        )
        settings = KMSSettings(
            raw_root=Path("/tmp/raw"),
            wiki_root=Path("/tmp/wiki"),
            artifact_root=Path("/tmp/artifacts"),
            ai_enabled=True,
            ai_model="gpt-4o",
            openai_api_key="test-key",
        )
        fake_client = FakeOpenAIClient({
            "candidates": [
                {
                    "candidate_type": "metric",
                    "title": "Revenue Definition",
                    "excerpt": "Revenue is a governed metric.",
                    "relevance_score": 0.91,
                    "confidence_score": 0.82,
                    "rationale": "Source defines a metric.",
                }
            ]
        })

        result = understand_knowledge((document,), settings=settings, ai_client=fake_client)

        self.assertEqual(result.provider, "openai:gpt-4o")
        self.assertFalse(result.fallback_used)
        self.assertEqual(result.candidates[0].candidate_type, KnowledgeCandidateType.METRIC)
        self.assertIn("AI-assisted extraction using gpt-4o", result.candidates[0].rationale)
        self.assertEqual(fake_client.calls, 1)

    def test_ai_failure_falls_back_to_deterministic_candidates(self) -> None:
        document = SourceDocument(
            source_document_id="doc-1",
            source_file_id="source-1",
            run_id="run-022",
            title="Process Notes",
            content_type="text/markdown",
            text="Process: Review workflow has approval steps.",
            metadata={"relative_path": "process.md"},
        )
        settings = KMSSettings(
            raw_root=Path("/tmp/raw"),
            wiki_root=Path("/tmp/wiki"),
            artifact_root=Path("/tmp/artifacts"),
            ai_enabled=True,
            ai_model="gpt-4o",
            openai_api_key="test-key",
        )

        result = understand_knowledge((document,), settings=settings, ai_client=FailingOpenAIClient())

        self.assertEqual(result.provider, "deterministic")
        self.assertTrue(result.fallback_used)
        self.assertEqual(result.candidates[0].candidate_type, KnowledgeCandidateType.PROCESS)

    def test_invalid_ai_scores_fall_back_to_deterministic_candidates(self) -> None:
        document = SourceDocument(
            source_document_id="doc-1",
            source_file_id="source-1",
            run_id="run-022",
            title="Metric Notes",
            content_type="text/markdown",
            text="Metric: Revenue rate is 42%.",
            metadata={"relative_path": "metric.md"},
        )
        settings = KMSSettings(
            raw_root=Path("/tmp/raw"),
            wiki_root=Path("/tmp/wiki"),
            artifact_root=Path("/tmp/artifacts"),
            ai_enabled=True,
            ai_model="gpt-4o",
            openai_api_key="test-key",
        )
        fake_client = FakeOpenAIClient({
            "candidates": [
                {
                    "candidate_type": "metric",
                    "title": "Revenue Definition",
                    "excerpt": "Revenue is a governed metric.",
                    "relevance_score": 1.2,
                    "confidence_score": 0.82,
                }
            ]
        })

        result = understand_knowledge((document,), settings=settings, ai_client=fake_client)

        self.assertTrue(result.fallback_used)
        self.assertEqual(result.provider, "deterministic")
        self.assertEqual(result.candidates[0].candidate_type, KnowledgeCandidateType.METRIC)


class FakeOpenAIClient:
    def __init__(self, response: dict[str, object]) -> None:
        self.response = response
        self.calls = 0

    def create_json_response(self, *, instructions: str, user_input: str) -> dict[str, object]:
        self.calls += 1
        self.instructions = instructions
        self.user_input = user_input
        return self.response


class FailingOpenAIClient:
    def create_json_response(self, *, instructions: str, user_input: str) -> dict[str, object]:
        raise OpenAIClientError("simulated API failure")


if __name__ == "__main__":
    unittest.main()
