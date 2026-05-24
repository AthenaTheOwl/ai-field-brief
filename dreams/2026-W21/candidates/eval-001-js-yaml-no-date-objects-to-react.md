---
id: eval-001-js-yaml-no-date-objects-to-react
target_kind: test_generation
spec_id: specs/0001-foundation
test_path: apps/web/src/lib/briefs.date-safety.test.ts
human_review_required: true
status: promoted
promotion_date: 2026-05-24
evidence:
  - kind: file
    ref: apps/web/src/lib/briefs.ts lines 70–72 — the comment "JSON_SCHEMA keeps dates as strings — otherwise React refuses to render the Date objects js-yaml deserializes by default" records the bug and the fix
  - kind: commit
    ref: c29b7ac — brief 2026-W21 rewrite + public reader; the public reader code is where the bug surfaced and the fix landed
  - kind: file
    ref: "briefs/2026-W21/meta.yaml — production fixture; carries `last_item_date: 2026-05-22` values that round-trip through js-yaml in the build pipeline"
---

## proposal

Add a regression test under `apps/web/src/test/briefs-meta-no-date-objects.test.ts` that loads `briefs/2026-W21/meta.yaml` via the production code path (`apps/web/src/lib/briefs.ts` `getBrief`) and asserts no field in the returned `BriefMeta` is a `Date` instance. The test fails the next time someone deletes the `{ schema: yaml.JSON_SCHEMA }` argument or swaps the YAML loader.

Proposed test skeleton (to be written and reviewed by a human, not auto-applied):

```ts
import { describe, it, expect } from "vitest";
import { getBrief } from "@/lib/briefs";

describe("brief meta yaml — no Date objects reach React", () => {
  it("getBrief('2026-W21') returns a meta with zero Date instances", () => {
    const record = getBrief("2026-W21");
    expect(record).not.toBeNull();
    const meta = record!.meta;
    expect(meta).not.toBeNull();
    walk(meta, (value, path) => {
      expect(value, `${path} is a Date object — React will refuse to render`).not.toBeInstanceOf(Date);
    });
  });
});

function walk(node: unknown, visit: (v: unknown, p: string) => void, path = "$") {
  if (node === null || node === undefined) return;
  if (typeof node !== "object") { visit(node, path); return; }
  if (node instanceof Date) { visit(node, path); return; }
  if (Array.isArray(node)) {
    node.forEach((item, i) => walk(item, visit, `${path}[${i}]`));
    return;
  }
  for (const [k, v] of Object.entries(node as Record<string, unknown>)) {
    visit(v, `${path}.${k}`);
    walk(v, visit, `${path}.${k}`);
  }
}
```

## why it earns its keep

The Date-object bug is the kind of regression that does not fail in unit tests because it does not throw — `js-yaml`'s default `DEFAULT_SCHEMA` returns a real `Date` for any ISO-date string, and React's reconciler throws at render time. The fix lives in one line of `briefs.ts` and one comment. A future refactor that loses the `JSON_SCHEMA` argument compiles, type-checks, and breaks the production build silently.

The test costs the build pipeline almost nothing (loads one YAML file and walks the object) and pins the contract: meta-yaml content stays string-typed through the read path. Without the test, the comment on line 70 of `briefs.ts` is the only memory of the bug.

## evidence

- `apps/web/src/lib/briefs.ts` lines 66–73:
  ```ts
  if (fs.existsSync(metaPath)) {
    const metaRaw = fs.readFileSync(metaPath, "utf8");
    // JSON_SCHEMA keeps dates as strings — otherwise React refuses to
    // render the Date objects js-yaml deserializes by default.
    meta = yaml.load(metaRaw, { schema: yaml.JSON_SCHEMA }) as BriefMeta;
  }
  ```
  The inline comment is the bug post-mortem. The test promotes it from a comment to a checked invariant.
- `c29b7ac` commit body: "BriefMarkdown component renders the body via react-markdown + remark-gfm; SiteNav + SiteFooter ship as shared chrome / meta panel under each brief shows sweep audit log". The render path that broke is the meta-panel render, which reads `BriefMeta` directly into JSX.
- `briefs/2026-W21/meta.yaml` carries six `last_item_date: YYYY-MM-DD` entries plus `iso_week`, `through_date`, and `generated_at`. Every one of those is a date-shaped string that js-yaml's default schema parses into a `Date`.
- `apps/web/src/test/env.test.ts` exists as a similar single-purpose vitest file; the new test follows the same shape (one describe block, no fixtures).

## promotion path

If approved, the change touches one new file plus one config check:

- `apps/web/src/test/briefs-meta-no-date-objects.test.ts` — new file with the proposed test.
- `apps/web/vitest.config.ts` — confirm the test glob already picks up `src/test/**`.
- `apps/web/package.json` — confirm `vitest` is in `devDependencies` (it is, per `env.test.ts`).
- No new dependencies.

Reviewer checks:

1. The test passes against the current `briefs/2026-W21/meta.yaml` (green baseline).
2. The test fails if the reviewer locally deletes the `{ schema: yaml.JSON_SCHEMA }` argument (red on regression).
3. The test name and the assertion message are self-documenting — a future failure points at the bug class without needing the dream report.
4. The walker handles nested objects and arrays without infinite recursion on a circular reference (the current `BriefMeta` is acyclic; the walker is conservative).

Owner role: `engineering.implementation`.

## risks if promoted blindly

- The test loads a real production fixture (`briefs/2026-W21/meta.yaml`). When the file gets pruned or rotated, the test fails for the wrong reason. Reviewer may want a synthetic fixture under `apps/web/src/test/fixtures/` instead.
- The walker scans every value in the meta object, which is fine today (the file is small) but could be slow when meta files grow. A bounded walker (max depth, max nodes) would be safer.
- The test only catches the Date-object failure mode. Other YAML-load surprises (BigInt, Symbol, RegExp from a custom tag) still slip through. Reviewer may want a stricter assertion: every leaf is `string | number | boolean | null`.
- The test is a content-shape test, not a render test. A change that returns a Date-shaped plain object (no `instanceof Date`) but still breaks React would pass this test. A full render test in a future pass would close the gap.
