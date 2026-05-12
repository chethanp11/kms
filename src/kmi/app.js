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
        <h1>Knowledge Manager Interface</h1>
        <p>Create OpenAI API-key-assisted candidates, review them through a HITL Knowledge Manager gate, then load approved knowledge to the wiki.</p>
      </div>
      <div class="status-card">
        <span>AI source</span>
        <strong>OpenAI API key only</strong>
        <small>Configure OPEN_AI_KEY in .env with KMS_AI_MODEL</small>
      </div>
    </header>

    <section class="stage-grid" aria-label="KMI stages">
      <article class="stage active" id="stageCreate">
        <span class="step">1</span>
        <h2>Create candidates</h2>
        <p>Use source documents and OpenAI-backed extraction to create proposal-only knowledge candidates.</p>
        <label>Source path
          <input id="sourcePath" value="${DEFAULT_TEST_SOURCE_PATH}" />
        </label>
        <button id="createCandidates">Create candidates</button>
      </article>

      <article class="stage" id="stageReview">
        <span class="step">2</span>
        <h2>Review & approve</h2>
        <p>HITL gate: the Knowledge Manager reviews candidates and approves selected candidates or all candidates.</p>
        <div class="button-row">
          <button id="approveSelected" disabled>Approve selected</button>
          <button id="approveAll" disabled>Approve all candidates</button>
        </div>
        <div id="candidateList" class="candidate-list muted">No candidates created yet.</div>
      </article>

      <article class="stage" id="stagePublish">
        <span class="step">3</span>
        <h2>Load to wiki</h2>
        <p>The Knowledge Manager loads approved candidates to the governed wiki. Loaded candidates are archived.</p>
        <label>Knowledge Manager
          <input id="reviewerId" value="knowledge-manager" />
        </label>
        <button id="publishApproved" disabled>Load approved candidates to wiki</button>
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
const approveAllButton = document.getElementById('approveAll');
const approveSelectedButton = document.getElementById('approveSelected');
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

function approvedCount() {
  return candidates.filter(candidate => candidate.approved && !candidate.archived).length;
}

function syncButtons() {
  const activeCandidates = candidates.filter(candidate => !candidate.archived);
  const selectable = activeCandidates.filter(candidate => !candidate.approved);
  approveAllButton.disabled = selectable.length === 0;
  approveSelectedButton.disabled = [...selectedCandidateIds].filter(id => selectable.some(candidate => candidate.candidate_id === id)).length === 0;
  publishButton.disabled = approvedCount() === 0;
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
    const checked = selectedCandidateIds.has(candidate.candidate_id) ? 'checked' : '';
    const disabled = candidate.approved || candidate.archived ? 'disabled' : '';
    return `
      <article class="candidate-card ${candidate.approved ? 'approved' : ''} ${candidate.archived ? 'archived' : ''}">
        <label class="candidate-selector">
          <input type="checkbox" data-candidate-id="${candidate.candidate_id}" ${checked} ${disabled} />
          <span>Select for approval</span>
        </label>
        <div>
          <span class="pill">${candidate.type}</span>
          ${candidate.approved ? '<span class="pill approved-pill">approved</span>' : ''}
          ${candidate.archived ? '<span class="pill archived-pill">archived</span>' : ''}
        </div>
        <h3>${candidate.title}</h3>
        <p>${candidate.excerpt}</p>
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
  selectedCandidateIds = new Set([...selectedCandidateIds].filter(id => candidates.some(candidate => candidate.candidate_id === id && !candidate.approved && !candidate.archived)));
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
  publishSummary.textContent = `${result.approved_candidate_ids.length} candidates approved and ready for Knowledge Manager wiki loading.`;
  setStage('stagePublish');
  show(result);
}

document.getElementById('createCandidates').addEventListener('click', async () => {
  try {
    setStage('stageCreate');
    show('Creating candidates with configured OpenAI API-key extraction...');
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
    publishSummary.textContent = 'Review and approve candidates before loading to wiki.';
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

approveSelectedButton.addEventListener('click', async () => {
  try {
    await approve({candidate_ids: [...selectedCandidateIds]});
  } catch (error) {
    show(`Error: ${error.message}`);
  }
});

approveAllButton.addEventListener('click', async () => {
  try {
    await approve({approve_all: true});
  } catch (error) {
    show(`Error: ${error.message}`);
  }
});

publishButton.addEventListener('click', async () => {
  try {
    setStage('stagePublish');
    const result = await request(`/api/candidates/${activeRunId}/publish`, {
      method: 'POST',
      headers: {'content-type': 'application/json'},
      body: JSON.stringify({reviewer_id: document.getElementById('reviewerId').value || 'knowledge-manager'}),
    });
    await refreshCandidates();
    publishSummary.innerHTML = `<strong>${result.published.length}</strong> wiki pages published. Loaded candidates are archived. Open Infopedia and search finalized wiki pages.`;
    show(result);
  } catch (error) {
    show(`Error: ${error.message}`);
  }
});
