# requirements: publishing

### R-PUB-001: public feed routes

The public site publishes RSS, Atom, and JSON Feed routes from the
same build-time brief snapshot used by the archive.

Acceptance:

- `/feed.xml`, `/atom.xml`, and `/feed.json` render without dynamic
  database access.
- Each feed links to the canonical brief URL for every published week.
- Feed dates come from `meta.yaml` when present.

### R-PUB-002: weekly email digest

The public site accepts subscriber emails and can send the latest
brief as a weekly Resend broadcast.

Acceptance:

- `/api/subscribe` adds a valid email to the configured Resend
  segment.
- `/api/cron/weekly-digest?dry_run=1` previews the current digest
  without sending email.
- The scheduled cron path sends only when the cron bearer secret is
  present and valid.
- The digest body links to the canonical brief and includes the
  Resend unsubscribe token.
