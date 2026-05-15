const API_BASE = window.KMS_API_BASE || 'http://127.0.0.1:8000';
const DEFAULT_TEST_SOURCE_PATH = 'tests/kmi-source';
const app = document.getElementById('app');
const initialUrlState = new URL(window.location.href);
const initialRunId = initialUrlState.searchParams.get('run_id') || '';
const initialCandidateId = initialUrlState.searchParams.get('candidate_id') || '';
const initialStage = initialUrlState.searchParams.get('stage') || (initialRunId ? 'stageReview' : 'stageCandidates');

let activeRunId = initialRunId;
let candidates = [];
let selectedCandidateIds = new Set();
let highlightedCandidateId = initialCandidateId;
let activeStage = 'stageCandidates';
let lastPublishedPages = [];

app.innerHTML = `
  <main class="kmi-shell">
    <header class="hero">
      <div>
        <p class="eyebrow">Governed maintenance</p>
        <h1>KMI Review</h1>
        <p>Navigate each stage from the left rail, inspect the full candidate list below, review with defaults set to approve, and publish approved knowledge to the wiki.</p>
      </div>
      <div class="status-card">
        <span>Review boundary</span>
        <strong>Human approval required</strong>
        <small>Use the review dropdown to approve by default, reject when needed, and add feedback inline.</small>
      </div>
    </header>

    <section class="kmi-layout" aria-label="KMI review layout">
      <nav class="stage-nav" aria-label="KMI stages">
        <button type="button" class="stage-nav-button active" data-stage="stageCandidates">
          <span class="nav-step">1</span>
          <span class="nav-copy">
            <strong>Candidate</strong>
            <small>Capture the full list</small>
          </span>
        </button>
        <button type="button" class="stage-nav-button" data-stage="stageReview">
          <span class="nav-step">2</span>
          <span class="nav-copy">
            <strong>Review &amp; Approve</strong>
            <small>Dropdowns, checkboxes, feedback</small>
          </span>
        </button>
        <button type="button" class="stage-nav-button" data-stage="stagePublish">
          <span class="nav-step">3</span>
          <span class="nav-copy">
            <strong>Publish wiki</strong>
            <small>Preview what goes live</small>
          </span>
        </button>
      </nav>

      <section class="stage-pages">
        <article class="stage-page active" id="stageCandidates" aria-labelledby="candidateStageTitle">
          <div class="stage-page-header">
            <div>
              <p class="eyebrow">Stage 1</p>
              <h2 id="candidateStageTitle">Candidate</h2>
              <p>Generate candidates from the source folder and keep the complete list visible below.</p>
            </div>
            <div class="stage-summary" id="candidateSummary">No candidates yet.</div>
          </div>

          <section class="stage-panel">
            <div class="panel-heading compact">
              <div>
                <h3>Create candidates</h3>
                <p>Use the source folder to create the governed candidate set.</p>
              </div>
            </div>
            <label>Source path
              <input id="sourcePath" value="${DEFAULT_TEST_SOURCE_PATH}" />
            </label>
            <div class="button-row">
              <button id="createCandidates">Create candidates</button>
              <button id="jumpToReview" class="secondary-button" type="button">Go to review</button>
            </div>
            <p id="createNote" class="muted">Ready to scan the test bundle.</p>
          </section>

          <section class="stage-panel">
            <div class="panel-heading compact">
              <div>
                <h3>Candidate list</h3>
                <p>The full set of candidates created from the source documents.</p>
              </div>
            </div>
            <div id="candidateOverviewList" class="candidate-list muted">No candidates created yet.</div>
          </section>
        </article>

        <article class="stage-page" id="stageReview" aria-labelledby="reviewStageTitle">
          <div class="stage-page-header">
            <div>
              <p class="eyebrow">Stage 2</p>
              <h2 id="reviewStageTitle">Review &amp; Approve</h2>
              <p>Use the checkbox to batch select, leave the decision dropdown on approve by default, or switch any candidate to reject with feedback.</p>
            </div>
            <div class="stage-summary" id="reviewSummary">Select a run to review.</div>
          </div>

          <section class="stage-panel">
            <div class="panel-heading compact">
              <div>
                <h3>Review controls</h3>
                <p>Each card behaves like a collapsible review item with a decision dropdown and feedback field.</p>
              </div>
            </div>
            <div class="button-row">
              <button id="selectAll" disabled>Select all pending</button>
              <button id="clearSelection" class="secondary-button" type="button" disabled>Clear selection</button>
              <button id="applySelected" disabled>Apply selected reviews</button>
            </div>
            <p class="muted">Default decision is approve. Reject only the specific items that need it and add feedback inline.</p>
            <div id="candidateReviewList" class="candidate-list muted">No candidates created yet.</div>
          </section>
        </article>

        <article class="stage-page" id="stagePublish" aria-labelledby="publishStageTitle">
          <div class="stage-page-header">
            <div>
              <p class="eyebrow">Stage 3</p>
              <h2 id="publishStageTitle">Publish wiki</h2>
              <p>Review the approval outcome, then publish the approved pages into the governed wiki.</p>
            </div>
            <div class="stage-summary" id="publishSummary">Waiting for approved candidates.</div>
          </div>

          <section class="stage-panel">
            <div class="panel-heading compact">
              <div>
                <h3>Publish details</h3>
                <p>Approved candidates become wiki pages; rejected and archived items stay out of the published set.</p>
              </div>
            </div>
            <div class="publish-actions">
              <button id="publishApproved" disabled>Publish approved candidates to wiki</button>
              <button id="refreshStage" class="secondary-button" type="button">Refresh status</button>
            </div>
            <ul class="publish-points">
              <li>Only approved candidates are eligible for publish.</li>
              <li>Published pages remain browseable in Infopedia.</li>
              <li>Archived candidates remain visible in review history.</li>
            </ul>
            <div id="publishedList" class="published-list muted">No pages published yet.</div>
          </section>
        </article>
      </section>
    </section>

    <div id="pageNotice" class="page-notice muted">Ready.</div>
  </main>
`;

