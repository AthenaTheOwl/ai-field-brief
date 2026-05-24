---
id: DEC-SRC-012-connector-provenance-version-stamp
spec: specs/0002-source-registry/
requirement: R-SRC-012
date: 2026-05-24
status: approved
reversible: true
decision: |
  Stamp every full connector output with `provenance.fetcher` in
  `<connector>@<semver>` form plus fetched time and source id.
alternatives:
  - label: fetcher name only
    rejected_because: |
      Parser behavior changes need a version marker for later audits.
  - label: runner writes all provenance
    rejected_because: |
      The connector owns parser identity; the runner owns transport
      context.
rationale: |
  Versioned fetcher names make future item audits traceable to the
  parser that produced the row. Fixtures assert each full connector
  writes the expected stamp.
evidence:
  - kind: doc
    ref: packages/sources/src/connectors/
  - kind: run
    ref: packages/sources/test/fixtures.test.ts
rollback: |
  Move fetcher stamping into the runner and keep connector versions in a
  separate registry table.
owner: platform
---

## decision

Stamp each connector output with a versioned provenance fetcher.

## alternatives

- Fetcher name only: rejected because parser changes need a marker.
- Runner writes all provenance: rejected because parser identity lives
  in the connector.

## rationale

Versioned fetcher names support later audits of source-item behavior.

## evidence

- `packages/sources/src/connectors/`
- `packages/sources/test/fixtures.test.ts`

## rollback

Move fetcher stamping to the runner and store connector versions apart.
