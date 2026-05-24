import { describe, expect, it } from "vitest";

import { canonicalizeUrl } from "../src/canonicalize";

describe("canonicalizeUrl", () => {
  it("strips utm params", () => {
    expect(canonicalizeUrl("https://example.com/a?utm_source=x&b=2")).toBe(
      "https://example.com/a?b=2",
    );
  });

  it("case-folds the host", () => {
    expect(canonicalizeUrl("https://EXAMPLE.com/a")).toBe("https://example.com/a");
  });

  it("trims a trailing slash from non-root paths", () => {
    expect(canonicalizeUrl("https://example.com/a/")).toBe("https://example.com/a");
  });

  it("keeps an already-canonical URL unchanged", () => {
    expect(canonicalizeUrl("https://example.com/a?b=2")).toBe("https://example.com/a?b=2");
  });

  it("handles unicode paths through URL encoding", () => {
    expect(canonicalizeUrl("https://example.com/ümlaut")).toBe(
      "https://example.com/%C3%BCmlaut",
    );
  });

  it("sorts query keys", () => {
    expect(canonicalizeUrl("https://example.com/a?z=1&a=2")).toBe(
      "https://example.com/a?a=2&z=1",
    );
  });
});
