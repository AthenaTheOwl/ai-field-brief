# AI Field Brief

AI Field Brief is a separate product repo for automated source monitoring,
transcription, retrieval, brief generation, publishing, and action-backlog
workflows.

This repo starts spec-first. Product code should not land until the bootstrap
specs define the source-ingestion contract, workflow orchestration, retrieval
schema, eval gates, and release proof.

## Governance

Specs name the what. Decisions name the why. Dreams name what we learned.
Skills name what we will reuse. The full charter lives in the sibling
athena-site repo at `../athena-site/ops/control-plane.md`.

- `specs/` — the spec ledger (one folder per phase; six-file pattern).
- `decisions/` — `DEC-*.md` files with alternatives, rationale,
  evidence, and rollback per requirement.
- `dreams/` — weekly offline-cognition outputs with human-gated
  promotion candidates.
- `.agents/AGENTS.md` — the single contract a coding agent reads first.
- `.agents/skills/<id>/SKILL.md` — graduated reuse packages.
- `.agents/roles/<id>/` — six worked-example role contracts.
- `.agents/tools.yaml` — the tool registry every role calls against.
- `.agents/policies/` — declarative permission rules with a
  default-deny baseline.
- `.agents/state-machines/` — artifact lifecycles for spec, run,
  release.
- `.agents/workflows/` — step graphs for single-change, weekly-dream,
  incident-response.
- `.agents/CATALOG.md` — the 44 deferred roles tracked by guild.
- `ops/event-log/YYYY-MM-DD.jsonl` — append-only workflow events.
- `ops/RELEASE_LEDGER.md` — every release with date, SHA, scope, proof.
- `ops/RESET_LEDGER.md` — every force-push, history rewrite, rollback.

Eight python gates run on every push: `spec_check`, `voice_lint`,
`validate_schemas`, `validate_registry`, `validate_decisions`,
`validate_roles`, `validate_tools`, `validate_policies`. A failed
gate blocks the merge.

## Planned shape

- `apps/web`
- `apps/mobile`
- `apps/extension`
- `apps/mcp-server`
- `packages/db`
- `packages/sources`
- `packages/pipeline`
- `packages/retrieval`
- `packages/evals`
- `packages/integrations`
- `packages/observability`
- `inngest/`
- `specs/`

## Phase 0 rule

Every feature from the v3 plan is either:

- in a numbered phase,
- explicitly out of scope,
- or blocked on account/provider setup.

No connector, prompt, model, workflow, or publish channel ships without a
fixture, eval, retry/rollback path, and traceable requirement.

