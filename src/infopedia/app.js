const API_BASE = window.KMS_API_BASE || 'http://127.0.0.1:8000';
const app = document.getElementById('app');
const initialUrlState = new URL(window.location.href);
const initialPageSlug = initialUrlState.searchParams.get('page') || '';

app.innerHTML = `
  <main class="info-shell">
    <header class="hero">
      <p class="eyebrow">Read-only knowledge</p>
      <h1>Infopedia</h1>
      <p>Browse finalized wiki source pages and search published knowledge with semantic and keyword confidence.</p>
    </header>

    <section class="toolbar">
      <button id="loadTree">Load wiki tree</button>
      <label>Search finalized knowledge
        <input id="query" value="" placeholder="Try revenue, workflow, approved metric..." />
      </label>
      <button id="search">Search</button>
    </section>

    <section class="results-panel">
      <div class="panel-heading">
        <span class="step">3</span>
        <div>
          <h2>Published knowledge</h2>
          <p id="searchScope">Search combines semantic and keyword matching over finalized wiki pages.</p>
        </div>
      </div>
      <section id="pagePanel" class="page-panel" hidden>
        <div class="panel-heading compact">
          <div>
            <h3 id="pageTitle">Published source</h3>
            <p>Open source pages directly inside Infopedia.</p>
          </div>
        </div>
        <pre id="pageContent" class="page-content"></pre>
      </section>
      <div id="results" class="empty">Load the tree or search after KMI publishes approved candidates.</div>
    </section>
  </main>
`;

const results = document.getElementById('results');
const query = document.getElementById('query');
const pagePanel = document.getElementById('pagePanel');
const pageTitle = document.getElementById('pageTitle');
const pageContent = document.getElementById('pageContent');

function pageLink(item) {
  const slug = item.slug || item.path || item.source_id;
  const url = new URL(window.location.href);
  url.searchParams.set('page', slug);
  url.hash = `page-${slug.replace(/[^a-z0-9]+/gi, '-')}`;
  return url.toString();
}

async function openPage(slug) {
  const page = await request(`/api/wiki/pages/${encodeURIComponent(slug)}`);
  pageTitle.textContent = page.slug;
  pageContent.textContent = page.markdown;
  pagePanel.hidden = false;
}

function render(value) {
  if (Array.isArray(value)) {
    results.className = value.length ? 'cards' : 'empty';
    results.innerHTML = value.length ? value.map(item => `
      <article class="knowledge-card">
        <span class="pill">${item.page_type || item.source_kind || 'wiki'}</span>
        <h3><a class="card-link" href="${pageLink(item)}">${item.title}</a></h3>
        <code>${item.slug || item.path || item.source_id}</code>
        ${item.confidence_score === undefined ? '' : `<p class="confidence">Confidence: ${Number(item.confidence_score).toFixed(2)}</p>`}
        <a class="card-link" href="${pageLink(item)}">Open published source</a>
      </article>
    `).join('') : 'No finalized knowledge found for this search.';
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

document.getElementById('loadTree').addEventListener('click', async () => {
  try { render(await request('/api/infopedia/tree')); } catch (error) { results.textContent = `Error: ${error.message}`; }
});

document.getElementById('search').addEventListener('click', async () => {
  try { render(await request(`/api/infopedia/search?q=${encodeURIComponent(query.value)}`)); } catch (error) { results.textContent = `Error: ${error.message}`; }
});

results.addEventListener('click', async event => {
  const link = event.target;
  if (!link.matches('a.card-link[href*="page="]')) return;
  event.preventDefault();
  const slug = new URL(link.href).searchParams.get('page');
  if (!slug) return;
  try {
    await openPage(slug);
    history.replaceState({}, '', link.href);
  } catch (error) {
    results.textContent = `Error: ${error.message}`;
  }
});

async function boot() {
  if (!initialPageSlug) return;
  try {
    await openPage(initialPageSlug);
  } catch (error) {
    pagePanel.hidden = false;
    pageTitle.textContent = 'Published source unavailable';
    pageContent.textContent = `Error: ${error.message}`;
  }
}

boot();
