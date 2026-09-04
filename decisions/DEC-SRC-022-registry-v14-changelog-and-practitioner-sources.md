---
id: DEC-SRC-022-registry-v14-changelog-and-practitioner-sources
spec: specs/0002-source-registry/
requirement: R-SRC-021
date: 2026-09-04
status: approved
reversible: true
decision: |
  Promote eight sources into `sources/registry.yaml` and bump the file to
  version 14, taking the active count from 214 to 222. Three are dated
  vendor changelogs treated as primary sources: `openai-api-changelog`,
  `claude-platform-release-notes`, and `claude-code-changelog`. Two are
  practitioner surfaces the reader asked for: `ai-engineer-talks` and
  `ai-engineer-youtube`. Two are Kaggle surfaces carrying long-form vendor
  practice: `kaggle-whitepapers` and `kaggle-learn-intensives`. One is a
  cross-vendor standard: `agentic-resource-discovery`.
alternatives:
  - label: rely on the existing github-releases and vendor-news entries
    rejected_because: |
      A release feed yields version numbers and a news index yields
      narrative. Neither yields the per-line mechanism a brief can act on.
      The 2026-W35 permission-boundary pick and the 2026-W36 cache-miss
      pick both came from CHANGELOG lines that never appeared in the
      corresponding release feed or announcement post, and the OpenAI news
      index returned 403 on both sweeps while its developer changelog was
      reachable and dated.
  - label: add only the changelogs and leave the practitioner surfaces out
    rejected_because: |
      Conference talks and vendor whitepapers carry framing that primary
      changelogs never do, and the Kaggle SDLC whitepaper's
      verification-rigor spectrum already produced an Action packet in
      2026-W35. Excluding them would keep the registry accurate about what
      shipped and blind to how practitioners describe the work.
  - label: fold ai-engineer-talks and ai-engineer-youtube into the existing ai-engineer-podcast entry
    rejected_because: |
      The three surfaces have different intake shapes and different failure
      modes. The podcast entry already carries a stale channel_id that has
      returned 404 on two consecutive sweeps; merging would hide which
      surface failed. Separate entries let per-source reliability be
      measured, which is the point of the registry.
rationale: |
  Two gaps showed up while authoring the 2026-W35 and 2026-W36 issues.
  First, the highest-yield primary evidence of both weeks came from dated
  changelogs the registry did not carry, and the two entries that could
  have covered them (`gh-anthropic-claude-code`, `openai-news`) either
  yield versions instead of mechanisms or refuse the sweep. Second, the
  reader named AI Engineer and Kaggle as surfaces the brief was missing,
  and both proved out: Kaggle's whitepaper produced an Action packet, and
  AI Engineer's talk archive is the only registry surface carrying
  practitioner transcripts. `agentic-resource-discovery` supersedes the
  single-vendor discovery surface covered in 2026-W26 and needs its own
  entry so the successor can be tracked instead of inferred.
evidence:
  - kind: doc
    ref: sources/registry.yaml
  - kind: doc
    ref: briefs/2026-W35/meta.yaml
  - kind: doc
    ref: briefs/2026-W36/meta.yaml
  - kind: run
    ref: scripts/validate_registry.py
rollback: |
  Remove the eight entries from `sources/registry.yaml` and restore
  `version: 13` with `last_curated: 2026-08-27`. The 2026-W35 and 2026-W36
  Sources reviewed tables would then name sources the registry does not
  carry, so those rows need editing in the same change.
owner: product.source-curator
systems_map: |
  A registry entry is a claim that a surface will be swept. When the
  highest-yield surface is absent, its findings arrive by accident through
  whichever adjacent source happened to mention them, and the sweep's
  reliability history describes the wrong thing.
transferable_principle: |
  Index the surface that carries the mechanism, not the one that carries
  the announcement. Dependency changelogs, migration notes, and commit
  histories beat their own release posts for the same reason.
falsification_test: |
  If the three changelog entries produce no Top signal across four
  consecutive issues while their release-feed siblings do, the split was
  wrong and the changelogs should fold back into the release entries.
adoption_ladder:
  minimum_viable: |
    Eight entries added, registry at version 14, `validate_registry` green.
  mid_adoption: |
    The three changelog sources are swept every week with per-source yield
    recorded in each issue's Sources reviewed table.
  full_adoption: |
    Per-source reliability history distinguishes changelog surfaces from
    release-feed and announcement surfaces, and low-yield entries are
    retired on evidence.
  monitoring_signals:
    - "picks per source per issue, split by changelog and announcement"
    - "consecutive sweep failures per source, currently two for the AI Engineer YouTube feed"
    - "sources retired for zero yield over four issues"
---

## decision

Promote eight sources and bump `sources/registry.yaml` to version 14, from
214 to 222 active. Changelogs as primary sources: `openai-api-changelog`,
`claude-platform-release-notes`, `claude-code-changelog`. Practitioner
surfaces: `ai-engineer-talks`, `ai-engineer-youtube`. Vendor long-form
practice: `kaggle-whitepapers`, `kaggle-learn-intensives`. Cross-vendor
standard: `agentic-resource-discovery`.

## alternatives

- Rely on existing release feeds and news indexes: rejected because they
  yield versions and narrative, and the two picks that mattered most across
  W35 and W36 came from CHANGELOG lines absent from both.
- Add only the changelogs: rejected because the Kaggle whitepaper already
  produced an Action packet and the AI Engineer archive is the only
  transcript-bearing practitioner surface in the registry.
- Fold the AI Engineer surfaces into the existing podcast entry: rejected
  because their intake shapes and failure modes differ, and the podcast
  entry's stale feed URL is exactly the failure that merging would hide.

## rationale

The 2026-W35 permission-boundary pick and the 2026-W36 cache-miss pick both
came from dated CHANGELOG lines that no release feed or announcement
carried, and the OpenAI news index returned 403 on both sweeps while its
developer changelog was reachable. The reader named AI Engineer and Kaggle
as gaps; both produced usable material on the first sweep.

## evidence

- `sources/registry.yaml` (`version: 14`, `last_curated: 2026-09-04`, 222 active)
- `briefs/2026-W35/meta.yaml` and `briefs/2026-W36/meta.yaml` (Sources reviewed and failures)
- `scripts/validate_registry.py` exits 0 against the expanded file
- `specs/0002-source-registry/requirements.md#R-SRC-021`

## rollback

Remove the eight entries, restore `version: 13` and
`last_curated: 2026-08-27`, and edit the Sources reviewed tables in the
2026-W35 and 2026-W36 issues so they name only registry-carried sources.
