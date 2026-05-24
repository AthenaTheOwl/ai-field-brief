---
id: DEC-FND-010-four-gate-scripts-block-pr
spec: specs/0001-foundation/
requirement: R-FND-010
date: 2026-05-24
status: approved
reversible: true
decision: |
  CI runs four python gates on every PR against `main`: `spec_check`,
  `voice_lint`, `validate_schemas`, `validate_registry`. The same job
  runs `pnpm turbo run lint typecheck test build` plus a security audit
  (`pnpm audit` + gitleaks). Any gate that exits non-zero blocks the
  merge. `pnpm verify` chains the gate set locally so a contributor
  catches the same failures before push.
alternatives:
  - label: voice + spec gates only, defer schema + registry
    rejected_because: |
      The schema + registry gates catch entire bug classes (invalid
      `sources/registry.yaml` entries, malformed JSON schemas) that
      the typecheck does not see. Deferring them means CI catches
      structural drift only when downstream code breaks.
  - label: gates as warnings, not blockers
    rejected_because: |
      A warning that does not block gets ignored. The cost of a
      false-positive block is one revert; the cost of a silent
      warning is months of drift before someone notices.
  - label: single mega-script that wraps every gate
    rejected_because: |
      Per-gate jobs surface which check failed in the GitHub UI. A
      single wrapper hides the failure type until the contributor
      reads the log.
rationale: |
  Four python gates plus the turbo pipeline plus the security audit
  is the minimum that catches the spec, voice, schema, registry, and
  dependency-vulnerability bug classes the project commits to. Spec
  0010 later adds four more gates (validate_decisions, _roles, _tools,
  _policies); the eight-gate set is the current baseline.

  The decision is reversible: turning off a gate is a one-line CI
  config change. The rollback cost is whichever bug class that gate
  was catching.
evidence:
  - kind: doc
    ref: .github/workflows/ci.yml
  - kind: doc
    ref: scripts/spec_check.py
  - kind: doc
    ref: scripts/voice_lint.py
  - kind: doc
    ref: scripts/validate_schemas.py
  - kind: doc
    ref: scripts/validate_registry.py
rollback: |
  Remove the failing gate's step from `.github/workflows/ci.yml`. The
  script files stay on disk so a future re-enable is a one-line
  config change. Document the removal in the commit body so a future
  reviewer sees the decision.
owner: platform
---

## decision

CI runs four python gates on every PR against `main`: `spec_check`,
`voice_lint`, `validate_schemas`, `validate_registry`. Plus
`pnpm turbo run lint typecheck test build` and a security audit.
Spec 0010 later extends the gate set to eight.

## alternatives

- Voice + spec gates only — schema and registry drift surfaces only
  through downstream breakage.
- Gates as warnings, not blockers — warnings that do not block get
  ignored.
- Single mega-script wrapper — hides which gate failed in the GitHub
  UI.

## rationale

Four python gates plus the turbo pipeline plus the security audit
is the minimum that catches the spec, voice, schema, registry, and
dependency-vulnerability bug classes the project commits to.

## evidence

- `.github/workflows/ci.yml` — `gates` job runs the python set;
  `node` job runs the turbo pipeline; `security` job runs `pnpm
  audit` plus gitleaks.
- `scripts/spec_check.py` — structural check across spec ledgers.
- `scripts/voice_lint.py` — banlist + structural rules.
- `scripts/validate_schemas.py` — JSON Schema validation across
  `*.schema.json`.
- `scripts/validate_registry.py` — sources/registry.yaml shape check.

## rollback

Remove the failing gate's step from `.github/workflows/ci.yml`. The
script files stay on disk so a future re-enable is a one-line
config change.
