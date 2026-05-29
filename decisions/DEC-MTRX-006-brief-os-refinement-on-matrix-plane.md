---
id: DEC-MTRX-006-brief-os-refinement-on-matrix-plane
spec: specs/0012-prompt-matrix-plane/
requirement: R-MTRX-007
date: 2026-05-29
status: approved
reversible: true
amends: DEC-MTRX-001-prompt-matrix-plane-install
decision: |
  ai-field-brief adopts the Brief OS framing on top of the matrix
  plane. The three-pass note system formalizes the matrix loop:
  Pass 1 (structured source note) maps to the `source_gist`,
  `claims_and_bets`, and `mechanism_extraction` lenses under
  `science.matrix-runner`; Pass 2 (faithfulness audit) maps to the
  seven-question check under `science.cell-verifier`; Pass 3
  (action extraction) maps to the `reusable_pattern`,
  `adoption_action`, and `risk_and_caveats` lenses under
  `science.matrix-synthesis-editor`. A scoring model
  (`config/scoring_model.yaml`) with three axes (`source_quality`,
  `profile_relevance`, `actionability`) and four penalties drives
  digest promotion: `final_score >= 12` lands in Top signals,
  `final_score in [9, 12)` drops to the Watchlist, `final_score < 9`
  archives. A profiles registry (`config/profiles.yaml`) carries the
  initial `personal` and `broad_builder` profiles; every MatrixRun
  pins to one profile id and the scoring axis weights respect any
  per-profile overrides. The action-surface taxonomy
  (`config/action_surface_taxonomy.yaml`) carries 14 canonical
  surfaces; every action candidate cites one and only one. The
  evidence-spine rules in `AGENTS.md` enforce the chain end-to-end:
  no digest claim without verified cells, no cell verified without
  source refs, no action promoted without the six required fields
  plus a surface from the taxonomy plus a scoring entry.
alternatives:
  - label: keep the matrix plane as the only contract; treat scoring and profiles as future work
    rejected_because: |
      Without scoring and profiles every verified cell becomes a
      candidate Top-signal claim, the digest grows to twenty picks,
      and the brief reverts to noise. The matrix plane gave the
      intermediate representation; the Brief OS gives the selection
      and ranking discipline that turns the cells into a brief a
      human reads in ten minutes. Deferring scoring and profiles
      means the second ChatGPT chat's framing
      ("source-to-action intelligence system, not AI news digest")
      stays prose, not contract.
  - label: bake the scoring weights into the matrix synthesis prompt
    rejected_because: |
      A scoring rubric living inside the synthesis prompt is opaque
      to the human review pass and to cross-week pattern detection.
      Configuration in YAML lets the human review the weights, the
      thresholds, and the per-profile overrides as a typed artifact
      every push. The prompt reads the configuration; the
      configuration is the contract.
  - label: ship one profile (the personal profile) and add others later
    rejected_because: |
      A single-profile brief over-fits to the personal portfolio and
      loses the cross-profile sanity check. The `broad_builder`
      profile lands now as the read-back signal that the brief is
      legible to readers who do not share the personal portfolio.
      Two profiles is the minimum honest configuration; one is the
      brief-as-personal-newsletter mode the Brief OS framing
      explicitly rejects.
  - label: let each brief invent its own action surfaces
    rejected_because: |
      An open-vocabulary surface list breaks cross-week pattern
      detection and lets the brief drift into ad-hoc categories
      every week. The 14-surface taxonomy is bounded by design;
      extensions land via a new DEC and a bump to
      `config/action_surface_taxonomy.yaml`, so adding a surface is
      a recorded choice, not a brief-author accident.
rationale: |
  The matrix plane (DEC-MTRX-001) gave the digest a verified
  intermediate representation; three published briefs under that
  shape showed two follow-on failure modes the matrix alone does
  not catch. First: every verified cell looks like a candidate
  Top-signal pick, and the digest grows to fifteen-plus picks
  unless a scoring rubric gates promotion. Second: a brief written
  for the personal portfolio drifts into a personal newsletter
  unless a second profile reads the same corpus. The scoring model
  plus the profiles config close both gaps inside the same
  contract. The action-surface taxonomy closes a third gap visible
  in the W22 brief: action candidates without a bounded surface
  vocabulary fragment into ad-hoc categories that defeat the
  cross-week pattern detection the brief's `Reusable patterns`
  section relies on. Naming the three-pass system in `AGENTS.md`
  ties the lenses to the passes explicitly; the brief author and
  the role contracts both read the same map. The evidence-spine
  rules upgrade the per-claim audit from a playbook step into a
  contract every role honors. The second ChatGPT chat's framing
  ("source-to-action intelligence system, not AI news digest") is
  now the contract this DEC names, not prose.
