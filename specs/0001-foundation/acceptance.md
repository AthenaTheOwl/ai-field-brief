# acceptance: foundation

## Phase 1 gates

- `python scripts/spec_check.py` exits 0 with two active specs
  (`0000-bootstrap`, `0001-foundation`).
- `python scripts/voice_lint.py` exits 0 across the repo.
- `python scripts/validate_schemas.py` exits 0 (still 6 contract schemas;
  Phase 1 adds no new JSON schemas).
- `python scripts/validate_registry.py` exits 0 with the 15 seed sources
  still parsing.
- `pnpm install` resolves the workspace without errors.
- `pnpm --filter @aifieldbrief/db typecheck` exits 0.
- `pnpm --filter @aifieldbrief/db test` runs the vitest suite green; the
  tenant-scoping case passes.
- `pnpm --filter @aifieldbrief/web typecheck` exits 0.
- `pnpm --filter @aifieldbrief/web build` produces a `.next` output.
- `pnpm --filter @aifieldbrief/web test` runs the env smoke test green.

## Done means

Phase 1 is done when an agent can clone the repo, run `pnpm install`, and
get a typechecked db package + a buildable Next.js web app with Clerk
middleware in place. No live Clerk keys, no real Postgres connection, no
Stripe wiring. The schema, helpers, and CI gates are the deliverable.

## Explicit non-acceptance

- No pgvector schema in this phase.
- No Stripe schema in this phase.
- No Inngest function code in this phase.
- No real Clerk sign-in screen in this phase.
- No production deploy in this phase.
