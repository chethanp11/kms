import { afterEach, describe, expect, it, vi } from "vitest";
import {
  createRun,
  getContradiction,
  getHealthFindings,
  getReviewDiff,
  getRun,
  getRunArtifacts,
  listRuns,
  submitApproval,
} from "./api";

function stubJsonResponse(payload, ok = true) {
  return {
    ok,
    statusText: ok ? "OK" : "Bad Request",
    headers: {
      get(name) {
        return name.toLowerCase() === "content-type" ? "application/json" : null;
      },
    },
    json: async () => payload,
    text: async () => JSON.stringify(payload),
  };
}

describe("KMI API", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("uses backend contracts for run and review actions", async () => {
    const payloads = [
      stubJsonResponse({
        items: [
          {
            run_id: "run_001",
            source_path: "/Users/chethan/Documents",
            created_by: "knowledge-manager",
            domain_hint: "customer-revenue",
            status: "in_progress",
            current_stage: "source_intake",
          },
        ],
        summary: { run_count: 1, blocked_runs: 0, pending_approvals: 0, open_contradictions: 0, lint_findings: 0 },
      }),
      stubJsonResponse({
        run: {
          run_id: "run_001",
          source_path: "/Users/chethan/Documents",
          created_by: "knowledge-manager",
          domain_hint: "customer-revenue",
          status: "in_progress",
          current_stage: "source_intake",
        },
        run_events: [],
        source_files: [],
        source_documents: [],
        source_notes: [],
        artifacts: [],
        revisions: [],
        approvals: [],
        contradictions: [],
        qa_reports: [],
        lint_findings: [],
      }),
      stubJsonResponse({
        run: {
          run_id: "run_002",
          source_path: "/Users/chethan/Documents",
          created_by: "knowledge-manager",
          domain_hint: "customer-revenue",
          status: "created",
          current_stage: "created",
        },
        run_events: [],
        source_files: [],
        source_documents: [],
        source_notes: [],
        artifacts: [],
        revisions: [],
        approvals: [],
        contradictions: [],
        qa_reports: [],
        lint_findings: [],
      }),
      stubJsonResponse({
        run: {
          run_id: "run_002",
          source_path: "/Users/chethan/Documents",
          created_by: "knowledge-manager",
          domain_hint: "customer-revenue",
          status: "created",
          current_stage: "created",
        },
        run_events: [],
        source_files: [],
        source_documents: [],
        source_notes: [],
        artifacts: [],
        revisions: [],
        approvals: [],
        contradictions: [],
        qa_reports: [],
        lint_findings: [],
      }),
      stubJsonResponse({
        revision: { revision_id: "rev_001", run_id: "run_001", status: "review_required" },
        page: { page_id: "page_001", status: "draft" },
        current_markdown: "# Draft",
        before_markdown: "",
        after_markdown: "# Draft",
        diff: "",
        source_trace_ids: [],
        rule_findings: null,
        approvals: [],
        contradictions: [],
      }),
      stubJsonResponse({
        contradiction: { contradiction_id: "contr_001", status: "open" },
        run: { run_id: "run_001" },
        revision: { revision_id: "rev_001" },
      }),
      stubJsonResponse({
        approval: { approval_id: "approval_001", revision_id: "rev_001", decision: "approved" },
        governance: { decision: "approved", status: "passed" },
        finalized: true,
        revision: { revision_id: "rev_001", status: "finalized" },
      }),
      stubJsonResponse({
        generated_at: "2026-04-05T00:00:00Z",
        items: { lint_findings: [], contradictions: [], open_questions: [], stale_pages: [] },
        summary: { lint_finding_count: 0, contradiction_count: 0, open_question_count: 0, stale_page_count: 0 },
      }),
    ];

    const fetchMock = vi.fn(async () => payloads.shift() || stubJsonResponse({}));
    vi.stubGlobal("fetch", fetchMock);

    const runs = await listRuns();
    expect(runs.items[0].source_path).toBe("/Users/chethan/Documents");

    const created = await createRun({
      source_path: "/Users/chethan/Documents",
      initiated_by: "knowledge-manager",
      domain_hint: "customer-revenue",
      run_notes: "Governed run.",
    });
    expect(created.run.run_id).toBe("run_001");

    const run = await getRun("run_002");
    expect(run.run.run_id).toBe("run_002");

    const artifacts = await getRunArtifacts("run_002");
    expect(artifacts.run.run_id).toBe("run_002");

    const diff = await getReviewDiff("rev_001");
    expect(diff.revision.revision_id).toBe("rev_001");

    const contradiction = await getContradiction("contr_001");
    expect(contradiction.contradiction.contradiction_id).toBe("contr_001");

    const approval = await submitApproval("rev_001", {
      decision: "approved",
      reviewer_id: "knowledge-manager",
      policy_version: "governance.v1",
      finalize: true,
    });
    expect(approval.finalized).toBe(true);

    const health = await getHealthFindings();
    expect(health.summary.lint_finding_count).toBe(0);
    expect(fetchMock).toHaveBeenCalled();
  });

  it("surfaces a clear error when the backend is unavailable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));

    await expect(listRuns()).rejects.toThrow("KMI backend unavailable");
  });
});
