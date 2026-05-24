# acceptance: source registry + ingestion

## Phase 2 gates

- `python scripts/spec_check.py` exits 0 with three active specs
  (`0000-bootstrap`, `0001-foundation`, `0002-source-registry`).
- `python scripts/voice_lint.py` exits 0 across the repo.
- `python scripts/validate_schemas.py` exits 0 with the same 6 contract
  schemas as Phase 1 (Phase 2 adds no new JSON schemas).
- `python scripts/validate_registry.py` exits 0 with the 15 seed sources
  parsing.
- `pnpm install` resolves the workspace.
- `pnpm --filter @aifieldbrief/sources typecheck` exits 0.
- `pnpm --filter @aifieldbrief/sources test` runs every vitest case green
  (canonicalize, hash, registry, fixtures, types).
- `pnpm --filter @aifieldbrief/db typecheck` exits 0 with the new
  `sources.ts` schema + queries in place.
- `pnpm --filter @aifieldbrief/db test` runs the tenant-scoping cases for
  the new source helpers and the seed loader case green.
- `pnpm turbo run typecheck` and `pnpm turbo run test` both exit 0.

## Connector fixtures rule

Every full connector ships with a fixtures-driven test:

1. Load the canonical fixture entry from
   `packages/sources/schemas/source-item.fixtures.json`.
2. Feed the connector a minimal raw input that, when parsed, should
   produce that fixture's `SourceItem`.
3. Assert deep equality on the canonical fields (id is fixed,
   timestamps stay deterministic via injected `now`).

A connector without a green fixtures test does not ship.

## Reliability score formula (booked for spec 0003)

For each active source S in workspace W:

```
included_rate(S, week) =
  count(items from S included in any brief that week)
  / count(items from S ingested that week)

avg_priority(S, week) =
  mean(priority_score for items from S that landed in any brief
       — priority_score is the 0..1 rank from the brief synth pass)

reliability_score(S) =
  ema_4(included_rate(S)) * 0.7 + ema_4(avg_priority(S)) * 0.3
```

Spec 0002 ships the `source_reliability_history` table and FK. The
write path lands in spec 0003 (run workflow), and the score lands on
`sources.reliability_score` after the brief synth pass finishes.

## Done means

Phase 2 is done when:

- An agent can clone the repo, run `pnpm install`, and get a typechecked
  `@aifieldbrief/sources` package with green tests for the four full
  connectors and 14 registered stubs.
- The Drizzle `sources` table exists with tenant-scoped query helpers
  that refuse missing `workspaceId` at runtime.
- The seed loader reads `sources/registry.yaml` and returns 15 insert
  payloads for any caller-supplied workspace id.
- Every gate listed above exits 0.

## Explicit non-acceptance

- No HTTP fetch in the connector code path (runner owns that, spec 0003).
- No Inngest function code in this phase.
- No source-registry CRUD UI in this phase.
- No OAuth flows in this phase.
- No reliability score writes in this phase.
