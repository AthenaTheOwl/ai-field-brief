---
id: DEC-SRC-008-article-url-heuristic-extractor
spec: specs/0002-source-registry/
requirement: R-SRC-008
date: 2026-05-24
status: approved
reversible: true
decision: |
  Ship `article-url` with a small HTML heuristic extractor. It prefers
  `<article>`, falls back to `<main>`, strips navigation chrome, and
  emits one `SourceItem`.
alternatives:
  - label: mozilla readability plus jsdom
    rejected_because: |
      That stack adds dependency weight before the repo has a 50-article
      recall corpus.
  - label: raw html only
    rejected_because: |
      Downstream scoring needs usable text, not only an HTML blob.
rationale: |
  The first connector pass needs deterministic extraction for fixtures.
  The heuristic is easy to replace after spec 0003 measures misses on
  real articles.
evidence:
  - kind: doc
    ref: packages/sources/src/connectors/article-url.ts
  - kind: run
    ref: packages/sources/test/fixtures.test.ts
rollback: |
  Replace the extractor with Readability while keeping the connector
  input and output shape.
owner: platform
---

## decision

Use a small heuristic extractor for article URLs.

## alternatives

- Readability plus jsdom: rejected until a larger article corpus exists.
- Raw HTML only: rejected because scoring needs text.

## rationale

The connector gives deterministic text now and stays easy to swap later.

## evidence

- `packages/sources/src/connectors/article-url.ts`
- `packages/sources/test/fixtures.test.ts`

## rollback

Swap the extractor internals and keep the connector shape.
