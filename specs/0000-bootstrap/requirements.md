# requirements: bootstrap

## Scope

Bootstrap the AI Field Brief repo as a spec-driven monorepo for a multi-tenant
briefing product. This spec codifies the end state enough to prevent early
agentic implementation from turning into unverified scaffolding.

## Requirements

### R-BOOT-001: separate repo and monorepo layout

WHEN development starts, THE SYSTEM SHALL live in a separate git repo with apps,
packages, workflow functions, and specs.

Acceptance:
- The repo has `apps/`, `packages/`, `inngest/`, and `specs/` planned or
  scaffolded.
- Root scripts expose install, lint, typecheck, test, build, eval, and verify.

### R-BOOT-002: source ingestion contract before connectors

WHEN a source connector is built, THE SYSTEM SHALL use one canonical item
schema for raw item, normalized item, transcript, citation, and provenance.

Acceptance:
- Every connector has fixtures and retry/rate-limit behavior.
- Audio/video sources require transcription by default, not keyword-gated
  transcription.
- Source provenance survives into brief citations.

### R-BOOT-003: durable workflow orchestration

WHEN ingestion, transcription, retrieval, brief generation, publishing, or
backlog sync runs in the background, THE SYSTEM SHALL model it as replayable
steps with idempotency keys.

Acceptance:
- Workflow steps have names, retries, cancellation behavior, and replay notes.
- Nightly cron, manual run-now, and per-workspace schedules share the same run
  model.

### R-BOOT-004: retrieval and citation contract

WHEN "Ask my briefs" or generated briefs use retrieval, THE SYSTEM SHALL record
the query, retrieved chunks, ranking signals, citations, and answer grounding.

Acceptance:
- Postgres + pgvector is the default persistence/retrieval base.
- Hybrid retrieval uses full-text plus vector retrieval before rerank.
- Citation-faithfulness evals gate prompt/model changes.

### R-BOOT-005: evals are release gates

WHEN prompt, model, source parsing, retrieval, or brief style changes, THE
SYSTEM SHALL run task-specific evals before merge.

Acceptance:
- Evals cover citation faithfulness, hallucination, source attribution, action
  extraction, style, and continuity from prior briefs.
- Eval results record model/provider/version, dataset, prompt version, and
  git SHA.

### R-BOOT-006: multi-tenant security and audit are not optional

WHEN the product supports workspaces and organizations, THE SYSTEM SHALL record
roles, permissions, audit events, API keys, BYOK secrets, custom domains, data
export, and deletion flows.

Acceptance:
- Tenant IDs are part of database access patterns and audit events.
- Every external publish/integration action emits an audit event.
- BYOK secrets and provider keys never appear in logs or eval artifacts.

### R-BOOT-007: publishing has rollback or unpublish paths

WHEN a brief is published to a feed, app, file, issue tracker, or collaboration
tool, THE SYSTEM SHALL retain the publish artifact, destination, status, and
undo path.

Acceptance:
- RSS/Atom/JSON Feed, Slack, Discord, email, Notion, Confluence, Linear, Jira,
  GitHub issues, webhook, PDF, ePub, JSON, markdown, audio, and widget publish
  paths are represented in the publish contract before implementation.

