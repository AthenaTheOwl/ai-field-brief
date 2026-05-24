---
id: DEC-CDCP-008-ci-failure-blocks-merge-to-main
spec: specs/0010-cognitive-delivery-control-plane/
requirement: R-CDCP-008
date: 2026-05-24
status: approved
reversible: false
decision: |
  Any failure of spec_check, voice_lint, validate_schemas,
  validate_registry, validate_decisions, validate_roles,
  validate_tools, or validate_policies fails the CI job and blocks
  the PR from merging to main. The .github/workflows/ci.yml gates
  job runs all eight python gates; the node job runs lint,
  typecheck, test, and build.
alternatives:
  - label: warn-only mode for the new gates
    rejected_because: |
      Warn-only gates get ignored. A failing gate that does not
      block the merge is a gate that does not exist. The phase 1
      ledger landed with zero blocking gates and the result was
      14 R-FND requirements without a DEC. Hard-block is the only
      enforcement that works.
  - label: block on a subset (voice_lint and spec_check only)
    rejected_because: |
      Each gate catches a different drift class. Validating the
      decision schema catches missing rationale fields; validating
      the registry catches a malformed source entry; validating
      the role catalog catches a forbidden-action misspelling. A
      subset leaves a gap.
  - label: pre-commit hook instead of CI
    rejected_because: |
      A pre-commit hook can be skipped (--no-verify) and runs only
      on the author's machine. CI is the durable enforcement layer.
      Both can coexist; CI is the load-bearing one.
rationale: |
  The gates are the executable contract. Specs name the what; DECs
  name the why; the gates are the how-we-know-it-stays-shaped. A
  gate that fires warning is decoration. A gate that fires blocking
  is enforcement.

  Reversibility is false because removing the block is a behavior
  change that affects every future PR. Reverting the workflow file
  is mechanical; rebuilding the discipline after the gates go away
  is not.
evidence:
  - kind: spec
    ref: specs/0010-cognitive-delivery-control-plane/requirements.md
  - kind: doc
    ref: .github/workflows/ci.yml
  - kind: doc
    ref: scripts/spec_check.py
  - kind: doc
    ref: scripts/voice_lint.py
  - kind: doc
    ref: scripts/validate_decisions.py
rollback: |
  Edit .github/workflows/ci.yml to drop the blocking behavior (set
  continue-on-error: true on the gates job, or remove the job). The
  scripts stay in place; the only loss is the per-PR enforcement.
  Re-establishing the block is a one-line edit.
owner: science
---

## decision

Any failure of `spec_check`, `voice_lint`, `validate_schemas`,
`validate_registry`, `validate_decisions`, `validate_roles`,
`validate_tools`, or `validate_policies` fails the CI job and
blocks the PR from merging to main. The
`.github/workflows/ci.yml` gates job runs all eight python gates;
the node job runs lint, typecheck, test, and build.

## alternatives

- Warn-only mode — warn-only gates get ignored.
- Block on a subset — each gate catches a different drift class;
  a subset leaves a gap.
- Pre-commit hook only — skippable (--no-verify); local-only.

## rationale

The gates are the executable contract. Specs name the what; DECs
name the why; the gates name the how-we-know-it-stays-shaped. A
warning gate is decoration; a blocking gate is enforcement.
Reversibility is false because removing the block changes
behavior for every future PR.

## evidence

- `specs/0010-cognitive-delivery-control-plane/requirements.md` —
  R-CDCP-008 acceptance.
- `.github/workflows/ci.yml` — the gates job with all eight python
  gates wired.
- `scripts/spec_check.py`, `scripts/voice_lint.py`,
  `scripts/validate_decisions.py` — three of the eight; the others
  follow the same shape.

## rollback

Edit `.github/workflows/ci.yml` to drop the blocking behavior
(`continue-on-error: true` or remove the job). The scripts stay in
place; the only loss is the per-PR enforcement.
