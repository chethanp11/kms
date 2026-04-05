import React, { useEffect, useMemo, useState } from "react";
import {
  createRun,
  getContradiction,
  getHealthFindings,
  getReviewDiff,
  getRunArtifacts,
  getRun,
  listRuns,
  submitApproval,
} from "./api";

function parseRoute(pathname, search) {
  const path = pathname.replace(/\/+$/, "") || "/";
  const query = new URLSearchParams(search);
  if (path === "/" || path === "") {
    return { name: "dashboard" };
  }
  if (path === "/runs/new") {
    return { name: "new-run" };
  }
  if (path === "/health") {
    return { name: "health" };
  }
  const parts = path.split("/").filter(Boolean);
  if (parts[0] === "runs" && parts[1]) {
    const runId = parts[1];
    if (parts.length === 2) {
      return { name: "run-detail", runId };
    }
    if (parts[2] === "source-review") {
      return { name: "source-review", runId };
    }
    if (parts[2] === "diff-review") {
      return { name: "diff-review", runId, revisionId: query.get("revision") };
    }
    if (parts[2] === "contradictions") {
      return { name: "contradictions", runId, contradictionId: query.get("contradiction") };
    }
    if (parts[2] === "approvals") {
      return { name: "approvals", runId, revisionId: query.get("revision") };
    }
  }
  return { name: "dashboard" };
}

function navigateTo(path) {
  window.history.pushState({}, "", path);
}

