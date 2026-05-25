# design: publishing

Publishing reads from the same `.briefs-snapshot` directory as the
public archive. That keeps the static archive, feeds, and email body on
one content source.

The feed routes are static. The subscriber and digest routes are
dynamic because they call Resend and read deployment secrets. The
Resend integration uses the REST API directly:

- `POST /contacts` for subscriber capture.
- `POST /broadcasts` with `send: true` for the weekly digest.

The cron path supports a dry-run query so CI and operators can inspect
the exact subject and preview text without sending mail.
