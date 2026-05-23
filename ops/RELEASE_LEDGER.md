# RELEASE_LEDGER

Every commit on main that represents shippable scope lands here with
date, SHA, title, scope, and proof refs. Backfilled entries cover
the nine pre-CDCP commits.

## Format

Each entry has the shape:

```
## YYYY-MM-DD — <sha> <title>

- scope: <one or two sentences>
- proof:
  - <gate or test name> — <where the proof lives>
```

## Entries

## 2026-05-22 — f126a87 phase 0: bootstrap monorepo + gate scripts + CI

- scope: pnpm workspaces, Turborepo, TypeScript strict baseline, four
  python gates (spec_check, voice_lint, validate_schemas,
  validate_registry), CI workflow.
- proof:
  - spec_check — `specs/0000-bootstrap/` ledger lands
  - voice_lint — root README + NOTICE pass clean
  - CI — `.github/workflows/ci.yml` runs the four gates plus turbo

## 2026-05-22 — 7737fd7 phase 0: canonical contracts + fixtures + eval skeletons

- scope: source-item, transcript, citation, provenance, and eval
  contract schemas under `packages/*/src/contracts/`, with fixtures
  and a vitest skeleton per package.
- proof:
  - validate_schemas — six contract schemas parse clean
  - vitest — eval skeletons run green

## 2026-05-22 — 7a3e7ca sources: seed registry with 15 tier-1 sources + candidates ledger

- scope: `sources/registry.yaml` with 15 active tier-1 sources;
  `sources/candidates.yaml` for promotion-pending entries.
- proof:
  - validate_registry — 15 active sources parse clean

## 2026-05-22 — b1d1951 phase 1 spec 0001: foundation — db + web scaffold + tenant-scoped queries

- scope: `specs/0001-foundation/` ledger with R-FND-001..014;
  `packages/db` Drizzle schema, Neon HTTP client, zod env validation,
  tenant-scoped query helpers; `apps/web` Next.js 15 scaffold with
  Clerk middleware (no live keys).
- proof:
  - spec_check — two active specs
  - pnpm --filter @aifieldbrief/db typecheck — passes
  - pnpm --filter @aifieldbrief/db test — tenant-scoping vitest passes
  - pnpm --filter @aifieldbrief/web typecheck — passes
  - pnpm --filter @aifieldbrief/web build — produces .next output

## 2026-05-22 — d811676 brief 2026-W21: contract speed, not model speed

- scope: first weekly brief under `briefs/2026-W21/brief.md` against
  `templates/weekly-brief.md`; sweep of the 15-source registry.
- proof:
  - voice_lint — brief passes clean
  - playbook — `playbook/run-weekly-brief.md` followed top-to-bottom

## 2026-05-22 — c29b7ac brief 2026-W21 rewrite + public reader + vercel deploy config

- scope: brief rewrite for tone and structure; public reader UI under
  `apps/web/src/app/briefs/`; Vercel deploy config in `vercel.json`.
- proof:
  - voice_lint — passes
  - pnpm --filter @aifieldbrief/web build — passes
  - vercel deploy — succeeds against the public reader URL

## 2026-05-22 — b3d3e27 fix lockfile after brief deploy update

- scope: pnpm-lock.yaml refresh after the brief deploy config.
- proof:
  - pnpm install --frozen-lockfile=false — resolves
  - CI gates — green

## 2026-05-22 — 11efda1 fix vercel monorepo next detection

- scope: vercel.json adjustment so the monorepo build resolves the
  Next.js app correctly.
- proof:
  - vercel deploy — succeeds

## 2026-05-22 — 992f3f2 fix public deploy without clerk env

- scope: env handling so the public reader deploy works without live
  Clerk keys; the protected admin routes remain gated.
- proof:
  - pnpm --filter @aifieldbrief/web build — passes
  - vercel deploy — succeeds against https://ai-field-brief.vercel.app/
  - manual smoke — landing page renders, brief reader renders
