# .agents/AGENTS.md

The single contract a coding agent (Claude, Codex, or other) reads
before acting on this repo. Specs name what we build. Decisions name
why. This file names how the agent behaves while building.

## Evidence-spine rule

The matrix plane is the join key between sources and the digest. The
following are non-negotiable, in the same way the voice-lint banlist
is non-negotiable:

- No digest claim ships unless it traces to one or more verified
  matrix cells. A cell is verified when
  `faithfulness_status: passed` per `schemas/matrix_cell.schema.json`.
- No matrix cell counts as verified unless it carries at least one
  entry in `source_refs`. A cell with no source span is rejected at
  write time and again at verify time.
- No action candidate gets promoted unless it carries the six
  required fields: source support (verified cell ids), action
  surface, test plan, expected benefit, risk, and disposition (one
  of `adopt_now`, `prototype`, `monitor`, `archive`, `reject`,
  `promote_to_os_candidate`).

The rule is recorded under DEC-MTRX-001 and lives in
[docs/MATRIX_PLANE_DESIGN.md](../docs/MATRIX_PLANE_DESIGN.md). An
amendment relaxing the rule requires a new DEC.

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
- Eight gates run on every push: `spec_check`, `voice_lint`,
  `validate_schemas`, `validate_registry`, `validate_decisions`,
  `validate_roles`, `validate_tools`, `validate_policies`.
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

## Role catalog

The operating-model layer (spec 0011) ships six worked-example roles
plus the deferred-role TODO list. Read the role contract for whichever
role the route plan pins the run to.

- `.agents/roles/` — six worked examples (control.coordinator,
  product.spec-writer, engineering.implementation,
  engineering.code-reviewer, science.proof-gate-runner,
  learning.dream-orchestrator). Each role carries `role.yaml`,
  `instructions.md`, `tools.yaml`, `output.schema.json`, and
  `gates.yaml`.
- `.agents/tools.yaml` — tool registry. 16 seed entries. Every
  tool call cross-checks the calling role's `allowed_tools` list
  against the tool's `allowed_roles` list.
- `.agents/policies/` — declarative permission rules. Default-deny
  baseline at priority 0; explicit allows at priority 100; the
  reviewer-cannot-edit-code deny at priority 200.
- `.agents/state-machines/` — artifact lifecycles for spec, run, and
  release.
- `.agents/workflows/` — step graphs for single-change, weekly-dream,
  and incident-response. Each step pins to one role and one gate.
- `.agents/CATALOG.md` — the 44 deferred roles tracked by guild.
  Promotion off the catalog and into `.agents/roles/` requires a PR
  with the file set, a DEC, and the catalog entry removal in the
  same commit.
- `ops/event-log/` — append-only JSONL events. One file per UTC day.

### How to add a new role

1. Pick a role from `.agents/CATALOG.md`. Confirm the guild and the
   one-line mission.
2. Scaffold `.agents/roles/<id>/role.yaml` against the cross-repo
   `role.schema.json`. The `id` field matches the directory name.
3. Write `.agents/roles/<id>/instructions.md` (80–120 lines) naming
   mission, inputs, outputs, allowed tools, forbidden actions,
   required gates, escalation paths, runtime hint.
4. Write `.agents/roles/<id>/tools.yaml` listing the tool subset the
   role calls.
5. Write `.agents/roles/<id>/output.schema.json` for the role's
   outputs.
6. Write `.agents/roles/<id>/gates.yaml` listing the gates the
   role's run must clear.
7. Add `owner_role: <new-role-id>` to the R-* rows in any spec
   `traceability.md` the role takes over.
8. Remove the role from `.agents/CATALOG.md`.
9. File a DEC under `decisions/DEC-*.md` recording the promotion.
10. Ship in one commit. `validate_roles.py` confirms the role file
    parses; `spec_check.py` confirms the owner-role token resolves.

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
| find a role contract | `.agents/roles/<id>/instructions.md` |
| read the tool registry | `.agents/tools.yaml` |
| read the policy set | `.agents/policies/*.yaml` |
| read the deferred-role catalog | `.agents/CATALOG.md` |
| audit a workflow event | `ops/event-log/YYYY-MM-DD.jsonl` |
| audit a release | `ops/RELEASE_LEDGER.md` |
| audit a history rewrite | `ops/RESET_LEDGER.md` |
| add a new spec | `specs/README.md` plus the six-file pattern |
| add a new decision | `decisions/README.md` |
| add a new role | the "How to add a new role" section above |

## Lessons promoted from weekly dreams

### Voice rules at commit time · promoted from 2026-W21 dream

Three commits across one week (`c29b7ac`, `d2186d2`, `b4b9cf2`) named `voice_lint` as a verified gate in the commit body; each push paid the cost of a late rewrite. The recurring hits cluster around antithetical structures, banned corporate verbs, and empty adverbial openers.

- do: run `python scripts/voice_lint.py` against staged markdown before `git commit`, and fix hits as prose edits, not as per-line allowlist additions.
- don't: ship `voice_lint:allow <label>` without a one-line note naming why the rule mis-fires on that line.
- source: [dreams/2026-W21/candidates/memory-001-voice-lint-pre-commit-discipline.md](../dreams/2026-W21/candidates/memory-001-voice-lint-pre-commit-discipline.md).

### Phase 2 WIP stash before agent runs · promoted from 2026-W21 dream

Until source-registry connectors ship, the working tree carries uncommitted Phase 2 WIP under `packages/sources/` plus `specs/0002-source-registry/`. Multi-step agent runs that touch gates, schemas, or commits stash the WIP first and pop it after, with a stash message prefixed `phase 2 WIP:` so the pop is unambiguous.

- do: stash the seven-file WIP set under a `phase 2 WIP: <job>` message before any gate-running or commit-pushing agent run, and pop on exit.
- don't: leave Phase 2 WIP in the working tree across a `spec_check` or `validate_decisions` pass; the orphan R-SRC-* IDs surface as gate noise.
- source: [dreams/2026-W21/candidates/memory-002-stash-phase2-wip-before-agent-runs.md](../dreams/2026-W21/candidates/memory-002-stash-phase2-wip-before-agent-runs.md).

### Cross-repo schema `$ref` needs a registry · promoted from 2026-W21 dream

A `*.schema.json` file that uses an absolute `$ref` URL fails in offline CI by default, because `jsonschema` resolves `$ref` by HTTP fetch. The repo's existing pattern builds a `referencing.Registry` of every local schema (see `scripts/validate_schemas.py` `build_registry()`) and falls back from a 5-second remote fetch to `ops/schemas-cache/<name>.json` (see `scripts/validate_decisions.py`). A new `validate_<thing>.py` script copies one of the two existing scripts as a starting point.

- do: when a new validator consumes a schema with `$ref` to a sibling, build a `referencing.Registry` keyed by `$id` and pass it to the validator constructor.
- don't: rely on `jsonschema.Draft202012Validator(schema)` alone for any cross-repo schema; the bare instance walks `$ref` URLs over the network.
- source: [dreams/2026-W21/candidates/memory-003-jsonschema-ref-needs-registry.md](../dreams/2026-W21/candidates/memory-003-jsonschema-ref-needs-registry.md).

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
