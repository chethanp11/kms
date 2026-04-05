const domain = "customer-revenue-analytics";

const pages = [
  {
    slug: "net-revenue-retention",
    title: "Net Revenue Retention",
    page_type: "metric",
    domain,
    freshness: "current",
    confidence: "high",
    status: "finalized",
    updated_at: "2026-04-05",
    path: "/wiki/metrics/customer-revenue-analytics/net-revenue-retention.md",
    source_trace_summary: [
      "Primary interpretation artifact: Net Revenue Retention Source Note",
      "Supporting raw source: /sources/reports/q4-revenue-ops-review.md",
      "Validation reference: Net Revenue Retention Source Reconciliation",
    ],
    related_slugs: [
      "net-revenue-retention-source-note",
      "monthly-revenue-close",
      "sales-orders-fact",
      "net-revenue-retention-clarification",
    ],
    backlink_slugs: ["net-revenue-retention-source-note"],
    sibling_slugs: ["net-revenue-retention-source-note", "net-revenue-retention-clarification"],
    snippet:
      "Net Revenue Retention measures how much recurring revenue is retained and expanded within an existing customer cohort.",
    content_markdown: `---
title: Net Revenue Retention
slug: net-revenue-retention
type: metric
domain: customer-revenue-analytics
status: finalized
confidence: high
review_required: false
---

# Net Revenue Retention

## Summary

Net Revenue Retention measures how much recurring revenue is retained and expanded within an existing customer cohort over a defined period.

## Current Understanding

The metric is governed by the monthly close process and the sales orders fact source.

## Source Trace

- Primary interpretation artifact: [Net Revenue Retention Source Note](/wiki/source-notes/customer-revenue-analytics/net-revenue-retention-source-note.md)
- Supporting raw source: \`/sources/reports/q4-revenue-ops-review.md\`
- Supporting raw source: \`/sources/meeting-notes/revenue-reviews/2026-03-28.md\`
`,
  },
  {
    slug: "net-revenue-retention-source-note",
    title: "Net Revenue Retention Source Note",
    page_type: "source-note",
    domain,
    freshness: "current",
    confidence: "medium",
    status: "finalized",
    updated_at: "2026-04-05",
    path: "/wiki/source-notes/customer-revenue-analytics/net-revenue-retention-source-note.md",
    source_trace_summary: ["Source reference: /sources/reports/nrr.csv", "Source reference: /sources/notes/revenue-note.md"],
    related_slugs: ["net-revenue-retention", "sales-orders-fact"],
    backlink_slugs: ["net-revenue-retention"],
    sibling_slugs: ["net-revenue-retention", "net-revenue-retention-clarification"],
    snippet: "NRR improved to 118% for enterprise accounts in Q4.",
    content_markdown: `---
title: Net Revenue Retention Source Note
slug: net-revenue-retention-source-note
type: source-note
domain: customer-revenue-analytics
status: finalized
confidence: medium
review_required: true
---

# Net Revenue Retention Source Note

## Summary

NRR improved to 118% for enterprise accounts in Q4.

## Source Details

Parsed from intake source files and the attached revenue note.

## Extracted Signals

- NRR
- enterprise accounts
- Q4 improvement
`,
  },
  {
    slug: "net-revenue-retention-clarification",
    title: "Net Revenue Retention Clarification",
    page_type: "open-question",
    domain,
    freshness: "stale",
    confidence: "provisional",
    status: "review_required",
    updated_at: "2026-04-05",
    path: "/wiki/open-questions/customer-revenue-analytics/net-revenue-retention-clarification.md",
    source_trace_summary: ["Source reference: /sources/reports/nrr.csv", "Source reference: /sources/notes/revenue-note.md"],
    related_slugs: ["net-revenue-retention", "net-revenue-retention-source-note"],
    backlink_slugs: ["net-revenue-retention"],
    sibling_slugs: ["net-revenue-retention", "net-revenue-retention-source-note"],
    snippet: "A clarification is needed on whether the Q4 NRR value should include one-time adjustments.",
    content_markdown: `---
title: Net Revenue Retention Clarification
slug: net-revenue-retention-clarification
type: open-question
domain: customer-revenue-analytics
status: review_required
confidence: provisional
review_required: true
---

# Net Revenue Retention Clarification

## Summary

A clarification is needed on whether the Q4 NRR value should include one-time adjustments.

## Why Unresolved

The current evidence does not establish an approved treatment for one-time adjustments.
`,
  },
  {
    slug: "monthly-revenue-close",
    title: "Monthly Revenue Close",
    page_type: "process",
    domain,
    freshness: "current",
    confidence: "high",
    status: "finalized",
    updated_at: "2026-04-05",
    path: "/wiki/processes/customer-revenue-analytics/monthly-revenue-close.md",
    source_trace_summary: ["Operational control: monthly revenue close checklist", "Governed owner: revenue operations"],
    related_slugs: ["net-revenue-retention", "sales-orders-fact"],
    backlink_slugs: ["net-revenue-retention"],
    sibling_slugs: ["sales-orders-fact", "net-revenue-retention"],
    snippet: "The monthly close process governs how recurring revenue is verified and finalized.",
    content_markdown: `---
title: Monthly Revenue Close
slug: monthly-revenue-close
type: process
domain: customer-revenue-analytics
status: finalized
confidence: high
review_required: false
---

# Monthly Revenue Close

## Summary

The monthly close process governs how recurring revenue is verified and finalized.
`,
  },
  {
    slug: "sales-orders-fact",
    title: "Sales Orders Fact",
    page_type: "data-asset",
    domain,
    freshness: "current",
    confidence: "high",
    status: "finalized",
    updated_at: "2026-04-05",
    path: "/wiki/data-assets/customer-revenue-analytics/sales-orders-fact.md",
    source_trace_summary: ["Source system: sales orders warehouse extract", "Quality check: revenue fact reconciliation"],
    related_slugs: ["net-revenue-retention", "monthly-revenue-close"],
    backlink_slugs: ["net-revenue-retention", "net-revenue-retention-source-note"],
    sibling_slugs: ["monthly-revenue-close", "net-revenue-retention"],
    snippet: "Canonical fact source for sales orders used by revenue analytics.",
    content_markdown: `---
title: Sales Orders Fact
slug: sales-orders-fact
type: data-asset
domain: customer-revenue-analytics
status: finalized
confidence: high
review_required: false
---

# Sales Orders Fact

## Summary

Canonical fact source for sales orders used by revenue analytics.
`,
  },
];

