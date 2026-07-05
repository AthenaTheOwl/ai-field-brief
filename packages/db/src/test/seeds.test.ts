import { describe, expect, it } from "vitest";

import { loadSourceRegistry } from "@aifieldbrief/sources/ops";

import {
  distinctRegistryTypes,
  loadSeedSources,
  REGISTRY_PATH,
  REGISTRY_TYPE_TO_SOURCE_TYPE,
} from "../seeds/sources-from-registry";

describe("source registry seed loader", () => {
  it("reads the seed registry and returns workspace-scoped payloads", () => {
    const rows = loadSeedSources("00000000-0000-4000-8000-000000000001");
    // Derived from the registry (loadSeedSources maps sources 1:1) so this
    // never drifts when the registry grows — the old hardcoded 173 broke CI.
    expect(rows).toHaveLength(loadSourceRegistry(REGISTRY_PATH).sources.length);
    expect(rows.length).toBeGreaterThan(0);
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