const candidateOverviewList = document.getElementById('candidateOverviewList');
const candidateReviewList = document.getElementById('candidateReviewList');
const candidateSummary = document.getElementById('candidateSummary');
const reviewSummary = document.getElementById('reviewSummary');
const publishSummary = document.getElementById('publishSummary');
const publishedList = document.getElementById('publishedList');
const pageNotice = document.getElementById('pageNotice');
const selectAllButton = document.getElementById('selectAll');
const clearSelectionButton = document.getElementById('clearSelection');
const applySelectedButton = document.getElementById('applySelected');
const publishButton = document.getElementById('publishApproved');
const createNote = document.getElementById('createNote');
const stageNavButtons = [...document.querySelectorAll('[data-stage]')];

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function show(message) {
  pageNotice.textContent = message;
}

function setStage(stageName, {syncUrl = true} = {}) {
  activeStage = stageName;
  stageNavButtons.forEach(button => button.classList.toggle('active', button.dataset.stage === stageName));
  document.querySelectorAll('.stage-page').forEach(page => page.classList.toggle('active', page.id === stageName));
  if (syncUrl) {
    const url = new URL(window.location.href);
    url.searchParams.set('stage', stageName);
    if (activeRunId) url.searchParams.set('run_id', activeRunId);
    if (highlightedCandidateId) url.searchParams.set('candidate_id', highlightedCandidateId);
    history.replaceState({}, '', url.toString());
  }
}

function candidateLink(candidate) {
  const url = new URL(window.location.href);
  url.searchParams.set('stage', 'stageReview');
  url.searchParams.set('run_id', candidate.run_id);
  url.searchParams.set('candidate_id', candidate.candidate_id);
  url.hash = `candidate-${candidate.candidate_id}`;
  return url.toString();
}

function focusCandidate(candidateId) {
  highlightedCandidateId = candidateId || '';
  const target = highlightedCandidateId ? document.getElementById(`candidate-${highlightedCandidateId}`) : null;
  if (target) {
    target.open = true;
    target.scrollIntoView({behavior: 'smooth', block: 'center'});
  }
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options);
  const data = response.status === 204 ? {} : await response.json();
  if (!response.ok) {
    const message = data.detail || data.error || response.statusText;
    if (response.status === 404 && path.startsWith('/api/candidates')) {
      throw new Error(`${message}. Candidate API route is unavailable; restart the KMS API server so the latest application routes are loaded.`);
    }
    throw new Error(message);
  }
  return data;
}

