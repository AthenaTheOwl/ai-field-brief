---
id: DEC-PUB-015-editorial-evidence-integrity
spec: specs/0007-publishing/
requirement: R-PUB-033
date: 2026-10-21
status: approved
reversible: true
decision: |
  Check explicit Evidence lines in every canonical issue, including the
  legacy layouts, against real faithfulness-passed cells with nonempty
  content and public source locators. Keep the later template-field gate
  separate. Backfill missing evidence as a dated current review without
  rewriting the original issue dates or run records.
alternatives:
  - label: leave older issues outside every evidence gate
    rejected_because: Missing matrices and dangling references remain invisible.
  - label: impose the current digest layout on every old issue
    rejected_because: Evidence integrity does not require replacing the author's historical form.
  - label: treat resolved cell ids as proof of factual correctness
    rejected_because: A reference check cannot decide whether a claim follows from its source.
rationale: |
  The existing field gate skips older layouts and accepts missing matrix
  files. The archive review found explicit ids with no backing matrix and
  issues with source links but no explicit cell binding. A dated backfill
  can repair the current publication while preserving what the original
  run recorded. Separate source reading remains required.
evidence:
  - kind: doc
    ref: scripts/validate_editorial_evidence.py
  - kind: doc
    ref: tests/scripts/test_validate_editorial_evidence.py
  - kind: doc
    ref: prompts/editorial_contract.md
  - kind: doc
    ref: VOICE.md
rollback: |
  Remove the new gate and its CI step. Keep source corrections and dated
  backfill records; deleting the gate does not reverse a factual correction.
owner: science.proof-gate-runner
---

The gate checks references and recorded review state. It makes no claim
that a URL is still reachable or that matching words prove the claim.
Those are source-review questions. A current correction does not change
the result of an old benchmark, sweep or run.
