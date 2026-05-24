---
id: DEC-SRC-009-github-releases-prefetched-mapper
spec: specs/0002-source-registry/
requirement: R-SRC-009
date: 2026-05-24
status: approved
reversible: true
decision: |
  Accept pre-fetched Octokit-shaped release objects and map each release
  into a `SourceItem`. The connector stores repo, tag, release id, and
  author metadata.
alternatives:
  - label: connector calls GitHub API
    rejected_because: |
      Auth, retry, and rate-limit handling belong to the runner, and
      tests should not need network credentials.
  - label: treat releases as article URLs
    rejected_because: |
      Release id, tag, and repo metadata matter for dedupe and search.
rationale: |
  The pre-fetched input keeps the connector deterministic and lets spec
  0003 own GitHub API behavior.
evidence:
  - kind: doc
    ref: packages/sources/src/connectors/github-releases.ts
  - kind: run
    ref: packages/sources/test/fixtures.test.ts
rollback: |
  Move GitHub API calls into the connector and update fixtures to mock
  the transport layer.
owner: platform
---

## decision

Map pre-fetched GitHub release objects into source items.

## alternatives

- Connector calls GitHub: rejected because runner owns API behavior.
- Treat releases as articles: rejected because release metadata matters.

## rationale

The connector stays deterministic while preserving release metadata.

## evidence

- `packages/sources/src/connectors/github-releases.ts`
- `packages/sources/test/fixtures.test.ts`

## rollback

Move GitHub API calls into the connector and mock transport in tests.
