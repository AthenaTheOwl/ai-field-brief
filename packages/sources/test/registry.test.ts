import { describe, expect, it } from "vitest";

import {
  getConnector,
  listRegisteredSourceTypes,
  NotImplementedError,
  SOURCE_TYPES,
  type SourceType,
} from "../src";

const FULL_CONNECTORS = new Set<SourceType>([
  "rss",
  "podcast-rss",
  "article-url",
  "github-releases",
]);

describe("connector registry", () => {
  it("registers every SourceType", () => {
    expect(new Set(listRegisteredSourceTypes())).toEqual(new Set(SOURCE_TYPES));
  });

  it("stub connectors throw NotImplementedError", async () => {
    const stubType = SOURCE_TYPES.find((sourceType) => !FULL_CONNECTORS.has(sourceType));
    expect(stubType).toBeTruthy();
    if (!stubType) {
      throw new Error("expected at least one stub connector");
    }
    await expect(
      getConnector(stubType).fetch({
        workspaceId: "00000000-0000-4000-8000-000000000001",
        sourceId: "aaaaaaaa-0000-4000-8000-000000000001",
        config: {},
        raw: { kind: "bytes", text: "" },
      }),
    ).rejects.toThrow(NotImplementedError);
  });
});
