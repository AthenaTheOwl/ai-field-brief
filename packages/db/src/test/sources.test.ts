import { describe, expect, it } from "vitest";

import {
  createSource,
  getSource,
  listSources,
  retireSource,
  SourceTypeError,
  updateSource,
} from "../queries/sources";
import { TenantScopeError } from "../queries/workspaces";

const undef = undefined as unknown as string;
const blank = "";
const sourceInput = {
  name: "Anthropic News",
  type: "rss" as const,
  lane: "primary-source",
  url: "https://www.anthropic.com/news",
  cadence: "irregular",
  intake: "full",
  status: "active",
};

describe("source query helpers refuse missing workspaceId", () => {
  it("listSources throws on undefined", async () => {
    await expect(listSources(undef)).rejects.toThrow(TenantScopeError);
  });

  it("getSource throws on blank", async () => {
    await expect(getSource(blank, "source-1")).rejects.toThrow(TenantScopeError);
  });

  it("createSource throws on undefined", async () => {
    await expect(createSource(undef, sourceInput)).rejects.toThrow(TenantScopeError);
  });

  it("updateSource throws on blank", async () => {
    await expect(updateSource(blank, "source-1", { name: "x" })).rejects.toThrow(
      TenantScopeError,
    );
  });

  it("retireSource throws on undefined", async () => {
    await expect(retireSource(undef, "source-1")).rejects.toThrow(TenantScopeError);
  });
});

describe("source type validation", () => {
  it("rejects source types outside the SourceType union before SQL", async () => {
    await expect(
      createSource("00000000-0000-4000-8000-000000000001", {
        ...sourceInput,
        type: "vendor-news" as "rss",
      }),
    ).rejects.toThrow(SourceTypeError);
  });
});
