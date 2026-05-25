import { describe, expect, it } from "vitest";

import { buildSourceOpsQueue, mapRegistryTypeToSourceType } from "../src/ops";

const AS_OF = new Date("2026-05-25T12:00:00Z");

describe("source ops queue", () => {
  it("builds readiness rows from the current source registry", () => {
    const queue = buildSourceOpsQueue({ asOf: AS_OF });

    expect(queue.summary.total).toBe(15);
    expect(queue.summary.ready).toBe(15);
    expect(queue.summary.connectorBlocked).toBe(0);
    expect(queue.summary.reviewDue).toBe(0);

    const cookbook = queue.rows.find((row) => row.id === "openai-cookbook");
    expect(cookbook).toMatchObject({
      lane: "primary-source",
      registryType: "github-releases",
      sourceType: "github-releases",
      connectorType: "github-releases",
      connectorImplemented: true,
      readinessStatus: "ready",
      freshnessStatus: "fresh",
    });
  });

  it("keeps registry type mapping deterministic", () => {
    expect(mapRegistryTypeToSourceType("vendor-news")).toBe("rss");
    expect(mapRegistryTypeToSourceType("podcast+newsletter")).toBe("podcast-rss");
    expect(mapRegistryTypeToSourceType("youtube-channel")).toBe("youtube-channel");
    expect(mapRegistryTypeToSourceType("missing-type")).toBeNull();
  });

  it("reports stale registry review and stub connectors without fetching", () => {
    const queue = buildSourceOpsQueue({
      asOf: AS_OF,
      registryText: `
version: 1
sources:
  - id: old-rss
    name: Old RSS
    type: blog
    lane: fast-signal
    url: https://example.com/feed
    cadence: weekly
    review_frequency: weekly
    intake: full
    status: active
    last_reviewed: 2026-05-01
  - id: youtube-source
    name: YouTube Source
    type: youtube-channel
    lane: fast-signal
    url: https://example.com/channel
    cadence: weekly
    review_frequency: weekly
    intake: full
    status: active
    last_reviewed: 2026-05-24
  - id: missing-source
    name: Missing Source
    type: custom-wire
    lane: fast-signal
    url: https://example.com/custom
    cadence: weekly
    review_frequency: weekly
    intake: full
    status: active
    last_reviewed: 2026-05-24
`,
    });

    expect(queue.summary.total).toBe(3);
    expect(queue.summary.reviewDue).toBe(1);
    expect(queue.summary.connectorBlocked).toBe(2);
    expect(queue.rows.map((row) => row.readinessStatus)).toEqual([
      "review-due",
      "connector-stub",
      "mapping-missing",
    ]);
  });
});