function pendingCandidates() {
  return candidates.filter(candidate => !candidate.approved && !candidate.rejected && !candidate.archived);
}

function approvedCount() {
  return candidates.filter(candidate => candidate.approved && !candidate.archived).length;
}

function rejectedCount() {
  return candidates.filter(candidate => candidate.rejected).length;
}

function archivedCount() {
  return candidates.filter(candidate => candidate.archived).length;
}

function selectedPendingIds() {
  const pending = pendingCandidates();
  return [...selectedCandidateIds].filter(id => pending.some(candidate => candidate.candidate_id === id));
}

function syncButtons() {
  const pending = pendingCandidates();
  const selected = selectedPendingIds();
  selectAllButton.disabled = pending.length === 0;
  clearSelectionButton.disabled = selected.length === 0;
  applySelectedButton.disabled = selected.length === 0;
  publishButton.disabled = approvedCount() === 0;
}

function statusPills(candidate) {
  const pills = [`<span class="pill">${escapeHtml(candidate.type)}</span>`];
  if (candidate.approved) pills.push('<span class="pill approved-pill">approved</span>');
  if (candidate.rejected) pills.push('<span class="pill rejected-pill">rejected</span>');
  if (candidate.archived) pills.push('<span class="pill archived-pill">archived</span>');
  return pills.join('');
}

function overviewCard(candidate) {
  return `
    <article class="candidate-card ${candidate.approved ? 'approved' : ''} ${candidate.rejected ? 'rejected' : ''} ${candidate.archived ? 'archived' : ''}">
      <div class="candidate-headline">
        <div>
          <h3>${escapeHtml(candidate.title)}</h3>
          <div>${statusPills(candidate)}</div>
        </div>
        <button type="button" class="secondary-button candidate-jump" data-focus-candidate="${candidate.candidate_id}">Open review</button>
      </div>
      <p>${escapeHtml(candidate.excerpt)}</p>
      <footer>
        <span>Source: <code>${escapeHtml(candidate.source_ref)}</code></span>
        <span>Confidence: ${Number(candidate.confidence_score).toFixed(2)}</span>
      </footer>
    </article>
  `;
}

function reviewCard(candidate) {
  const pending = !candidate.approved && !candidate.rejected && !candidate.archived;
  const selected = selectedCandidateIds.has(candidate.candidate_id) ? 'checked' : '';
  const detailsOpen = highlightedCandidateId === candidate.candidate_id || selected === 'checked';
  const duplicate = candidate.duplicate_rationale ? `<p class="notice">${escapeHtml(candidate.duplicate_rationale)}</p>` : '';
  return `
    <details id="candidate-${candidate.candidate_id}" class="review-card ${candidate.approved ? 'approved' : ''} ${candidate.rejected ? 'rejected' : ''} ${candidate.archived ? 'archived' : ''}" ${detailsOpen ? 'open' : ''}>
      <summary>
        <label class="candidate-selector">
          <input type="checkbox" data-candidate-id="${candidate.candidate_id}" ${selected} ${pending ? '' : 'disabled'} />
          <span>Select</span>
        </label>
        <div class="review-summary-main">
          <div class="review-summary-title-row">
            <h3>${escapeHtml(candidate.title)}</h3>
            <div>${statusPills(candidate)}</div>
          </div>
          <p>${escapeHtml(candidate.excerpt)}</p>
        </div>
        <label class="decision-label">Decision
          <select data-decision-for="${candidate.candidate_id}" ${pending ? '' : 'disabled'}>
            <option value="approve" ${candidate.rejected ? '' : 'selected'}>Approve</option>
            <option value="reject" ${candidate.rejected ? 'selected' : ''}>Reject</option>
          </select>
        </label>
      </summary>
      <div class="review-body">
        <div class="review-panel">
          <div class="review-panel-grid">
            <div>
              <span class="field-label">Source</span>
              <code>${escapeHtml(candidate.source_ref)}</code>
            </div>
            <div>
              <span class="field-label">Confidence</span>
              <strong>${Number(candidate.confidence_score).toFixed(2)}</strong>
            </div>
            <div>
              <span class="field-label">Review state</span>
              <strong>${escapeHtml(candidate.review_status)}</strong>
            </div>
          </div>
          ${duplicate}
        </div>
        <label class="feedback-label">Feedback
          <textarea data-feedback-for="${candidate.candidate_id}" ${pending ? '' : 'disabled'} placeholder="Add approval notes or rejection feedback">${escapeHtml(candidate.modification_text || '')}</textarea>
        </label>
      </div>
    </details>
  `;
}

