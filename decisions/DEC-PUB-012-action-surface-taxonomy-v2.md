---
id: DEC-PUB-012-action-surface-taxonomy-v2
spec: specs/0007-publishing/
requirement: R-PUB-030
date: 2026-09-04
status: approved
reversible: true
decision: |
  Amend `config/action_surface_taxonomy.yaml` to version 2, adding five
  surfaces the weekly briefs have needed and been unable to name:
  `security`, `cost`, `context`, `observability`, and `governance`. Record
  the three labels used off-taxonomy in briefs 2026-W32 through 2026-W34
  as retired aliases mapping to their canonical replacements: `state` to
  `runtime-adapter`, `protocol` to `architecture`, and `containment` to
  `security`.
alternatives:
  - label: keep taxonomy v1 and force picks onto the nearest existing surface
    rejected_because: |
      Three consecutive issues invented labels instead, which is the
      observable cost of a taxonomy that does not cover the corpus. Forcing
      an authorization-boundary pick onto `tool-policy` or a cache-pricing
      pick onto `config` also destroys the cross-week pattern detection the
      bounded taxonomy exists to serve.
  - label: adopt every label the briefs have used, including state, protocol, and containment
    rejected_because: |
      `state` duplicates `runtime-adapter`, which already covers snapshots,
      checkpoints, and replay. `protocol` duplicates `architecture`, which
      already covers interop contracts. `containment` is a subset of the new
      `security` surface. Adding all three would grow the taxonomy by eight
      entries while making two pairs indistinguishable at classification
      time.
  - label: drop the taxonomy constraint from AGENTS.md
    rejected_because: |
      The constraint is what makes an action surface a queryable field
      instead of a free-text label. Removing it would end cross-week
      aggregation and remove the reason the file exists.
rationale: |
  The taxonomy shipped at version 1 with fourteen surfaces chosen before
  the Brief OS format carried Action packets, Scout radar, or a security
  lane. Since then the corpus has produced picks about authorization
  boundaries, token and cache economics, context assembly, run evidence,
  and supplier posture, none of which resolve against v1. Briefs W32, W33,
  and W34 responded by writing labels that were never in the file, which
  went uncaught because nothing validated the field. Five additions cover
  the observed gap; the three retired aliases cover the observed
  duplication. `context` is kept distinct from `prompt` because the
  instruction artifact and the material carried alongside it are edited by
  different work and measured by different evidence, a split the 2026-W35
  context-file result makes concrete.
evidence:
  - kind: doc
    ref: config/action_surface_taxonomy.yaml
  - kind: doc
    ref: briefs/2026-W35/brief.md
  - kind: doc
    ref: briefs/2026-W36/brief.md
  - kind: run
    ref: scripts/validate_brief_fields.py
rollback: |
  Restore `version: 1` in `config/action_surface_taxonomy.yaml`, delete the
  five added surfaces and the `aliases` block, and reclassify the 2026-W35
  and 2026-W36 picks onto v1 surfaces. Remove the surface check from
  `scripts/validate_brief_fields.py`, which is the only consumer of the
  `aliases` key.
owner: product.spec-writer
systems_map: |
  A pick's action surface is the join key between a weekly brief and the
  portfolio's work queue. When the taxonomy cannot express a pick, the
  author invents a label, the join breaks silently, and cross-week pattern
  detection degrades without anyone seeing a failure.
transferable_principle: |
  A controlled vocabulary that cannot express what its authors observe gets
  bypassed, not obeyed, and the bypass is invisible until something
  validates the field. The same applies to incident taxonomies, expense
  categories, and issue labels.
falsification_test: |
  If briefs 2026-W37 through 2026-W40 introduce two or more further
  off-taxonomy labels, five additions were the wrong shape and the surface
  field should become a two-level scheme with a small top level instead of
  a growing flat list.
adoption_ladder:
  minimum_viable: |
    Taxonomy at version 2 with the five added surfaces and the alias block,
    and both new briefs authored against it.
  mid_adoption: |
    `scripts/validate_brief_fields.py` rejects any surface not in the file
    and names the replacement for a retired alias.
  full_adoption: |
    Action-surface counts are aggregated across the archive so a surface
    trending upward becomes a signal about where the portfolio's work is
    concentrating.
  monitoring_signals:
    - "off-taxonomy surface labels caught per issue"
    - "picks per surface per quarter"
    - "surfaces with zero picks over four issues, which are candidates for retirement"
---

## decision

Amend `config/action_surface_taxonomy.yaml` to version 2. Add five
surfaces: `security` (authorization boundary, permission rule, credential
scope, sandbox isolation, blast-radius limit), `cost` (token, cache, or
routing economics), `context` (what the model carries, as distinct from the
`prompt` instruction artifact), `observability` (traces, run evidence, and
the accounting that shows whether a change worked), and `governance`
(approval path, disclosure obligation, supplier or procurement posture).
Record `state`, `protocol`, and `containment` as retired aliases pointing at
`runtime-adapter`, `architecture`, and `security`.

## alternatives

- Keep v1 and force picks onto the nearest surface: rejected because three
  issues already invented labels instead, and forcing destroys the
  cross-week aggregation the taxonomy exists to serve.
- Adopt every label the briefs have used: rejected because `state`,
  `protocol`, and `containment` duplicate surfaces that already exist.
- Drop the taxonomy constraint: rejected because the constraint is what
  makes the field queryable.

## rationale

Version 1 predates the Brief OS format's security lane, Action packets, and
Scout radar. The corpus has since produced picks the file cannot name, and
the authors wrote new labels instead of mis-filing them. Nothing validated
the field, so the drift ran for three issues. Five additions cover the
observed gap and three aliases cover the observed duplication.

## evidence

- `config/action_surface_taxonomy.yaml` (`version: 2`, 19 surfaces, 3 aliases)
- `briefs/2026-W32/brief.md`, `briefs/2026-W33/brief.md`,
  `briefs/2026-W34/brief.md` (the off-taxonomy labels)
- `briefs/2026-W35/brief.md`, `briefs/2026-W36/brief.md` (first issues
  authored against v2)
- `scripts/validate_brief_fields.py` (the surface check)
- `specs/0007-publishing/requirements.md#R-PUB-030`

## rollback

Restore `version: 1`, delete the five added surfaces and the `aliases`
block, reclassify the W35 and W36 picks, and remove the surface check from
`scripts/validate_brief_fields.py`.
