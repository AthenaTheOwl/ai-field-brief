---
id: DEC-SRC-004-in-memory-connector-registry
spec: specs/0002-source-registry/
requirement: R-SRC-004
date: 2026-05-24
status: approved
reversible: true
decision: |
  Register connectors in a module-scoped map keyed by `SourceType`.
  Importing `@aifieldbrief/sources` registers the four full connectors
  and the stubs.
alternatives:
  - label: dynamic import by source type
    rejected_because: |
      Dynamic imports make missing connector coverage harder to catch in
      a simple unit test.
  - label: switch statement in the runner
    rejected_because: |
      The runner would need edits for each source type and would own
      connector knowledge.
rationale: |
  A registry lets tests assert every source type has a connector entry
  before the runner exists. Duplicate registration throws so a source
  type cannot be wired twice by accident.
evidence:
  - kind: doc
    ref: packages/sources/src/registry.ts
  - kind: run
    ref: packages/sources/test/registry.test.ts
rollback: |
  Replace registry lookup with a runner switch statement and delete the
  registration side effects.
owner: platform
---

## decision

Use an in-memory connector registry keyed by `SourceType`.

## alternatives

- Dynamic import by source type: rejected because test coverage would be
  less direct.
- Runner switch statement: rejected because it puts connector knowledge
  in the runner.

## rationale

The registry lets the package prove full connector coverage before the
run workflow lands.

## evidence

- `packages/sources/src/registry.ts`
- `packages/sources/test/registry.test.ts`

## rollback

Replace registry lookup with a switch statement in the future runner.
