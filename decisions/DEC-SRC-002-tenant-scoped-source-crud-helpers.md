---
id: DEC-SRC-002-tenant-scoped-source-crud-helpers
spec: specs/0002-source-registry/
requirement: R-SRC-002
date: 2026-05-24
status: approved
reversible: true
decision: |
  Route all source registry reads and writes through query helpers whose
  first parameter is `workspaceId`. Each helper calls `assertWorkspaceId`
  before building SQL.
alternatives:
  - label: direct drizzle access
    rejected_because: |
      Direct table access repeats the tenant filter at each call site and
      makes one missed predicate a tenant leak.
  - label: request-scoped workspace context
    rejected_because: |
      Hidden context is harder to test than a typed positional argument.
rationale: |
  The helper pattern repeats the Phase 1 tenant-scope rule for the new
  `sources` table. Tests cast bad inputs to string and prove the guard
  throws before any database call is needed.
evidence:
  - kind: doc
    ref: packages/db/src/queries/sources.ts
  - kind: run
    ref: packages/db/src/test/sources.test.ts
rollback: |
  Delete the helpers and expose raw Drizzle table access. Any caller
  must then own its tenant predicate.
owner: platform
---

## decision

All source registry reads and writes go through tenant-scoped helpers.

## alternatives

- Direct Drizzle access: rejected because the tenant predicate would be
  repeated by every caller.
- Request-scoped workspace context: rejected because it hides the tenant
  key from the type signature.

## rationale

The helper pattern repeats the Phase 1 tenant-scope rule and gives CI a
small runtime test for the guard.

## evidence

- `packages/db/src/queries/sources.ts`
- `packages/db/src/test/sources.test.ts`

## rollback

Delete the helpers and make callers own the tenant predicate.
