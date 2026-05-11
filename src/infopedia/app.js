const API_BASE = window.KMS_API_BASE || 'http://127.0.0.1:8000';
const app = document.getElementById('app');

app.innerHTML = `
  <section class="shell">
    <h1>Infopedia</h1>
    <p>Read-only browse and search over finalized wiki pages.</p>
    <button id="loadTree">Load tree</button>
    <label>Search
      <input id="query" value="" placeholder="Search finalized knowledge" />
    </label>
    <button id="search">Search</button>
    <div id="results">Ready.</div>
  </section>
`;

const results = document.getElementById('results');
function render(value) {
  if (Array.isArray(value)) {
    results.innerHTML = value.length ? `<ul>${value.map(item => `<li><strong>${item.title}</strong><br><code>${item.slug || item.path || item.source_id}</code></li>`).join('')}</ul>` : '<p>No results.</p>';
  } else {
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
  try { render(await request(`/api/infopedia/search?q=${encodeURIComponent(document.getElementById('query').value)}`)); } catch (error) { results.textContent = `Error: ${error.message}`; }
});
