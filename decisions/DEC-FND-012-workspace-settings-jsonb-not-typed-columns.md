---
id: DEC-FND-012-workspace-settings-jsonb-not-typed-columns
spec: specs/0001-foundation/
requirement: R-FND-012
date: 2026-05-24
status: approved
reversible: true
decision: |
  Per-workspace configuration (rubric ref, voice rules ref, integration
  creds ref, billing ref) lives on `workspaces.settings`, a JSONB column
  with a `{}` default. Later specs (0005 rubric, 0010 integrations,
  0011 billing) add typed accessors over the `settings` bag instead of
  promoting each key to a top-level column. The accessors land in the
  spec that owns the key, not at Phase 1.
alternatives:
  - label: typed top-level columns per workspace setting
    rejected_because: |
      Each new spec adds 3 to 5 settings keys. A typed-column approach
      would mean a migration plus a schema bump per spec. The jsonb
      bag carries the same data without a migration per key; the typed
      accessor over the bag gives the spec's code the same compile-
      time safety.
  - label: separate settings table per workspace
    rejected_because: |
      A side table doubles the read for every workspace load and adds
      a join to the hot path. The settings load runs alongside every
      workspace fetch; a column on the workspace row keeps the read
      single-statement.
  - label: settings on the org row instead of the workspace row
    rejected_because: |
      Settings differ per workspace within one org (voice rules per
      brand surface, rubric per editorial style). Org-level settings
      do exist (billing config), and those live on `orgs` instead;
      workspace-level settings live on `workspaces`.
rationale: |
  The JSONB bag absorbs future-spec settings without a migration per
  key, while the per-spec typed accessor pattern keeps the consumer
  side type-safe. The cost is the absence of database-level shape
  enforcement on the bag; the typed accessor in each spec carries
  that enforcement at the application layer.

  The decision is reversible: a key that earns a top-level column
  promotes through a per-key migration. The bag stays for the keys
  that have not promoted.
evidence:
  - kind: spec
    ref: specs/0001-foundation/requirements.md
  - kind: doc
    ref: packages/db/src/schema/workspaces.ts
rollback: |
  Migrate hot-path settings keys onto top-level columns; keep the
  bag for the long tail. The rollback is per-key, not big-bang;
  each migration carries its own DEC.
owner: platform
---

## decision

Per-workspace configuration lives on `workspaces.settings`, a JSONB
column with a `{}` default. Later specs add typed accessors over the
bag instead of promoting each key to a column.

## alternatives

- Typed top-level columns per setting — one migration per spec per
  key.
- Separate settings table — adds a join to every workspace load.
- Settings on the org row — workspace-level settings differ per
  workspace within one org.

## rationale

The JSONB bag absorbs future settings without a migration per key,
while the per-spec typed accessor pattern keeps the consumer side
type-safe. The bag's lack of database-level shape enforcement is
covered by the typed accessor at the application layer.

## evidence

- `specs/0001-foundation/requirements.md` — R-FND-012 acceptance.
- `packages/db/src/schema/workspaces.ts` — `settings` jsonb column
  with `'{}'::jsonb` default; comment names specs 0005, 0010, 0011
  as the owners that add typed accessors.

## rollback

Migrate hot-path settings keys onto top-level columns; keep the
bag for the long tail. The rollback is per-key, not big-bang.
