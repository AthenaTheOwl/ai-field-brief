# .agents/AGENTS.md

The single contract a coding agent (Claude, Codex, or other) reads
before acting on this repo. Specs name what we build. Decisions name
why. This file names how the agent behaves while building.

## Coding style

- TypeScript strict everywhere. `tsconfig.base.json` carries
  `noUncheckedIndexedAccess: true`. Per-package `tsconfig.json` extends
  the base.
- Edit existing files. Use the `Edit` tool over `Write` when the file
  already exists; `Write` rewrites the whole file and risks losing
  context. Reserve `Write` for new files.
- `zod` env validation at module load. Every package or app that
  touches env vars defines a schema in `src/lib/env.ts` (web) or
  `src/env.ts` (db) and parses at import time. Missing keys throw
  before any handler runs. See `DEC-FND-007`.
- Multi-tenant rule: every db query takes `workspaceId` as a typed
  parameter. `assertWorkspaceId(workspaceId)` runs as the first line
  of every helper in `packages/db/src/queries/`. Raw drizzle clients
  do not get re-exported. See `DEC-FND-001`.
- Server components by default. Add `"use client"` only where
  interaction requires it. The landing page and layout stay server-only.
- UTC storage everywhere. Every `*_at` column uses
  `timestamp({ withTimezone: true })`. Display layers read the
  workspace timezone.

## Domain decisions

- Code ships under Apache-2.0. Content mirrors ship under CC BY 4.0
  in a sibling repo. The repo carries `LICENSE`, `NOTICE`, and the
  CHANGELOG names the spec ID per phase.
- Weekly brief cadence. The dream job runs Friday or on manual
  trigger; the brief lands in `briefs/YYYY-WNN/brief.md` against
  `templates/weekly-brief.md`. See `.agents/skills/run-weekly-brief/`.
- Source curation comes from `sources/registry.yaml`. The agent does
  not invent a source; it adds a candidate to
  `sources/candidates.yaml` and a human promotes the entry.
- Voice rules in `scripts/voice_lint.py` are not optional. Every
  markdown file under the documented globs runs the lint and exits
  clean before commit. Banlist is hard-FAIL.
- Audit-event plumbing covers admin action: settings, key rotation,
  membership, role change. The `log()` helper in
  `packages/db/src/queries/audit.ts` is the only write path.

## Workflow conventions

- Push to main directly. The repo's branch protection runs the CI
  gates on push; a failed gate blocks the merge.
- Five gates run on every push: `spec_check`, `voice_lint`,
  `validate_schemas`, `validate_registry`, `validate_decisions`.
  Plus turbo's `lint`, `typecheck`, `test`, `build`.
- Every shipped R-* requirement gets at least one DEC-* file before
  the commit reaches main. `spec_check` flags an orphan R-* and
  refuses the commit unless the requirement is listed in
  `decisions/.spec-check-allowlist.yaml` as deferred backfill.
- Dream-job outputs are human-gated. A dream candidate (memory update,
  generated test, skill patch, backlog item) carries
  `human_review_required: true` per the cross-repo schema default. No
  CI job auto-applies a dream candidate.
- A force-push, history rewrite, or rollback gets an entry in
  `ops/RESET_LEDGER.md` in the same push that performs the rewrite.
- A release gets an entry in `ops/RELEASE_LEDGER.md` with date, SHA,
  title, scope, and proof refs.
- Phase 2 source-registry work is in flight; Phase 1 backfill DECs
  for R-FND-002..006 and R-FND-008..014 land in a later pass and the
  allowlist defers them.

## Cross-repo links

- The CDCP charter at `../athena-site/ops/control-plane.md` names the
  six artifact types and the cross-repo contracts.
- The schemas at `../athena-site/ops/schemas/` are the source of
  truth for decision, dream-output, skill, artifact, and run shapes.
  This repo references them by URL and keeps a cache copy under
  `ops/schemas-cache/` for offline CI.
- The portfolio manifest at
  `../athena-site/ops/portfolio-manifest.yml` lists every product
  repo and which gates each repo runs.

## Where to look

| If you want to | Read |
|---|---|
| understand the what | `specs/NNNN-*/requirements.md` |
| understand the why | `decisions/DEC-*.md` |
| understand what we learned last week | `dreams/YYYY-WNN/report.md` |
| run the weekly brief | `.agents/skills/run-weekly-brief/SKILL.md` |
| audit a release | `ops/RELEASE_LEDGER.md` |
| audit a history rewrite | `ops/RESET_LEDGER.md` |
| add a new spec | `specs/README.md` plus the six-file pattern |
| add a new decision | `decisions/README.md` |

## Failure modes the agent watches for

- A new R-* requirement without a DEC: `spec_check` fails. Fix by
  adding the DEC file in the same commit, or add the ID to the
  allowlist with a tracking note.
- A DEC file out of schema shape: `validate_decisions` fails. Fix the
  front-matter against `ops/schemas-cache/decision.schema.json`.
- A voice-lint hit: rewrite the line. Per-line allowlist via
  `voice_lint:allow <label>` ships only when the rule does not apply
  and the agent leaves a note.
- A skill graduation without an eval: the SKILL.md may ship with an
  empty `evals` array plus a TODO; promotion past version 0.1.0
  requires `passing_skill_eval` per the promotion_policy field.
