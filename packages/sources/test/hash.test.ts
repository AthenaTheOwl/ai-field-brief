import { describe, expect, it } from "vitest";

import { contentHash } from "../src/hash";

describe("contentHash", () => {
  it("is deterministic for the same input", () => {
    const input = {
      title: "A",
      canonicalUrl: "https://example.com/a",
      body: "body",
    };
    expect(contentHash(input)).toBe(contentHash(input));
  });

  it("changes when the body changes", () => {
    const base = contentHash({
      title: "A",
      canonicalUrl: "https://example.com/a",
      body: "body",
    });
    const changed = contentHash({
      title: "A",
      canonicalUrl: "https://example.com/a",
      body: "changed",
    });
    expect(changed).not.toBe(base);
  });
});
