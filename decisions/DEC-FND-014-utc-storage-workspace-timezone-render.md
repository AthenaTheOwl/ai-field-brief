---
id: DEC-FND-014-utc-storage-workspace-timezone-render
spec: specs/0001-foundation/
requirement: R-FND-014
date: 2026-05-24
status: approved
reversible: true
decision: |
  Every `*_at` column in the schema uses `timestamp({ withTimezone:
  true })`; storage is UTC. The display layer reads
  `workspaces.timezone` (a text column with default `'UTC'`) and
  renders timestamps in the workspace's chosen zone. A docstring on
  the `timezone` column names the rule so a future schema reader
  does not re-litigate.
alternatives:
  - label: store in workspace timezone
    rejected_because: |
      Per-workspace storage means a cross-tenant query has to
      normalize on read, and a workspace timezone change requires a
      data migration. UTC storage keeps every row on the same scale;
      timezone is a display concern.
  - label: timestamp without time zone
    rejected_because: |
      `timestamp without time zone` is timezone-ambiguous: the column
      carries no metadata about which zone the value belongs to. Two
      writes from two zones land as different absolute instants under
      the same column value. With-timezone is the only column type
      that survives a multi-region workforce.
  - label: render in user-browser timezone
    rejected_because: |
      Browser timezone is a per-user choice that may not match the
      workspace's editorial calendar. A workspace publishing weekly
      briefs on Fridays in PT should render every timestamp in PT
      regardless of which contributor's browser opens the page.
rationale: |
  UTC storage plus per-workspace display timezone separates the two
  concerns cleanly: every row is comparable on the wire, every
  display layer reads one source of truth for the zone. The pattern
  scales to a multi-region workforce, supports cross-workspace
  reporting at the org tier, and matches how every other timestamp-
  heavy product in the portfolio handles the same trade-off.

  The decision is reversible: the timezone column can become a
  per-user setting; the with-timezone columns can stay either way.
evidence:
  - kind: spec
    ref: specs/0001-foundation/requirements.md
  - kind: doc
    ref: packages/db/src/schema/identity.ts
  - kind: doc
    ref: packages/db/src/schema/workspaces.ts
  - kind: doc
    ref: packages/db/src/schema/audit.ts
rollback: |
  Switch the display layer to read user timezone from the Clerk
  user profile instead of workspace timezone. Drop the
  `workspaces.timezone` column. Schema timestamp columns stay
  with-timezone either way.
owner: platform
---

## decision

Every `*_at` column uses `timestamp({ withTimezone: true })`;
storage is UTC. The display layer reads `workspaces.timezone` (text
column, default `'UTC'`) and renders timestamps in the workspace's
zone.

## alternatives

- Store in workspace timezone — cross-tenant queries would normalize
  on read; timezone change forces a migration.
- `timestamp without time zone` — column carries no zone metadata;
  multi-region writes land as different absolute instants.
- Render in user-browser timezone — browser zone may not match the
  workspace's editorial calendar.

## rationale

UTC storage plus per-workspace display timezone separates the two
concerns: every row is comparable on the wire, every display layer
reads one source of truth for the zone. The pattern scales to a
multi-region workforce and supports cross-workspace reporting at
the org tier.

## evidence

- `specs/0001-foundation/requirements.md` — R-FND-014 acceptance.
- `packages/db/src/schema/identity.ts` — `users.lastSeenAt`,
  `users.createdAt`, `orgs.createdAt`, `orgMembers.joinedAt` all
  `timestamp({ withTimezone: true })`.
- `packages/db/src/schema/workspaces.ts` — `workspaces.timezone`
  text column with `'UTC'` default and the docstring naming the
  rule; every `*_at` column with-timezone.
- `packages/db/src/schema/audit.ts` — `auditEvents.createdAt`
  with-timezone.

## rollback

Switch the display layer to read user timezone from Clerk instead
of workspace timezone. Drop the `workspaces.timezone` column.
Schema timestamp columns stay with-timezone either way.
