---
id: DEC-SRC-013-source-type-union-schema-sync-test
spec: specs/0002-source-registry/
requirement: R-SRC-013
date: 2026-05-24
status: approved
reversible: true
decision: |
  Keep the TypeScript `SOURCE_TYPES` tuple and JSON Schema
  `source_type.enum` as two checked surfaces. A test asserts set
  equality between them.
alternatives:
  - label: generate TypeScript from JSON Schema
    rejected_because: |
      The repo has no schema codegen step yet; adding one for one enum
      would add machinery before it pays for itself.
  - label: manual discipline only
    rejected_because: |
      Manual sync is easy to miss when adding a connector.
rationale: |
  The test gives immediate drift detection without introducing a
  generator. New source types must update the tuple, schema enum, and
  registry entry together.
evidence:
  - kind: doc
    ref: packages/sources/src/types.ts
  - kind: run
    ref: packages/sources/test/types.test.ts
rollback: |
  Add schema-to-TypeScript generation and delete the set-equality test.
owner: platform
---

## decision

Test that the SourceType tuple matches the JSON Schema enum.

## alternatives

- Generate TypeScript from schema: rejected because codegen is early
  overhead here.
- Manual sync only: rejected because drift is easy.

## rationale

The test catches enum drift with no generator.

## evidence

- `packages/sources/src/types.ts`
- `packages/sources/test/types.test.ts`

## rollback

Adopt schema codegen and delete the test.
