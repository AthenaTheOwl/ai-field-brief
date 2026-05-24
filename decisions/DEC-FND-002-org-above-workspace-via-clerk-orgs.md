---
id: DEC-FND-002-org-above-workspace-via-clerk-orgs
spec: specs/0001-foundation/
requirement: R-FND-002
date: 2026-05-24
status: approved
reversible: false
decision: |
  Model identity as a two-tier hierarchy: an `orgs` row owns one or more
  `workspaces`, and Clerk's organizations feature carries the external
  identity (clerk_org_id) so SSO + billing scope live one level above the
  workspace. A user joins orgs through `org_members`; workspace-level
  membership lives separately in `workspace_members` so a single user
  can hold different workspace roles across orgs without the schema
  blocking it.
alternatives:
  - label: flat workspaces with no org tier
    rejected_because: |
      Billing, SSO, and enterprise contracts attach to the org, not the
      workspace. A flat model would force per-workspace billing or a
      synthetic org column added later under data migration. Adding the
      org tier at Phase 1 costs one table and one FK; adding it later
      costs a backfill across every tenant row.
  - label: Clerk organizations only, no local mirror
    rejected_because: |
      Joining query paths against an external identifier means every
      tenant query proxies to Clerk. The `orgs` table mirrors the
      Clerk identity so joins stay in Postgres and Clerk stays
      authoritative on auth events.
  - label: org membership inferred from workspace membership
    rejected_because: |
      A user with a viewer role on one workspace should not automatically
      hold org-level rights. Tracking the two memberships separately keeps
      the workspace role scoped to its workspace.
rationale: |
  The two-tier shape matches how enterprise contracts get signed (at
  the org) and how SSO gets configured (per org domain), while keeping
  workspace as the unit of product surface and tenant isolation. The
  cost is one extra table (`orgs`) plus one FK on `workspaces.org_id`;
  the benefit is that spec 0011 (billing) and spec 0013 (security)
  inherit a schema that already knows where to attach.

  The decision is reversible: false because dropping the org tier means
  rewriting `workspaces.org_id` as nullable, migrating every workspace
  row, and adopting a per-workspace billing model.
evidence:
  - kind: spec
    ref: specs/0001-foundation/requirements.md
  - kind: doc
    ref: packages/db/src/schema/identity.ts
  - kind: doc
    ref: packages/db/src/schema/workspaces.ts
rollback: |
  Drop `orgs`, `org_members`, and the `workspaces.org_id` FK. Rewrite
  Clerk middleware to ignore the organization claim. Migrate every
  workspace to a self-owned billing model. The rollback crosses every
  workspace row and every external billing record, which is why this
  DEC carries reversible: false.
owner: platform
---

## decision

Identity is a two-tier hierarchy: an `orgs` row owns one or more
`workspaces`. Clerk organizations feed `orgs.clerk_org_id` so SSO and
billing scope live at the org tier. Membership tracks separately in
`org_members` (org tier) and `workspace_members` (workspace tier).

## alternatives

- Flat workspaces with no org tier — billing and SSO attach to the
  org, not the workspace; later migration is expensive.
- Clerk organizations only with no local mirror — every join would
  proxy to Clerk; the local mirror keeps joins in Postgres.
- Org membership inferred from workspace membership — a workspace
  viewer should not automatically hold org-level rights.

## rationale

The two-tier shape matches how enterprise contracts get signed (at
the org) and how SSO gets configured (per org domain), while keeping
workspace as the unit of product surface and tenant isolation. Spec
0011 billing and spec 0013 security both inherit a schema that knows
where to attach.

## evidence

- `specs/0001-foundation/requirements.md` — R-FND-002 acceptance.
- `packages/db/src/schema/identity.ts` — `orgs`, `org_members`,
  `users.twoFactorEnabled`.
- `packages/db/src/schema/workspaces.ts` — `workspaces.orgId` non-null
  FK to `orgs.id`.

## rollback

Drop `orgs`, `org_members`, and the `workspaces.org_id` FK. Rewrite
Clerk middleware to ignore the organization claim. Migrate every
workspace to a self-owned billing model. The rollback crosses every
workspace row and every external billing record, which is why this
DEC carries `reversible: false`.
