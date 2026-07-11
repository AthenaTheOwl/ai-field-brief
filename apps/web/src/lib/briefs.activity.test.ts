import { describe, expect, it } from "vitest";

import { formatBriefActivity, listBriefs, type BriefMeta } from "./briefs";

describe("brief activity summary", () => {
  it("uses aggregate sweep fields from the current metadata shape", () => {
    const meta = {
      iso_week: "2026-W27",
      through_date: "2026-06-30",
      generated_at: "2026-06-30T19:40:00Z",
      generated_by: "test",
      title: "Frameworks are becoming the control plane for agent work",
      volume: 9,
      sweep: { attempted: 32, succeeded: 28, failed: 4 },
      top_signal_count: 7,
      action_packet_count: 5,
      sources_reviewed: [
        { label: "LangChain Blog", disposition: "registry_addition" },
      ],
    } satisfies BriefMeta;

    expect(formatBriefActivity(meta)).toBe(
      "28 of 32 sources swept, 7 Top signals, 5 action packets.",
    );
  });

  it("falls back to per-source status counts for older metadata", () => {
    const meta = {
      iso_week: "2026-W21",
      through_date: "2026-05-22",
      generated_at: "2026-05-22T00:00:00Z",
      generated_by: "test",
      title: "Contract speed, not model speed",
      volume: 2,
      sources_reviewed: [
        { label: "one", status: "ok", items_included: 2 },
        { label: "two", status: "failed", items_included: 0 },
        { label: "three", status: "ok", items_included: 1 },
      ],
    } satisfies BriefMeta;

    expect(formatBriefActivity(meta)).toBe("2 sources swept, 3 items included.");
  });

  it("keeps the newest checked-in brief from rendering as zero sources", () => {
    const latest = listBriefs()[0];
    if (!latest) {
      throw new Error("expected at least one checked-in brief fixture");
    }
    if (!latest.meta?.sweep) {
      throw new Error("expected newest brief fixture to use aggregate sweep metadata");
    }

    const activity = formatBriefActivity(latest.meta);

    expect(latest.week).toMatch(/^\d{4}-W\d{2}$/);
    expect(activity).toContain(
      `${latest.meta.sweep.succeeded} of ${latest.meta.sweep.attempted} sources swept`,
    );
    // Word-boundary match: a literal `toContain("0 sources")` false-positives
    // on legitimate counts like "16 of 20 sources swept" (W29). The guard is
    // for a standalone zero, so anchor it against a preceding digit.
    expect(activity).not.toMatch(/(?<!\d)0 sources/);
  });
});
