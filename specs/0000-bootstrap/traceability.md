# traceability: bootstrap

| Requirement | Owner role | Design surface | Planned proof |
|---|---|---|---|
| R-BOOT-001 | owner_role: engineering.implementation | root repo layout, scripts, CI | root verify command |
| R-BOOT-002 | owner_role: engineering.implementation | `packages/sources`, canonical schemas | connector fixtures |
| R-BOOT-003 | owner_role: engineering.implementation | `inngest/`, workflow run table | replay/idempotency tests |
| R-BOOT-004 | owner_role: engineering.implementation | `packages/retrieval`, db schema | retrieval/citation eval fixtures |
| R-BOOT-005 | owner_role: science.proof-gate-runner | `packages/evals` | eval report with thresholds |
| R-BOOT-006 | owner_role: engineering.implementation; owner_role_pending_graduation: security.threat-modeler | `packages/db`, auth/audit design | tenant and audit tests |
| R-BOOT-007 | owner_role: engineering.implementation | `packages/integrations` | publish contract tests |

