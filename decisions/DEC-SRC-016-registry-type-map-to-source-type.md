---
id: DEC-SRC-016-registry-type-map-to-source-type
spec: specs/0002-source-registry/
requirement: R-SRC-016
date: 2026-05-24
status: approved
reversible: true
decision: |
  Map human-friendly registry type labels to canonical `SourceType`
  values in an explicit table. The seed-loader test asserts the mapping
  covers every distinct type in `sources/registry.yaml`.
alternatives:
  - label: rename registry type values
    rejected_because: |
      The seed registry uses labels that are useful to humans reviewing
      the source list.
  - label: infer by URL
    rejected_because: |
      URL heuristics hide review decisions and are brittle for Substack
      and vendor pages.
rationale: |
  The mapping separates editorial labels from connector labels. A total
  mapping test catches any new registry type before seed generation runs.
evidence:
  - kind: doc
    ref: packages/db/src/seeds/sources-from-registry.ts
  - kind: run
    ref: packages/db/src/test/seeds.test.ts
rollback: |
  Change `sources/registry.yaml` to use canonical `SourceType` values
  directly and delete the mapping table.
owner: platform
---

## decision

Map registry labels to canonical source types explicitly.

## alternatives

- Rename registry labels: rejected because the current labels help
  source review.
- Infer by URL: rejected because it hides editorial choices.

## rationale

The mapping keeps human labels and connector labels separate.

## evidence

- `packages/db/src/seeds/sources-from-registry.ts`
- `packages/db/src/test/seeds.test.ts`

## rollback

Use canonical source types directly in `sources/registry.yaml`.
