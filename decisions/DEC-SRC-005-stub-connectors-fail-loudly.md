---
id: DEC-SRC-005-stub-connectors-fail-loudly
spec: specs/0002-source-registry/
requirement: R-SRC-005
date: 2026-05-24
status: approved
reversible: true
decision: |
  Register stub connectors for every source type that lacks a full
  implementation. Each stub throws `NotImplementedError` with the
  source type name when fetched.
alternatives:
  - label: leave missing source types unregistered
    rejected_because: |
      Missing registrations make registry tests fail before the error
      can name the planned source type.
  - label: return an empty array
    rejected_because: |
      Silent empties hide missing ingestion work and make the runner
      look green while it skipped a source.
rationale: |
  Stubs preserve total registry coverage while keeping missing work
  visible at runtime. The runner can distinguish a planned source type
  from an unknown source type.
evidence:
  - kind: doc
    ref: packages/sources/src/connectors/stubs.ts
  - kind: run
    ref: packages/sources/test/registry.test.ts
rollback: |
  Remove the stubs and let missing source types throw
  `UnknownSourceTypeError` during lookup.
owner: platform
---

## decision

Register stubs for source types that do not have a full connector yet.

## alternatives

- Leave them unregistered: rejected because the error would be less
  specific.
- Return empty arrays: rejected because it hides missing ingestion work.

## rationale

The registry stays total while runtime behavior remains explicit.

## evidence

- `packages/sources/src/connectors/stubs.ts`
- `packages/sources/test/registry.test.ts`

## rollback

Remove the stubs and rely on unknown-source lookup errors.
