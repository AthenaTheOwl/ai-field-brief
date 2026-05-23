---
id: DEC-FND-007-zod-env-validation-at-boot
spec: specs/0001-foundation/
requirement: R-FND-007
date: 2026-05-22
status: approved
reversible: true
decision: |
  Validate every required env var with a zod schema at module load
  time, so a missing or malformed key throws before any handler runs.
  packages/db/src/env.ts covers DATABASE_URL and DIRECT_DATABASE_URL;
  apps/web/src/lib/env.ts covers DATABASE_URL plus the two Clerk
  publishable and secret keys. Import-time validation; no lazy reads.
alternatives:
  - label: process.env reads at use site
    rejected_because: |
      A missing key surfaces as a runtime error inside a request
      handler, which makes the failure mode look like a transient
      query error. Boot-time validation surfaces the failure as a
      startup throw, which is the right place to fail loud.
  - label: dotenv with no validation
    rejected_because: |
      Loads keys but does not type them or check shape. A url-shaped
      key with a typo silently boots and breaks at first query.
  - label: a t3-env style schema in a separate package
    rejected_because: |
      The t3-env package adds a dep and a layer of indirection for
      what is a 20-line zod schema. The simpler path lands inline in
      each package's env.ts.
rationale: |
  The boot-time throw catches the failure at the right place: before
  any handler runs, with a clear error message naming the missing
  field. The pattern is small (two files, ~40 lines total), uses zod
  which is already in the dependency tree, and matches the broader
  rule that startup should fail loud and runtime should fail safe.

  A vitest case in apps/web parses a known-good env to confirm the
  schema accepts a valid set. The same approach lands in
  packages/db's test path.
evidence:
  - kind: spec
    ref: specs/0001-foundation/requirements.md
  - kind: doc
    ref: packages/db/src/env.ts
  - kind: doc
    ref: apps/web/src/lib/env.ts
  - kind: doc
    ref: apps/web/src/test/env.test.ts
rollback: |
  Replace the zod schemas with direct process.env reads at use site.
  Drop the env smoke test from the web vitest suite. The rollback is
  bounded: two files plus one test case, no data migration. This DEC
  carries reversible: true.
owner: platform
---

## decision

Validate every required env var with a zod schema at module load
time. `packages/db/src/env.ts` covers DATABASE_URL and
DIRECT_DATABASE_URL; `apps/web/src/lib/env.ts` covers DATABASE_URL
plus the two Clerk keys. Import-time validation; missing keys throw
before any handler runs.

## alternatives

- `process.env` reads at use site — missing key surfaces inside a
  handler as a transient-looking error.
- `dotenv` with no validation — loads keys without type or shape
  check.
- `t3-env` style separate package — adds a dep for a 20-line schema.

## rationale

The boot-time throw catches the failure at the right place: before
any handler runs, with a clear error message naming the missing
field. The pattern is small, uses zod which is already a dependency,
and matches the broader rule that startup fails loud.

## evidence

- `specs/0001-foundation/requirements.md` — R-FND-007 acceptance.
- `packages/db/src/env.ts` — the db env schema.
- `apps/web/src/lib/env.ts` — the web env schema.
- `apps/web/src/test/env.test.ts` — the smoke test.

## rollback

Replace the zod schemas with direct `process.env` reads at use site.
Drop the env smoke test from the web vitest suite. The rollback is
bounded: two files plus one test case, no data migration. This DEC
carries `reversible: true`.
