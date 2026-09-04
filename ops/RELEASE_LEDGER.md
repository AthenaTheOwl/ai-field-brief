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

## 2026-05-23 to 2026-09-04 — gap in this ledger

- scope: this ledger stopped being written after the 2026-05-22 deploy
  entries, while briefs 2026-W22 through 2026-W34 and their supporting
  control-plane changes shipped to main. Those commits are recoverable
  from `git log` and from `ops/run-records/`, which stayed current
  throughout, but they were never summarized here.
- proof:
  - `git log --oneline bf33821` — the unrecorded range
  - `ops/run-records/` — 22 run records covering the same period
- note: recorded as a gap instead of backfilled. Backfilling 13 issues
  from memory would produce a ledger that reads complete and is not.
  Entries resume below.

## 2026-09-04 — 0a2a80a chore: normalize matrix cell vocabulary to the cell schema

- scope: 172 enum substitutions across the eight cell files that had
  drifted from `schemas/matrix_cell.schema.json` since 2026-W24, plus
  `scripts/validate_matrix_cells.py` to hold the vocabulary. Cell
  content, source refs, confidence, and faithfulness status untouched.
- proof:
  - `python scripts/validate_matrix_cells.py` — OK over 6,184 cells in
    17 files
  - negative control — reintroducing one drifted enum value reproduces a
    single named violation
  - `python -m pytest tests/` — 186 passed, 10 skipped
  - DEC-MTRX-009, R-MTRX-019

## 2026-09-04 — b6cd864 brief: publish W35 and W36 field briefs

- scope: the two missing weekly issues (vol. 18 and vol. 19), source
  registry to v14 at 222 active, action-surface taxonomy to v2, and
  `scripts/validate_brief_fields.py` enforcing the Top-signal field
  contract that W32 through W34 had silently dropped.
- proof:
  - fifteen repository gates — all green, including the two added here
  - `python -m pytest tests/` — 186 passed, 10 skipped
  - `ops/run-records/run-4483229ed9b8.json` (W35) and
    `ops/run-records/run-69b6fe82a9cf.json` (W36) — run evidence with
    eleven gate results each
  - DEC-SRC-022, DEC-PUB-012, DEC-PUB-013

