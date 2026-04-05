import React, { useEffect, useMemo, useState } from "react";
import { getInfopediaPage, getInfopediaSearch, getInfopediaTree } from "./api";

function parseRoute(pathname, search) {
  const path = pathname.replace(/\/+$/, "") || "/";
  const query = new URLSearchParams(search);
  if (path.startsWith("/page/")) {
    return {
      name: "page",
      slug: decodeURIComponent(path.slice("/page/".length)),
      domain: query.get("domain") || "",
      q: query.get("q") || "",
      pageType: query.get("page_type") || "",
      freshness: query.get("freshness") || "",
      confidence: query.get("confidence") || "",
      status: query.get("status") || "",
    };
  }
  if (path === "/search") {
    return {
      name: "search",
      q: query.get("q") || "",
      domain: query.get("domain") || "",
      pageType: query.get("page_type") || "",
      freshness: query.get("freshness") || "",
      confidence: query.get("confidence") || "",
      status: query.get("status") || "",
    };
  }
  return {
    name: "browse",
    q: query.get("q") || "",
    domain: query.get("domain") || "",
    pageType: query.get("page_type") || "",
    freshness: query.get("freshness") || "",
    confidence: query.get("confidence") || "",
    status: query.get("status") || "",
  };
}

function buildSearchPath(state) {
  const params = new URLSearchParams();
  if (state.q) params.set("q", state.q);
  if (state.domain) params.set("domain", state.domain);
  if (state.pageType) params.set("page_type", state.pageType);
  if (state.freshness) params.set("freshness", state.freshness);
  if (state.confidence) params.set("confidence", state.confidence);
  if (state.status) params.set("status", state.status);
  const query = params.toString();
  return query ? `/search?${query}` : "/search";
}

