# traceability: source registry + ingestion

| Requirement | Design surface | Decision | Planned proof |
|---|---|---|---|
| R-SRC-001 owner_role: engineering.implementation | `packages/db/src/schema/sources.ts` (`sources` table + index) | `DEC-SRC-001-source-registry-table-per-workspace` | drizzle typecheck on schema |
| R-SRC-002 owner_role: engineering.implementation | `packages/db/src/queries/sources.ts` (`listSources`, `getSource`, `createSource`, `updateSource`, `retireSource`) | `DEC-SRC-002-tenant-scoped-source-crud-helpers` | `packages/db/src/test/sources.test.ts` |
| R-SRC-003 owner_role: engineering.implementation | `packages/sources/src/contract.ts` (`Connector`, `FetchCtx`, `ConnectorInput`) | `DEC-SRC-003-connector-contract-pure-inputs` | typecheck + fixtures test |
| R-SRC-004 owner_role: engineering.implementation | `packages/sources/src/registry.ts` (`registerConnector`, `getConnector`) | `DEC-SRC-004-in-memory-connector-registry` | `packages/sources/test/registry.test.ts` |
| R-SRC-005 owner_role: engineering.implementation | `packages/sources/src/connectors/stubs.ts` (`NotImplementedError`) | `DEC-SRC-005-stub-connectors-fail-loudly` | registry test asserts each stub throws |
| R-SRC-006 owner_role: engineering.implementation | `packages/sources/src/connectors/rss.ts` | `DEC-SRC-006-rss-connector-pure-parser` | `packages/sources/test/fixtures.test.ts` (rss case) |
| R-SRC-007 owner_role: engineering.implementation | `packages/sources/src/connectors/podcast-rss.ts` | `DEC-SRC-007-podcast-rss-itunes-enclosure-parser` | fixtures test (podcast case) |
| R-SRC-008 owner_role: engineering.implementation | `packages/sources/src/connectors/article-url.ts` | `DEC-SRC-008-article-url-heuristic-extractor` | fixtures test (article case) |
| R-SRC-009 owner_role: engineering.implementation | `packages/sources/src/connectors/github-releases.ts` | `DEC-SRC-009-github-releases-prefetched-mapper` | fixtures test (github case) |
| R-SRC-010 owner_role: engineering.implementation | `packages/sources/src/canonicalize.ts` | `DEC-SRC-010-canonical-url-dedupe-key` | `packages/sources/test/canonicalize.test.ts` |
| R-SRC-011 owner_role: engineering.implementation | `packages/sources/src/hash.ts` | `DEC-SRC-011-content-hash-dedupe-key` | `packages/sources/test/hash.test.ts` |
| R-SRC-012 owner_role: engineering.implementation | `provenance` writes in every full connector + `VERSION` const | `DEC-SRC-012-connector-provenance-version-stamp` | fixtures test asserts `provenance.fetcher` |
| R-SRC-013 owner_role: science.proof-gate-runner | `packages/sources/src/types.ts` (`SOURCE_TYPES` const tuple) | `DEC-SRC-013-source-type-union-schema-sync-test` | `packages/sources/test/types.test.ts` cross-checks JSON Schema |
| R-SRC-014 owner_role: engineering.implementation | `packages/db/src/schema/sources.ts` (`source_reliability_history` table) | `DEC-SRC-014-reliability-history-table-now-writes-later` | drizzle typecheck; write path lands in spec 0003 |
| R-SRC-015 owner_role: engineering.implementation | `packages/db/src/seeds/sources-from-registry.ts` (`loadSeedSources`) | `DEC-SRC-015-seed-loader-reads-registry-yaml` | `packages/db/src/test/seeds.test.ts` |
| R-SRC-016 owner_role: science.proof-gate-runner | `packages/db/src/seeds/sources-from-registry.ts` (`REGISTRY_TYPE_TO_SOURCE_TYPE`) | `DEC-SRC-016-registry-type-map-to-source-type` | seeds test asserts mapping is total over `sources/registry.yaml` |
| R-SRC-017 owner_role: product.subscriber-experience | `packages/sources/src/ops.ts`; `apps/web/src/app/ops/sources/page.tsx` | `DEC-SRC-017-static-registry-connector-readiness` | `packages/sources/test/ops.test.ts`; web typecheck/build |
| R-SRC-018 owner_role: product.source-curator | `sources/registry.yaml` (134 entries across 4 lanes) | `DEC-SRC-019-w22-tier-1-ecosystem-sweep` | `scripts/validate_registry.py` exits 0 |
| R-SRC-019 owner_role: product.source-curator | `sources/registry.yaml` (159 entries; +25 long-tail sources) | `DEC-SRC-020-w22-forums-courses-textbooks-recovery` | `scripts/validate_registry.py` exits 0 |
