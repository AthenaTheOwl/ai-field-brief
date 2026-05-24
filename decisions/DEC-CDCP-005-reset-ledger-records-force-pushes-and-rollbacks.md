---
id: DEC-CDCP-005-reset-ledger-records-force-pushes-and-rollbacks
spec: specs/0010-cognitive-delivery-control-plane/
requirement: R-CDCP-005
date: 2026-05-24
status: approved
reversible: true
decision: |
  Every force-push, history rewrite, or production rollback appends
  one entry to ops/RESET_LEDGER.md with date, operator, the
  from/to SHAs, and a one-line cause. The ledger entry lands in the
  same push that performs the rewrite.
alternatives:
  - label: rely on git reflog and the GitHub force-push log
    rejected_because: |
      Reflog is local-only; the GitHub force-push log is access-
      restricted to repo admins. Neither is durable across a host
      change. A markdown ledger lives in the repo and survives any
      host change.
  - label: forbid force-pushes outright
    rejected_because: |
      A force-push is sometimes the only safe rollback (a secret
      leaked in a commit; a malformed brief published by mistake).
      Forbidding the operation removes a load-bearing tool. The
      ledger keeps the operation visible without removing it.
  - label: record rewrites in commit messages only
    rejected_because: |
      Commit messages on rewritten history get rewritten too. A
      separate ledger file survives the rewrite. Cross-referencing
      from the reset ledger to the deleted SHAs keeps the
      causal trail intact.
rationale: |
  A history rewrite without a record is the worst kind of audit
  gap: the gap is invisible. The reset ledger surfaces the rewrite
  on the same push that performs it, with the from/to SHAs as the
  load-bearing field for forensic reconstruction.

  The "No resets recorded." sentinel keeps the file present and
  diff-able from day one; the first real entry replaces the
  sentinel with a one-line cause.
evidence:
  - kind: spec
    ref: specs/0010-cognitive-delivery-control-plane/requirements.md
  - kind: doc
    ref: ops/RESET_LEDGER.md
  - kind: doc
    ref: ../athena-site/ops/control-plane.md
rollback: |
  Stop appending entries to ops/RESET_LEDGER.md. Historical entries
  stay as documentation. The audit gap on future resets returns; no
  data loss.
owner: control
---

## decision

Every force-push, history rewrite, or production rollback appends
one entry to `ops/RESET_LEDGER.md` with date, operator, the from/to
SHAs, and a one-line cause. The entry lands in the same push that
performs the rewrite.

## alternatives

- Rely on git reflog and the GitHub force-push log — local-only or
  access-restricted; neither survives a host change.
- Forbid force-pushes — removes a load-bearing rollback tool.
- Record rewrites in commit messages — messages get rewritten too.

## rationale

A history rewrite without a record is the worst audit gap: the gap
is invisible. The reset ledger surfaces the rewrite on the same
push that performs it. The "No resets recorded." sentinel keeps the
file present and diff-able from day one.

## evidence

- `specs/0010-cognitive-delivery-control-plane/requirements.md` —
  R-CDCP-005 acceptance.
- `ops/RESET_LEDGER.md` — the ledger itself with the documented
  format header and the sentinel.
- `../athena-site/ops/control-plane.md` — the cross-repo charter.

## rollback

Stop appending entries. Historical entries stay as documentation.
The audit gap on future resets returns; no data loss.
