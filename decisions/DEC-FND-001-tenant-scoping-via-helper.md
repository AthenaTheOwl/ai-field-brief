---
id: DEC-FND-001-tenant-scoping-via-helper
spec: specs/0001-foundation/
requirement: R-FND-001
date: 2026-05-22
status: approved
reversible: false
decision: |
  Tenant-scope every row read and write through a Drizzle query helper
  that takes workspaceId as a typed positional parameter, with an
  assertWorkspaceId guard as the first line of every helper. Raw
  drizzle clients do not get re-exported from packages/db; consumers
  go through the helpers.
alternatives:
  - label: row-level security in Postgres
    rejected_because: |
      Neon's serverless driver pools connections; per-request session
      variables for RLS are hard to keep correct across edge runtime
      and node-postgres test paths. Application-layer enforcement is
      easier to test and matches the multi-app shape (web, mcp-server,
      mobile) where every entry point already needs the workspaceId.
  - label: middleware that injects workspaceId into a request-scoped store
    rejected_because: |
      An async-local-storage approach hides the parameter from the
      type system. The helper signature lets the compiler catch
      missing-workspaceId at call sites instead of catching it at
      runtime via assert.
  - label: trust callers to pass the right workspaceId without a guard
    rejected_because: |
      One missed call is a tenant-data leak. The assertWorkspaceId
      guard is the belt-and-suspenders that catches an empty string,
      undefined, or a coercion bug before any query runs.
rationale: |
  Application-layer enforcement plus an explicit positional parameter
  gives the compiler one shot to catch missing workspaceId and the
  runtime one shot to catch coercion bugs. The pattern lands once in
  packages/db/src/queries and every downstream app inherits it. A
  vitest case asserts the guard throws on empty or undefined; CI
  enforces the test.

  The reversibility cost is real: once tenants share a schema and the
  helpers carry workspaceId everywhere, undoing the pattern means
  rewriting every query call site. That is why this DEC is marked
  reversible: false.
evidence:
  - kind: spec
    ref: specs/0001-foundation/requirements.md
  - kind: spec
    ref: specs/0001-foundation/design.md
  - kind: doc
    ref: packages/db/src/queries/workspaces.ts
  - kind: doc
    ref: packages/db/src/test/tenant-scoping.test.ts
rollback: |
  To undo: rewrite every helper in packages/db/src/queries/ to drop
  the workspaceId parameter, drop the assertWorkspaceId guard, and
  re-export the raw drizzle client. Adopt Postgres row-level security
  in its place. The rollback path crosses every downstream app and
  is the reason this DEC carries reversible: false.
owner: platform
---

## decision

Tenant-scope every row read and write through a Drizzle query helper
that takes `workspaceId` as a typed positional parameter, with an
`assertWorkspaceId` guard as the first line of every helper. Raw
drizzle clients do not get re-exported from `packages/db`.

## alternatives

- Row-level security in Postgres — Neon's pooled connections make
  per-request session variables hard to keep correct.
- Async-local-storage workspaceId — hides the parameter from the
  type system.
- Trust callers without a guard — one missed call is a tenant-data
  leak.

## rationale

Application-layer enforcement plus an explicit positional parameter
gives the compiler one shot to catch missing `workspaceId` and the
runtime one shot to catch coercion bugs. The pattern lands once in
`packages/db/src/queries/` and every downstream app inherits it.

## evidence

- `specs/0001-foundation/requirements.md` — R-FND-001 acceptance.
- `specs/0001-foundation/design.md` — query helper section.
- `packages/db/src/queries/workspaces.ts` — the helpers.
- `packages/db/src/test/tenant-scoping.test.ts` — the guard test.

## rollback

Rewrite every helper to drop the `workspaceId` parameter, drop the
`assertWorkspaceId` guard, re-export the raw drizzle client, and
adopt Postgres RLS in its place. The rollback path crosses every
downstream app, which is why this DEC carries `reversible: false`.
