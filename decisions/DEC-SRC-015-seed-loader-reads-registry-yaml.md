---
id: DEC-SRC-015-seed-loader-reads-registry-yaml
spec: specs/0002-source-registry/
requirement: R-SRC-015
date: 2026-05-24
status: approved
reversible: true
decision: |
  Provide a seed loader that reads `sources/registry.yaml` and returns
  source insert payloads for a caller-supplied workspace id. The loader
  does not write to the database.
alternatives:
  - label: seed script inserts directly
    rejected_because: |
      Direct writes would need live database configuration in a package
      unit test.
  - label: duplicate seed data in TypeScript
    rejected_because: |
      The yaml registry is already the source of curated seed truth.
rationale: |
  Returning payloads keeps seeding testable and lets setup flows decide
  when to write. The test asserts the current registry produces 15 rows.
evidence:
  - kind: doc
    ref: packages/db/src/seeds/sources-from-registry.ts
  - kind: run
    ref: packages/db/src/test/seeds.test.ts
rollback: |
  Replace the loader with a migration-time seed script that writes
  directly to the database.
owner: platform
---

## decision

Read `sources/registry.yaml` into insert payloads without database
writes.

## alternatives

- Direct insert script: rejected because unit tests would need a live db.
- Duplicate TypeScript data: rejected because the yaml registry is the
  seed source.

## rationale

Payload generation keeps setup flows in control of writes.

## evidence

- `packages/db/src/seeds/sources-from-registry.ts`
- `packages/db/src/test/seeds.test.ts`

## rollback

Replace the loader with a direct seed script.