function renderCandidateOverview() {
  candidateSummary.textContent = candidates.length
    ? `${candidates.length} candidates loaded • ${approvedCount()} approved • ${rejectedCount()} rejected`
    : 'No candidates yet.';
  if (!candidates.length) {
    candidateOverviewList.className = 'candidate-list muted';
    candidateOverviewList.textContent = 'No candidates created yet.';
    return;
  }
  candidateOverviewList.className = 'candidate-list';
  candidateOverviewList.innerHTML = candidates.map(candidate => overviewCard(candidate)).join('');
}

function renderReviewList() {
  reviewSummary.textContent = candidates.length
    ? `${pendingCandidates().length} pending • ${approvedCount()} approved • ${rejectedCount()} rejected`
    : 'Select a run to review.';
  if (!candidates.length) {
    candidateReviewList.className = 'candidate-list muted';
    candidateReviewList.textContent = 'No candidates created yet.';
    return;
  }
  candidateReviewList.className = 'candidate-list';
  candidateReviewList.innerHTML = candidates.map(candidate => reviewCard(candidate)).join('');
}

function renderPublishPanel() {
  publishSummary.textContent = activeRunId
    ? `${approvedCount()} approved • ${rejectedCount()} rejected • ${archivedCount()} archived`
    : 'Waiting for approved candidates.';
  if (lastPublishedPages.length) {
    publishedList.className = 'published-list';
    publishedList.innerHTML = `
      <strong>${lastPublishedPages.length}</strong> pages published to the wiki.
      <ul>${lastPublishedPages.map(path => `<li><code>${escapeHtml(path)}</code></li>`).join('')}</ul>
    `;
  } else if (approvedCount() > 0) {
    publishedList.className = 'published-list muted';
    publishedList.textContent = `${approvedCount()} approved candidates are ready to publish.`;
  } else {
    publishedList.className = 'published-list muted';
    publishedList.textContent = 'No pages published yet.';
  }
}

function renderAll() {
  renderCandidateOverview();
  renderReviewList();
  renderPublishPanel();
  syncButtons();
  focusCandidate(highlightedCandidateId);
}

async function refreshCandidates() {
  if (!activeRunId) return;
  candidates = await request(`/api/candidates/${activeRunId}`);
  selectedCandidateIds = new Set(selectedPendingIds());
  renderAll();
}

async function approveCandidate(candidateId, feedback) {
  const body = feedback
    ? {candidate_ids: [candidateId], modifications: {[candidateId]: feedback}}
    : {candidate_ids: [candidateId]};
  return request(`/api/candidates/${activeRunId}/approve`, {
    method: 'POST',
    headers: {'content-type': 'application/json'},
    body: JSON.stringify(body),
  });
}

async function rejectCandidate(candidateId, feedback) {
  return request(`/api/candidates/${activeRunId}/approve`, {
    method: 'POST',
    headers: {'content-type': 'application/json'},
    body: JSON.stringify({decision: 'reject', candidate_ids: [candidateId], reason: feedback || 'Rejected from KMI review.'}),
  });
}

async function createCandidatesFromSource() {
  const result = await request('/api/candidates', {
    method: 'POST',
    headers: {'content-type': 'application/json'},
    body: JSON.stringify({
      source_path: document.getElementById('sourcePath').value,
      run_id: activeRunId || `candidate-run-${Date.now()}`,
    }),
  });
  activeRunId = result.run_id || activeRunId || `candidate-run-${Date.now()}`;
  candidates = result.candidates || [];
  selectedCandidateIds = new Set(pendingCandidates().map(candidate => candidate.candidate_id));
  lastPublishedPages = [];
  createNote.textContent = `Loaded ${candidates.length} candidates from ${document.getElementById('sourcePath').value}.`;
  show(`Created ${candidates.length} candidates.`);
  renderAll();
  setStage('stageCandidates');
}

