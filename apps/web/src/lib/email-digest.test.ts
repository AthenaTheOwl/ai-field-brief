import { describe, expect, it, vi } from "vitest";

import type { BriefRecord } from "./briefs";
import {
  buildLatestDigestEmail,
  isAuthorizedCronRequest,
  readEmailConfig,
  sendDigestBroadcast,
  subscribeToDigest,
  validateSubscriberEmail,
} from "./email-digest";

const env = {
  RESEND_API_KEY: "re_test",
  RESEND_SEGMENT_ID: "seg_123",
  DIGEST_FROM_EMAIL: "ai-field-brief <brief@example.com>",
  CRON_SECRET: "cron-secret",
};

function brief(): BriefRecord {
  return {
    week: "2026-W21",
    title: "Contract speed, not model speed",
    volume: 2,
    date: "2026-05-22",
    markdown:
      "# Contract speed, not model speed\n\nAI is finishing its handshake with operators.",
    meta: {
      iso_week: "2026-W21",
      through_date: "2026-05-22",
      generated_at: "2026-05-22T00:00:00Z",
      generated_by: "test",
      title: "Contract speed, not model speed",
      volume: 2,
      sources_reviewed: [
        { id: "anthropic", status: "ok", items_included: 2 },
        { id: "openai", status: "ok", items_included: 1 },
      ],
    },
  };
}

function jsonFetch() {
  return vi.fn(async () =>
    new Response(JSON.stringify({ id: "ok" }), {
      status: 200,
      headers: { "content-type": "application/json" },
    }),
  );
}

describe("email digest", () => {
  it("validates and normalizes subscriber emails", () => {
    expect(validateSubscriberEmail(" PERSON@Example.COM ")).toBe(
      "person@example.com",
    );
    expect(() => validateSubscriberEmail("nope")).toThrow(/valid email/);
  });

  it("requires Resend digest configuration", () => {
    expect(readEmailConfig(env).segmentId).toBe("seg_123");
    expect(() => readEmailConfig({})).toThrow(/missing RESEND_API_KEY/);
  });

  it("builds a digest from the latest brief", () => {
    const digest = buildLatestDigestEmail([brief()]);

    expect(digest.week).toBe("2026-W21");
    expect(digest.subject).toContain("Contract speed");
    expect(digest.html).toContain("{{{RESEND_UNSUBSCRIBE_URL}}}");
    expect(digest.text).toContain("https://ai-field-brief.vercel.app/briefs/2026-W21");
  });

  it("subscribes contacts through Resend contacts API", async () => {
    const fetchImpl = jsonFetch();

    await subscribeToDigest({
      email: "reader@example.com",
      env,
      fetchImpl,
    });

    expect(fetchImpl).toHaveBeenCalledWith(
      "https://api.resend.com/contacts",
      expect.objectContaining({
        method: "POST",
        body: expect.stringContaining("reader@example.com"),
      }),
    );
    expect(fetchImpl).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        body: expect.stringContaining("seg_123"),
      }),
    );
  });

  it("creates and sends a broadcast for the weekly digest", async () => {
    const fetchImpl = jsonFetch();
    const digest = buildLatestDigestEmail([brief()]);

    await sendDigestBroadcast({ digest, env, fetchImpl });

    expect(fetchImpl).toHaveBeenCalledWith(
      "https://api.resend.com/broadcasts",
      expect.objectContaining({
        method: "POST",
        body: expect.stringContaining('"send":true'),
      }),
    );
  });

  it("checks cron bearer authorization", () => {
    const request = new Request("https://example.com", {
      headers: { authorization: "Bearer cron-secret" },
    });
    const rejected = new Request("https://example.com");

    expect(isAuthorizedCronRequest(request, env)).toBe(true);
    expect(isAuthorizedCronRequest(rejected, env)).toBe(false);
    expect(isAuthorizedCronRequest(request, {})).toBe(false);
  });
});
