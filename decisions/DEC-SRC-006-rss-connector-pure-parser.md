---
id: DEC-SRC-006-rss-connector-pure-parser
spec: specs/0002-source-registry/
requirement: R-SRC-006
date: 2026-05-24
status: approved
reversible: true
decision: |
  Ship the rss connector as a pure parser for RSS 2.0, Atom 1.0, and
  JSON Feed text. The connector emits canonical `SourceItem` rows with
  feed metadata and no network access.
alternatives:
  - label: rss-only parser
    rejected_because: |
      Several seed sources expose Atom or JSON Feed; one `rss` source
      type needs to handle common feed formats.
  - label: external parser package
    rejected_because: |
      The first fixtures need a small parser and no extra dependency.
rationale: |
  The parser covers the feed shapes the seed registry needs now. Spec
  0003 can replace internals with a parser package if field coverage
  becomes weak against a larger corpus.
evidence:
  - kind: doc
    ref: packages/sources/src/connectors/rss.ts
  - kind: run
    ref: packages/sources/test/fixtures.test.ts
rollback: |
  Swap the internal parser for a feed parser package behind the same
  connector contract.
owner: platform
---

## decision

Ship rss as a pure parser for RSS, Atom, and JSON Feed text.

## alternatives

- RSS-only parser: rejected because seed sources also use Atom.
- External parser package: rejected because the first fixture set is
  covered by a small local parser.

## rationale

The connector satisfies seed-registry needs now and leaves the contract
ready for a parser swap later.

## evidence

- `packages/sources/src/connectors/rss.ts`
- `packages/sources/test/fixtures.test.ts`

## rollback

Replace the parser internals behind the same connector interface.