function useRouteState() {
  const [route, setRoute] = useState(() => parseRoute(window.location.pathname, window.location.search));

  useEffect(() => {
    const onPopState = () => setRoute(parseRoute(window.location.pathname, window.location.search));
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, []);

  const push = (path) => {
    navigateTo(path);
    setRoute(parseRoute(window.location.pathname, window.location.search));
  };

  return [route, push];
}

function useResource(loader, deps) {
  const [state, setState] = useState({ loading: true, data: null, error: null });

  useEffect(() => {
    let active = true;
    const controller = new AbortController();
    setState({ loading: true, data: null, error: null });
    loader(controller.signal)
      .then((data) => {
        if (active) {
          setState({ loading: false, data, error: null });
        }
      })
      .catch((error) => {
        if (active && error.name !== "AbortError") {
          setState({ loading: false, data: null, error });
        }
      });
    return () => {
      active = false;
      controller.abort();
    };
  }, deps); // eslint-disable-line react-hooks/exhaustive-deps

  return state;
}

function App() {
  const [route, navigate] = useRouteState();
  const header = useMemo(() => headerForRoute(route), [route]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">KMS</div>
          <div>
            <div className="brand-title">Knowledge Manager Interface</div>
            <div className="brand-subtitle">Governed maintenance control plane</div>
          </div>
        </div>

        <nav className="nav">
          <NavLink active={route.name === "dashboard"} onClick={() => navigate("/")}>
            Dashboard
          </NavLink>
          <NavLink active={route.name === "new-run"} onClick={() => navigate("/runs/new")}>
            New Run
          </NavLink>
          <NavLink active={route.name === "health"} onClick={() => navigate("/health")}>
            Maintenance Health
          </NavLink>
        </nav>

        <div className="sidebar-note">
          <p>KMI is the only sanctioned maintenance surface.</p>
          <p>/wiki remains canonical and is only written through governed backend actions.</p>
        </div>
      </aside>

      <main className="content">
        <header className="hero">
          <div>
            <p className="eyebrow">Knowledge Manager Interface</p>
            <h1>{header.title}</h1>
            <p className="hero-copy">{header.copy}</p>
          </div>
          <div className="hero-badges">
            {header.badges.map((badge) => (
              <Badge key={badge.label} tone={badge.tone}>
                {badge.label}
              </Badge>
            ))}
          </div>
        </header>

        <div className="workspace">
          {route.name === "dashboard" ? <DashboardScreen navigate={navigate} /> : null}
          {route.name === "new-run" ? <NewRunScreen navigate={navigate} /> : null}
          {route.name === "health" ? <HealthScreen navigate={navigate} /> : null}
          {route.name === "run-detail" ? <RunDetailScreen runId={route.runId} navigate={navigate} /> : null}
          {route.name === "source-review" ? (
            <SourceReviewScreen runId={route.runId} navigate={navigate} />
          ) : null}
          {route.name === "diff-review" ? (
            <DiffReviewScreen runId={route.runId} revisionId={route.revisionId} navigate={navigate} />
          ) : null}
          {route.name === "contradictions" ? (
            <ContradictionsScreen
              runId={route.runId}
              contradictionId={route.contradictionId}
              navigate={navigate}
            />
          ) : null}
          {route.name === "approvals" ? (
            <ApprovalsScreen runId={route.runId} revisionId={route.revisionId} navigate={navigate} />
          ) : null}
        </div>
      </main>
    </div>
  );
}

function DashboardScreen({ navigate }) {
  const { data, loading, error } = useResource(
    async () => {
      const [runs, health] = await Promise.all([listRuns(), getHealthFindings()]);
      return { runs, health };
    },
    []
  );

  if (loading) {
    return <Panel><LoadingState label="Loading maintenance dashboard" /></Panel>;
  }
  if (error) {
    return <ErrorState error={error} onRetry={() => window.location.reload()} />;
  }

  const runs = data.runs.items;
  const summary = data.runs.summary;
  const health = data.health;
  const latestRun = runs[0];

  return (
    <div className="stack">
      <MetricGrid
        items={[
          { label: "Runs", value: summary.run_count },
          { label: "Blocked", value: summary.blocked_runs },
          { label: "Pending approvals", value: summary.pending_approvals },
          { label: "Open contradictions", value: summary.open_contradictions },
          { label: "Lint findings", value: summary.lint_findings },
        ]}
      />

      <div className="two-column">
        <Panel title="Recent runs" eyebrow="Triage queue">
          <div className="list">
            {runs.map((run) => (
              <button
                key={run.run_id}
                className="list-row clickable"
                onClick={() => navigate(`/runs/${run.run_id}`)}
              >
                <div>
                  <div className="row-title">{run.run_id}</div>
                  <div className="row-subtitle">
                    {run.source_path} • {run.domain_hint || "No domain hint"}
                  </div>
                </div>
                <div className="row-meta">
                  <Badge tone={badgeToneForRun(run.status)}>{run.status}</Badge>
                  <span>{run.current_stage || "created"}</span>
                </div>
              </button>
            ))}
          </div>
        </Panel>

        <Panel title="Maintenance Health" eyebrow="Backend findings">
          <div className="health-list">
            <HealthStat label="Lint findings" value={health.summary.lint_finding_count} tone="warn" />
            <HealthStat label="Contradictions" value={health.summary.contradiction_count} tone="warn" />
            <HealthStat label="Open questions" value={health.summary.open_question_count} tone="warn" />
            <HealthStat label="Stale pages" value={health.summary.stale_page_count} tone="danger" />
          </div>
          <div className="inline-actions">
            <Button onClick={() => navigate("/health")}>Open maintenance health</Button>
            {latestRun ? (
              <Button variant="ghost" onClick={() => navigate(`/runs/${latestRun.run_id}`)}>
                Open latest run
              </Button>
            ) : null}
          </div>
        </Panel>
      </div>

      <div className="three-column">
        <Panel title="Pending approvals" eyebrow="Finalization queue">
          {runs.filter((run) => run.pending_approvals > 0).length ? (
            runs
              .filter((run) => run.pending_approvals > 0)
              .map((run) => (
                <div key={run.run_id} className="queue-item">
                  <div>
                    <div className="row-title">{run.run_id}</div>
                    <div className="row-subtitle">{run.pending_approvals} staged revisions</div>
                  </div>
                  <Button variant="ghost" onClick={() => navigate(`/runs/${run.run_id}/approvals`)}>
                    Review
                  </Button>
                </div>
              ))
          ) : (
            <EmptyState title="No pending approvals" description="All queued revisions are either finalized or blocked." />
          )}
        </Panel>

        <Panel title="Contradictions" eyebrow="Governance queue">
          {runs.filter((run) => run.contradiction_count > 0).length ? (
            runs
              .filter((run) => run.contradiction_count > 0)
              .map((run) => (
                <div key={run.run_id} className="queue-item">
                  <div>
                    <div className="row-title">{run.run_id}</div>
                    <div className="row-subtitle">{run.contradiction_count} contradiction record(s)</div>
                  </div>
                  <Button variant="ghost" onClick={() => navigate(`/runs/${run.run_id}/contradictions`)}>
                    Review
                  </Button>
                </div>
              ))
          ) : (
            <EmptyState title="No contradiction queue" description="There are no active conflict records." />
          )}
        </Panel>

        <Panel title="Latest finalized updates" eyebrow="Publish trail">
          {runs.filter((run) => run.status === "completed").length ? (
            runs
              .filter((run) => run.status === "completed")
              .slice(0, 3)
              .map((run) => (
                <div key={run.run_id} className="queue-item">
                  <div>
                    <div className="row-title">{run.run_id}</div>
                    <div className="row-subtitle">{formatDate(run.completed_at)}</div>
                  </div>
                  <Badge tone="success">published</Badge>
                </div>
              ))
          ) : (
            <EmptyState title="No finalized runs" description="Publish activity will appear here after approval and finalization." />
          )}
        </Panel>
      </div>
    </div>
  );
}

function NewRunScreen({ navigate }) {
  const [payload, setPayload] = useState({
    source_path: "",
    initiated_by: "knowledge-manager",
    domain_hint: "",
    run_notes: "",
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  async function onSubmit(event) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const result = await createRun(payload);
      navigate(`/runs/${result.run.run_id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Panel title="Start a governed run" eyebrow="Intake">
      <form className="form-grid" onSubmit={onSubmit}>
        <Field label="Local source path" hint="Backend validates access before orchestration begins.">
          <input
            value={payload.source_path}
            onChange={(event) => setPayload({ ...payload, source_path: event.target.value })}
            placeholder="/Users/…/source-folder"
            required
          />
        </Field>
        <Field label="Initiated by">
          <input
            value={payload.initiated_by}
            onChange={(event) => setPayload({ ...payload, initiated_by: event.target.value })}
          />
        </Field>
        <Field label="Domain hint">
          <input
            value={payload.domain_hint}
            onChange={(event) => setPayload({ ...payload, domain_hint: event.target.value })}
            placeholder="customer-revenue"
          />
        </Field>
        <Field label="Run notes">
          <textarea
            rows="4"
            value={payload.run_notes}
            onChange={(event) => setPayload({ ...payload, run_notes: event.target.value })}
            placeholder="What should the Knowledge Manager expect from this run?"
          />
        </Field>

        {error ? <InlineAlert tone="danger">{error}</InlineAlert> : null}

        <div className="inline-actions">
          <Button type="submit" disabled={submitting}>
            {submitting ? "Launching…" : "Launch governed run"}
          </Button>
          <Button variant="ghost" type="button" onClick={() => navigate("/")}>
            Back to dashboard
          </Button>
        </div>
      </form>
    </Panel>
  );
}

function RunDetailScreen({ runId, navigate }) {
  const { data, loading, error } = useResource(() => getRun(runId), [runId]);

  if (loading) {
    return <Panel><LoadingState label="Loading run detail" /></Panel>;
  }
  if (error) {
    return <ErrorState error={error} onRetry={() => navigate(`/runs/${runId}`)} />;
  }

  const run = data.run;
  const stages = stageTimeline(data.run_events);
  const topRevisions = data.revisions.slice().sort((a, b) => (a.created_at < b.created_at ? 1 : -1));

  return (
    <div className="stack">
      <MetricGrid
        items={[
          { label: "Source files", value: data.source_files.length },
          { label: "Source notes", value: data.source_notes.length },
          { label: "Revisions", value: data.revisions.length },
          { label: "Approvals", value: data.approvals.length },
          { label: "Contradictions", value: data.contradictions.length },
          { label: "Lint findings", value: data.lint_findings.length },
        ]}
      />

      <Panel title="Run timeline" eyebrow={run.run_id}>
        <div className="timeline">
          {stages.map((stage) => (
            <div key={`${stage.stage}-${stage.message}`} className="timeline-item">
              <div className="timeline-marker" data-tone={stage.tone} />
              <div className="timeline-content">
                <div className="timeline-head">
                  <span className="timeline-stage">{stage.stage}</span>
                  <Badge tone={stage.tone}>{stage.status}</Badge>
                </div>
                <div className="timeline-message">{stage.message}</div>
              </div>
            </div>
          ))}
        </div>
      </Panel>

      <div className="two-column">
        <Panel title="Governance state" eyebrow="Backend summary">
          <div className="stack-tight">
            <InfoRow label="Status" value={run.status} />
            <InfoRow label="Current stage" value={run.current_stage || "created"} />
            <InfoRow label="Source path" value={run.source_path} />
            <InfoRow label="Domain hint" value={run.domain_hint || "—"} />
            <InfoRow label="Created by" value={run.created_by || "—"} />
            <InfoRow label="Completed at" value={formatDate(run.completed_at)} />
          </div>
          {run.status === "blocked" ? (
            <InlineAlert tone="danger">Run blocked at {run.current_stage}. Review the policy output and approval queue.</InlineAlert>
          ) : null}
          <div className="inline-actions">
            <Button onClick={() => navigate(`/runs/${runId}/source-review`)}>Source review</Button>
            <Button variant="ghost" onClick={() => navigate(`/runs/${runId}/diff-review`)}>
              Diff review
            </Button>
          </div>
        </Panel>

        <Panel title="Revision queue" eyebrow="Staged work">
          {topRevisions.length ? (
            <div className="list">
              {topRevisions.map((revision) => (
                <button
                  key={revision.revision_id}
                  className="list-row clickable"
                  onClick={() => navigate(`/runs/${runId}/diff-review?revision=${revision.revision_id}`)}
                >
                  <div>
                    <div className="row-title">{revision.draft_title || revision.revision_id}</div>
                    <div className="row-subtitle">
                      {revision.draft_page_type} • {revision.change_type} • {revision.draft_path}
                    </div>
                  </div>
                  <div className="row-meta">
                    <Badge tone={badgeToneForRevision(revision.status)}>{revision.status}</Badge>
                    <span>{formatDate(revision.created_at)}</span>
                  </div>
                </button>
              ))}
            </div>
          ) : (
            <EmptyState title="No revisions" description="This run has not staged any changes yet." />
          )}
        </Panel>
      </div>

      <div className="three-column">
        <QuickLinkCard
          title="Source review"
          body="Inspect discovered files, parse outcomes, and source notes."
          onClick={() => navigate(`/runs/${runId}/source-review`)}
        />
        <QuickLinkCard
          title="Contradictions"
          body="Review conflicts and open questions surfaced by governance."
          onClick={() => navigate(`/runs/${runId}/contradictions`)}
        />
        <QuickLinkCard
          title="Approvals"
          body="Review blockers and finalize eligible revisions."
          onClick={() => navigate(`/runs/${runId}/approvals`)}
        />
      </div>
    </div>
  );
}

function SourceReviewScreen({ runId, navigate }) {
  const { data, loading, error } = useResource(() => getRunArtifacts(runId), [runId]);

  if (loading) {
    return <Panel><LoadingState label="Loading source review" /></Panel>;
  }
  if (error) {
    return <ErrorState error={error} onRetry={() => navigate(`/runs/${runId}/source-review`)} />;
  }

  return (
    <div className="stack">
      <MetricGrid
        items={[
          { label: "Source files", value: data.source_files.length },
          { label: "Parsed documents", value: data.source_documents.length },
          { label: "Source notes", value: data.source_notes.length },
          { label: "Artifacts", value: data.artifacts.length },
        ]}
      />

      <div className="two-column">
        <Panel title="Discovered files" eyebrow="Intake evidence">
          <div className="list">
            {data.source_files.map((file) => (
              <div key={file.source_file_id} className="list-row">
                <div>
                  <div className="row-title">{file.path}</div>
                  <div className="row-subtitle">
                    {file.file_type} • {file.parse_status} • {file.hash.slice(0, 10)}
                  </div>
                </div>
                <Badge tone={file.parse_status === "parsed" ? "success" : file.parse_status === "unsupported" ? "warn" : "neutral"}>
                  {file.parse_status}
                </Badge>
              </div>
            ))}
          </div>
        </Panel>

        <Panel title="Source notes" eyebrow="Traceable extraction">
          <div className="list">
            {data.source_notes.map((note) => (
              <div key={note.source_note_id} className="note-card">
                <div className="row-title">{note.title}</div>
                <div className="row-subtitle">{note.summary}</div>
                <div className="chip-row">
                  {note.source_refs.map((ref) => (
                    <span key={ref} className="chip">
                      {ref}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </Panel>
      </div>

      <Panel title="Run artifacts" eyebrow="Workflow outputs">
        <div className="artifact-grid">
          <InfoRow label="Revisions staged" value={data.revisions.length} />
          <InfoRow label="Approvals recorded" value={data.approvals.length} />
          <InfoRow label="Contradictions" value={data.contradictions.length} />
          <InfoRow label="QA reports" value={data.qa_reports.length} />
          <InfoRow label="Lint findings" value={data.lint_findings.length} />
        </div>
      </Panel>

      <Panel title="Intake artifacts" eyebrow="Audit trail">
        <div className="list">
          {data.artifacts.map((artifact) => (
            <div key={artifact.artifact_id} className="list-row">
              <div>
                <div className="row-title">{artifact.artifact_type}</div>
                <div className="row-subtitle">{artifact.summary}</div>
              </div>
              <div className="row-meta">
                <Badge tone={artifact.status === "created" ? "neutral" : "warn"}>{artifact.status}</Badge>
                <span>{artifact.path || "—"}</span>
              </div>
            </div>
          ))}
        </div>
      </Panel>
    </div>
  );
}

function DiffReviewScreen({ runId, revisionId, navigate }) {
  const { data: runData, loading, error } = useResource(() => getRun(runId), [runId]);
  const selectedRevision = revisionId || (runData?.revisions?.[0]?.revision_id ?? null);
  const diffState = useResource(
    () => (selectedRevision ? getReviewDiff(selectedRevision) : Promise.resolve(null)),
    [selectedRevision]
  );

  if (loading) {
    return <Panel><LoadingState label="Loading diff review" /></Panel>;
  }
  if (error) {
    return <ErrorState error={error} onRetry={() => navigate(`/runs/${runId}/diff-review`)} />;
  }

  const revisions = runData.revisions;

  return (
    <div className="stack">
      <Panel title="Proposed changes" eyebrow="Diff review">
        <div className="form-grid compact">
          <Field label="Revision">
            <select
              value={selectedRevision || ""}
              onChange={(event) => navigate(`/runs/${runId}/diff-review?revision=${event.target.value}`)}
            >
              {revisions.map((revision) => (
                <option key={revision.revision_id} value={revision.revision_id}>
                  {revision.draft_title || revision.revision_id} ({revision.status})
                </option>
              ))}
            </select>
          </Field>
        </div>
      </Panel>

      {diffState.loading ? <Panel><LoadingState label="Loading review diff" /></Panel> : null}
      {diffState.error ? <ErrorState error={diffState.error} onRetry={() => navigate(`/runs/${runId}/diff-review`)} /> : null}
      {diffState.data ? (
        <>
          <MetricGrid
            items={[
              { label: "Source traces", value: diffState.data.source_trace_ids.length },
              { label: "Approvals", value: diffState.data.approvals.length },
              { label: "Contradictions", value: diffState.data.contradictions.length },
            ]}
          />
          <div className="two-column">
            <Panel title="Rule & approval state" eyebrow="Governance">
              <div className="stack-tight">
                <InfoRow label="Revision status" value={diffState.data.revision.status} />
                <InfoRow label="Page status" value={diffState.data.page.status} />
                <InfoRow label="Source traces" value={diffState.data.source_trace_ids.length} />
                <InfoRow label="Latest QA summary" value={diffState.data.rule_findings?.summary || "—"} />
              </div>
              <div className="chip-row">
                {diffState.data.source_trace_ids.map((trace) => (
                  <span key={trace} className="chip">
                    {trace}
                  </span>
                ))}
              </div>
              <div className="stack-tight">
                {diffState.data.rule_findings?.rule_ids?.length ? (
                  diffState.data.rule_findings.rule_ids.map((ruleId) => (
                    <div key={ruleId} className="rule-line">
                      <Badge tone="warn">{ruleId}</Badge>
                    </div>
                  ))
                ) : (
                  <InlineAlert tone="success">No rule violations recorded for this revision.</InlineAlert>
                )}
              </div>
            </Panel>

            <Panel title="Before / after" eyebrow="Structured markdown">
              <DiffView before={diffState.data.before_markdown} after={diffState.data.after_markdown} diff={diffState.data.diff} />
            </Panel>
          </div>
        </>
      ) : null}
    </div>
  );
}

function ContradictionsScreen({ runId, contradictionId, navigate }) {
  const { data, loading, error } = useResource(() => getRun(runId), [runId]);
  const selectedContradictionId = contradictionId || data?.contradictions?.[0]?.contradiction_id || null;
  const contradictionState = useResource(
    () => (selectedContradictionId ? getContradiction(selectedContradictionId) : Promise.resolve(null)),
    [selectedContradictionId]
  );

  if (loading) {
    return <Panel><LoadingState label="Loading contradictions" /></Panel>;
  }
  if (error) {
    return <ErrorState error={error} onRetry={() => navigate(`/runs/${runId}/contradictions`)} />;
  }

  return (
    <div className="stack">
      <MetricGrid
        items={[
          { label: "Contradictions", value: data.contradictions.length },
          { label: "Open questions", value: data.contradictions.filter((item) => item.status !== "resolved").length },
          { label: "Blocked revisions", value: data.revisions.filter((item) => item.status === "review_required").length },
        ]}
      />

      <Panel title="Contradictions / open questions" eyebrow="Conflict management">
        {data.contradictions.length ? (
          <div className="list">
            {data.contradictions.map((item) => (
              <div
                key={item.contradiction_id}
                className={`note-card clickable ${item.contradiction_id === selectedContradictionId ? "selected" : ""}`}
                onClick={() => navigate(`/runs/${runId}/contradictions?contradiction=${item.contradiction_id}`)}
                onKeyDown={(event) => {
                  if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    navigate(`/runs/${runId}/contradictions?contradiction=${item.contradiction_id}`);
                  }
                }}
                role="button"
                tabIndex={0}
              >
                <div className="note-head">
                  <div>
                    <div className="row-title">{item.contradiction_id}</div>
                    <div className="row-subtitle">
                      Revision {item.revision_id || "—"} • Page {item.page_id || "—"}
                    </div>
                  </div>
                  <Badge tone={badgeToneForContradiction(item.severity)}>{item.severity}</Badge>
                </div>
                <p className="note-summary">{item.conflicting_claims.join(" • ")}</p>
                <div className="chip-row">
                  {item.source_refs.map((ref) => (
                    <span key={ref} className="chip">
                      {ref}
                    </span>
                  ))}
                </div>
                <div className="inline-actions">
                  <Button
                    variant="ghost"
                    onClick={(event) => {
                      event.stopPropagation();
                      navigate(`/runs/${runId}/diff-review?revision=${item.revision_id}`);
                    }}
                  >
                    Inspect revision
                  </Button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <EmptyState title="No contradictions" description="This run has not produced any conflict records." />
        )}
      </Panel>

      {selectedContradictionId ? (
        <Panel title="Selected contradiction" eyebrow="Governed detail">
          {contradictionState.loading ? <LoadingState label="Loading contradiction detail" /> : null}
          {contradictionState.data ? (
            <div className="stack-tight">
              <InfoRow label="Status" value={contradictionState.data.contradiction.status} />
              <InfoRow label="Severity" value={contradictionState.data.contradiction.severity} />
              <InfoRow label="Run" value={contradictionState.data.run?.run_id || "—"} />
              <InfoRow label="Revision" value={contradictionState.data.revision?.revision_id || "—"} />
              <div className="chip-row">
                {contradictionState.data.contradiction.source_refs.map((ref) => (
                  <span key={ref} className="chip">
                    {ref}
                  </span>
                ))}
              </div>
              <Button
                variant="ghost"
                onClick={() =>
                  contradictionState.data.revision
                    ? navigate(`/runs/${runId}/diff-review?revision=${contradictionState.data.revision.revision_id}`)
                    : null
                }
              >
                Open linked diff
              </Button>
            </div>
          ) : null}
        </Panel>
      ) : null}
    </div>
  );
}

function ApprovalsScreen({ runId, revisionId, navigate }) {
  const { data, loading, error } = useResource(() => getRun(runId), [runId]);
  const [actionError, setActionError] = useState(null);
  const selectedRevision = revisionId || (data?.revisions?.find((item) => item.status !== "finalized")?.revision_id ?? data?.revisions?.[0]?.revision_id);
  const diffState = useResource(
    () => (selectedRevision ? getReviewDiff(selectedRevision) : Promise.resolve(null)),
    [selectedRevision]
  );

  async function actOnRevision(revision, decision, finalize) {
    setActionError(null);
    try {
      await submitApproval(revision.revision_id, {
        decision,
        reviewer_id: "knowledge-manager",
        policy_version: "governance.v1",
        reason: decision === "approved" ? "Approved through KMI." : "Managed through KMI.",
        finalize,
      });
      navigate(`/runs/${runId}/approvals?revision=${revision.revision_id}`);
      window.location.reload();
    } catch (err) {
      setActionError(err.message);
    }
  }

  if (loading) {
    return <Panel><LoadingState label="Loading approvals" /></Panel>;
  }
  if (error) {
    return <ErrorState error={error} onRetry={() => navigate(`/runs/${runId}/approvals`)} />;
  }

  const revisions = data.revisions.slice().sort((a, b) => (a.created_at < b.created_at ? 1 : -1));

  return (
    <div className="stack">
      <MetricGrid
        items={[
          { label: "Staged revisions", value: revisions.filter((item) => item.status !== "finalized").length },
          { label: "Pending approvals", value: revisions.filter((item) => item.status === "review_required" || item.status === "staged").length },
          { label: "Finalized", value: revisions.filter((item) => item.status === "finalized").length },
        ]}
      />

      <Panel title="Approval queue" eyebrow="Final governed checkpoint">
        {actionError ? <InlineAlert tone="danger">{actionError}</InlineAlert> : null}
        <div className="approval-stack">
          {revisions.map((revision) => (
            <div key={revision.revision_id} className="approval-card">
              <div className="approval-head">
                <div>
                  <div className="row-title">{revision.draft_title || revision.revision_id}</div>
                  <div className="row-subtitle">
                    {revision.draft_path} • {revision.change_type} • {formatDate(revision.created_at)}
                  </div>
                </div>
                <Badge tone={badgeToneForRevision(revision.status)}>{revision.status}</Badge>
              </div>
              <div className="approval-grid">
                <InfoRow label="Source trace count" value={revision.source_trace_ids.length} />
                <InfoRow label="Finalized at" value={formatDate(revision.finalized_at)} />
              </div>
              <div className="inline-actions">
                <Button onClick={() => actOnRevision(revision, "approved", true)}>Approve & finalize</Button>
                <Button variant="ghost" onClick={() => actOnRevision(revision, "rejected", false)}>
                  Reject
                </Button>
                <Button variant="ghost" onClick={() => actOnRevision(revision, "deferred", false)}>
                  Defer
                </Button>
                <Button variant="ghost" onClick={() => actOnRevision(revision, "escalated", false)}>
                  Escalate
                </Button>
              </div>
            </div>
          ))}
        </div>
      </Panel>

      {selectedRevision ? (
        <Panel title="Selected revision" eyebrow="Finalization detail">
          {diffState.loading ? <LoadingState label="Loading revision detail" /> : null}
          {diffState.data ? (
            <div className="stack-tight">
              <InfoRow label="QA summary" value={diffState.data.rule_findings?.summary || "—"} />
              <InfoRow label="QA status" value={diffState.data.rule_findings?.status || "—"} />
              <InfoRow label="Contradictions" value={diffState.data.contradictions.length} />
              <InfoRow label="Current markdown preview" value="Available in diff review" />
              <div className="rule-stack">
                {diffState.data.rule_findings?.rule_ids?.length ? (
                  diffState.data.rule_findings.rule_ids.map((ruleId) => (
                    <Badge key={ruleId} tone="warn">
                      {ruleId}
                    </Badge>
                  ))
                ) : (
                  <InlineAlert tone="success">No approval blockers recorded for this revision.</InlineAlert>
                )}
                {diffState.data.contradictions.length ? (
                  <InlineAlert tone="warn">
                    {diffState.data.contradictions.length} contradiction record(s) remain linked to this revision.
                  </InlineAlert>
                ) : null}
              </div>
              <div className="inline-actions">
                <Button variant="ghost" onClick={() => navigate(`/runs/${runId}/diff-review?revision=${selectedRevision}`)}>
                  Open diff review
                </Button>
              </div>
            </div>
          ) : null}
        </Panel>
      ) : null}
    </div>
  );
}

function HealthScreen({ navigate }) {
  const { data, loading, error } = useResource(() => getHealthFindings(), []);

  if (loading) {
    return <Panel><LoadingState label="Loading maintenance health" /></Panel>;
  }
  if (error) {
    return <ErrorState error={error} onRetry={() => navigate("/health")} />;
  }

  return (
    <div className="stack">
      <MetricGrid
        items={[
          { label: "Lint findings", value: data.summary.lint_finding_count },
          { label: "Contradictions", value: data.summary.contradiction_count },
          { label: "Open questions", value: data.summary.open_question_count },
          { label: "Stale pages", value: data.summary.stale_page_count },
        ]}
      />

      <div className="two-column">
        <Panel title="Lint findings" eyebrow="Post-publish hygiene">
          {data.items.lint_findings.length ? (
            <div className="list">
              {data.items.lint_findings.map((finding) => (
                <div key={finding.lint_finding_id} className="note-card">
                  <div className="note-head">
                    <div>
                      <div className="row-title">{finding.code}</div>
                      <div className="row-subtitle">{finding.message}</div>
                    </div>
                    <Badge tone={badgeToneForSeverity(finding.severity)}>{finding.severity}</Badge>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="No lint findings" description="Post-publish checks have not recorded issues." />
          )}
        </Panel>

        <Panel title="Open questions and stale pages" eyebrow="Maintenance queue">
          <div className="stack-tight">
            {data.items.open_questions.length ? (
              <>
                <h3 className="subheading">Open questions</h3>
                {data.items.open_questions.map((question) => (
                  <div key={question.contradiction_id} className="queue-item">
                    <div>
                      <div className="row-title">{question.contradiction_id}</div>
                      <div className="row-subtitle">{question.conflicting_claims.join(" • ")}</div>
                    </div>
                    <Badge tone={badgeToneForSeverity(question.severity)}>{question.status}</Badge>
                  </div>
                ))}
              </>
            ) : (
              <EmptyState title="No open questions" description="There are no unresolved contradiction records." />
            )}

            {data.items.stale_pages.length ? (
              <>
                <h3 className="subheading">Stale pages</h3>
                {data.items.stale_pages.map((page) => (
                  <div key={page.page_id} className="queue-item">
                    <div>
                      <div className="row-title">{page.title}</div>
                      <div className="row-subtitle">{page.slug}</div>
                    </div>
                    <Badge tone="warn">{page.freshness_status}</Badge>
                  </div>
                ))}
              </>
            ) : (
              <EmptyState title="No stale pages" description="All pages are marked current." />
            )}
          </div>
        </Panel>
      </div>
    </div>
  );
}

function Panel({ title, eyebrow, children }) {
  return (
    <section className="panel">
      {eyebrow ? <div className="panel-eyebrow">{eyebrow}</div> : null}
      {title ? <h2 className="panel-title">{title}</h2> : null}
      <div className="panel-body">{children}</div>
    </section>
  );
}

function Field({ label, hint, children }) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>
      {hint ? <span className="field-hint">{hint}</span> : null}
      {children}
    </label>
  );
}

function MetricGrid({ items }) {
  return (
    <div className="metric-grid">
      {items.map((item) => (
        <div key={item.label} className="metric-card">
          <div className="metric-label">{item.label}</div>
          <div className="metric-value">{item.value}</div>
        </div>
      ))}
    </div>
  );
}

function HealthStat({ label, value, tone = "neutral" }) {
  return (
    <div className="queue-item">
      <div className="row-title">{label}</div>
      <div className="row-meta">
        <Badge tone={tone}>{String(value)}</Badge>
      </div>
    </div>
  );
}

function InfoRow({ label, value }) {
  return (
    <div className="info-row">
      <span className="info-label">{label}</span>
      <span className="info-value">{String(value ?? "—")}</span>
    </div>
  );
}

function Badge({ tone = "neutral", children }) {
  return <span className={`badge badge-${tone}`}>{children}</span>;
}

function Button({ children, variant = "primary", ...props }) {
  return (
    <button className={`button button-${variant}`} {...props}>
      {children}
    </button>
  );
}

function NavLink({ children, active, ...props }) {
  return (
    <button className={`nav-link ${active ? "active" : ""}`} {...props}>
      {children}
    </button>
  );
}

function EmptyState({ title, description }) {
  return (
    <div className="empty-state">
      <div className="row-title">{title}</div>
      <div className="row-subtitle">{description}</div>
    </div>
  );
}

function LoadingState({ label }) {
  return <div className="loading-state">{label}</div>;
}

function ErrorState({ error, onRetry }) {
  return (
    <div className="error-state">
      <div className="row-title">Backend request failed</div>
      <div className="row-subtitle">{error?.message || String(error)}</div>
      {onRetry ? (
        <div className="inline-actions">
          <Button onClick={onRetry}>Retry</Button>
        </div>
      ) : null}
    </div>
  );
}

function InlineAlert({ tone = "neutral", children }) {
  return <div className={`inline-alert inline-alert-${tone}`}>{children}</div>;
}

function QuickLinkCard({ title, body, onClick }) {
  return (
    <button className="quick-link" onClick={onClick}>
      <div className="row-title">{title}</div>
      <div className="row-subtitle">{body}</div>
    </button>
  );
}

function DiffView({ before, after, diff }) {
  return (
    <div className="diff-view">
      <pre className="diff-block">{diff || "No diff available."}</pre>
      <div className="diff-columns">
        <div>
          <div className="diff-label">Before</div>
          <pre className="diff-block compact">{before || "Empty draft"}</pre>
        </div>
        <div>
          <div className="diff-label">After</div>
          <pre className="diff-block compact">{after || "Empty draft"}</pre>
        </div>
      </div>
    </div>
  );
}

function stageTimeline(events) {
  return events.map((event) => ({
    stage: event.stage,
    status: event.status,
    message: event.message,
    tone:
      event.kind === "run_blocked" || event.kind === "stage_blocked"
        ? "danger"
        : event.status === "blocked"
          ? "danger"
          : event.status === "completed"
            ? "success"
            : "neutral",
  }));
}

function badgeToneForRun(status) {
  if (status === "blocked" || status === "failed") {
    return "danger";
  }
  if (status === "completed" || status === "completed_with_warnings") {
    return "success";
  }
  return "warn";
}

function badgeToneForRevision(status) {
  if (status === "finalized" || status === "approved") {
    return "success";
  }
  if (status === "rejected") {
    return "danger";
  }
  if (status === "review_required" || status === "staged") {
    return "warn";
  }
  return "neutral";
}

function badgeToneForContradiction(severity) {
  if (severity === "error") return "danger";
  if (severity === "warning") return "warn";
  return "neutral";
}

function badgeToneForSeverity(severity) {
  if (severity === "error") return "danger";
  if (severity === "warning") return "warn";
  return "neutral";
}

function formatDate(value) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

function headerForRoute(route) {
  switch (route.name) {
    case "new-run":
      return {
        title: "Start a governed run",
        copy: "Validate the path, launch orchestration, and keep every maintenance action inside the backend workflow.",
        badges: [{ label: "Intake", tone: "info" }, { label: "Governed", tone: "success" }],
      };
    case "run-detail":
      return {
        title: "Run detail",
        copy: "Inspect stage progress, artifacts, governance blockers, and publish eligibility without leaving the controlled maintenance surface.",
        badges: [{ label: "Workflow", tone: "info" }, { label: "Stage-aware", tone: "success" }],
      };
    case "source-review":
      return {
        title: "Source review",
        copy: "Review discovered files, parse quality, and source notes before revisions move deeper into the governed pipeline.",
        badges: [{ label: "Sources", tone: "info" }, { label: "Traceable", tone: "success" }],
      };
    case "diff-review":
      return {
        title: "Diff review",
        copy: "Inspect structured markdown deltas, inline traces, and validation findings before approval or finalization.",
        badges: [{ label: "Diffs", tone: "info" }, { label: "Policy-aware", tone: "success" }],
      };
    case "contradictions":
      return {
        title: "Contradictions and open questions",
        copy: "Keep conflicts explicit until they are resolved or intentionally escalated through policy.",
        badges: [{ label: "Conflict", tone: "warn" }, { label: "Escalation", tone: "danger" }],
      };
    case "approvals":
      return {
        title: "Approvals and finalization",
        copy: "Finalize only eligible revisions and make blockers visible before any write to /wiki occurs.",
        badges: [{ label: "Final gate", tone: "warn" }, { label: "/wiki", tone: "success" }],
      };
    case "health":
      return {
        title: "Maintenance health",
        copy: "Track lint findings, stale content, and unresolved maintenance issues as first-class operational work.",
        badges: [{ label: "Health", tone: "warn" }, { label: "Hygiene", tone: "info" }],
      };
    default:
      return {
        title: "Dashboard",
        copy: "See runs, reviews, contradictions, approvals, and health issues in one governed control view.",
        badges: [{ label: "Governed", tone: "success" }, { label: "Maintenance", tone: "info" }],
      };
  }
}

export { headerForRoute, parseRoute };
export default App;
