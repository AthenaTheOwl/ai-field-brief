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

## 2026-09-21 — ead3ac4 brief: publish the 2026-W38 field brief

- scope: vol. 21 covering 2026-09-12 to 2026-09-18, published three days
  late after the 2026-09-20 attempt was rejected (four of ten cited URLs
  404, one arXiv id cited for a paper it does not name) and parked on
  `rejected/w38-gemini-2026-09-20`. Eight Top signals across eight
  distinct action surfaces, 14 matrix cells, 8 action packets, 4 scout
  radar items. Single-author method, no lane agents: the seven in-window
  daily briefs and the 2026-09-18 weekly digest mined for 105 candidate
  primaries (`ops/w38/candidates.tsv`), each shortlisted primary fetched
  and dated; framework releases dated through the GitHub API
  (`ops/w38/scout.tsv`). Eleven discovery items found out of window on
  recheck and listed in Archive notes only. Index and README cadence
  updated.
- proof:
  - `python ops/w38/verify_quotes.py` — 26 of 26 quote-typed source_refs
    matched verbatim against live sources after whitespace normalization
  - `python scripts/validate_brief_fields.py` — OK, 4 briefs checked
  - `python scripts/validate_matrix_cells.py` — OK over 6,218 cells in
    19 files
  - `python scripts/voice_lint.py` — clean over 281 files
  - `python scripts/cadence_check.py` — OK after index and README update
  - `python scripts/spec_check.py` — OK, 7 active specs
  - `python -m pytest tests/ --basetemp=<scratch>` — 200 passed, 14
    skipped
  - run evidence — `ops/run-records/run-4f18599a1eda.json`, replay
    equivalent (`ops/replay-records/run-4f18599a1eda/`)
  - DEC-PUB-012, DEC-MTRX-009

## 2026-09-11 — d72056c brief: publish the 2026-W37 field brief

- scope: vol. 20 covering 2026-09-05 to 2026-09-11, closing the window
  W36 left open when it ended on a Friday. Nine Top signals across nine
  distinct action surfaces, 20 matrix cells, 9 action packets, 6 scout
  radar items. Sourced from a 24-lane sweep with an adversarial
  refutation pass on every finding: 325 raw, 246 deduped, 116 verified
  in-window, 51 refuted and dropped. Index and README cadence updated.
- proof:
  - `python scripts/validate_brief_fields.py` — OK, 3 briefs checked
  - `python scripts/validate_matrix_cells.py` — OK over 6,204 cells in
    18 files
  - `python scripts/voice_lint.py` — clean over 280 files
  - `python scripts/cadence_check.py` — OK after index and README update
  - `python scripts/spec_check.py` — OK, 7 active specs
  - `python -m pytest tests/ --basetemp=<scratch>` — 193 passed, 12
    skipped. A bare run reports 49 setup errors from a Windows
    PermissionError on the shared pytest temp root; supplying a basetemp
    clears them, so they are a workstation sandbox artifact and not a
    repo defect.
  - run evidence — `ops/run-records/run-6eaf944f0dbe.json`, replay
    equivalent

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

## 2026-10-03 — 98d603d brief: publish the 2026-W39 and 2026-W40 field briefs, and bind W32-W34

- scope: the two owed weekly issues (vol. 22 and vol. 23), closing a
  cadence gap that had reached 14 days against an 8-day window, plus the
  DEC-PUB-013 field backfill for 2026-W32 through 2026-W34 and the removal
  of those three weeks from `LEGACY_BRIEFS`.
- method: lane sweep over 195 active registry sources, 168 candidate
  primary URLs mined from the seven in-window daily digests and the weekly
  digest, and 216 framework releases dated through the GitHub API. Every
  item dated by its own primary, never by the day a digest named it — 187
  items the digests presented as current were dated outside both windows
  and appear only as discovery inputs. Every finding was then put to a
  skeptic instructed to refute it, with refutation the default where a
  claim could not be re-verified; refuted findings were dropped, never
  downgraded. W39 carried 109 verified against 15 refuted, W40 154 against
  13.
