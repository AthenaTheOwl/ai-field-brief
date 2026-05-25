# traceability: publishing

| Requirement | Owner role | Decision | Design surface | Planned proof |
|---|---|---|---|---|
| R-PUB-001 | owner_role: product.spec-writer | [DEC-PUB-001-public-feeds-from-build-snapshot](../../decisions/DEC-PUB-001-public-feeds-from-build-snapshot.md) | `apps/web/src/lib/feeds.ts`, feed route handlers | `pnpm --filter @aifieldbrief/web test` confirms feed shape |
| R-PUB-002 | owner_role: product.subscriber-experience | [DEC-PUB-002-resend-contacts-plus-broadcast-cron](../../decisions/DEC-PUB-002-resend-contacts-plus-broadcast-cron.md) | `apps/web/src/lib/email-digest.ts`, `/api/subscribe`, `/api/cron/weekly-digest` | unit tests cover digest body, contact request, broadcast request, and cron auth |
| R-PUB-003 | owner_role: product.subscriber-experience | [DEC-PUB-003-credential-safe-subscriber-ops-page](../../decisions/DEC-PUB-003-credential-safe-subscriber-ops-page.md) | `apps/web/src/lib/subscriber-ops.ts`, `/ops/subscriber` | unit tests cover readiness without exposing env values |
