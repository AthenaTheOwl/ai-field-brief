---
id: DEC-FND-003-four-role-workspace-membership
spec: specs/0001-foundation/
requirement: R-FND-003
date: 2026-05-24
status: approved
reversible: true
decision: |
  Workspace membership carries a four-role enum (`owner`, `admin`,
  `editor`, `viewer`) on a composite primary key `(workspace_id,
  user_id)`. Pending invites land in a separate `workspace_invites`
  table with a unique opaque token; the only path that writes a non-
  owner into `workspace_members` is invite acceptance.
alternatives:
  - label: three roles (owner / member / viewer)
    rejected_because: |
      Editorial work (write brief drafts, run sources) and admin work
      (rotate keys, add members) are different scopes. Collapsing them
      into one `member` role forces a permission split later via
      settings; promoting the split into the role enum at Phase 1
      keeps the policy layer simple.
  - label: many-to-many roles via a separate role_grants table
    rejected_because: |
      One-role-per-member-per-workspace covers the planned product
      surface. A grants table is one indirection more than the
      product needs at Phase 1; promote later if a role mix appears.
  - label: token-free invites by email send only
    rejected_because: |
      A token-shaped invite gives the accept endpoint a single
      lookup key and lets a workspace member resend or revoke the
      invite without a second flow. Email-only invites force the
      accept handler to match by email at acceptance time, which
      breaks when the invitee signs up with a different address.
rationale: |
  The four-role enum maps to the product's known scopes: owner pays,
  admin governs, editor writes, viewer reads. The composite PK keeps
  one row per (workspace, user) and lets the schema reject a duplicate
  add at the database. The separate invites table gives the accept
  flow an idempotent token, a known expiry, and an `accepted_at`
  trace for the audit log.

  The decision is reversible: the role enum can expand or contract via
  a single migration; the invites table can collapse into a settings
  jsonb field if the flow gets simpler.
evidence:
  - kind: spec
    ref: specs/0001-foundation/requirements.md
  - kind: doc
    ref: packages/db/src/schema/workspaces.ts
  - kind: doc
    ref: packages/db/src/queries/workspaces.ts
rollback: |
  Drop the `workspaceRole` enum and adopt a three-role model. Migrate
  every `workspace_members` row to map admin onto member. The rollback
  is bounded to one enum migration plus one data update. The invites
  table can stay as-is or fold into a settings field.
owner: platform
---

## decision

Workspace membership carries a four-role enum: `owner`, `admin`,
`editor`, `viewer`. Composite PK `(workspace_id, user_id)`. Pending
invites live in `workspace_invites` with a unique token; invite
acceptance is the only write path for non-owner members.

## alternatives

- Three roles (`owner / member / viewer`) — editorial and admin
  scopes do not fit one `member` role; the split lands cheaper at
  Phase 1.
- Many-to-many roles via `role_grants` — one indirection more than
  the product needs at Phase 1.
- Token-free invites — the accept handler would match by email at
  acceptance, which breaks when the invitee uses a different address.

## rationale

The four roles map to the product's known scopes: owner pays, admin
governs, editor writes, viewer reads. The composite PK rejects
duplicate adds at the database. The invites table gives the accept
flow an idempotent token, a known expiry, and an `accepted_at` trace
for the audit log.

## evidence

- `specs/0001-foundation/requirements.md` — R-FND-003 acceptance.
- `packages/db/src/schema/workspaces.ts` — `workspaceRole` enum,
  `workspace_members` composite PK, `workspace_invites` with unique
  token.
- `packages/db/src/queries/workspaces.ts` — `createInvite` and
  `acceptInvite` carry the only write path into `workspace_members`
  for non-owners.

## rollback

Drop the `workspaceRole` enum and adopt a three-role model; migrate
every `workspace_members` row to map admin onto member. The rollback
is bounded to one enum migration plus one data update.
