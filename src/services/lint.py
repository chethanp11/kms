"""Post-publish lint checks for finalized wiki pages."""

from __future__ import annotations

from src.contracts import LintFinding, LintSeverity, LintStatus
from src.storage.wiki_store import WikiStore


def lint_wiki(wiki_store: WikiStore) -> tuple[LintFinding, ...]:
    findings: list[LintFinding] = []
    for index, path in enumerate(wiki_store.list_pages(), start=1):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(wiki_store.root).as_posix()
        if "## Source Trace" not in text:
            findings.append(LintFinding(f"lint-{index}", LintSeverity.ERROR, LintStatus.OPEN, "Published page lacks Source Trace section.", path=rel, rule_id="kms.source_trace.required"))
    return tuple(findings)


__all__ = ["lint_wiki"]
