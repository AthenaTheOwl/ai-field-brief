# AI Field Brief

AI Field Brief is a separate product repo for automated source monitoring,
transcription, retrieval, brief generation, publishing, and action-backlog
workflows.

This repo starts spec-first. Product code should not land until the bootstrap
specs define the source-ingestion contract, workflow orchestration, retrieval
schema, eval gates, and release proof.

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

