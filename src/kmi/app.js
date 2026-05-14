const API_BASE = window.KMS_API_BASE || 'http://127.0.0.1:8000';
const DEFAULT_TEST_SOURCE_PATH = 'tests/kmi-source';
const app = document.getElementById('app');

let activeRunId = '';
let candidates = [];
let selectedCandidateIds = new Set();

app.innerHTML = `
  <main class="kmi-shell">
    <header class="hero">
      <div>
        <p class="eyebrow">Governed maintenance</p>
        <h1>KMI Review</h1>
        <p>Create semantically decomposed candidates, review each source proposal, then publish approved knowledge to the wiki.</p>
      </div>
      <div class="status-card">
        <span>Review boundary</span>
        <strong>Human approval required</strong>
        <small>Duplicates are auto-rejected and kept visible for awareness.</small>
      </div>
    </header>

    <section class="stage-grid" aria-label="KMI stages">
      <article class="stage active" id="stageCreate">
        <span class="step">1</span>
        <h2>Create candidates</h2>
        <p>Use source documents to create proposal-only knowledge candidates.</p>
        <label>Source path
          <input id="sourcePath" value="${DEFAULT_TEST_SOURCE_PATH}" />
        </label>
        <button id="createCandidates">Create candidates</button>
      </article>

      <article class="stage" id="stageReview">
        <span class="step">2</span>
        <h2>Review & approve</h2>
        <p>Review candidates individually or select pending candidates for batch approval.</p>
        <div class="button-row">
          <button id="selectAll" disabled>Select all</button>
          <button id="approveSelected" disabled>Approve selected</button>
          <button id="rejectSelected" disabled>Reject selected</button>
        </div>
        <div id="candidateList" class="candidate-list muted">No candidates created yet.</div>
      </article>

      <article class="stage" id="stagePublish">
        <span class="step">3</span>
        <h2>Publish to wiki</h2>
        <p>Publish approved candidates as finalized source wiki pages. Rejected and duplicate candidates stay out of the wiki.</p>
        <button id="publishApproved" disabled>Publish approved candidates to wiki</button>
        <div id="publishSummary" class="muted">Waiting for approvals.</div>
      </article>
    </section>

    <section class="console-panel">
      <h2>Run output</h2>
      <pre id="output">Ready.</pre>
    </section>
  </main>
`;

const output = document.getElementById('output');
const candidateList = document.getElementById('candidateList');
const publishSummary = document.getElementById('publishSummary');
const selectAllButton = document.getElementById('selectAll');
const approveSelectedButton = document.getElementById('approveSelected');
const rejectSelectedButton = document.getElementById('rejectSelected');
const publishButton = document.getElementById('publishApproved');

function show(value) {
  output.textContent = typeof value === 'string' ? value : JSON.stringify(value, null, 2);
}

