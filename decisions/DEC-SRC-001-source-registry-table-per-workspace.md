---
id: DEC-SRC-001-source-registry-table-per-workspace
spec: specs/0002-source-registry/
requirement: R-SRC-001
date: 2026-05-24
status: approved
reversible: true
decision: |
  Store sources in a workspace-scoped `sources` table with quality
  signals, cadence, intake mode, status, config, notes, and soft-delete
  fields. Keep `type` as text and validate it in application code.
alternatives:
  - label: postgres enum for source type
    rejected_because: |
      Connector types will change during early ingestion work. Text plus
      application validation avoids enum migrations during each source
      experiment.
  - label: registry yaml only
    rejected_because: |
      Workspaces need custom sources, status, last review dates, and
      per-source config that cannot live only in the global seed file.
rationale: |
  The table gives the runner one durable place to read active sources
  per workspace. The `(workspace_id, status, lane)` index matches the
  first runner query shape and the review dashboard shape.
evidence:
  - kind: spec
    ref: specs/0002-source-registry/requirements.md
  - kind: doc
    ref: packages/db/src/schema/sources.ts
rollback: |
  Drop the `sources` table and route the runner back to
  `sources/registry.yaml`. Workspace custom sources and review status
  would need another storage surface before rollback.
owner: platform
---

## decision

Store sources in a workspace-scoped table with quality signals,
cadence, intake mode, status, config, notes, and soft-delete fields.

## alternatives

- Postgres enum for source type: rejected because connector types will
  change during early ingestion work.
- Registry yaml only: rejected because workspaces need custom sources
  and per-source state.

## rationale

The table gives the runner one durable place to read active sources per
workspace. The index matches the first runner query shape and review
dashboard shape.

## evidence

- `packages/db/src/schema/sources.ts`
- `specs/0002-source-registry/requirements.md`

## rollback

Drop the table and route the runner back to `sources/registry.yaml`.