function App() {
  const [route, setRoute] = useState(() => parseRoute(window.location.pathname, window.location.search));

  useEffect(() => {
    const onPopState = () => setRoute(parseRoute(window.location.pathname, window.location.search));
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, []);

  const navigate = (path) => {
    window.history.pushState({}, "", path);
    setRoute(parseRoute(window.location.pathname, window.location.search));
  };

  const chrome = useMemo(() => chromeForRoute(route), [route]);

  return (
    <div className="infopedia-shell">
      <aside className="infopedia-sidebar">
        <div className="brand">
          <div className="brand-mark">IO</div>
          <div>
            <div className="brand-title">Infopedia</div>
            <div className="brand-subtitle">Read-only knowledge browse surface</div>
          </div>
        </div>

        <SearchBar route={route} onSubmit={(next) => navigate(buildSearchPath({ ...route, ...next }))} />

        <div className="boundary-note">
          <strong>Read-only boundary</strong>
          <p>Infopedia only reads finalized `/wiki` content and derived navigation metadata.</p>
        </div>

        <TreeNavigator route={route} navigate={navigate} />
      </aside>

      <main className="infopedia-main">
        <header className="hero">
          <div>
            <p className="eyebrow">Knowledge Consumer Surface</p>
            <h1>{chrome.title}</h1>
            <p className="hero-copy">{chrome.copy}</p>
          </div>
          <div className="hero-badges">
            {chrome.badges.map((badge) => (
              <Badge key={badge.label} tone={badge.tone}>
                {badge.label}
              </Badge>
            ))}
          </div>
        </header>

        <div className="workspace">
          {route.name === "browse" ? <BrowseHome route={route} navigate={navigate} /> : null}
          {route.name === "search" ? <SearchResults route={route} navigate={navigate} /> : null}
          {route.name === "page" ? <PageView route={route} navigate={navigate} /> : null}
        </div>
      </main>
    </div>
  );
}

function BrowseHome({ route, navigate }) {
  const { data, loading, error } = useResource(() => getInfopediaTree(route.domain || undefined), [route.domain]);

  if (loading) {
    return <Panel title="Tree browsing" eyebrow="Finalized knowledge"><LoadingState label="Loading Infopedia tree" /></Panel>;
  }
  if (error) {
    return <ErrorState error={error} onRetry={() => window.location.reload()} />;
  }

  const firstDomain = data.domains[0];
  const firstPage = firstDomain?.children?.[0]?.pages?.[0];

  return (
    <div className="stack">
      <MetricGrid
        items={[
          { label: "Domains", value: data.summary.domain_count },
          { label: "Pages", value: data.summary.page_count },
          { label: "Current focus", value: route.domain || "All domains" },
        ]}
      />

      <Panel title="Tree navigation" eyebrow="Browse-first hierarchy">
        <div className="tree-grid">
          {data.domains.map((domain) => (
            <details key={domain.domain} className="tree-domain" open={!route.domain || route.domain === domain.domain}>
              <summary>
                <div>
                  <div className="row-title">{domain.title}</div>
                  <div className="row-subtitle">{domain.count} finalized pages</div>
                </div>
              </summary>
              <div className="tree-families">
                {domain.children.map((family) => (
                  <div key={family.page_type} className="tree-family">
                    <div className="tree-family-head">
                      <div className="row-title">{family.title}</div>
                      <Badge tone="info">{family.count}</Badge>
                    </div>
                    <div className="tree-pages">
                      {family.pages.map((page) => (
                        <button key={page.slug} className="tree-page" onClick={() => navigate(`/page/${encodeURIComponent(page.slug)}?domain=${domain.domain}`)}>
                          <div>
                            <div className="row-title">{page.title}</div>
                            <div className="row-subtitle">{page.slug}</div>
                          </div>
                          <StatusPills page={page} />
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </details>
          ))}
        </div>
      </Panel>

      {firstPage ? (
        <Panel title="Start reading" eyebrow="Quick access">
          <div className="inline-actions">
            <Button onClick={() => navigate(`/page/${encodeURIComponent(firstPage.slug)}?domain=${firstPage.domain}`)}>
              Open {firstPage.title}
            </Button>
            <Button variant="ghost" onClick={() => navigate(buildSearchPath({ ...route, q: firstPage.title }))}>
              Search this domain
            </Button>
          </div>
        </Panel>
      ) : null}
    </div>
  );
}

function SearchResults({ route, navigate }) {
  const { data, loading, error } = useResource(
    () =>
      getInfopediaSearch({
        q: route.q,
        domain: route.domain || undefined,
        page_type: route.pageType || undefined,
        freshness: route.freshness || undefined,
        confidence: route.confidence || undefined,
        status: route.status || undefined,
      }),
    [route.q, route.domain, route.pageType, route.freshness, route.confidence, route.status]
  );

  if (loading) {
    return <Panel title="Search results" eyebrow="Infopedia search"><LoadingState label="Loading search results" /></Panel>;
  }
  if (error) {
    return <ErrorState error={error} onRetry={() => window.location.reload()} />;
  }

  return (
    <div className="stack">
      <MetricGrid
        items={[
          { label: "Results", value: data.total },
          { label: "Domains", value: Object.keys(data.facets.domains).length },
          { label: "Page families", value: Object.keys(data.facets.page_types).length },
        ]}
      />

      <Panel title="Search filters" eyebrow="Facet-aware discovery">
        <FacetSummary facets={data.facets} />
      </Panel>

      <Panel title="Search results" eyebrow="Finalized pages only">
        {data.items.length ? (
          <div className="result-list">
            {data.items.map((item) => (
              <button key={item.slug} className="result-card" onClick={() => navigate(`/page/${encodeURIComponent(item.slug)}?domain=${item.domain}`)}>
                <div className="result-head">
                  <div>
                    <div className="row-title">{item.title}</div>
                    <div className="row-subtitle">{item.snippet}</div>
                  </div>
                  <StatusPills page={item} />
                </div>
                <div className="chip-row">
                  <span className="chip">{item.domain}</span>
                  <span className="chip">{item.page_type}</span>
                  <span className="chip">{item.related_count} related</span>
                  <span className="chip">{item.backlink_count} backlinks</span>
                </div>
              </button>
            ))}
          </div>
        ) : (
          <EmptyState
            title="No matching pages"
            description="Try clearing filters or broadening the search term across finalized knowledge."
          />
        )}
      </Panel>
    </div>
  );
}

function PageView({ route, navigate }) {
  const { data, loading, error } = useResource(() => getInfopediaPage(route.slug), [route.slug]);

  if (loading) {
    return <Panel title="Page view" eyebrow="Reading"><LoadingState label="Loading page" /></Panel>;
  }
  if (error) {
    return <ErrorState error={error} onRetry={() => navigate(`/page/${encodeURIComponent(route.slug)}`)} />;
  }

  const page = data.page;

  return (
    <div className="stack">
      <MetricGrid
        items={[
          { label: "Freshness", value: page.freshness },
          { label: "Confidence", value: page.confidence },
          { label: "Status", value: page.status },
          { label: "Source traces", value: data.source_trace_summary.length },
        ]}
      />

      <Panel title={page.title} eyebrow={`${page.domain} / ${page.page_type}`}>
        <div className="page-meta">
          <StatusPills page={page} />
          <div className="chip-row">
            {data.breadcrumbs.map((item) => (
              <button key={item.slug} className="chip chip-link" onClick={() => navigate(item.slug)}>
                {item.title}
              </button>
            ))}
          </div>
        </div>

        <div className="page-layout">
          <article className="page-body">
            <MarkdownView markdown={data.content_markdown} />
          </article>

          <aside className="page-aside">
            <InfoBlock title="Source trace" items={data.source_trace_summary} />
            <RelatedBlock
              title="Related pages"
              items={data.related_pages}
              emptyLabel="No related pages were projected."
              onOpen={(slug) => navigate(`/page/${encodeURIComponent(slug)}`)}
            />
            <RelatedBlock
              title="Backlinks"
              items={data.backlinks}
              emptyLabel="No backlinks are currently projected."
              onOpen={(slug) => navigate(`/page/${encodeURIComponent(slug)}`)}
            />
            <RelatedBlock
              title="Sibling pages"
              items={data.siblings}
              emptyLabel="No sibling pages in this family."
              onOpen={(slug) => navigate(`/page/${encodeURIComponent(slug)}`)}
            />
          </aside>
        </div>
      </Panel>
    </div>
  );
}

function TreeNavigator({ route, navigate }) {
  const { data, loading } = useResource(() => getInfopediaTree(route.domain || undefined), [route.domain]);

  if (loading) {
    return <div className="sidebar-panel"><LoadingState label="Loading tree" /></div>;
  }

  return (
    <div className="sidebar-panel">
      <div className="panel-eyebrow">Tree</div>
      <div className="sidebar-tree">
        {data.domains.map((domain) => (
          <details key={domain.domain} open={!route.domain || route.domain === domain.domain}>
            <summary>{domain.title}</summary>
            <div className="sidebar-families">
              {domain.children.map((family) => (
                <div key={family.page_type}>
                  <div className="sidebar-family-title">{family.title}</div>
                  <div className="sidebar-pages">
                    {family.pages.map((page) => (
                      <button key={page.slug} className="sidebar-page" onClick={() => navigate(`/page/${encodeURIComponent(page.slug)}?domain=${domain.domain}`)}>
                        {page.title}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </details>
        ))}
      </div>
    </div>
  );
}

function SearchBar({ route, onSubmit }) {
  const [state, setState] = useState({
    q: route.q || "",
    domain: route.domain || "",
    pageType: route.pageType || "",
    freshness: route.freshness || "",
    confidence: route.confidence || "",
    status: route.status || "",
  });

  useEffect(() => {
    setState({
      q: route.q || "",
      domain: route.domain || "",
      pageType: route.pageType || "",
      freshness: route.freshness || "",
      confidence: route.confidence || "",
      status: route.status || "",
    });
  }, [route.q, route.domain, route.pageType, route.freshness, route.confidence, route.status]);

  function submit(event) {
    event.preventDefault();
    onSubmit(state);
  }

  return (
    <form className="search-panel" onSubmit={submit}>
      <input
        value={state.q}
        onChange={(event) => setState({ ...state, q: event.target.value })}
        placeholder="Search finalized knowledge"
      />
      <div className="filter-grid">
        <input value={state.domain} onChange={(event) => setState({ ...state, domain: event.target.value })} placeholder="Domain" />
        <input value={state.pageType} onChange={(event) => setState({ ...state, pageType: event.target.value })} placeholder="Page family" />
        <input value={state.freshness} onChange={(event) => setState({ ...state, freshness: event.target.value })} placeholder="Freshness" />
        <input value={state.confidence} onChange={(event) => setState({ ...state, confidence: event.target.value })} placeholder="Confidence" />
        <input value={state.status} onChange={(event) => setState({ ...state, status: event.target.value })} placeholder="Status" />
      </div>
      <div className="inline-actions">
        <Button type="submit">Search</Button>
        <Button variant="ghost" type="button" onClick={() => onSubmit({ q: "", domain: "", pageType: "", freshness: "", confidence: "", status: "" })}>
          Clear
        </Button>
      </div>
    </form>
  );
}

function MarkdownView({ markdown }) {
  const blocks = useMemo(() => renderMarkdownBlocks(markdown), [markdown]);
  return <div className="markdown">{blocks}</div>;
}

function renderMarkdownBlocks(markdown) {
  const lines = String(markdown || "").split(/\r?\n/);
  const nodes = [];
  let paragraph = [];
  let listItems = [];
  let codeFence = null;
  let codeLines = [];

  const flushParagraph = () => {
    if (!paragraph.length) return;
    nodes.push(
      <p key={`p-${nodes.length}`} className="md-paragraph">
        {renderInline(paragraph.join(" "))}
      </p>
    );
    paragraph = [];
  };

  const flushList = () => {
    if (!listItems.length) return;
    nodes.push(
      <ul key={`ul-${nodes.length}`} className="md-list">
        {listItems.map((item, index) => (
          <li key={`${item}-${index}`}>{renderInline(item)}</li>
        ))}
      </ul>
    );
    listItems = [];
  };

  const flushCode = () => {
    if (!codeFence) return;
    nodes.push(
      <pre key={`code-${nodes.length}`} className="md-code">
        <code>{codeLines.join("\n")}</code>
      </pre>
    );
    codeFence = null;
    codeLines = [];
  };

  lines.forEach((line) => {
    const trimmed = line.trimEnd();
    if (codeFence) {
      if (trimmed.startsWith("```")) {
        flushCode();
      } else {
        codeLines.push(line);
      }
      return;
    }

    if (!trimmed) {
      flushParagraph();
      flushList();
      return;
    }
    if (trimmed.startsWith("```")) {
      flushParagraph();
      flushList();
      codeFence = trimmed;
      return;
    }
    const headingMatch = trimmed.match(/^(#{1,3})\s+(.*)$/);
    if (headingMatch) {
      flushParagraph();
      flushList();
      const level = headingMatch[1].length;
      const Tag = `h${Math.min(level + 1, 4)}`;
      nodes.push(
        <Tag key={`h-${nodes.length}`} className="md-heading">
          {renderInline(headingMatch[2])}
        </Tag>
      );
      return;
    }
    if (trimmed.startsWith("- ")) {
      flushParagraph();
      listItems.push(trimmed.slice(2));
      return;
    }
    if (trimmed.startsWith("> ")) {
      flushParagraph();
      flushList();
      nodes.push(
        <blockquote key={`quote-${nodes.length}`} className="md-quote">
          {renderInline(trimmed.slice(2))}
        </blockquote>
      );
      return;
    }
    paragraph.push(trimmed);
  });

  flushParagraph();
  flushList();
  flushCode();
  return nodes;
}

function renderInline(text) {
  const parts = [];
  const pattern = /\[([^\]]+)\]\(([^)]+)\)/g;
  let index = 0;
  let match;
  while ((match = pattern.exec(text))) {
    if (match.index > index) {
      parts.push(text.slice(index, match.index));
    }
    parts.push(
      <a key={`${match.index}-${match[2]}`} href={match[2]}>
        {match[1]}
      </a>
    );
    index = match.index + match[0].length;
  }
  if (index < text.length) {
    parts.push(text.slice(index));
  }
  return parts.length ? parts : text;
}

function InfoBlock({ title, items }) {
  return (
    <section className="aside-block">
      <h3>{title}</h3>
      {items.length ? (
        <div className="chip-row">
          {items.map((item) => (
            <span key={item} className="chip">
              {item}
            </span>
          ))}
        </div>
      ) : (
        <EmptyMini label="No data projected." />
      )}
    </section>
  );
}

function RelatedBlock({ title, items, emptyLabel, onOpen }) {
  return (
    <section className="aside-block">
      <h3>{title}</h3>
      {items.length ? (
        <div className="related-list">
          {items.map((item) => (
            <button key={item.slug} className="related-card" onClick={() => onOpen(item.slug)}>
              <div className="row-title">{item.title}</div>
              <div className="row-subtitle">{item.slug}</div>
              <StatusPills page={item} />
            </button>
          ))}
        </div>
      ) : (
        <EmptyMini label={emptyLabel} />
      )}
    </section>
  );
}

function FacetSummary({ facets }) {
  return (
    <div className="facet-grid">
      <FacetCard label="Domains" entries={facets.domains} />
      <FacetCard label="Families" entries={facets.page_types} />
      <FacetCard label="Freshness" entries={facets.freshness} />
      <FacetCard label="Confidence" entries={facets.confidence} />
      <FacetCard label="Status" entries={facets.status} />
    </div>
  );
}

function FacetCard({ label, entries }) {
  return (
    <div className="facet-card">
      <div className="facet-title">{label}</div>
      <div className="facet-items">
        {Object.keys(entries).length ? (
          Object.entries(entries).map(([key, value]) => (
            <div key={key} className="facet-item">
              <span>{key}</span>
              <Badge tone="info">{value}</Badge>
            </div>
          ))
        ) : (
          <EmptyMini label="No matches." />
        )}
      </div>
    </div>
  );
}

function StatusPills({ page }) {
  return (
    <div className="status-pills">
      <Badge tone={toneForStatus(page.status)}>{page.status}</Badge>
      <Badge tone={toneForFreshness(page.freshness)}>{page.freshness}</Badge>
      <Badge tone={toneForConfidence(page.confidence)}>{page.confidence}</Badge>
    </div>
  );
}

function Panel({ title, eyebrow, children }) {
  return (
    <section className="panel">
      {eyebrow ? <div className="panel-eyebrow">{eyebrow}</div> : null}
      {title ? <h2 className="panel-title">{title}</h2> : null}
      <div className="panel-body">{children}</div>
    </section>
  );
}

function MetricGrid({ items }) {
  return (
    <div className="metric-grid">
      {items.map((item) => (
        <div key={item.label} className="metric-card">
          <div className="metric-label">{item.label}</div>
          <div className="metric-value">{item.value}</div>
        </div>
      ))}
    </div>
  );
}

function Badge({ tone = "neutral", children }) {
  return <span className={`badge badge-${tone}`}>{children}</span>;
}

function Button({ children, variant = "primary", ...props }) {
  return (
    <button className={`button button-${variant}`} {...props}>
      {children}
    </button>
  );
}

function EmptyState({ title, description }) {
  return (
    <div className="empty-state">
      <div className="row-title">{title}</div>
      <div className="row-subtitle">{description}</div>
    </div>
  );
}

function EmptyMini({ label }) {
  return <div className="empty-mini">{label}</div>;
}

function LoadingState({ label }) {
  return <div className="loading-state">{label}</div>;
}

function ErrorState({ error, onRetry }) {
  return (
    <div className="error-state">
      <div className="row-title">Backend request failed</div>
      <div className="row-subtitle">{error?.message || String(error)}</div>
      {onRetry ? (
        <div className="inline-actions">
          <Button onClick={onRetry}>Retry</Button>
        </div>
      ) : null}
    </div>
  );
}

function useResource(loader, deps) {
  const [state, setState] = useState({ loading: true, data: null, error: null });

  useEffect(() => {
    let active = true;
    const controller = new AbortController();
    setState({ loading: true, data: null, error: null });
    loader(controller.signal)
      .then((data) => {
        if (active) {
          setState({ loading: false, data, error: null });
        }
      })
      .catch((error) => {
        if (active && error.name !== "AbortError") {
          setState({ loading: false, data: null, error });
        }
      });
    return () => {
      active = false;
      controller.abort();
    };
  }, deps); // eslint-disable-line react-hooks/exhaustive-deps

  return state;
}

function chromeForRoute(route) {
  if (route.name === "page") {
    return {
      title: "Page view",
      copy: "Read the finalized markdown, inspect related pages, and follow backlinks without any maintenance controls.",
      badges: [
        { label: "Read-only", tone: "success" },
        { label: "Finalized", tone: "info" },
      ],
    };
  }
  if (route.name === "search") {
    return {
      title: "Search results",
      copy: "Discover finalized knowledge with facet-aware filtering, freshness indicators, and canonical page links.",
      badges: [
        { label: "Search", tone: "info" },
        { label: "Browse", tone: "success" },
      ],
    };
  }
  return {
    title: "Browse finalized knowledge",
    copy: "Traverse the Infopedia tree to see what exists, what is authoritative, and where to read next.",
    badges: [
      { label: "Tree", tone: "info" },
      { label: "Read only", tone: "success" },
    ],
  };
}

function toneForStatus(status) {
  if (status === "finalized") return "success";
  if (status === "draft") return "warn";
  if (status === "deprecated") return "danger";
  return "neutral";
}

function toneForFreshness(freshness) {
  if (freshness === "current") return "success";
  if (freshness === "stale") return "warn";
  if (freshness === "missing") return "danger";
  return "neutral";
}

function toneForConfidence(confidence) {
  if (confidence === "high") return "success";
  if (confidence === "medium") return "warn";
  if (confidence === "low") return "danger";
  return "neutral";
}

export { chromeForRoute, parseRoute, renderMarkdownBlocks };
export default App;
