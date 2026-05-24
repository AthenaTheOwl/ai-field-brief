---
id: DEC-SRC-010-canonical-url-dedupe-key
spec: specs/0002-source-registry/
requirement: R-SRC-010
date: 2026-05-24
status: approved
reversible: true
decision: |
  Canonicalize URLs by dropping tracking keys and fragments, lowercasing
  hostnames, trimming non-root trailing slashes, and sorting query keys.
alternatives:
  - label: store raw URL as dedupe key
    rejected_because: |
      Feed URLs often carry tracking params that would duplicate the
      same item across runs.
  - label: aggressive path normalization
    rejected_because: |
      Lowercasing paths can change meaning on case-sensitive servers.
rationale: |
  The chosen normalization removes common noise while preserving path
  semantics. Tests lock the behavior so connector outputs stay stable.
evidence:
  - kind: doc
    ref: packages/sources/src/canonicalize.ts
  - kind: run
    ref: packages/sources/test/canonicalize.test.ts
rollback: |
  Replace `canonicalizeUrl` with a stricter or looser normalization
  function and rerun connector fixtures.
owner: platform
---

## decision

Normalize URLs with a narrow, deterministic canonicalization function.

## alternatives

- Raw URL key: rejected because tracking params duplicate items.
- Aggressive path normalization: rejected because paths can be
  case-sensitive.

## rationale

The function removes common noise while preserving path meaning.

## evidence

- `packages/sources/src/canonicalize.ts`
- `packages/sources/test/canonicalize.test.ts`

## rollback

Swap the canonicalization function and update fixtures.
