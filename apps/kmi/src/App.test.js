import { describe, expect, it } from "vitest";
import { headerForRoute, parseRoute } from "./App.jsx";

describe("KMI routes", () => {
  it("parses contradiction detail routes", () => {
    expect(parseRoute("/runs/run_123/contradictions", "?contradiction=contr_001")).toEqual({
      name: "contradictions",
      runId: "run_123",
      contradictionId: "contr_001",
    });
  });

  it("parses diff review routes", () => {
    expect(parseRoute("/runs/run_123/diff-review", "?revision=rev_001")).toEqual({
      name: "diff-review",
      runId: "run_123",
      revisionId: "rev_001",
    });
  });
});

describe("KMI hero headers", () => {
  it("describes approval screens with governed publish language", () => {
    const header = headerForRoute({ name: "approvals" });
    expect(header.title).toContain("Approvals");
    expect(header.copy).toContain("/wiki");
  });
});