- proof:
  - seven repository gates — all green, `cadence_check` included
  - `ops/w39/verify_quotes.py` — 28 of 28 quote-typed spans verbatim
  - `ops/w40/verify_quotes.py` — 49 of 49 quote-typed spans verbatim
  - `ops/run-records/run-96dc70585181.json` (W39) and
    `ops/run-records/run-d0adad00d35c.json` (W40) — run evidence pinned at
    98d603df126a5cbba88c612ee48f63fe236b94f4
  - `python scripts/replay_run.py` — equivalent for both runs
  - `python scripts/validate_run_evidence.py` — OK over 377 events and 28
    run records
  - `python scripts/validate_brief_fields.py` — OK over 9 briefs, 12 legacy
    skipped, up from 6 and 15
  - DEC-PUB-012, DEC-PUB-013, DEC-MTRX-009

## 2026-10-12 — dd6c7bd brief: publish the 2026-W41 field brief

- scope: the owed issue for the week ending Friday 2026-10-09 (vol. 24).
- method: candidate dating over 85 URLs from the in-window digests, a GitHub
  release scout over 98 releases, and a sweep of 42 vendor and practitioner
  feeds; no lane agents. 78 of 85 digest candidates were dated outside the
  window by their own primaries. A skeptic re-opened every primary behind the
  published signals and corrected eight claims before release, including an
  out-of-window title figure.
- proof:
  - seven repository gates — all green, `cadence_check` included
  - `ops/w41/verify_quotes.py` — 81 of 81 quote-typed spans verbatim
  - `ops/run-records/run-5796c008c3e0.json` — run evidence pinned at dd6c7bd
  - `python scripts/replay_run.py` — equivalent
  - DEC-PUB-012, DEC-PUB-013, DEC-MTRX-009

## 2026-10-18 — fdd6b36 brief: prepare the 2026-W42 publication candidate

- scope: four selected Top signals, 36 matrix cells and a cadence gate that
  detects historical missing weeks. Source checks covered twenty public
  surfaces, nineteen returned; the full source registry was not swept.
- acceptance: an independent coordinating agent reread all four factual
  payloads against live primaries and returned PASS. Runtime and paid-model
  experiments remain proposals.
- proof:
  - sixteen repository gates passed on the actual fdd6b36 content commit
  - 84 Python tests and 23 web tests passed; typecheck and production build passed
  - `ops/run-records/run-w42-20261018-refresh.json` binds six pending URIs to
    fdd6b36d01036242d1656a13e4b86f552b566808
  - `ops/replay-records/run-w42-20261018-refresh/cbfdde84-35a8-4930-bf4f-7ff8aef2bfff.json`
    records equivalent replay at that exact HEAD after restoring the bound
    record, following DEC-PUB-008; no live LLM re-execution is claimed
  - `ops/w42/independent-review.json` records the factual review scope
- publication: release candidate for branch CI and coordinated publication;
  this record does not claim a deployment or email delivery.

## 2026-10-19 — fdd6b36 correction: W42 proof lines

- scope: corrects two proof lines in the 2026-10-18 fdd6b36 entry above,
  which stays as written. This entry changes no brief content. On the
  same branch, c2f29ef separately repoints two W42 record links to
  GitHub, and 7b2c634 rewrites Signal 3's "Why it matters" line and three
  related lines so they stay within the Scion evidence cells.
- proof:
  - "sixteen repository gates passed on the actual fdd6b36 content commit":
    the retained `ops/w42/validation-results.json` (checked_at
    2026-10-19T03:16:57Z, committed in 39e423d) was captured on a later
    tree that already held the W42 replay ledger, and reports 415
    run-evidence events. fdd6b36 holds 414, as the copy committed with it
    (checked_at 03:12:22Z) shows. Re-run on 2026-10-19 against an export
    of fdd6b36, all sixteen gates exit 0 with 414 events. `cadence_check`,
    which fdd6b36 changed, was not among the sixteen; it also passes there.
  - "84 Python tests": that count is `tests/scripts/` plus
    `tests/test_source_audit.py`. The full `python -m pytest tests/` at
    fdd6b36 collects 257: 235 passed, 22 skipped.
  - the web line holds: `@aifieldbrief/web` runs 23 tests, and they,
    `pnpm typecheck` and `pnpm build` pass at fdd6b36 (re-run 2026-10-19).
