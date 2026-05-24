# requirements: cdcp-operating-model

## Scope

Spec 0011 installs the CDCP operating-model layer on top of the base
spec 0010 shipped. Roles, tools, policies, state machines, workflows,
and the event log become first-class records the gates check. Six
roles ship as worked examples; the rest of the 50-role catalog stays
tracked under `.agents/CATALOG.md` as deferred work.

The cross-repo schemas under
`https://raw.githubusercontent.com/AthenaTheOwl/athena-site/main/ops/schemas/`
remain the source of truth. This repo references the schemas by URL
and keeps a cache copy under `ops/schemas-cache/` for offline CI.

## Requirements

### R-CDCP-011: six minimum-viable roles installed

WHEN a coding agent reads `.agents/roles/`, THE SYSTEM SHALL hold the
file set for six worked-example roles: `control.coordinator`,
`product.spec-writer`, `engineering.implementation`,
`engineering.code-reviewer`, `science.proof-gate-runner`, and
`learning.dream-orchestrator`. Each role carries `role.yaml`,
`instructions.md`, `tools.yaml`, `output.schema.json`, and
`gates.yaml`.

Acceptance:
- `python scripts/validate_roles.py` walks the six role.yaml files
  and exits zero.
- Each `instructions.md` runs 80–120 lines naming mission, inputs,
  outputs, allowed tools, forbidden actions, required gates,
  escalation paths, and the runtime that owns the role.
- `voice_lint` passes on every `instructions.md`.

### R-CDCP-012: tool registry validated against the cross-repo schema

WHEN a tool entry lands in `.agents/tools.yaml`, THE SYSTEM SHALL
match the cross-repo `tool.schema.json` contract and name `id`,
`description`, `risk_level`, `allowed_roles`, `requires_approval`,
`forbidden_paths`, `emits_events`, and `output_schema`.

Acceptance:
- `python scripts/validate_tools.py` reads the registry as a YAML
  list, validates each entry against the cross-repo schema, and
  exits zero on the 16 seed entries.
- The validator fetches the schema by URL with a local cache fallback
  at `ops/schemas-cache/tool.schema.json`.
- Every tool's `allowed_roles` list names only role ids that exist
  under `.agents/roles/`.

### R-CDCP-013: policies validated with a default-deny baseline

WHEN a policy file lands under `.agents/policies/`, THE SYSTEM SHALL
match the cross-repo `policy.schema.json` contract and the policy set
SHALL include a default-deny baseline at priority 0 that targets all
roles and all tools.

Acceptance:
- `python scripts/validate_policies.py` walks every
  `.agents/policies/*.yaml`, validates each against the cross-repo
  schema, and confirms the default-deny baseline is present.
- The validator fetches the schema by URL with a local cache fallback
  at `ops/schemas-cache/policy.schema.json`.
- A missing default-deny baseline fails the gate.

### R-CDCP-014: workflows reference only catalog roles

WHEN a workflow lands under `.agents/workflows/`, THE SYSTEM SHALL
match the cross-repo `workflow.schema.json` contract and every step's
`role` field SHALL name a role id either installed under
`.agents/roles/` or tracked under `.agents/CATALOG.md`.

Acceptance:
- The three workflows (`single-change`, `weekly-dream`,
  `incident-response`) parse against the schema.
- Every step references a role id that resolves to either an
  installed role or a deferred-catalog entry.
- The legacy file at `control-plane/workflows/single-change.yaml`
  carries a `moved_to:` pointer to the new path.

### R-CDCP-015: event log is append-only JSONL

WHEN a workflow event fires, THE SYSTEM SHALL append one JSON object
per line to `ops/event-log/YYYY-MM-DD.jsonl`. Each line matches the
cross-repo `event.schema.json` contract. Existing lines are never
edited or deleted; a correction lands as a new event with a
`parent_event_id` pointer.

Acceptance:
- `ops/event-log/2026-05-24.jsonl` carries one event per line.
- The first two events name the operating-model install
  (`cdcp.operating_model.installed`) and the spec creation
  (`spec.created`).
- Each event carries `event_id`, `type`, `created_at`, `actor`, and
  `payload` per the schema.

### R-CDCP-016: 44 deferred roles tracked in the catalog

WHEN a role from the 50-role catalog has not yet shipped, THE SYSTEM
SHALL track the role in `.agents/CATALOG.md` under the owning guild
with name, mission, and status (`not-installed`). Promotion of a role
off the catalog and into `.agents/roles/` requires a PR that lands
the file set, a DEC, and the catalog entry removal in the same
commit.

Acceptance:
- `.agents/CATALOG.md` lists 44 deferred roles organized by guild.
- Each entry carries name, one-line mission, and status.
- The catalog header documents the promotion rule.
