---
id: skill-001-install-cdcp-governance
target_kind: skill_patch
target: .agents/skills/install-cdcp-governance/SKILL.md
skill_id: install-cdcp-governance
human_review_required: true
status: promoted
promotion_date: 2026-05-24
evidence:
  - kind: commit
    ref: 5b3b792 — spec 0010 install in ai-field-brief (Cognitive Delivery Control Plane governance + executable DEC enforcement)
  - kind: commit
    ref: b4b9cf2 — spec 0011 install in ai-field-brief (six roles, tool registry, policies, state machines, workflows, event log)
  - kind: file
    ref: .agents/roles/, .agents/policies/, .agents/state-machines/, .agents/workflows/, .agents/tools.yaml, .agents/CATALOG.md — the artifact set the install produces
  - kind: doc
    ref: decisions/DEC-CDCP-001-install-cdcp-governance.md and DEC-CDCP-002-install-operating-model.md — the two-DEC pattern that records the install in any new repo
  - kind: doc
    ref: ai-field-brief is the third repo in the portfolio to receive this scaffold (per DEC-CDCP-001 rationale; sibling repos supplier-risk-rag-agent and procurement-lab carry sibling installs)
---

## proposal

Promote the install pattern from a one-off two-commit sequence into a named skill at `.agents/skills/install-cdcp-governance/SKILL.md`. The skill captures the install playbook so the fourth repo in the portfolio runs it as one named operation instead of re-discovering the steps.

Proposed `SKILL.md` outline (the actual file lands during promotion, not during this dream pass):

```markdown
# install-cdcp-governance

## When to use
A new repo joins the portfolio and needs the governance scaffold:
specs/, decisions/, dreams/, ops/, .agents/, plus executable gates.

## What it produces
- `.agents/` with 6 worked roles, 16 tools, 5 policies, 3 state machines,
  3 workflows, plus CATALOG of deferred roles
- `decisions/` with two seed DECs (install-governance, install-operating-model)
- `dreams/` with README reserving the contract
- `ops/event-log/` and `ops/RELEASE_LEDGER.md`
- `scripts/` — eight gates: spec_check, voice_lint, validate_schemas,
  validate_registry, validate_decisions, validate_roles, validate_tools,
  validate_policies
- `ops/schemas-cache/` — local mirror of cross-repo schemas

## Inputs
- repo name, primary product surface, owner guild
- which of the 44 deferred roles get worked-example treatment in this repo

## Steps
1. Land spec 0010 (governance scaffold) — commit shape per 5b3b792.
2. Land spec 0011 (operating model) — commit shape per b4b9cf2.
3. Pick worked-example roles, scaffold each per AGENTS.md "How to add a new role".
4. Run all eight gates, push.

## Evals
- Every gate exits 0 against a clean working tree.
- spec_check sees ≥2 active specs and resolves every owner_role token.
- validate_roles / validate_tools / validate_policies see the new files.
- DEC-CDCP-001 and DEC-CDCP-002 land before the spec_check sweep.

## Version: 0.1.0 (skill graduates to 1.0.0 after a fourth install ships clean)
```

## why it earns its keep

This week shipped the install in ai-field-brief across two commits totaling roughly 2000 lines of governance scaffold. The same install pattern lives in (per DEC-CDCP-001 rationale) athena-site and the procurement repos. Three installs in three repos with the same shape is the dream's threshold for graduation.

The install is also the kind of operation that an agent does once and forgets. Naming it as a skill captures the steps before the institutional memory drifts. The next install becomes "run the skill" instead of "re-read the prior install commit and copy the structure."

The skill also gives the dream-orchestrator a place to write candidates against. If a future install run flags a missing step or a regression, the report writes a `skill_patch` candidate against `install-cdcp-governance` — which is the kind of feedback loop the current scaffold lacks.

## evidence

- `5b3b792` — first install commit. Touches 50+ files across `.agents/`, `decisions/`, `dreams/`, `ops/`, `scripts/`. Repeatable shape.
- `b4b9cf2` — second install commit (operating model layer). Touches the same directory tree with a second pass. The two-commit shape is the install's actual shape.
- `decisions/DEC-CDCP-001-install-cdcp-governance.md` rationale section: "The CDCP framing came out of a synthesis pass across athena-site and ai-field-brief." Two repos as the synthesis input, ai-field-brief as the third install — the threshold for the skill is met.
- `.agents/CATALOG.md` — the 44 deferred roles. A skill that automates the install scopes the role-set decision; without the skill, every install re-litigates which roles ship as worked examples.
- The current `.agents/skills/` directory holds one skill (`run-weekly-brief`); the install pattern is the natural second.

## promotion path

If approved, the promotion creates a new skill folder:

- `.agents/skills/install-cdcp-governance/SKILL.md` — the skill content.
- `.agents/skills/install-cdcp-governance/install.md` (optional) — the actual playbook with copyable bash blocks.
- `.agents/CATALOG.md` — entry if the skill is owned by a deferred role.
- `decisions/DEC-CDCP-003-install-skill-graduation.md` — DEC recording the graduation.

Reviewer checks:

1. The skill's steps reproduce `5b3b792` and `b4b9cf2` against a fresh repo.
2. The eval list is concrete enough to gate the skill at version bump time.
3. The skill carries the `human_review_required` flag on its output (the install creates an `apply_patch`-class change; the policy layer must allow it).
4. The skill does not duplicate `templates/spec-six-pack.md` (if it exists) — if it does, point at it instead of re-stating.

Owner role: `control.coordinator` (the install is a portfolio-coordination operation, not a feature-shipping one).

## risks if promoted blindly

- Three installs in three repos with the same shape is the graduation threshold, but the third install (ai-field-brief, this week) is the largest of the three. A skill that codifies the largest install assumes new repos need the full set. A smaller repo may want a `governance-lite` variant.
- The install touches `.agents/AGENTS.md` and other contract files. A skill that auto-applies risks overwriting bespoke per-repo customization. The `human_review_required: true` flag is the safeguard; reviewer should confirm the skill never runs without it.
- The 16-tool registry and 5-policy set are this week's choices, not eternal ones. A skill that bakes them in becomes the source of policy drift across the portfolio. Reviewer should treat the tool list and the policy list as inputs to the skill, not as hard-coded constants.
- Once the skill exists, future installs that diverge from it create a "skill vs reality" gap that the dream-orchestrator should watch for. The skill needs an attached drift-detection eval.
