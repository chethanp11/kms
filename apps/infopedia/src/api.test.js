import { afterEach, describe, expect, it, vi } from "vitest";
import { getInfopediaPage, getInfopediaSearch, getInfopediaTree } from "./api";

describe("Infopedia API fallback", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("falls back to local fixtures when the backend is unavailable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));

    const tree = await getInfopediaTree();
    expect(tree.summary.page_count).toBeGreaterThan(0);
    expect(tree.domains[0].children.length).toBeGreaterThan(0);

    const search = await getInfopediaSearch({ q: "Net Revenue Retention" });
    expect(search.total).toBeGreaterThan(0);
    expect(search.items[0].slug).toBeTruthy();

    const page = await getInfopediaPage("net-revenue-retention");
    expect(page.page.slug).toBe("net-revenue-retention");
    expect(page.content_markdown).toContain("Net Revenue Retention");
  });
});

