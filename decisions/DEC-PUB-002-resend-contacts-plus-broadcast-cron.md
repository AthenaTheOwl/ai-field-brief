---
id: DEC-PUB-002-resend-contacts-plus-broadcast-cron
spec: specs/0007-publishing/
requirement: R-PUB-002
date: 2026-05-25
status: approved
reversible: true
decision: |
  Email delivery uses Resend contacts for subscriber capture and the
  Resend broadcast API for the weekly brief. The send path is behind
  deployment env vars and cron bearer authorization.
alternatives:
  - label: store subscribers in the application database first
    rejected_because: |
      Subscriber storage would add lifecycle obligations before the
      public site needs custom preference management. Resend already
      owns contact status and unsubscribe handling for broadcasts.
  - label: send one email per contact from the app
    rejected_because: |
      Per-contact sending would make queueing, unsubscribe handling,
      retry behavior, and suppression status the app's job. Broadcasts
      are the right boundary for a weekly digest.
  - label: leave email as a roadmap note
    rejected_because: |
      The public site already invites subscription. A concrete Resend
      path closes that promise while keeping credentials outside the
      repo.
rationale: |
  The digest should reuse the same brief snapshot as the archive and
  feeds. Resend owns contact and broadcast delivery; the app owns the
  digest body, subject, and send authorization. Dry-run support lets a
  human inspect the next broadcast without sending email.
evidence:
  - kind: code
    ref: apps/web/src/lib/email-digest.ts
  - kind: test
    ref: apps/web/src/lib/email-digest.test.ts
  - kind: code
    ref: apps/web/src/app/api/cron/weekly-digest/route.ts
rollback: |
  Remove the subscription form, `/api/subscribe`, the weekly-digest
  route, and the Vercel cron entry. RSS, Atom, and JSON Feed remain.
owner: product
---

## decision

Email delivery uses Resend contacts for subscriber capture and the
Resend broadcast API for the weekly brief. The send path is behind
deployment env vars and cron bearer authorization.

## alternatives

- Store subscribers in the application database first. Rejected because
  Resend already owns contact status and unsubscribe handling.
- Send one email per contact from the app. Rejected because queueing,
  retries, unsubscribe handling, and suppression status belong in the
  email provider for this phase.
- Leave email as a roadmap note. Rejected because the public site now
  has a subscription surface.

## rationale

The digest should reuse the same brief snapshot as the archive and
feeds. Resend owns contact and broadcast delivery; the app owns the
digest body, subject, and send authorization. Dry-run support lets a
human inspect the next broadcast without sending email.

## evidence

- `apps/web/src/lib/email-digest.ts`
- `apps/web/src/lib/email-digest.test.ts`
- `apps/web/src/app/api/cron/weekly-digest/route.ts`

## rollback

Remove the subscription form, `/api/subscribe`, the weekly-digest
route, and the Vercel cron entry. RSS, Atom, and JSON Feed remain.
