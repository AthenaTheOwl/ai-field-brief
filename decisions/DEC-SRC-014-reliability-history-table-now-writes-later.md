---
id: DEC-SRC-014-reliability-history-table-now-writes-later
spec: specs/0002-source-registry/
requirement: R-SRC-014
date: 2026-05-24
status: approved
reversible: true
decision: |
  Ship the `source_reliability_history` table in Phase 2 and defer the
  write path to the run workflow spec. The table stores week, included
  rate, average priority, item count, and snapshot time.
alternatives:
  - label: defer the table too
    rejected_because: |
      Runner design needs the persistence target before reliability
      score writes are specified.
  - label: compute reliability in the source table only
    rejected_because: |
      A current score without history makes weekly drift hard to audit.
rationale: |
  Phase 2 owns source registry shape. Spec 0003 can write into the table
  without reopening the schema decision.
evidence:
  - kind: doc
    ref: packages/db/src/schema/sources.ts
  - kind: spec
    ref: specs/0002-source-registry/acceptance.md
rollback: |
  Drop the history table and store only the current reliability score on
  `sources`.
owner: platform
---

## decision

Create reliability history storage now and leave writes to spec 0003.

## alternatives

- Defer the table: rejected because runner design needs a target.
- Current score only: rejected because weekly drift needs history.

## rationale

The registry schema lands as one unit while run behavior stays in its
own spec.

## evidence

- `packages/db/src/schema/sources.ts`
- `specs/0002-source-registry/acceptance.md`

## rollback

Drop the history table and keep only the current source score.
