---
id: DEC-PUB-013-brief-top-signal-conformance-gate
spec: specs/0007-publishing/
requirement: R-PUB-031
date: 2026-09-04
status: approved
reversible: true
decision: |
  Add `scripts/validate_brief_fields.py` as a repository gate that checks
  every Top signal in a published brief for the four systems-thinking
  fields required by DEC-MTRX-007 and DEC-CDCP-020, plus a Confidence
  label, an Evidence line whose cell ids resolve against the sibling
  `matrix/cells.yaml`, a Source line, and an action surface that resolves
  against `config/action_surface_taxonomy.yaml`. Wire the gate into CI and
  the pre-commit list in AGENTS.md. Grandfather briefs 2026-W20 through
  2026-W34 in an explicit `LEGACY_BRIEFS` set, so the debt is named in code
  instead of hidden by a narrower rule.
alternatives:
  - label: enforce the rule on every brief in the archive
    rejected_because: |
      Fifteen published issues would fail on the first run, which turns the
      gate red for a backfill that has not been scoped. A red gate that
      cannot be made green gets bypassed, and the bypass would cover the new
      issues too.
  - label: rely on AGENTS.md and reviewer attention
    rejected_because: |
      That is the arrangement that produced the drift. AGENTS.md has said
      "these are not optional" since DEC-MTRX-007, and issues W32, W33, and
      W34 shipped without transferable_principle, falsification_test,
      adoption_ladder, Confidence, or Evidence on any pick.
  - label: relax the rule to match what recent briefs carry
    rejected_because: |
      The four fields are what separates a pick from a link with commentary.
      Dropping falsification_test in particular would remove the only field
      that commits a pick to being wrong in a stated way.
  - label: backfill W32 through W34 in the same change
    rejected_because: |
      Backfilling three issues means reconstructing adoption ladders and
      cell-level evidence for 21 picks from sources read weeks ago. That is
      research work, not editing, and bundling it would delay the gate that
      stops the next issue from drifting.
rationale: |
  AGENTS.md carries the rule and nothing enforced it. The evidence-spine
  quality gates listed there are checked by eight scripts, none of which
  reads a brief's Top signals. The drift was found while authoring 2026-W35
  and is measurable: running the gate with W34 un-grandfathered reports 38
  violations across seven picks; with W33 un-grandfathered, 36. The
  same run also caught an off-taxonomy action surface in both issues, which
  is the check DEC-PUB-012 makes possible. The `LEGACY_BRIEFS` set is the
  honest form of the compromise: removing a week from it is the backfill's
  definition of done, and the set is small enough to read.
evidence:
  - kind: doc
    ref: scripts/validate_brief_fields.py
  - kind: doc
    ref: AGENTS.md
  - kind: doc
    ref: config/action_surface_taxonomy.yaml
  - kind: run
    ref: .github/workflows/ci.yml
rollback: |
  Delete `scripts/validate_brief_fields.py`, remove its step from
  `.github/workflows/ci.yml`, and remove the line from the AGENTS.md
  pre-commit list and the playbook verify step. No brief content changes,
  because the gate reads and never writes.
owner: science.proof-gate-runner
systems_map: |
  A rule written in AGENTS.md constrains an agent that reads AGENTS.md and
  chooses to comply. A rule written in a gate constrains the merge. Between
  the two sits the interval where a rule is believed to hold and does not,
  and the length of that interval is set by whether anything checks.
transferable_principle: |
  An unenforced invariant decays at a rate set by how convenient it is to
  skip, and its decay is invisible until something measures it. Style
  guides, schema conventions, and runbook steps all fail this way.
falsification_test: |
  If a brief passes this gate while carrying a pick whose falsification test
  names no observation, or whose adoption ladder repeats the Try line, the
  gate is checking for headings and not for content, and it needs a
  substance check on field length and distinctness.
adoption_ladder:
  minimum_viable: |
    The gate runs locally and in CI, checks briefs from 2026-W35 forward,
    and names the legacy set in code.
  mid_adoption: |
    2026-W32 through 2026-W34 are backfilled and removed from
    `LEGACY_BRIEFS` one week at a time.
  full_adoption: |
    `LEGACY_BRIEFS` is empty and the gate covers the whole archive, so the
    published corpus is uniformly queryable by field.
  monitoring_signals:
    - "violations caught per pull request"
    - "weeks remaining in LEGACY_BRIEFS"
    - "issues shipped with an off-taxonomy action surface, which should stay at zero"
---

## decision

Add `scripts/validate_brief_fields.py` and wire it into CI and the
pre-commit gate list. The gate checks each Top signal for a Source line, an
action surface that resolves against the taxonomy, the four systems-thinking
fields, an adoption ladder naming all four rungs, a Confidence label in
{high, medium, low}, and an Evidence line whose cell ids resolve against the
sibling `matrix/cells.yaml` when that file exists. Briefs 2026-W20 through
2026-W34 are listed in `LEGACY_BRIEFS` and skipped.

## alternatives

- Enforce on the whole archive: rejected because fifteen issues fail
  immediately and a permanently red gate gets bypassed.
- Rely on AGENTS.md and review: rejected because that is the arrangement
  that produced the drift.
- Relax the rule to match recent practice: rejected because the four fields
  are what makes a pick more than an annotated link.
- Backfill in the same change: rejected because reconstructing evidence for
  21 picks is research, and bundling it delays the gate.

## rationale

The rule existed and nothing checked it. Running the gate against
2026-W34 with the grandfather entry removed reports 38 violations across
seven picks; 2026-W33 reports 36. Both also used action surfaces absent from
`config/action_surface_taxonomy.yaml`. The legacy set records the debt in a
place a reader will find it.

## evidence

- `scripts/validate_brief_fields.py` (the gate, with `LEGACY_BRIEFS`)
- `AGENTS.md` (the rule, and the pre-commit list the gate joins)
- `config/action_surface_taxonomy.yaml` (`version: 2`, per DEC-PUB-012)
- `.github/workflows/ci.yml` (the CI step)
- `briefs/2026-W35/brief.md`, `briefs/2026-W36/brief.md` (first passing issues)
- `specs/0007-publishing/requirements.md#R-PUB-031`

## rollback

Delete the script, remove its CI step, and remove it from the AGENTS.md
pre-commit list and the playbook verify step. The gate never writes, so no
brief content changes on rollback.
