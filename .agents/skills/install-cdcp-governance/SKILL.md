---
id: install-cdcp-governance
version: 0.1.0
owner_guild: control
trigger:
  - install-cdcp-in-a-new-or-existing-repo
  - bring a repo into the portfolio governance scaffold
  - bootstrap specs/decisions/dreams + .agents/ across a repo
instructions_file: .agents/skills/install-cdcp-governance/SKILL.md
scripts: []
evals: []
promotion_policy:
  requires:
    - human_approval
---

# skill: install-cdcp-governance

Promote a repo onto the Cognitive Delivery Control Plane (CDCP): the
spec ledger, the decisions ledger, the dream cadence, the operating-model
artifacts under `.agents/`, the event log, and the eight executable gates
that block a PR when any of the contracts drift. Graduated from three
prior installs (athena-site, supplier-risk-rag-agent, ai-field-brief).

## Pre-conditions

The repo must satisfy all of:

- Python 3.11 or newer on the contributor's path and on CI.
- A `git remote` named `origin`. The install commits push to `main`.
- The contributor holds push rights to `main`. The repo's branch
  protection runs the eight gates on push.
- One of:
  - greenfield repo with no `.agents/AGENTS.md` (full install), or
  - existing `.agents/AGENTS.md` without `.agents/roles/` (operating-
    model layer install only), or
  - existing `.agents/roles/` (deferred-role promotion only; this
    skill does not apply).

If any pre-condition fails, halt and file a DEC naming the gap before
running the install.

## Detect-state branch

Run these three checks at the repo root in order. The first branch that
matches drives the install:

1. **Greenfield** — no `.agents/` directory. The install lands both the
   governance base (spec 0010) and the operating-model layer
   (spec 0011) in two sequential commits. See branch (a) below.
2. **Base-CDCP-already-present** — `.agents/AGENTS.md` exists and
   `decisions/DEC-CDCP-001-*.md` exists, but `.agents/roles/` is
   absent. The install lands only the operating-model layer. See
   branch (b) below.
3. **Operating-model-already-present** — `.agents/roles/` exists with
   one or more role directories. The install is complete; this skill
   does not apply. Open a DEC for whatever extension you intended
   instead.

## Steps

### Branch (a) — greenfield install (two commits)

Commit 1: governance scaffold (mirror of `5b3b792` in ai-field-brief).
File order matters because some files reference others:

1. `ops/schemas-cache/` — fetch the seven cross-repo schemas from
   `athena-site/ops/schemas/` and cache locally. Validators read
   the cache when CI runs offline.
2. `specs/README.md` and `specs/0010-cognitive-delivery-control-plane/`
   — the six-file spec ledger (requirements, design, tasks, acceptance,
   research, traceability). Reserves the R-CDCP-* prefix.
3. `decisions/README.md` and the first two DECs:
   `DEC-CDCP-001-install-cdcp-governance.md` (records the install),
   `decisions/.spec-check-allowlist.yaml` (defers backfill R-* IDs).
4. `dreams/README.md` — reserves the dream contract; no per-week
   directories yet.
5. `ops/event-log/` and `ops/RELEASE_LEDGER.md` — append-only ledgers.
6. `.agents/AGENTS.md` — the agent contract.
7. `scripts/` — `spec_check.py`, `voice_lint.py`,
   `validate_schemas.py`, `validate_registry.py`,
   `validate_decisions.py` (five gates at this point).
8. `.github/workflows/ci.yml` — add a `gates` job that runs the five
   python gates. Keep the existing `node` and `security` jobs.

Commit 2: operating-model layer (mirror of `b4b9cf2` in ai-field-brief):

1. `.agents/tools.yaml` — 16 seed tools. Cross-checked against
   `tool.schema.json` by `validate_tools.py`.
2. `.agents/policies/*.yaml` — 5 declarative permission rules.
   Default-deny baseline (priority 0); explicit allows (priority 100);
   reviewer-cannot-edit-code deny (priority 200).
3. `.agents/state-machines/*.yaml` — 3 artifact lifecycles
   (spec, run, release).
