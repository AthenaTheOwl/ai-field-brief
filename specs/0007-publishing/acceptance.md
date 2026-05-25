# acceptance: publishing

Run:

```sh
pnpm --filter @aifieldbrief/web test
pnpm turbo run typecheck
pnpm --filter @aifieldbrief/web build
python scripts/spec_check.py
python scripts/voice_lint.py
```

Manual checks:

- Visit `/feed.xml`, `/atom.xml`, and `/feed.json`.
- Submit a test email on a deployment with Resend env vars set.
- Call `/api/cron/weekly-digest?dry_run=1` and confirm the latest
  brief appears in the response.
