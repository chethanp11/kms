CREATE TABLE IF NOT EXISTS runs (
  run_id TEXT PRIMARY KEY,
  status TEXT NOT NULL,
  source_path TEXT NOT NULL,
  domain_hint TEXT,
  run_notes TEXT,
  created_at TEXT NOT NULL,
  started_at TEXT,
  completed_at TEXT,
  created_by TEXT,
  current_stage TEXT
);

CREATE TABLE IF NOT EXISTS source_files (
  source_file_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
  path TEXT NOT NULL,
  file_type TEXT NOT NULL,
  hash TEXT NOT NULL,
  parse_status TEXT NOT NULL,
  discovered_at TEXT NOT NULL,
  error_summary TEXT
);

CREATE TABLE IF NOT EXISTS source_documents (
  source_document_id TEXT PRIMARY KEY,
  source_file_id TEXT NOT NULL REFERENCES source_files(source_file_id) ON DELETE CASCADE,
  run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
  title TEXT,
  content_type TEXT NOT NULL,
  normalized_text TEXT NOT NULL,
  summary TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  parse_metadata TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS source_notes (
  source_note_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
  source_document_id TEXT NOT NULL REFERENCES source_documents(source_document_id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  summary TEXT NOT NULL,
  source_refs TEXT NOT NULL,
  extracted_signals TEXT NOT NULL,
  review_required INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS intake_artifacts (
  artifact_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
  artifact_type TEXT NOT NULL,
  status TEXT NOT NULL,
  path TEXT,
  summary TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS wiki_pages (
  page_id TEXT PRIMARY KEY,
  slug TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  page_type TEXT NOT NULL,
  status TEXT NOT NULL,
  freshness_status TEXT NOT NULL,
  confidence_status TEXT NOT NULL,
  current_revision_id TEXT,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS wiki_page_revisions (
  revision_id TEXT PRIMARY KEY,
  page_id TEXT NOT NULL REFERENCES wiki_pages(page_id) ON DELETE CASCADE,
  run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
  status TEXT NOT NULL,
  change_type TEXT NOT NULL,
  section_changes TEXT NOT NULL,
  source_trace_ids TEXT NOT NULL,
  diff_summary TEXT NOT NULL,
  created_at TEXT NOT NULL,
  finalized_at TEXT
);

CREATE TABLE IF NOT EXISTS impact_records (
  impact_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
  source_document_id TEXT NOT NULL REFERENCES source_documents(source_document_id) ON DELETE CASCADE,
  target_page_id TEXT,
  impact_type TEXT NOT NULL,
  summary TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS contradiction_records (
  contradiction_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
  page_id TEXT REFERENCES wiki_pages(page_id) ON DELETE SET NULL,
  revision_id TEXT REFERENCES wiki_page_revisions(revision_id) ON DELETE SET NULL,
  severity TEXT NOT NULL,
  status TEXT NOT NULL,
  conflicting_claims TEXT NOT NULL,
  source_refs TEXT NOT NULL,
  open_question_page_id TEXT,
  created_at TEXT NOT NULL,
  resolved_at TEXT
);

CREATE TABLE IF NOT EXISTS qa_reports (
  qa_report_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
  revision_id TEXT REFERENCES wiki_page_revisions(revision_id) ON DELETE SET NULL,
  status TEXT NOT NULL,
  rule_ids TEXT NOT NULL,
  summary TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS approval_records (
  approval_id TEXT PRIMARY KEY,
  revision_id TEXT NOT NULL REFERENCES wiki_page_revisions(revision_id) ON DELETE CASCADE,
  decision TEXT NOT NULL,
  reviewer_id TEXT,
  reason TEXT,
  override_requested INTEGER NOT NULL DEFAULT 0,
  policy_version TEXT NOT NULL,
  reviewed_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lint_findings (
  lint_finding_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
  page_id TEXT REFERENCES wiki_pages(page_id) ON DELETE SET NULL,
  revision_id TEXT REFERENCES wiki_page_revisions(revision_id) ON DELETE SET NULL,
  severity TEXT NOT NULL,
  code TEXT NOT NULL,
  message TEXT NOT NULL,
  created_at TEXT NOT NULL,
  resolved_at TEXT
);

CREATE TABLE IF NOT EXISTS infopedia_nodes (
  node_id TEXT PRIMARY KEY,
  page_id TEXT NOT NULL REFERENCES wiki_pages(page_id) ON DELETE CASCADE,
  parent_node_id TEXT REFERENCES infopedia_nodes(node_id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  slug TEXT NOT NULL,
  path TEXT NOT NULL,
  freshness_status TEXT NOT NULL,
  status TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS search_documents (
  search_doc_id TEXT PRIMARY KEY,
  page_id TEXT REFERENCES wiki_pages(page_id) ON DELETE CASCADE,
  run_id TEXT REFERENCES runs(run_id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  status TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
