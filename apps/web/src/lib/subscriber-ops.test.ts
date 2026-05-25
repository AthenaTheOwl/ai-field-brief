import { describe, expect, it } from "vitest";

import type { BriefRecord } from "./briefs";
import { buildSubscriberOpsStatus } from "./subscriber-ops";

function brief(): BriefRecord {
  return {
    week: "2026-W22",
    title: "The agents outran the humans downstream",
    volume: 3,
    date: "2026-05-29",
    markdown: "# The agents outran the humans downstream\n\nA brief.",
    meta: {
      iso_week: "2026-W22",
      through_date: "2026-05-29",
      generated_at: "2026-05-29T00:00:00Z",
      generated_by: "test",
      title: "The agents outran the humans downstream",
      volume: 3,
      sources_reviewed: [],
    },
  };
}

describe("subscriber ops status", () => {
  it("reports missing configuration without exposing secret values", () => {
    const status = buildSubscriberOpsStatus([brief()], {});

    expect(status.ready).toBe(false);
    expect(status.latest.week).toBe("2026-W22");
    expect(status.nextActions).toContain(
      "Set RESEND_API_KEY before sends can run.",
    );
    expect(JSON.stringify(status)).not.toContain("re_secret");
  });

  it("accepts legacy Resend env aliases", () => {
    const status = buildSubscriberOpsStatus(
      [brief()],
      {
        RESEND_API_KEY: "re_secret",
        RESEND_AUDIENCE_ID: "aud_123",
        RESEND_FROM_ADDRESS: "brief@example.com",
        CRON_SECRET: "cron_secret",
      },
    );

    expect(status.ready).toBe(true);
    expect(status.checks.every((check) => check.configured)).toBe(true);
    expect(status.nextActions[0]).toBe("Run the dry-run endpoint before Friday.");
  });
});
