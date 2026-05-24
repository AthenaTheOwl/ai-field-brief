---
id: DEC-FND-011-audit-events-table-required-on-admin-actions
spec: specs/0001-foundation/
requirement: R-FND-011
date: 2026-05-24
status: approved
reversible: true
decision: |
  Every admin action (settings change, key rotation, member add or
  remove, role change) writes one row to `audit_events`. The single
  write path is `log()` in `packages/db/src/queries/audit.ts`, which
  throws on a missing required field via `AuditScopeError`. The table
  carries actor_user_id, action, target_type, target_id, before / after
  jsonb, ip, ua, plus nullable workspace_id and org_id so org-scoped
  events (billing, org member) share the table with workspace-scoped
  events.
alternatives:
  - label: log to stdout or a separate logging service
    rejected_because: |
      A logging service makes audit queries depend on an external
      vendor's retention + access controls. Storing audit rows in
      Postgres alongside tenant data keeps the audit data under the
      same backup, retention, and compliance regime as the data it
      audits.
  - label: write audit rows directly from each call site
    rejected_because: |
      A direct insert at every admin call site means a future schema
      change touches every call. The `log()` helper centralizes the
      shape so a schema change lands once.
  - label: one audit table per workspace
    rejected_because: |
      Per-workspace tables explode the schema and lose the org-scoped
      events (billing, SSO config) that do not attach to a workspace.
      One table with two nullable scope columns covers both cases.
rationale: |
  A single audit table plus a single write helper makes the audit
  contract enforceable at the type system (`AuditLogInput` interface)
  and the runtime (`AuditScopeError` on missing required fields). The
  table's nullable scope columns let the same row shape cover org-
  scoped and workspace-scoped events. Spec 0013 (security + compliance)
  inherits the table and adds retention rules on top.

  The decision is reversible: switching to a logging service means
  replacing the `log()` helper's insert with an HTTP call and
  draining the existing rows.
evidence:
  - kind: spec
    ref: specs/0001-foundation/requirements.md
  - kind: doc
    ref: packages/db/src/schema/audit.ts
  - kind: doc
    ref: packages/db/src/queries/audit.ts
  - kind: doc
    ref: packages/db/src/test/tenant-scoping.test.ts
rollback: |
  Replace `log()`'s insert with a call to a logging service. Drain
  existing `audit_events` rows. Drop the table after the drain
  completes. The rollback is bounded; the new write path is one
  function change.
owner: platform
---

## decision

Every admin action writes one row to `audit_events` via `log()` in
`packages/db/src/queries/audit.ts`. The helper throws on missing
required fields. The table carries actor_user_id, action,
target_type, target_id, before / after jsonb, ip, ua, plus nullable
workspace_id and org_id.

## alternatives

- Log to stdout or a separate logging service — external vendor
  controls retention and access.
- Direct inserts at each call site — a schema change touches every
  call.
- One audit table per workspace — explodes the schema and loses
  org-scoped events.

## rationale

A single audit table plus a single write helper makes the audit
contract enforceable at the type system (`AuditLogInput`) and the
runtime (`AuditScopeError`). The nullable scope columns let one
row shape cover org-scoped and workspace-scoped events.

## evidence

- `specs/0001-foundation/requirements.md` — R-FND-011 acceptance.
- `packages/db/src/schema/audit.ts` — `audit_events` table with
  nullable workspace_id and org_id, jsonb before / after, ip + ua.
- `packages/db/src/queries/audit.ts` — `log()` helper with
  `AuditScopeError` on missing actorUserId, action, targetType, or
  scope.
- `packages/db/src/test/tenant-scoping.test.ts` — vitest covers
  the missing-args throw paths.

## rollback

Replace `log()`'s insert with a call to a logging service. Drain
existing `audit_events` rows. Drop the table after the drain.
