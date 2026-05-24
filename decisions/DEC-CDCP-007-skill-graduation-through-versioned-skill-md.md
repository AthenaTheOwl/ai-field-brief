---
id: DEC-CDCP-007-skill-graduation-through-versioned-skill-md
spec: specs/0010-cognitive-delivery-control-plane/
requirement: R-CDCP-007
date: 2026-05-24
status: approved
reversible: true
decision: |
  A recurring pattern earns reuse as
  .agents/skills/<id>/SKILL.md with semantic version, owner_guild,
  and an evals reference (which may start empty with a TODO).
  Graduation past v0.1.0 requires human_approval per the promotion
  policy. The learning.skill-curator role owns the graduation
  cadence; the SKILL.md front-matter parses against the cross-repo
  skill.schema.json.
alternatives:
  - label: implicit reuse (just copy-paste across roles)
    rejected_because: |
      Copy-paste reuse drifts. Three copies of the same playbook
      diverge in three weeks. A SKILL.md with one canonical body
      and a version stamp gives the agent a stable reference.
  - label: skills as un-versioned playbooks
    rejected_because: |
      Without a version, a SKILL update silently changes the
      behavior every downstream caller gets. SemVer keeps the
      contract explicit; minor bumps for behavior changes, patch
      bumps for body edits.
  - label: graduate every recurrence on first occurrence
    rejected_because: |
      A pattern is not a skill until it recurs. The three-recurrence
      rule (documented in the skill-curator instructions) keeps the
      registry from filling with one-off ideas.
rationale: |
  Skills are the reuse layer. They sit between memory (per-agent
  preferences) and tools (per-role atomic actions). A SKILL.md
  carries the workflow, the gates it must clear, the inputs and
  outputs, and the version stamp. Semantic versioning lets a
  caller pin to a known-good version while the curator iterates.

  The human-approval-on-graduation policy keeps a fresh agent from
  auto-promoting its own work. The learning.skill-curator role
  drafts the SKILL and the matching DEC; a human signs off before
  the patch lands.
evidence:
  - kind: spec
    ref: specs/0010-cognitive-delivery-control-plane/requirements.md
  - kind: doc
    ref: .agents/skills/run-weekly-brief/SKILL.md
  - kind: doc
    ref: .agents/skills/install-cdcp-governance/SKILL.md
  - kind: doc
    ref: .agents/roles/learning.skill-curator/
  - kind: doc
    ref: ../athena-site/ops/schemas/skill.schema.json
rollback: |
  Delete .agents/skills/ and the skill-curator role files. Fold the
  graduated playbooks back under playbook/ as un-versioned markdown.
  Reuse drift returns; no data loss.
owner: editorial
---

## decision

A recurring pattern earns reuse as `.agents/skills/<id>/SKILL.md`
with semantic version, owner_guild, and an evals reference.
Graduation past v0.1.0 requires `human_approval`. The
`learning.skill-curator` role owns the graduation cadence.

## alternatives

- Implicit reuse (copy-paste across roles) — three copies diverge
  in three weeks.
- Un-versioned playbooks — a SKILL update silently changes
  downstream behavior.
- Graduate every recurrence on first occurrence — a pattern is
  not a skill until it recurs (three-recurrence rule).

## rationale

Skills are the reuse layer between memory and tools. A SKILL.md
carries the workflow, the gates it must clear, and the version
stamp. Semantic versioning lets a caller pin to a known-good
version while the curator iterates. The
human-approval-on-graduation policy keeps a fresh agent from
auto-promoting its own work; the skill-curator drafts the SKILL
and the matching DEC, a human signs off, and the patch lands.

## evidence

- `specs/0010-cognitive-delivery-control-plane/requirements.md` —
  R-CDCP-007 acceptance.
- `.agents/skills/run-weekly-brief/SKILL.md` — v0.1.0, the first
  graduated skill.
- `.agents/skills/install-cdcp-governance/SKILL.md` — second
  graduated skill (promoted in 2026-W21 dream pass).
- `.agents/roles/learning.skill-curator/` — the owning role.
- `../athena-site/ops/schemas/skill.schema.json` — the cross-repo
  contract.

## rollback

Delete `.agents/skills/` and the skill-curator role files. Fold
the playbooks back under `playbook/` as un-versioned markdown. No
data loss.
