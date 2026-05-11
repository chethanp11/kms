const API_BASE = window.KMS_API_BASE || 'http://127.0.0.1:8000';
const app = document.getElementById('app');

app.innerHTML = `
  <section class="shell">
    <h1>Knowledge Manager Interface</h1>
    <p>Start a governed maintenance run from a local source folder.</p>
    <label>Source path
      <input id="sourcePath" value="/private/tmp/kms-demo/raw" />
    </label>
    <label class="inline"><input id="autoApprove" type="checkbox" checked /> Auto-approve valid draft pages</label>
    <button id="seedDemo">Create demo source</button>
    <button id="startRun">Start run</button>
    <pre id="output">Ready.</pre>
  </section>
`;

const output = document.getElementById('output');

function show(value) {
  output.textContent = typeof value === 'string' ? value : JSON.stringify(value, null, 2);
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || data.error || response.statusText);
  return data;
}

document.getElementById('seedDemo').addEventListener('click', async () => {
  show('Creating demo source through the local runtime is not exposed in the browser. Use an existing local folder, or run src/scripts/seed_fixtures.py from Python.');
});

document.getElementById('startRun').addEventListener('click', async () => {
  try {
    show('Starting run...');
    const payload = {
      source_path: document.getElementById('sourcePath').value,
      run_id: `run-${Date.now()}`,
      auto_approve: document.getElementById('autoApprove').checked,
    };
    const result = await request('/api/runs', {
      method: 'POST',
      headers: {'content-type': 'application/json'},
      body: JSON.stringify(payload),
    });
    show(result);
  } catch (error) {
    show(`Error: ${error.message}`);
  }
});