const pageBySlug = new Map(pages.map((page) => [page.slug, page]));

function linkPage(slug) {
  const page = pageBySlug.get(slug);
  if (!page) {
    return null;
  }
  return {
    slug: page.slug,
    title: page.title,
    domain: page.domain,
    page_type: page.page_type,
    freshness: page.freshness,
    confidence: page.confidence,
    status: page.status,
    related_count: page.related_slugs.length,
    backlink_count: page.backlink_slugs.length,
    updated_at: page.updated_at,
  };
}

function groupPages() {
  const grouped = new Map();
  for (const page of pages) {
    const domainBucket = grouped.get(page.domain) || new Map();
    const familyBucket = domainBucket.get(page.page_type) || [];
    familyBucket.push(page);
    domainBucket.set(page.page_type, familyBucket);
    grouped.set(page.domain, domainBucket);
  }
  return grouped;
}

function buildTree(domainFilter) {
  const grouped = groupPages();
  const domains = [];
  for (const [domainName, families] of [...grouped.entries()].sort(([a], [b]) => a.localeCompare(b))) {
    if (domainFilter && domainFilter !== domainName) {
      continue;
    }
    const children = [...families.entries()]
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([pageType, familyPages]) => ({
        page_type: pageType,
        title: titleizeFamily(pageType),
        count: familyPages.length,
        pages: familyPages
          .slice()
          .sort((a, b) => a.title.localeCompare(b.title))
          .map(linkPage)
          .filter(Boolean),
      }));
    domains.push({
      domain: domainName,
      title: titleizeDomain(domainName),
      count: children.reduce((total, child) => total + child.count, 0),
      children,
    });
  }

  return {
    generated_at: "2026-04-05T00:00:00Z",
    summary: {
      page_count: domains.reduce((total, bucket) => total + bucket.count, 0),
      domain_count: domains.length,
    },
    domains,
  };
}

