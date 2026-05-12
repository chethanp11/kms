const API_BASE = window.KMS_API_BASE || 'http://127.0.0.1:8000';
const DEFAULT_TEST_SOURCE_PATH = 'tests/kmi-source';
const app = document.getElementById('app');

let activeRunId = '';
let candidates = [];

app.innerHTML = `
  <main class="kmi-shell">
    <header class="hero">
      <div>
        <p class="eyebrow">Governed maintenance</p>
        <h1>Knowledge Manager Interface</h1>
        <p>Create LLM-assisted candidates, approve what is trusted, then publish approved knowledge to the wiki.</p>
      </div>
      <div class="status-card">
        <span>AI source</span>
        <strong>.env API key</strong>
        <small>OPENAI_API_KEY + KMS_AI_MODEL</small>
      </div>
    </header>

    <section class="stage-grid" aria-label="KMI stages">
      <article class="stage active" id="stageCreate">
        <span class="step">1</span>
        <h2>Create candidates</h2>
        <p>Use source documents and LLM-backed extraction to create proposal-only knowledge candidates.</p>
        <label>Source path
          <input id="sourcePath" value="${DEFAULT_TEST_SOURCE_PATH}" />
        </label>
        <button id="createCandidates">Create candidates</button>
      </article>

      <article class="stage" id="stageReview">
        <span class="step">2</span>
        <h2>Review & approve</h2>
        <p>Inspect extracted candidates before they become eligible for wiki publication.</p>
        <button id="approveAll" disabled>Approve all candidates</button>
        <div id="candidateList" class="candidate-list muted">No candidates created yet.</div>
      </article>

      <article class="stage" id="stagePublish">
        <span class="step">3</span>
        <h2>Load to wiki</h2>
        <p>Publish approved candidates to the governed wiki and refresh Infopedia projections.</p>
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
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || data.error || response.statusText);
  return data;
}

function renderCandidates() {
  if (!candidates.length) {
    candidateList.className = 'candidate-list muted';
    candidateList.textContent = 'No candidates created yet.';
    return;
  }
  candidateList.className = 'candidate-list';
  candidateList.innerHTML = candidates.map(candidate => `
    <article class="candidate-card ${candidate.approved ? 'approved' : ''}">
      <div>
        <span class="pill">${candidate.type}</span>
        ${candidate.approved ? '<span class="pill approved-pill">approved</span>' : ''}
      </div>
      <h3>${candidate.title}</h3>
      <p>${candidate.excerpt}</p>
      <footer>
        <span>Source: <code>${candidate.source_ref}</code></span>
        <span>Confidence: ${Number(candidate.confidence_score).toFixed(2)}</span>
      </footer>
    </article>
  `).join('');
}

async function refreshCandidates() {
  if (!activeRunId) return;
  candidates = await request(`/api/candidates/${activeRunId}`);
  renderCandidates();
}

document.getElementById('createCandidates').addEventListener('click', async () => {
  try {
    setStage('stageCreate');
    show('Creating candidates with configured AI extraction...');
    activeRunId = `candidate-run-${Date.now()}`;
    const result = await request('/api/candidates', {
      method: 'POST',
      headers: {'content-type': 'application/json'},
      body: JSON.stringify({
        source_path: document.getElementById('sourcePath').value,
        run_id: activeRunId,
      }),
    });
    candidates = result.candidates || [];
    approveAllButton.disabled = candidates.length === 0;
    publishButton.disabled = true;
    publishSummary.textContent = 'Approve candidates before loading to wiki.';
    renderCandidates();
    setStage('stageReview');
    show(result);
  } catch (error) {
    show(`Error: ${error.message}`);
  }
});

approveAllButton.addEventListener('click', async () => {
  try {
    setStage('stageReview');
    const result = await request(`/api/candidates/${activeRunId}/approve`, {
      method: 'POST',
      headers: {'content-type': 'application/json'},
      body: JSON.stringify({approve_all: true}),
    });
    await refreshCandidates();
    publishButton.disabled = false;
    publishSummary.textContent = `${result.approved_candidate_ids.length} candidates approved and ready for wiki publication.`;
    setStage('stagePublish');
    show(result);
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
      body: JSON.stringify({reviewer_id: 'knowledge-manager'}),
    });
    publishSummary.innerHTML = `<strong>${result.published.length}</strong> wiki pages published. Open Infopedia and load the tree/search to view them.`;
    show(result);
  } catch (error) {
    show(`Error: ${error.message}`);
  }
});
