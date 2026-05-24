import { describe, expect, it } from "vitest";

import { listBriefs } from "./briefs";

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
});
