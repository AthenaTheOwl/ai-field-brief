---
id: DEC-FND-008-apache-2-code-cc-by-content-split
spec: specs/0001-foundation/
requirement: R-FND-008
date: 2026-05-24
status: approved
reversible: false
decision: |
  Ship product code in this repository under Apache License 2.0 with a
  NOTICE file naming the project author. Reserve CC BY 4.0 for published
  brief content, which lives in the sibling `ai-field-brief-content`
  mirror repository. The CHANGELOG carries one entry per spec ID at
  every phase release.
alternatives:
  - label: single Apache-2.0 license for code and content
    rejected_because: |
      Brief content reads as editorial work, not software. Apache covers
      patent and code-level distribution; CC BY covers attribution-based
      reuse of writing. Mixing them under one license confuses both
      audiences. The split puts each license where it fits.
  - label: MIT for code, public domain for content
    rejected_because: |
      MIT skips the explicit patent grant Apache carries; public domain
      forfeits attribution. Both choices give up signal that the
      portfolio's other repos already carry. Consistency wins.
  - label: code and content in the same repo under dual licenses
    rejected_because: |
      A single repo with two licenses forces every reader to figure out
      which file falls under which. The sibling-repo split lets the
      content mirror carry the CC BY notice at its root and the code
      repo carry the Apache notice at its root, with no per-file
      tagging.
rationale: |
  Apache-2.0 for code matches the portfolio's other product repos and
  carries the explicit patent grant that contributors and downstream
  consumers expect from a 2026 OSS project. CC BY 4.0 for content
  keeps brief reuse permissive while requiring attribution, which is
  the right shape for a weekly editorial product. The sibling-repo
  split keeps the two licenses cleanly scoped.

  The decision is reversible: false because relicensing requires
  consent from every contributor who landed code under Apache, and
  every reader who reused content under CC BY may have already
  attributed under the old license.
evidence:
  - kind: doc
    ref: LICENSE
  - kind: doc
    ref: NOTICE
  - kind: doc
    ref: CHANGELOG.md
  - kind: doc
    ref: README.md
rollback: |
  Relicensing requires a notice on the repository, contributor consent
  for any code under Apache that gets relicensed, and a fresh start
  for the content mirror's CC BY history. No single-commit rollback
  exists; this DEC carries reversible: false.
owner: platform
---

## decision

Ship code under Apache-2.0 with a NOTICE file. Reserve CC BY 4.0 for
published brief content in the sibling `ai-field-brief-content`
mirror. The CHANGELOG carries one entry per spec ID at every phase
release.

## alternatives

- Single Apache-2.0 for code and content — Apache covers code-level
  distribution; CC BY covers editorial reuse.
- MIT + public domain — MIT skips the patent grant; public domain
  forfeits attribution.
- Code and content in the same repo under dual licenses — per-file
  tagging confuses readers.

## rationale

Apache-2.0 matches the portfolio's other product repos and carries
the patent grant that 2026 OSS projects need. CC BY 4.0 for content
keeps reuse permissive while requiring attribution, which fits a
weekly editorial product. The sibling-repo split keeps the two
licenses cleanly scoped.

## evidence

- `LICENSE` — Apache-2.0 text with 2026 copyright header.
- `NOTICE` — names the project author plus the AthenaTheOwl
  attribution and the CC BY 4.0 reservation for content.
- `CHANGELOG.md` — Phase 1 entry names spec 0001 by ID.
- `README.md` — repo intro names the spec ledger as the source of
  truth for what ships in each phase.

## rollback

Relicensing requires a notice on the repository, contributor consent
for any code under Apache that gets relicensed, and a fresh start
for the content mirror's CC BY history. No single-commit rollback
exists.
