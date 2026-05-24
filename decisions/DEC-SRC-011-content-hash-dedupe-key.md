---
id: DEC-SRC-011-content-hash-dedupe-key
spec: specs/0002-source-registry/
requirement: R-SRC-011
date: 2026-05-24
status: approved
reversible: true
decision: |
  Compute `content_hash` as SHA-256 over title, canonical URL, and body.
  Use lowercase hex output.
alternatives:
  - label: hash raw body only
    rejected_because: |
      Several feeds emit empty or boilerplate bodies; title and URL add
      needed identity.
  - label: hash raw html
    rejected_because: |
      Markup churn would change hashes while extracted text stayed the
      same.
rationale: |
  The hash balances stable dedupe with visible content changes. Tests
  assert determinism and body-change divergence.
evidence:
  - kind: doc
    ref: packages/sources/src/hash.ts
  - kind: run
    ref: packages/sources/test/hash.test.ts
rollback: |
  Change the hash input tuple and run a migration for any persisted
  source items that spec 0003 has written.
owner: platform
---

## decision

Compute source content hashes from title, canonical URL, and body.

## alternatives

- Body-only hash: rejected because many feeds emit thin bodies.
- Raw HTML hash: rejected because markup churn can hide same text.

## rationale

The tuple gives stable dedupe while preserving real content changes.

## evidence

- `packages/sources/src/hash.ts`
- `packages/sources/test/hash.test.ts`

## rollback

Change the tuple and migrate persisted hashes after storage lands.
