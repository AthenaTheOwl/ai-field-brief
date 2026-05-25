---
id: DEC-PUB-001-public-feeds-from-build-snapshot
spec: specs/0007-publishing/
requirement: R-PUB-001
date: 2026-05-25
status: approved
reversible: true
decision: |
  The RSS, Atom, and JSON Feed routes are generated from the same
  build-time brief snapshot as the public archive. They do not query
  the database or call source connectors at request time.
alternatives:
  - label: generate feeds from the database
    rejected_because: |
      The public archive already renders from markdown. Pulling feeds
      from the database would create a second content source before the
      source-ingestion pipeline is the canonical store.
  - label: maintain hand-written feed files
    rejected_because: |
      Hand-written feed files drift from the archive. The route should
      fail or pass with the same brief snapshot as the page renderer.
rationale: |
  The feed routes are publishing surfaces, not ingestion surfaces. The
  archive is already a static projection of `briefs/<week>/brief.md`
  and `meta.yaml`; feeds should be another projection of that same
  source. This keeps the public reader experience stable while source
  connectors keep maturing.
evidence:
  - kind: code
    ref: apps/web/src/lib/feeds.ts
  - kind: test
    ref: apps/web/src/lib/feeds.test.ts
  - kind: code
    ref: apps/web/src/app/feed.xml/route.ts
rollback: |
  Remove the three feed route folders and the feed links from the home
  page and layout metadata. The archive continues to render briefs.
owner: product
---

## decision

The RSS, Atom, and JSON Feed routes are generated from the same
build-time brief snapshot as the public archive. They do not query the
database or call source connectors at request time.

## alternatives

- Generate feeds from the database. Rejected because markdown is still
  the canonical public brief source.
- Maintain hand-written feed files. Rejected because those files would
  drift from the archive.

## rationale

The feed routes are publishing surfaces. The archive is already a
static projection of `briefs/<week>/brief.md` and `meta.yaml`; feeds
are another projection of that source. This keeps the public reader
experience stable while source connectors keep maturing.

## evidence

- `apps/web/src/lib/feeds.ts`
- `apps/web/src/lib/feeds.test.ts`
- `apps/web/src/app/feed.xml/route.ts`

## rollback

Remove the three feed route folders and the feed links from the home
page and layout metadata. The archive continues to render briefs.
