import {
  getOfflineInfopediaPage,
  getOfflineInfopediaSearch,
  getOfflineInfopediaTree,
} from "./fixtures";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";
const ALLOW_FIXTURE_FALLBACK = import.meta.env.MODE !== "production";

let fallbackMode = false;

async function request(path, options = {}) {
  if (fallbackMode) {
    return offlineRequest(path);
  }

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
    if (ALLOW_FIXTURE_FALLBACK && isConnectionFailure(error)) {
      fallbackMode = true;
      return offlineRequest(path);
    }
    throw error;
  }
}

function offlineRequest(path) {
  const [pathname, search = ""] = String(path).split("?");
  const params = new URLSearchParams(search);

  if (pathname === "/infopedia/tree") {
    return Promise.resolve(
      getOfflineInfopediaTree({
        domain: params.get("domain") || undefined,
      })
    );
  }
  if (pathname === "/infopedia/search") {
    return Promise.resolve(
      getOfflineInfopediaSearch({
        q: params.get("q") || undefined,
        domain: params.get("domain") || undefined,
        page_type: params.get("page_type") || undefined,
        freshness: params.get("freshness") || undefined,
        confidence: params.get("confidence") || undefined,
        status: params.get("status") || undefined,
        scope: params.get("scope") || undefined,
      })
    );
  }
  const pageMatch = pathname.match(/^\/infopedia\/pages\/(.+)$/);
  if (pageMatch) {
    return Promise.resolve(getOfflineInfopediaPage(decodeURIComponent(pageMatch[1])));
  }

  throw new Error(`No offline fixture available for ${path}`);
}

function isConnectionFailure(error) {
  const message = String(error?.message || error || "");
  return (
    error instanceof TypeError ||
    /Failed to fetch|NetworkError|ECONNREFUSED|fetch/i.test(message)
  );
}

export function getInfopediaTree(filters = {}) {
  const params = new URLSearchParams();
  if (filters.domain) params.set("domain", filters.domain);
  const query = params.toString();
  return request(`/infopedia/tree${query ? `?${query}` : ""}`);
}

export function getInfopediaSearch(filters = {}) {
  const params = new URLSearchParams();
  if (filters.q) params.set("q", filters.q);
  if (filters.domain) params.set("domain", filters.domain);
  if (filters.page_type) params.set("page_type", filters.page_type);
  if (filters.freshness) params.set("freshness", filters.freshness);
  if (filters.confidence) params.set("confidence", filters.confidence);
  if (filters.status) params.set("status", filters.status);
  const query = params.toString();
  return request(`/infopedia/search${query ? `?${query}` : ""}`);
}

export function getInfopediaPage(slug) {
  return request(`/infopedia/pages/${encodeURIComponent(slug)}`);
}

