---
id: DEC-CDCP-004-release-ledger-as-durable-evidence
spec: specs/0010-cognitive-delivery-control-plane/
requirement: R-CDCP-004
date: 2026-05-24
status: approved
reversible: true
decision: |
  Every commit that reaches main and represents shippable scope gets
  one entry in ops/RELEASE_LEDGER.md with date, SHA, title, scope
  (1-2 sentences), and proof refs. The backfill on this commit
  records the nine pre-CDCP commits from f126a87 through 992f3f2.
alternatives:
  - label: rely on git log + GitHub releases
    rejected_because: |
      Git log carries no scope summary and no proof refs. GitHub
      releases are tag-scoped, not commit-scoped, and they decay if
      the repo moves hosts. A markdown ledger lives in the repo
      itself and survives any host change.
  - label: tag every release and use tag descriptions
    rejected_because: |
      Tags map one-to-one with versions, not with shippable commits.
      A repo can ship five times before a version tag lands; the
      ledger captures those five.
  - label: defer the ledger until the first non-foundation release
    rejected_because: |
      Backfilling the first ten commits is bounded work; backfilling
      fifty is not. The ledger lands now and accepts new entries on
      every shippable commit.
rationale: |
  The release ledger is the durable evidence trail. Tags and
  GitHub releases are convenience surfaces; the ledger is the audit
  surface. Each entry names which gates the release passed, which
  spec it addresses, and where the proof lives (test report, eval
  run, screenshot path).

  Manual review is the gate today. A future automation can parse
  the ledger and cross-check against the gate runs, but the manual
  pass at the commit author keeps the discipline visible.
evidence:
  - kind: spec
    ref: specs/0010-cognitive-delivery-control-plane/requirements.md
  - kind: doc
    ref: ops/RELEASE_LEDGER.md
  - kind: doc
    ref: ../athena-site/ops/control-plane.md
rollback: |
  Stop appending entries to ops/RELEASE_LEDGER.md. The historical
  entries stay as documentation. Audit cost rises; no data loss.
owner: control
---

## decision

Every shippable commit reaches `ops/RELEASE_LEDGER.md` with date,
SHA, title, scope (1-2 sentences), and proof refs. The current
backfill records nine pre-CDCP commits from f126a87 through
992f3f2.

## alternatives

- Rely on git log + GitHub releases — git log has no scope; tags
  are version-scoped, not commit-scoped.
- Tag every release — tags map to versions, not to shippable
  commits.
- Defer until the first non-foundation release — bounded backfill
  now, unbounded later.

## rationale

The release ledger is the durable evidence trail. Tags and GitHub
releases are convenience surfaces; the ledger is the audit surface.
Each entry names which gates the release passed and where the proof
lives. Manual review at the commit author keeps the discipline
visible.

## evidence

- `specs/0010-cognitive-delivery-control-plane/requirements.md` —
  R-CDCP-004 acceptance.
- `ops/RELEASE_LEDGER.md` — the ledger itself, with the nine-commit
  backfill.
- `../athena-site/ops/control-plane.md` — the cross-repo charter
  that names the ledger pattern.

## rollback

Stop appending entries. Historical entries stay as documentation.
No data loss.
