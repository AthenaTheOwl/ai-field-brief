---
id: DEC-PUB-003-credential-safe-subscriber-ops-page
spec: specs/0007-publishing/
requirement: R-PUB-003
date: 2026-05-25
status: approved
reversible: true
decision: |
  Subscriber operations use a server-rendered readiness page that
  reports booleans, latest digest metadata, and operator links without
  printing credential values.
alternatives:
  - label: authenticated subscriber admin
    rejected_because: |
      Authentication and provider dashboards are more surface than the
      public digest needs. The immediate gap is deployment readiness,
      not contact management.
  - label: rely on Vercel environment settings only
    rejected_because: |
      Vercel can show whether keys exist, but it does not connect those
      keys to the digest preview, cron endpoint, and reader-facing feeds.
  - label: expose a JSON-only readiness route
    rejected_because: |
      A page is easier to inspect during deploy checks and still keeps
      the underlying model unit-testable.
rationale: |
  The digest path already has subscriber capture, dry-run, cron, and
  feed endpoints. A credential-safe page lets the operator confirm
  whether the weekly send is blocked before Friday while keeping secret
  values out of HTML, logs, and tests.
evidence:
  - kind: code
    ref: apps/web/src/lib/subscriber-ops.ts
  - kind: code
    ref: apps/web/src/app/ops/subscriber/page.tsx
  - kind: test
    ref: apps/web/src/lib/subscriber-ops.test.ts
rollback: |
  Remove `/ops/subscriber`, the subscriber-ops readiness model, and the
  homepage link. The subscription form, feeds, and cron route continue
  to work.
owner: product
---

## decision

Subscriber operations use a server-rendered readiness page that reports
booleans, latest digest metadata, and operator links without printing
credential values.

## alternatives

- Authenticated subscriber admin. Rejected because authentication and
  provider dashboards are more surface than the public digest needs.
- Vercel environment settings only. Rejected because environment
  settings do not connect the keys to the digest preview, cron endpoint,
  and reader-facing feeds.
- JSON-only readiness route. Rejected because a page is easier to
  inspect during deploy checks and the model remains unit-testable.

## rationale

The digest path already has subscriber capture, dry-run, cron, and feed
endpoints. A credential-safe page lets the operator confirm whether the
weekly send is blocked before Friday while keeping secret values out of
HTML, logs, and tests.

## evidence

- `apps/web/src/lib/subscriber-ops.ts`
- `apps/web/src/app/ops/subscriber/page.tsx`
- `apps/web/src/lib/subscriber-ops.test.ts`

## rollback

Remove `/ops/subscriber`, the subscriber-ops readiness model, and the
homepage link. The subscription form, feeds, and cron route continue to
work.
