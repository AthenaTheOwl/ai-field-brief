---
id: DEC-FND-005-drizzle-migrations-gated-by-ci-drift-check
spec: specs/0001-foundation/
requirement: R-FND-005
date: 2026-05-24
status: approved
reversible: true
decision: |
  Track every schema change as a Drizzle-Kit migration under
  `packages/db/drizzle/migrations/`. `drizzle.config.ts` points at
  `src/schema/index.ts` and writes migrations to `drizzle/migrations/`
  in strict mode. The CI gate that catches drift is
  `pnpm --filter @aifieldbrief/db typecheck` plus drizzle-kit `generate`
  in a later pass; pgvector lands in spec 0005, so no vector columns
  ship in this phase.
alternatives:
  - label: hand-written SQL migrations
    rejected_because: |
      Drizzle already generates idempotent SQL from the schema files.
      Hand-written SQL means the schema and the migration drift
      separately; the typecheck cannot catch the gap.
  - label: schema synchronization on boot (no migration history)
    rejected_because: |
      Production data does not tolerate a schema sync that drops a
      column. Migrations carry the audit trail of what changed and
      when; a sync-on-boot model has no rollback path.
  - label: defer migration discipline until first data lands
    rejected_because: |
      The migration tree gets harder to bootstrap once data is in.
      Landing the first migration during the Phase 1 schema commit
      sets the convention before any data exists.
rationale: |
  Drizzle's generated migrations carry the schema diff in version
  control, which is what the CI typecheck reads to catch drift. The
  strict + verbose flags in `drizzle.config.ts` make generation fail
  loud when the schema does not match the migration tree. pgvector
  defers to spec 0005 so the first migration set stays small and
  reviewable.

  The decision is reversible: dropping the migration tree means
  switching to hand-written SQL or schema sync; both rollbacks are
  bounded to the migrations directory + the drizzle config.
evidence:
  - kind: spec
    ref: specs/0001-foundation/requirements.md
  - kind: doc
    ref: packages/db/drizzle.config.ts
  - kind: doc
    ref: packages/db/drizzle/migrations/
  - kind: doc
    ref: packages/db/package.json
rollback: |
  Delete `drizzle/migrations/`. Rewrite `drizzle.config.ts` for hand-
  written SQL or schema sync. Drop the `db:generate` script from the
  package. The schema files in `src/schema/` stay correct under any
  migration model.
owner: platform
---

## decision

Track every schema change as a Drizzle-Kit migration under
`packages/db/drizzle/migrations/`. `drizzle.config.ts` points at
`src/schema/index.ts`, writes to `drizzle/migrations/`, and runs in
strict mode. CI gates drift via `pnpm --filter @aifieldbrief/db
typecheck`.

## alternatives

- Hand-written SQL migrations — schema and migration drift
  separately; typecheck cannot catch the gap.
- Schema sync on boot — no audit trail; no rollback path.
- Defer migration discipline until first data lands — harder to
  bootstrap after data exists; convention is cheaper at Phase 1.

## rationale

Drizzle's generated migrations carry the schema diff in version
control; the strict + verbose flags make generation fail loud when
the schema and the migration tree drift. pgvector defers to spec
0005 so the first migration set stays small.

## evidence

- `specs/0001-foundation/requirements.md` — R-FND-005 acceptance.
- `packages/db/drizzle.config.ts` — `schema: ./src/schema/index.ts`,
  `out: ./drizzle/migrations`, `strict: true`, `verbose: true`.
- `packages/db/drizzle/migrations/` — directory present in repo.
- `packages/db/package.json` — `db:generate` and `db:migrate`
  scripts wired.

## rollback

Delete `drizzle/migrations/`. Rewrite `drizzle.config.ts` for hand-
written SQL or schema sync. Drop the `db:generate` script. The
schema files in `src/schema/` stay correct under any migration
model.
