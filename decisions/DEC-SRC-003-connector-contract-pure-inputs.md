---
id: DEC-SRC-003-connector-contract-pure-inputs
spec: specs/0002-source-registry/
requirement: R-SRC-003
date: 2026-05-24
status: approved
reversible: true
decision: |
  Define `Connector<TConfig>` as a pure parser contract. Fetch context
  carries workspace id, source id, config, raw input, time, provenance
  metadata, and test hooks for ids and hashes.
alternatives:
  - label: connector owns HTTP
    rejected_because: |
      Retry, ETag, auth, and rate-limit handling belong to the runner in
      spec 0003 so tests can stay network-free.
  - label: one function per connector
    rejected_because: |
      A shared interface lets the runner call each source type through
      one registry surface.
rationale: |
  The contract keeps connector tests deterministic and leaves network
  behavior to the run workflow. The id and hash hooks exist for fixtures;
  default production behavior still uses UUIDs and SHA-256.
evidence:
  - kind: doc
    ref: packages/sources/src/contract.ts
  - kind: run
    ref: packages/sources/test/fixtures.test.ts
rollback: |
  Collapse the contract into per-connector functions and update the
  runner once spec 0003 lands.
owner: platform
---

## decision

Use a pure parser contract for every connector.

## alternatives

- Connector owns HTTP: rejected because runner retry and cache behavior
  needs one owner.
- One function per connector: rejected because the runner needs one
  calling shape.

## rationale

Network-free connectors are easier to test and safer to compose into the
run workflow.

## evidence

- `packages/sources/src/contract.ts`
- `packages/sources/test/fixtures.test.ts`

## rollback

Replace the interface with per-connector functions before spec 0003 uses
the registry.
