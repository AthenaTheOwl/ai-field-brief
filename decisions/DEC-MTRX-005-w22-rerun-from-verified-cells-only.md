---
id: DEC-MTRX-005-w22-rerun-from-verified-cells-only
spec: specs/0012-prompt-matrix-plane/
requirement: R-MTRX-003
date: 2026-05-29
status: approved
reversible: true
decision: |
  When the 2026-W22 brief regenerates under the matrix plane, the
  brief is built from verified matrix cells only. Every pick in
  the regenerated brief carries an inline `<!-- cell-id: <id> -->`
  comment naming the cell or cells it traces to. A pick that
  cannot trace to a verified cell either drops or routes to the
  watchlist with a note. The regenerated brief replaces the
  published 2026-W22 markdown only after the human review pass
  (playbook step 13) signs off; the prior 2026-W22 run record and
  ledger stay as published evidence of the pre-matrix shape.
alternatives:
  - label: hand-port the 2026-W22 brief into cell shape after the fact
    rejected_because: |
      A retroactive cell mapping is a fiction. The cells need to
      drive the digest, not the other way around. Hand-porting
      would produce cells that match the brief's claims by
      construction, which is the opposite of the audit shape the
      matrix plane is supposed to provide.
  - label: skip the W22 rerun; start fresh with W23
    rejected_because: |
      The matrix plane's first proof is a brief that ran the loop.
      W22 has fresh sweep data and an existing run record that
      makes the before/after comparison tight. Skipping W22 means
      waiting a week for the first matrix-shape brief; running W22
      now puts the loop into evidence before the next sweep.
  - label: rerun W22 without the inline cell-id comments
    rejected_because: |
      The cell-id comments are the audit trail that lets a future
      reader trace a pick to a cell to a source span. Without the
      comments, the trace lives only in the run-evidence ledger,
      which is harder to read alongside the brief. Markdown
      comments render as nothing in HTML but stay in the source.
rationale: |
  The W22 rerun is the matrix plane's first proof. The rerun
  produces three artifacts the future reader can compare: the
  prior 2026-W22 brief (pre-matrix), the matrix run record (cells,
  faithfulness verdicts, synthesis output), and the regenerated
  brief (which links each pick to one or more verified cells via
  inline comments). The three together let the reader read the
  before/after, audit any pick from claim to cell to source, and
  decide whether the matrix plane buys what this DEC says it does.
evidence:
  - kind: doc
    ref: briefs/2026-W22/brief.md
  - kind: doc
    ref: docs/MATRIX_PLANE_DESIGN.md
  - kind: doc
    ref: playbook/run-weekly-brief.md
  - kind: decision
    ref: decisions/DEC-MTRX-001-prompt-matrix-plane-install.md
rollback: |
  Restore the prior 2026-W22 brief markdown from git history and
  drop the cell-id comments. The matrix run record and
  faithfulness report stay as evidence of the failed rerun. The
  next brief either reruns under the matrix loop or runs under
  the prior playbook shape per the controlling DEC.
owner: science.matrix-synthesis-editor
---

## decision

The 2026-W22 brief regenerates under the matrix plane from verified
cells only. Every pick carries an inline `<!-- cell-id: <id> -->`
comment naming the cell or cells it traces to. A pick that cannot
trace to a verified cell either drops or routes to the watchlist
with a note. The regenerated brief replaces the published markdown
only after the human review pass signs off.

## alternatives

- Hand-port the 2026-W22 brief into cell shape after the fact.
  Rejected because a retroactive cell mapping is a fiction; the
  cells need to drive the digest, not match the brief by
  construction.
- Skip the W22 rerun and start fresh with W23. Rejected because
  W22 has fresh sweep data and an existing run record that makes
  the before/after comparison tight.
- Rerun W22 without the inline cell-id comments. Rejected
  because the comments are the audit trail that lets a future
  reader trace a pick to a cell to a source span.

## rationale

The W22 rerun is the matrix plane's first proof. The rerun
produces three artifacts a future reader can compare: the prior
brief (pre-matrix), the matrix run record (cells, verdicts,
synthesis output), and the regenerated brief (which links each
pick to one or more verified cells via inline comments).

## evidence

- `briefs/2026-W22/brief.md` is the pre-matrix shape.
- `docs/MATRIX_PLANE_DESIGN.md` carries the loop shape and the
  playbook integration.
- `playbook/run-weekly-brief.md` carries steps 4-6 as the matrix
  pass plus step 8 as the per-cell audit.
- DEC-MTRX-001 is the install DEC this rerun proves out.

## rollback

Restore the prior 2026-W22 brief markdown from git history and
drop the cell-id comments. The matrix run record and faithfulness
report stay as evidence of the failed rerun. The next brief
either reruns under the matrix loop or runs under the prior
playbook shape.
