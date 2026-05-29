---
id: DEC-MTRX-004-db-migration-parked-not-wired
spec: specs/0012-prompt-matrix-plane/
requirement: R-MTRX-006
date: 2026-05-29
status: approved
reversible: true
decision: |
  The SQL migration at
  `packages/db/migrations/staged/001_prompt_matrix.sql` lands as
  a parked reference artifact for a future Drizzle wiring pass.
  The brief workflow today writes matrix cells to file artifacts
  under the brief run folder; the relational store wiring lands
  behind a follow-up DEC that names the workspace scoping rule,
  the audit-event plumbing, and the schema-sync test.
alternatives:
  - label: wire the migration into Drizzle this pass
    rejected_because: |
      The matrix plane's first job is to land the schemas, the
      role contracts, and the playbook step. Wiring the
      relational store adds workspace scoping, the
      `assertWorkspaceId` helper for three new query files, the
      schema-sync test, the audit-event row per write, and the
      Drizzle migration cycle. That work is its own spec slice;
      mixing it with the install pass risks shipping broken
      state.
  - label: drop the migration entirely; rely on file artifacts forever
    rejected_because: |
      File artifacts are fine for the W22 rerun but scale poorly
      for cross-week analysis (a year of weekly briefs is 52 *
      ~30 cells = ~1500 cells; without an index, theme clustering
      across weeks reads slowly). The SQL shape lands now so the
      future wiring pass has a known starting shape.
  - label: land the migration under `drizzle/migrations/` (active)
    rejected_because: |
      The active migrations directory is reserved for migrations
      the Drizzle migrator picks up on `pnpm db:migrate`. A
      migration in there that no code reads breaks the contract
      that an active migration is in the live schema.
rationale: |
  The matrix plane's evidence-spine rule does not depend on the
  relational store; the rule depends on the cell shape and the
  faithfulness verdict. Cells can live as file artifacts today
  (one JSON per cell under the brief run folder) and migrate to
  the relational store under a future DEC. Parking the SQL under
  `staged/` documents the future shape without putting it on the
  active migration path. The drizzle config's migration search
  pattern excludes `staged/` so the migrator does not pick it up.
evidence:
  - kind: doc
    ref: packages/db/migrations/staged/001_prompt_matrix.sql
  - kind: doc
    ref: packages/db/drizzle.config.ts
  - kind: doc
    ref: specs/0012-prompt-matrix-plane/acceptance.md
  - kind: decision
    ref: decisions/DEC-FND-005-drizzle-migrations-gated-by-ci-drift-check.md
rollback: |
  Move the SQL file from `packages/db/migrations/staged/` into
  `packages/db/drizzle/migrations/` and wire the workspace
  scoping helper, the audit-event row, and the schema-sync test
  under a new DEC. Or delete the staged migration if the matrix
  plane never grows past file artifacts.
owner: engineering.implementation
---

## decision

The SQL migration at
`packages/db/migrations/staged/001_prompt_matrix.sql` lands as a
parked reference artifact for a future Drizzle wiring pass. The
brief workflow today writes matrix cells to file artifacts under
the brief run folder; the relational store wiring lands behind a
follow-up DEC.

## alternatives

- Wire the migration into Drizzle this pass. Rejected because
  the wiring work is its own spec slice (workspace scoping,
  assertWorkspaceId helper, schema-sync test, audit-event row);
  mixing it with the install pass risks shipping broken state.
- Drop the migration entirely and rely on file artifacts forever.
  Rejected because cross-week clustering scales poorly without
  an index; the SQL shape lands now so the future wiring pass
  has a known starting shape.
- Land the migration under active `drizzle/migrations/`.
  Rejected because the active migrations directory is reserved
  for migrations the migrator picks up; a migration that no code
  reads breaks the contract.

## rationale

The evidence-spine rule depends on the cell shape and the
faithfulness verdict, not on the relational store. Cells can
live as file artifacts today and migrate to the relational store
under a future DEC. The `staged/` subdir documents the future
shape without putting it on the active migration path.

## evidence

- `packages/db/migrations/staged/001_prompt_matrix.sql` is the
  parked migration.
- `packages/db/drizzle.config.ts` defines the migrations search
  pattern (excludes `staged/`).
- `specs/0012-prompt-matrix-plane/acceptance.md::R-MTRX-006`
  names the acceptance criteria for the parked state.
- `DEC-FND-005` is the Drizzle migration gate this DEC honors.

## rollback

Move the SQL file from `migrations/staged/` into the active
`drizzle/migrations/` directory and wire the workspace scoping
helper, audit-event row, and schema-sync test under a new DEC.
Or delete the staged migration if the matrix plane never grows
past file artifacts.
