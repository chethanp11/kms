const API_BASE = window.KMS_API_BASE || 'http://127.0.0.1:8000';
const app = document.getElementById('app');

app.innerHTML = `
  <main class="info-shell">
    <header class="hero">
      <p class="eyebrow">Read-only knowledge</p>
      <h1>Infopedia</h1>
      <p>Browse finalized wiki pages published from approved KMI candidates. Candidate proposals stay hidden unless explicitly included.</p>
    </header>

    <section class="toolbar">
      <button id="loadTree">Load wiki tree</button>
      <label>Search finalized knowledge
        <input id="query" value="" placeholder="Try revenue, workflow, approved metric..." />
      </label>
      <label class="checkbox-label">
        <input id="includeCandidates" type="checkbox" />
        <span>Include candidate proposals</span>
      </label>
      <button id="search">Search</button>
    </section>

    <section class="results-panel">
      <div class="panel-heading">
        <span class="step">3</span>
        <div>
          <h2>Published knowledge</h2>
          <p id="searchScope">Default search shows approved wiki pages only. Enable candidate proposals when review context is needed.</p>
        </div>
      </div>
      <div id="results" class="empty">Load the tree or search after KMI publishes approved candidates.</div>
    </section>
  </main>
`;

const results = document.getElementById('results');
const query = document.getElementById('query');
const includeCandidates = document.getElementById('includeCandidates');
const searchScope = document.getElementById('searchScope');

function render(value) {
  if (Array.isArray(value)) {
    results.className = value.length ? 'cards' : 'empty';
    results.innerHTML = value.length ? value.map(item => `
      <article class="knowledge-card ${item.source_kind === 'knowledge_candidate' ? 'candidate-result' : ''}">
        <span class="pill">${item.page_type || item.source_kind || 'wiki'}</span>
        <h3>${item.title}</h3>
        <code>${item.slug || item.path || item.source_id}</code>
      </article>
    `).join('') : 'No finalized knowledge found for this search scope.';
  } else {
    results.className = 'empty';
    results.textContent = JSON.stringify(value, null, 2);
  }
}

async function request(path) {
  const response = await fetch(`${API_BASE}${path}`);
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || data.error || response.statusText);
  return data;
}

function updateScopeText() {
  searchScope.textContent = includeCandidates.checked
    ? 'Search includes approved wiki pages plus inspectable candidate proposals and archived candidate records.'
    : 'Default search shows approved wiki pages only. Enable candidate proposals when review context is needed.';
}

document.getElementById('loadTree').addEventListener('click', async () => {
  try { render(await request('/api/infopedia/tree')); } catch (error) { results.textContent = `Error: ${error.message}`; }
});

document.getElementById('search').addEventListener('click', async () => {
  try {
    updateScopeText();
    const include = includeCandidates.checked ? '&include_candidates=true' : '';
    render(await request(`/api/infopedia/search?q=${encodeURIComponent(query.value)}${include}`));
  } catch (error) { results.textContent = `Error: ${error.message}`; }
});

includeCandidates.addEventListener('change', updateScopeText);
