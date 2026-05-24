---
id: DEC-FND-006-tsconfig-strict-plus-no-unchecked-indexed-access
spec: specs/0001-foundation/
requirement: R-FND-006
date: 2026-05-24
status: approved
reversible: true
decision: |
  Every package and app inherits `tsconfig.base.json`, which sets
  `strict: true`, `noUncheckedIndexedAccess: true`, and
  `noImplicitOverride: true`. Per-package `tsconfig.json` extends the
  base with whatever package-specific lib + module + paths it needs.
  CI runs `pnpm typecheck` across the workspace and fails the push on
  any TS error.
alternatives:
  - label: strict mode only, without noUncheckedIndexedAccess
    rejected_because: |
      Array and record access without the unchecked-index flag returns
      a non-undefined type, which hides one of the most common bug
      classes (off-by-one, missing-key). Turning the flag on at Phase 1
      forces every read-by-index call site to handle the absent case.
  - label: per-package tsconfig with no shared base
    rejected_because: |
      Drift across packages would surface as cross-package type errors
      only when a consumer imports the producer. The shared base means
      every package compiles against the same strictness baseline.
  - label: loose mode + a lint rule for strict patterns
    rejected_because: |
      Lint rules miss what the type checker catches. Strict mode is
      the cheaper place to fail loud.
rationale: |
  Strict mode plus `noUncheckedIndexedAccess` is the cheapest way to
  catch a large class of bugs at compile time. The flag forces every
  array or record access to handle the absent case, which is the
  source of most production undefined-is-not-a-function failures in
  TypeScript code. The base config lands once; every package inherits
  for free.

  The decision is reversible: turning off the strict flag is a one-
  line config change. The cost of the reversal is the bug class that
  re-opens.
evidence:
  - kind: spec
    ref: specs/0001-foundation/requirements.md
  - kind: doc
    ref: tsconfig.base.json
  - kind: doc
    ref: apps/web/tsconfig.json
  - kind: doc
    ref: packages/db/tsconfig.json
rollback: |
  Set `noUncheckedIndexedAccess: false` in `tsconfig.base.json`. Fix
  the small handful of files that adopt the safer pattern only because
  the flag forced them to. The rollback is one config line plus
  optional code cleanup.
owner: platform
---

## decision

Every package and app inherits `tsconfig.base.json`, which sets
`strict: true`, `noUncheckedIndexedAccess: true`, and
`noImplicitOverride: true`. Per-package `tsconfig.json` extends the
base. CI runs `pnpm typecheck` across the workspace.

## alternatives

- Strict mode only without `noUncheckedIndexedAccess` — hides the
  off-by-one / missing-key bug class.
- Per-package tsconfig with no shared base — drift surfaces only
  through cross-package imports.
- Loose mode with a lint rule — lint misses what the type checker
  catches.

## rationale

Strict plus `noUncheckedIndexedAccess` is the cheapest way to catch
a large bug class at compile time. The base config lands once and
every package inherits for free.

## evidence

- `specs/0001-foundation/requirements.md` — R-FND-006 acceptance.
- `tsconfig.base.json` — `strict: true`,
  `noUncheckedIndexedAccess: true`, `noImplicitOverride: true`.
- `apps/web/tsconfig.json` — `extends: ../../tsconfig.base.json`.
- `packages/db/tsconfig.json` — same extends; CI typecheck passes.

## rollback

Set `noUncheckedIndexedAccess: false` in `tsconfig.base.json`. Fix
the small handful of files that adopted the safer pattern only
because the flag forced them to.
