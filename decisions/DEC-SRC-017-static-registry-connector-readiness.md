---
id: DEC-SRC-017-static-registry-connector-readiness
spec: specs/0002-source-registry/
requirement: R-SRC-017
date: 2026-05-25
status: approved
reversible: true
decision: |
  Source operations start with a static registry and connector readiness
  queue. The page reads local registry metadata and connector registrations
  only, so it can run during deploy checks without source URL crawling.
alternatives:
  - label: live source checks on page render
    rejected_because: |
      Page render would inherit provider latency, rate limits, and network
      failures before the runner owns retry and cache policy.
  - label: database-only operations page
    rejected_because: |
      The seed registry and connector package already hold the readiness
      inputs needed for the first operator queue.
  - label: wait for the ingestion runner
    rejected_because: |
      Operators need a visible source readiness queue before live ingestion
      jobs land.
rationale: |
  The first source ops boundary should answer whether the curated registry
  is fresh and whether each row has a non-stub connector. Keeping it static
  protects the public request path from live crawling while still exposing
  the next ingestion blockers.
evidence:
  - kind: code
    ref: packages/sources/src/ops.ts
  - kind: code
    ref: apps/web/src/app/ops/sources/page.tsx
  - kind: test
    ref: packages/sources/test/ops.test.ts
rollback: |
  Remove `/ops/sources`, remove the source ops model, and keep the seed
  loader mapping in packages/db until a later ingestion runner owns source
  readiness.
owner: product
---

## decision

Source operations start with a static registry and connector readiness
queue. The page reads local registry metadata and connector registrations
only, so it can run during deploy checks without source URL crawling.

## alternatives

- Live source checks on page render. Rejected because page render would
  inherit provider latency, rate limits, and network failures before the
  runner owns retry and cache policy.
- Database-only operations page. Rejected because the seed registry and
  connector package already hold the readiness inputs needed for the first
  operator queue.
- Wait for the ingestion runner. Rejected because operators need a visible
  source readiness queue before live ingestion jobs land.

## rationale

The first source ops boundary should answer whether the curated registry is
fresh and whether each row has a non-stub connector. Keeping it static
protects the public request path from live crawling while still exposing
the next ingestion blockers.

## evidence

- `packages/sources/src/ops.ts`
- `apps/web/src/app/ops/sources/page.tsx`
- `packages/sources/test/ops.test.ts`

## rollback

Remove `/ops/sources`, remove the source ops model, and keep the seed
loader mapping in packages/db until a later ingestion runner owns source
readiness.