function buildSearch(params = {}) {
  const query = String(params.q || "").trim().toLowerCase();
  const domain = params.domain || "";
  const pageType = params.page_type || "";
  const freshness = params.freshness || "";
  const confidence = params.confidence || "";
  const status = params.status || "";

  const filtered = pages.filter((page) => {
    if (domain && page.domain !== domain) return false;
    if (pageType && page.page_type !== pageType) return false;
    if (freshness && page.freshness !== freshness) return false;
    if (confidence && page.confidence !== confidence) return false;
    if (status && page.status !== status) return false;
    if (!query) return true;
    return [page.title, page.snippet, page.content_markdown, page.domain, page.page_type].join(" ").toLowerCase().includes(query);
  });

  return {
    generated_at: "2026-04-05T00:00:00Z",
    query: params.q || "",
    filters: {
      domain: domain || null,
      page_type: pageType || null,
      freshness: freshness || null,
      confidence: confidence || null,
      status: status || null,
      scope: params.scope || "wiki",
    },
    total: filtered.length,
    items: filtered
      .slice()
      .sort((a, b) => a.title.localeCompare(b.title))
      .map((page) => ({
        slug: page.slug,
        title: page.title,
        domain: page.domain,
        page_type: page.page_type,
        freshness: page.freshness,
        confidence: page.confidence,
        status: page.status,
        updated_at: page.updated_at,
        snippet: page.snippet,
        related_count: page.related_slugs.length,
        backlink_count: page.backlink_slugs.length,
      })),
    facets: buildFacets(filtered),
  };
}

function buildPage(slug) {
  const page = pageBySlug.get(slug);
  if (!page) {
    throw new Error(`Offline Infopedia page fixture not found for slug: ${slug}`);
  }
  return {
    generated_at: "2026-04-05T00:00:00Z",
    page: {
      slug: page.slug,
      title: page.title,
      domain: page.domain,
      page_type: page.page_type,
      freshness: page.freshness,
      confidence: page.confidence,
      status: page.status,
      updated_at: page.updated_at,
      path: page.path,
      related_count: page.related_slugs.length,
      backlink_count: page.backlink_slugs.length,
      current_revision_id: `fixture-${page.slug}`,
    },
    breadcrumbs: [
      { title: "Infopedia", slug: "/" },
      { title: titleizeDomain(page.domain), slug: `/search?domain=${encodeURIComponent(page.domain)}` },
      { title: titleizeFamily(page.page_type), slug: `/search?domain=${encodeURIComponent(page.domain)}&page_type=${encodeURIComponent(page.page_type)}` },
      { title: page.title, slug: `/page/${encodeURIComponent(page.slug)}?domain=${encodeURIComponent(page.domain)}` },
    ],
    content_markdown: page.content_markdown,
    source_trace_summary: page.source_trace_summary,
    related_pages: page.related_slugs.map(linkPage).filter(Boolean),
    backlinks: page.backlink_slugs.map(linkPage).filter(Boolean),
    siblings: page.sibling_slugs.map(linkPage).filter(Boolean),
  };
}

function buildFacets(items) {
  const facets = {
    domains: {},
    page_types: {},
    freshness: {},
    confidence: {},
    status: {},
  };
  for (const item of items) {
    facets.domains[item.domain] = (facets.domains[item.domain] || 0) + 1;
    facets.page_types[item.page_type] = (facets.page_types[item.page_type] || 0) + 1;
    facets.freshness[item.freshness] = (facets.freshness[item.freshness] || 0) + 1;
    facets.confidence[item.confidence] = (facets.confidence[item.confidence] || 0) + 1;
    facets.status[item.status] = (facets.status[item.status] || 0) + 1;
  }
  return facets;
}

function titleizeDomain(value) {
  return String(value)
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function titleizeFamily(value) {
  return String(value)
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export function getOfflineInfopediaTree(params = {}) {
  return buildTree(params.domain || undefined);
}

export function getOfflineInfopediaSearch(params = {}) {
  return buildSearch(params);
}

export function getOfflineInfopediaPage(slug) {
  return buildPage(slug);
}