evidence:
  - kind: decision
    ref: decisions/DEC-MTRX-001-prompt-matrix-plane-install.md
  - kind: decision
    ref: decisions/DEC-PUB-004-faithfulness-audit-before-publish.md
  - kind: spec
    ref: specs/0012-prompt-matrix-plane/
  - kind: doc
    ref: config/scoring_model.yaml
  - kind: doc
    ref: config/profiles.yaml
  - kind: doc
    ref: config/action_surface_taxonomy.yaml
  - kind: doc
    ref: templates/weekly-brief.md
  - kind: doc
    ref: AGENTS.md
  - kind: doc
    ref: playbook/run-weekly-brief.md
rollback: |
  Remove `config/scoring_model.yaml`, `config/profiles.yaml`, and
  `config/action_surface_taxonomy.yaml`. Revert
  `templates/weekly-brief.md` to the pre-Brief-OS shape (drop the
  Field thesis, Reusable patterns, Action queue, Watchlist,
  Archive notes, and Sources reviewed sections). Drop the Brief OS
  evidence-spine, three-pass, scoring, and profiles sections from
  `AGENTS.md`. Drop the configuration references from
  `playbook/run-weekly-brief.md` (steps 4-6 keep the matrix-plane
  framing from DEC-MTRX-001). Drop R-MTRX-007..014 from
  `specs/0012-prompt-matrix-plane/requirements.md`,
  `acceptance.md`, `tasks.md`, and `traceability.md`. The matrix
  plane itself (DEC-MTRX-001) stays intact; the refinement layer
  unwinds without touching the underlying cell + verifier +
  synthesis loop.
owner: science.matrix-synthesis-editor
---

## decision

ai-field-brief adopts the Brief OS framing on top of the matrix
plane installed under DEC-MTRX-001. The three-pass note system
formalizes the matrix loop: Pass 1 produces structured source
notes, Pass 2 audits faithfulness, Pass 3 extracts actions. A
scoring model with three axes (source_quality, profile_relevance,
actionability) and four penalties drives digest promotion. A
profiles registry pins each MatrixRun to a `profile_id` and the
initial set carries `personal` and `broad_builder`. A canonical
14-surface action taxonomy bounds the action candidates the
digest emits. The evidence-spine rules in `AGENTS.md` enforce the
chain end-to-end.

## alternatives

- Keep the matrix plane as the only contract; defer scoring and
  profiles. Rejected because every verified cell becomes a
  candidate Top-signal claim without a ranking gate; the digest
  reverts to noise and the second ChatGPT chat's framing stays
  prose, not contract.
- Bake the scoring weights into the synthesis prompt. Rejected
  because a rubric inside the prompt is opaque to human review and
  to cross-week pattern detection; YAML configuration lets the
  reader see the weights as a typed artifact.
- Ship one profile and add others later. Rejected because a
  single-profile brief over-fits to the personal portfolio and
  loses the cross-profile sanity check; `broad_builder` lands now
  as the read-back signal.
- Let each brief invent its own action surfaces. Rejected because
  an open vocabulary fragments the brief week-to-week and breaks
  cross-week pattern detection; the bounded 14-surface taxonomy
  carries extension via a recorded DEC, not a brief-author
  accident.

## rationale

The matrix plane gave the digest a verified intermediate
representation; three published briefs under that shape exposed
two follow-on failure modes. First: every verified cell looks
like a candidate Top-signal pick unless a scoring rubric gates
promotion. Second: a brief written for the personal portfolio
drifts into a personal newsletter unless a second profile reads
the same corpus. The scoring model plus profiles close both gaps
inside the same contract; the action-surface taxonomy closes a
third gap visible in the W22 brief (ad-hoc action categories).
Naming the three-pass system in `AGENTS.md` ties the lenses to
the passes; the evidence-spine rules upgrade the per-claim audit
from a playbook step into a contract every role honors.

## evidence

- `decisions/DEC-MTRX-001-prompt-matrix-plane-install.md` is the
  install DEC this DEC amends.
- `decisions/DEC-PUB-004-faithfulness-audit-before-publish.md`
  carries the per-pick audit pattern the evidence-spine rules
  upgrade into a cross-role contract.
- `specs/0012-prompt-matrix-plane/` carries R-MTRX-007..014 with
  acceptance per requirement.
- `config/scoring_model.yaml`, `config/profiles.yaml`, and
  `config/action_surface_taxonomy.yaml` carry the typed shape of
  the scoring rubric, the profiles registry, and the action
  taxonomy.
- `templates/weekly-brief.md`, `AGENTS.md`, and
  `playbook/run-weekly-brief.md` carry the user-facing surfaces
  the Brief OS framing lands on.

## rollback

Remove the three new configuration files, revert the Brief OS
sections from the template, drop the Brief OS sections from
`AGENTS.md`, drop the configuration references from the
playbook, and drop R-MTRX-007..014 from the matrix-plane spec.
The matrix-plane install (DEC-MTRX-001) stays intact; the
refinement layer unwinds cleanly without touching the underlying
cell + verifier + synthesis loop.
