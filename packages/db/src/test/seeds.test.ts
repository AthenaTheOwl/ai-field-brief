import { describe, expect, it } from "vitest";

import {
  distinctRegistryTypes,
  loadSeedSources,
  REGISTRY_TYPE_TO_SOURCE_TYPE,
} from "../seeds/sources-from-registry";

describe("source registry seed loader", () => {
  it("reads the seed registry and returns workspace-scoped payloads", () => {
    const rows = loadSeedSources("00000000-0000-4000-8000-000000000001");
    expect(rows).toHaveLength(173);
    expect(rows.every((row) => row.workspaceId === "00000000-0000-4000-8000-000000000001")).toBe(
      true,
    );
    expect(rows.every((row) => row.name && row.url && row.type)).toBe(true);
    expect(rows.find((row) => row.name === "E2B GitHub")).toMatchObject({
      type: "github-releases",
      lane: "frontier-scout",
      signal: 4,
      actionability: 5,
      credibility: 4,
    });
  });

  it("maps every registry type to a canonical SourceType", () => {
    const types = distinctRegistryTypes();
    expect(types.length).toBeGreaterThan(0);
    for (const type of types) {
      expect(REGISTRY_TYPE_TO_SOURCE_TYPE[type]).toBeTruthy();
    }
  });
});