async function applySelectedReviews() {
  const selected = pendingCandidates().filter(candidate => selectedCandidateIds.has(candidate.candidate_id));
  if (!selected.length) return;
  let approved = 0;
  let rejected = 0;
  for (const candidate of selected) {
    const decision = document.querySelector(`[data-decision-for="${candidate.candidate_id}"]`)?.value || 'approve';
    const feedback = document.querySelector(`[data-feedback-for="${candidate.candidate_id}"]`)?.value.trim() || '';
    if (decision === 'reject') {
      await rejectCandidate(candidate.candidate_id, feedback);
      rejected += 1;
    } else {
      await approveCandidate(candidate.candidate_id, feedback);
      approved += 1;
    }
  }
  selectedCandidateIds.clear();
  show(`Applied reviews to ${selected.length} candidates: ${approved} approved, ${rejected} rejected.`);
  await refreshCandidates();
  setStage('stageReview');
}

async function publishApprovedCandidates() {
  if (!activeRunId) return;
  const result = await request(`/api/candidates/${activeRunId}/publish`, {
    method: 'POST',
    headers: {'content-type': 'application/json'},
    body: JSON.stringify({}),
  });
  lastPublishedPages = result.published || [];
  await refreshCandidates();
  publishSummary.innerHTML = `<strong>${lastPublishedPages.length}</strong> wiki pages published.`;
  show(`Published ${lastPublishedPages.length} wiki pages.`);
  setStage('stagePublish');
}

stageNavButtons.forEach(button => {
  button.addEventListener('click', () => setStage(button.dataset.stage || 'stageCandidates'));
});

document.getElementById('createCandidates').addEventListener('click', async () => {
  try {
    setStage('stageCandidates');
    show('Creating candidates...');
    await createCandidatesFromSource();
  } catch (error) {
    show(`Error: ${error.message}`);
  }
});

document.getElementById('jumpToReview').addEventListener('click', () => {
  setStage('stageReview');
  focusCandidate(highlightedCandidateId || (candidates[0] && candidates[0].candidate_id) || '');
});

document.getElementById('refreshStage').addEventListener('click', async () => {
  try {
    await refreshCandidates();
    show('Refreshed candidate and publish status.');
  } catch (error) {
    show(`Error: ${error.message}`);
  }
});

candidateOverviewList.addEventListener('click', event => {
  const button = event.target;
  if (!button.matches('button[data-focus-candidate]')) return;
  const candidateId = button.getAttribute('data-focus-candidate');
  setStage('stageReview');
  focusCandidate(candidateId);
});

candidateReviewList.addEventListener('change', event => {
  const checkbox = event.target;
  if (!checkbox.matches('input[type="checkbox"][data-candidate-id]')) return;
  const id = checkbox.getAttribute('data-candidate-id');
  if (checkbox.checked) selectedCandidateIds.add(id);
  else selectedCandidateIds.delete(id);
  syncButtons();
});

selectAllButton.addEventListener('click', () => {
  selectedCandidateIds = new Set(pendingCandidates().map(candidate => candidate.candidate_id));
  renderReviewList();
  syncButtons();
});

clearSelectionButton.addEventListener('click', () => {
  selectedCandidateIds.clear();
  renderReviewList();
  syncButtons();
});

applySelectedButton.addEventListener('click', async () => {
  try {
    await applySelectedReviews();
  } catch (error) {
    show(`Error: ${error.message}`);
  }
});

publishButton.addEventListener('click', async () => {
  try {
    await publishApprovedCandidates();
  } catch (error) {
    show(`Error: ${error.message}`);
  }
});

async function boot() {
  setStage(initialStage, {syncUrl: false});
  if (!activeRunId) return;
  createNote.textContent = 'Loading candidate run from hyperlink.';
  try {
    await refreshCandidates();
    if (initialCandidateId) focusCandidate(initialCandidateId);
    if (initialStage === 'stageReview') setStage('stageReview', {syncUrl: false});
  } catch (error) {
    show(`Error: ${error.message}`);
  }
}

boot();