function setStage(stageName) {
  for (const stage of document.querySelectorAll('.stage')) stage.classList.remove('active');
  document.getElementById(stageName).classList.add('active');
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

function selectedPendingIds() {
  const pending = pendingCandidates();
  return [...selectedCandidateIds].filter(id => pending.some(candidate => candidate.candidate_id === id));
}

function syncButtons() {
  selectAllButton.disabled = pendingCandidates().length === 0;
  approveSelectedButton.disabled = selectedPendingIds().length === 0;
  rejectSelectedButton.disabled = selectedPendingIds().length === 0;
  publishButton.disabled = approvedCount() === 0;
}

function statusPills(candidate) {
  const pills = [`<span class="pill">${candidate.type}</span>`];
  if (candidate.approved) pills.push('<span class="pill approved-pill">approved</span>');
  if (candidate.rejected) pills.push('<span class="pill rejected-pill">rejected</span>');
  if (candidate.archived) pills.push('<span class="pill archived-pill">archived</span>');
  return pills.join('');
}

function renderCandidates() {
  if (!candidates.length) {
    candidateList.className = 'candidate-list muted';
    candidateList.textContent = 'No candidates created yet.';
    syncButtons();
    return;
  }
  candidateList.className = 'candidate-list';
  candidateList.innerHTML = candidates.map(candidate => {
    const pending = !candidate.approved && !candidate.rejected && !candidate.archived;
    const checked = selectedCandidateIds.has(candidate.candidate_id) ? 'checked' : '';
    const disabled = pending ? '' : 'disabled';
    const duplicate = candidate.duplicate_rationale ? `<p class="notice">${candidate.duplicate_rationale}</p>` : '';
    return `
      <article class="candidate-card ${candidate.approved ? 'approved' : ''} ${candidate.rejected ? 'rejected' : ''} ${candidate.archived ? 'archived' : ''}">
        <label class="candidate-selector">
          <input type="checkbox" data-candidate-id="${candidate.candidate_id}" ${checked} ${disabled} />
          <span>Select</span>
        </label>
        <div>${statusPills(candidate)}</div>
        <h3>${candidate.title}</h3>
        <p>${candidate.excerpt}</p>
        ${duplicate}
        <label class="mods-label">Mods text
          <textarea data-mods-for="${candidate.candidate_id}" ${pending ? '' : 'disabled'} placeholder="Optional text for Approve with Mods">${candidate.modification_text || ''}</textarea>
        </label>
        <div class="button-row candidate-actions">
          <button data-action="approve" data-candidate-id="${candidate.candidate_id}" ${pending ? '' : 'disabled'}>Approve</button>
          <button data-action="reject" data-candidate-id="${candidate.candidate_id}" ${pending ? '' : 'disabled'}>Reject</button>
          <button data-action="approve-mods" data-candidate-id="${candidate.candidate_id}" ${pending ? '' : 'disabled'}>Approve with Mods</button>
        </div>
        <footer>
          <span>Source: <code>${candidate.source_ref}</code></span>
          <span>Confidence: ${Number(candidate.confidence_score).toFixed(2)}</span>
        </footer>
      </article>
    `;
  }).join('');
  syncButtons();
}

async function refreshCandidates() {
  if (!activeRunId) return;
  candidates = await request(`/api/candidates/${activeRunId}`);
  selectedCandidateIds = new Set(selectedPendingIds());
  renderCandidates();
}

async function approve(payload) {
  setStage('stageReview');
  const result = await request(`/api/candidates/${activeRunId}/approve`, {
    method: 'POST',
    headers: {'content-type': 'application/json'},
    body: JSON.stringify(payload),
  });
  selectedCandidateIds.clear();
  await refreshCandidates();
  publishSummary.textContent = `${result.approved_candidate_ids.length} candidates approved and ready to publish.`;
  setStage('stagePublish');
  show(result);
}

async function reject(candidateIds) {
  const result = await request(`/api/candidates/${activeRunId}/approve`, {
    method: 'POST',
    headers: {'content-type': 'application/json'},
    body: JSON.stringify({decision: 'reject', candidate_ids: candidateIds}),
  });
  selectedCandidateIds.clear();
  await refreshCandidates();
  publishSummary.textContent = `${result.rejected_candidate_ids.length} candidates rejected.`;
  show(result);
}

document.getElementById('createCandidates').addEventListener('click', async () => {
  try {
    setStage('stageCreate');
    show('Creating candidates...');
    activeRunId = `candidate-run-${Date.now()}`;
    selectedCandidateIds.clear();
    const result = await request('/api/candidates', {
      method: 'POST',
      headers: {'content-type': 'application/json'},
      body: JSON.stringify({
        source_path: document.getElementById('sourcePath').value,
        run_id: activeRunId,
      }),
    });
    candidates = result.candidates || [];
    publishSummary.textContent = 'Review and approve candidates before publishing to wiki.';
    renderCandidates();
    setStage('stageReview');
    show(result);
  } catch (error) {
    show(`Error: ${error.message}`);
  }
});

candidateList.addEventListener('change', event => {
  const checkbox = event.target;
  if (!checkbox.matches('input[type="checkbox"][data-candidate-id]')) return;
  const id = checkbox.getAttribute('data-candidate-id');
  if (checkbox.checked) selectedCandidateIds.add(id);
  else selectedCandidateIds.delete(id);
  syncButtons();
});

candidateList.addEventListener('click', async event => {
  const button = event.target;
  if (!button.matches('button[data-action][data-candidate-id]')) return;
  const id = button.getAttribute('data-candidate-id');
  try {
    if (button.dataset.action === 'reject') await reject([id]);
    if (button.dataset.action === 'approve') await approve({candidate_ids: [id]});
    if (button.dataset.action === 'approve-mods') {
      const text = document.querySelector(`textarea[data-mods-for="${id}"]`).value;
      await approve({candidate_ids: [id], modifications: {[id]: text || 'Approved with requested modifications.'}});
    }
  } catch (error) {
    show(`Error: ${error.message}`);
  }
});

selectAllButton.addEventListener('click', () => {
  selectedCandidateIds = new Set(pendingCandidates().map(candidate => candidate.candidate_id));
  renderCandidates();
});

approveSelectedButton.addEventListener('click', async () => {
  try { await approve({candidate_ids: selectedPendingIds()}); } catch (error) { show(`Error: ${error.message}`); }
});

rejectSelectedButton.addEventListener('click', async () => {
  try { await reject(selectedPendingIds()); } catch (error) { show(`Error: ${error.message}`); }
});

publishButton.addEventListener('click', async () => {
  try {
    setStage('stagePublish');
    const result = await request(`/api/candidates/${activeRunId}/publish`, {
      method: 'POST',
      headers: {'content-type': 'application/json'},
      body: JSON.stringify({}),
    });
    await refreshCandidates();
    publishSummary.innerHTML = `<strong>${result.published.length}</strong> wiki pages published. Open Infopedia and search finalized wiki pages.`;
    show(result);
  } catch (error) {
    show(`Error: ${error.message}`);
  }
});