4. `.agents/workflows/*.yaml` — 3 step graphs (single-change,
   weekly-dream, incident-response).
5. `.agents/roles/<id>/` — 6 worked-example role directories. Each
   carries `role.yaml`, `instructions.md`, `tools.yaml`,
   `output.schema.json`, `gates.yaml`.
6. `.agents/CATALOG.md` — the 44 deferred role TODO list.
7. `scripts/validate_roles.py`, `validate_tools.py`,
   `validate_policies.py` — the three new gates.
8. `.github/workflows/ci.yml` — extend the `gates` job to run the
   three new gates (eight gates total).
9. `decisions/DEC-CDCP-002-install-operating-model.md` — records the
   layer install. Add R-CDCP-001..010 entries to the allowlist's
   `roles_deferred` section.

### Branch (b) — base-CDCP-already-present (one commit)

Run commit 2 from branch (a) only. The governance base is already on
disk; the install adds the operating-model layer on top.

## Verification

The gate chain that must exit 0 before the push:

```bash
python scripts/spec_check.py
python scripts/voice_lint.py
python scripts/validate_schemas.py
python scripts/validate_registry.py
python scripts/validate_decisions.py
python scripts/validate_roles.py
python scripts/validate_tools.py
python scripts/validate_policies.py
```

Per-repo build and test gates run after the python set:

```bash
pnpm install                # if the repo carries a node workspace
pnpm turbo run typecheck
pnpm turbo run test
pnpm turbo run build
```

A green run plus a clean `git status` is the install's exit condition.

## Stash + restore protocol

If the working tree carries uncommitted WIP across the install (a
common case in ai-field-brief, where Phase 2 source-registry work
lives in the tree across runs), stash before starting:

```bash
git stash push --include-untracked -m "cdcp install: hold during run" -- \
  <specific files and dirs the WIP touches>
```

After both install commits push and gates exit 0:

```bash
git stash pop
```

The pop may produce a small conflict on `specs/README.md` if the
install added a new spec entry on the same lines the WIP touched.
Resolve by keeping both entries; unstage so the WIP returns to its
original unstaged-plus-untracked shape.

## Honest deferrals

The install ships only the worked examples; the long tail stays
deferred and tracked in `.agents/CATALOG.md`:

- 44 deferred roles in `CATALOG.md`. Promotion off the catalog
  requires a PR with the role file set, a DEC, and the catalog entry
  removal in the same commit. The full set lands across later passes.
- R-CDCP-001..010 owner_role tokens stay in
  `decisions/.spec-check-allowlist.yaml` under `roles_deferred` until
  the spec 0010 `traceability.md` gets a backfill pass.
- R-FND-* and R-BOOT-* requirements that pre-date the CDCP install
  stay in the allowlist's `deferred` section; per-requirement DECs
  land in a backfill pass.
- The skill's `evals` array is empty at v0.1.0. A `passing_skill_eval`
  lands when a fourth install runs clean against a fresh repo using
  this SKILL.md as the only input.

Name what is not done in the install commit body; do not let a
deferred item ship as silently absent.

## References

Exemplar install commits across the portfolio (read these before
running the install for the first time):

- `ai-field-brief` `b4b9cf2` — operating-model layer install
  (six roles, 16 tools, five policies, three state machines, three
  workflows, three validators, CATALOG of 44 deferred roles).
- `supplier-risk-rag-agent` `5274a4d` — sibling install in the
  RAG-agent product surface.
- `procurement-lab` `3cd9314` — sibling install in the legacy
  procurement-negotiation-lab repo.

Source-of-truth schemas:

- [athena-site/ops/schemas/](https://github.com/AthenaTheOwl/athena-site/tree/main/ops/schemas)
  — the seven cross-repo schemas the install caches and validates against.
- [athena-site/ops/control-plane.md](https://github.com/AthenaTheOwl/athena-site/blob/main/ops/control-plane.md)
  — the CDCP charter naming the six artifact types and the cross-repo
  contracts.
