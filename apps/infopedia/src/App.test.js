import { describe, expect, it } from "vitest";
import { chromeForRoute, parseRoute } from "./App.jsx";

describe("Infopedia routes", () => {
  it("parses page routes", () => {
    expect(parseRoute("/page/net-revenue-retention", "?domain=customer-revenue")).toEqual({
      name: "page",
      slug: "net-revenue-retention",
      domain: "customer-revenue",
      q: "",
      pageType: "",
      freshness: "",
      confidence: "",
      status: "",
    });
  });

  it("parses search routes with filters", () => {
    expect(parseRoute("/search", "?q=nrr&domain=customer-revenue&page_type=metric")).toEqual({
      name: "search",
      q: "nrr",
      domain: "customer-revenue",
      pageType: "metric",
      freshness: "",
      confidence: "",
      status: "",
    });
  });
});

describe("Infopedia chrome", () => {
  it("describes browse mode as read only", () => {
    const chrome = chromeForRoute({ name: "browse" });
    expect(chrome.copy).toContain("tree");
    expect(chrome.badges[1].label).toContain("Read");
  });
});
