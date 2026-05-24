import type { Connector, FetchCtx } from "../contract";
import { NotImplementedError } from "../contract";
import { registerConnector } from "../registry";
import { SOURCE_TYPES, type SourceItem, type SourceType } from "../types";

const IMPLEMENTED = new Set<SourceType>([
  "rss",
  "podcast-rss",
  "article-url",
  "github-releases",
]);

function createStubConnector(sourceType: SourceType): Connector<unknown> {
  return {
    sourceType,
    version: "0.0.0-stub",
    async fetch(_ctx: FetchCtx<unknown>): Promise<SourceItem[]> {
      throw new NotImplementedError(sourceType);
    },
  };
}

for (const sourceType of SOURCE_TYPES) {
  if (!IMPLEMENTED.has(sourceType)) {
    registerConnector(createStubConnector(sourceType));
  }
}
