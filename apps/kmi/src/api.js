const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";

async function request(path, options = {}) {
  try {
    const response = await fetch(`${API_BASE}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      ...options,
    });

    const contentType = response.headers.get("content-type") || "";
    const body = contentType.includes("application/json") ? await response.json() : await response.text();

    if (!response.ok) {
      const message = typeof body === "string" ? body : body?.detail || response.statusText;
      throw new Error(message || "Request failed");
    }

    return body;
  } catch (error) {
    if (error instanceof TypeError || /Failed to fetch|ECONNREFUSED|NetworkError/i.test(String(error?.message || error))) {
      throw new Error("KMI backend unavailable. Start the API service and retry.");
    }
    throw error;
  }
}

export function listRuns() {
  return request("/runs");
}

export function createRun(payload) {
  return request("/runs", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getRun(runId) {
  return request(`/runs/${encodeURIComponent(runId)}`);
}

export function getRunArtifacts(runId) {
  return request(`/runs/${encodeURIComponent(runId)}/artifacts`);
}

export function getReviewDiff(revisionId) {
  return request(`/reviews/${encodeURIComponent(revisionId)}/diff`);
}

export function getContradiction(contradictionId) {
  return request(`/contradictions/${encodeURIComponent(contradictionId)}`);
}

export function submitApproval(revisionId, payload) {
  return request(`/approvals/${encodeURIComponent(revisionId)}`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getHealthFindings() {
  return request("/health/findings");
}

