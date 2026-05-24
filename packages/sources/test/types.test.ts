import { readFileSync } from "node:fs";

import { describe, expect, it } from "vitest";

import { SOURCE_TYPES } from "../src";

describe("SourceType", () => {
  it("matches the JSON Schema enum", () => {
    const schema = JSON.parse(
      readFileSync(new URL("../schemas/source-item.schema.json", import.meta.url), "utf8"),
    ) as { properties?: { source_type?: { enum?: string[] } } };
    expect(new Set(schema.properties?.source_type?.enum ?? [])).toEqual(
      new Set(SOURCE_TYPES),
    );
  });
});
