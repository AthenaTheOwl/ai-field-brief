---
id: DEC-FND-009-readme-hook-plus-setup-pattern
spec: specs/0001-foundation/
requirement: R-FND-009
date: 2026-05-24
status: approved
reversible: true
decision: |
  The root README opens with the N degree 18 door hook, names the
  product's planned shape, names the Phase 0 spec-first rule, then
  shows setup commands. Phase 1 (and every later phase) extends the
  README by appending the new phase's setup steps under a phase-named
  heading; no rewrite of the existing copy.
alternatives:
  - label: rewrite the README at each phase
    rejected_because: |
      A rewrite loses the prior phase's framing context. The hook +
      planned shape + Phase 0 rule sequence carries the why of the
      project; rewriting per phase forces the reader to re-establish
      that context every release.
  - label: split the README into a marketing page + a CONTRIBUTING file
    rejected_because: |
      The root README is the first thing a GitHub visitor sees. The
      marketing pitch and the setup commands need to live together so
      a reader does not have to click through to figure out what the
      project does and how to run it.
  - label: defer setup steps until the docs site ships
    rejected_because: |
      Setup commands belong next to the source they install. A docs
      site that drifts from the source becomes the source of an
      outdated install path.
rationale: |
  The hook + planned shape + Phase 0 rule sequence already names the
  project's why; the append-only pattern lets each phase add what it
  shipped without invalidating prior framing. The cost is a README
  that grows over time; the benefit is a reader can trace which
  phase added which surface by reading top-to-bottom.

  The decision is reversible: a future README restructure replaces
  the append model with whatever shape better fits the project's
  audience at that point.
evidence:
  - kind: doc
    ref: README.md
  - kind: spec
    ref: specs/0001-foundation/requirements.md
rollback: |
  Restructure the README at any point. The git history preserves the
  prior shape; no data migration. The rollback cost is the editorial
  pass to rewrite.
owner: editorial
---

## decision

The root README opens with the N degree 18 hook, the planned shape,
and the Phase 0 spec-first rule. Later phases append setup steps
under a phase-named heading; no rewrite of the existing copy.

## alternatives

- Rewrite the README at each phase — loses framing context.
- Split into a marketing page + CONTRIBUTING file — root README is
  the first GitHub touch; setup commands need to live next to the
  pitch.
- Defer setup steps to a docs site — setup commands belong with the
  source they install.

## rationale

The hook + planned shape + Phase 0 rule sequence already names the
project's why; the append-only pattern lets each phase add what it
shipped without invalidating prior framing.

## evidence

- `README.md` — opens with the door hook, names the spec-first rule,
  and ships the Phase 1 setup steps appended without rewriting the
  Phase 0 copy.
- `specs/0001-foundation/requirements.md` — R-FND-009 acceptance.

## rollback

Restructure the README at any point. Git history preserves the
prior shape; no data migration.
