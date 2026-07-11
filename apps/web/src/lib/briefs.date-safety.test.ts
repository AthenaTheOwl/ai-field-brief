import { describe, expect, it } from "vitest";

import { listBriefs } from "./briefs";

function isoWeekFor(dateText: string): string {
  const parts = dateText.split("-").map(Number);
  if (parts.length !== 3 || parts.some((part) => !Number.isInteger(part))) {
    throw new Error(`invalid ISO date: ${dateText}`);
  }
  const [year, month, day] = parts as [number, number, number];
  const date = new Date(Date.UTC(year, month - 1, day));
  const weekday = (date.getUTCDay() + 6) % 7;
  date.setUTCDate(date.getUTCDate() - weekday + 3);
  const isoYear = date.getUTCFullYear();
  const firstThursday = new Date(Date.UTC(isoYear, 0, 4));
  const firstWeekday = (firstThursday.getUTCDay() + 6) % 7;
  firstThursday.setUTCDate(firstThursday.getUTCDate() - firstWeekday + 3);
  const week = 1 + Math.round((date.getTime() - firstThursday.getTime()) / 604_800_000);
  return `${isoYear}-W${String(week).padStart(2, "0")}`;
}

/**
 * eval-001 (promoted from 2026-W21 dream).
 *
 * js-yaml's DEFAULT_SCHEMA parses an ISO-date scalar into a real `Date`,
 * which React's reconciler throws on at render time. The fix in
 * `briefs.ts` passes `{ schema: yaml.JSON_SCHEMA }` so date scalars stay
 * strings. This test pins that invariant: every date-shaped field on a
 * `BriefMeta` survives the load path as a string (or null).
 *
 * A future refactor that loses the JSON_SCHEMA argument compiles,
 * type-checks, and breaks the production render silently — until this
 * test fires.
 */
describe("briefs meta dates survive serialization", () => {
  it("no Date objects survive loadYaml", () => {
    const briefs = listBriefs();
    for (const b of briefs) {
      if (!b.meta) continue;
      // through_date and generated_at are YAML date / date-time literals
      // in the source meta.yaml; they must remain strings after the
      // JSON_SCHEMA-scoped load so React can render them.
      expect(
        typeof b.meta.through_date === "string" || b.meta.through_date == null,
      ).toBe(true);
      expect(
        typeof b.meta.generated_at === "string" || b.meta.generated_at == null,
      ).toBe(true);
      // Per-source last_item_date entries are the second class of date
      // scalar that would silently become a Date under DEFAULT_SCHEMA.
      for (const src of b.meta.sources_reviewed ?? []) {
        expect(
          typeof src.last_item_date === "string" || src.last_item_date == null,
        ).toBe(true);
      }
    }
  });

  it("folder, metadata, and through date name the same ISO week", () => {
    for (const brief of listBriefs()) {
      expect(brief.meta).not.toBeNull();
      expect(brief.week).toBe(brief.meta?.iso_week);
      expect(brief.meta?.iso_week).toBe(isoWeekFor(brief.date));
    }
  });
});
