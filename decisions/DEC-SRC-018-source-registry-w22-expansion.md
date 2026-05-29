---
id: DEC-SRC-018-source-registry-w22-expansion
spec: specs/0002-source-registry/
requirement: R-SRC-015
date: 2026-05-29
status: approved
reversible: true
decision: |
  Expand the active source registry from 15 to 52 entries to enable a
  broader W22 tier-1 sweep. The expansion adds primary-source vendor
  blogs (DeepMind, Google Research, Meta AI, Microsoft AI, AWS ML,
  NVIDIA, Mistral, Cohere, Hugging Face), fast-signal podcasts and
  newsletters (Latent Space podcast, AI Daily Brief, Last Week in AI,
  No Priors, ThursdAI, Import AI, Stratechery, ACX, Hard Fork),
  builder-practice practitioners and shows (Lilian Weng, Chip Huyen,
  Karpathy, Practical AI, MLOps Community, TWIML, AI Engineer),
  research feeds (arXiv cs.AI, cs.CL, cs.LG, cs.CR, Hugging Face
  Daily Papers), aggregators (HN front page, r/MachineLearning,
  r/LocalLLaMA), and GitHub release feeds (claude-code, openai-agents
  -python, langgraph, openai-cookbook commits).
alternatives:
  - label: keep the 15-source seed and add candidates incrementally
    rejected_because: |
      The inaugural W22 brief swept under 10 sources because the
      registry was too narrow. Operator review of the candidate pool
      already identified the 37 entries this DEC promotes; staging
      them one at a time would delay the next brief without changing
      the eventual scope.
  - label: promote every candidate in `sources/candidates.md`
    rejected_because: |
      The full candidate pool includes lower-credibility aggregators
      and single-author Substacks that have not cleared the tier-1
      bar. The expansion limits to entries with a verifiable tie to
      a primary surface, a recognized practitioner, or a track record
      inside both labs.
rationale: |
  The inaugural 2026-W22 brief swept under 10 sources because the
  active registry held 15 entries and the runner skipped feeds with
  stub connectors. The expansion targets the next cut of tier-1
  surfaces: vendor blogs that anchor primary-source verification,
  practitioner blogs that drive applied LLM patterns, podcasts that
  break news inside the builder community, arXiv categories that hold
  the underlying papers, and a small aggregator lane for noise-floor
  awareness. Each entry carries a `quality` triple, an `intake`
  policy (podcasts and aggregators ride show-notes-only intake to
  protect against false-precision transcript citations), and a
  `last_reviewed` stamp so the static ops queue surfaces review
  drift.
evidence:
  - kind: doc
    ref: sources/registry.yaml
  - kind: code
    ref: packages/sources/src/ops.ts
  - kind: run
    ref: scripts/validate_registry.py
rollback: |
  Revert `sources/registry.yaml` to version 1 (the 15-entry seed) and
  reset `last_curated` to 2026-05-22. The added entries are
  individually reversible by flipping `status` from `active` to
  `retired`, so partial rollback is supported per source id.
owner: product
---

## decision

Expand the active source registry from 15 to 52 entries to enable a
broader W22 tier-1 sweep across vendor blogs, practitioner blogs,
podcasts, research feeds, aggregators, and GitHub release feeds.

## alternatives

- Keep the 15-source seed and promote candidates one at a time:
  rejected because the inaugural W22 brief already showed the
  registry was too narrow; one-at-a-time staging would delay the
  next brief without changing the final scope.
- Promote every entry in `sources/candidates.md`: rejected because
  the candidate pool includes entries that have not cleared the
  tier-1 bar (single-author Substacks without an Anthropic / OpenAI
  tie, low-signal aggregators).

## rationale

The inaugural 2026-W22 brief covered under 10 sources because the
registry held 15 entries and the runner skipped feeds with stub
connectors. The expansion targets primary-source vendor blogs for
verification, practitioner blogs for applied patterns, podcasts that
break news inside the builder community, arXiv categories for
research depth, and a small aggregator lane for noise-floor
awareness. Podcasts and aggregators use `show-notes-only` intake to
avoid false-precision transcript citations.

## evidence

- `sources/registry.yaml` (52 entries, version bumped to 2,
  `last_curated: 2026-05-29`)
- `packages/sources/src/ops.ts` (registry type mapping)
- `scripts/validate_registry.py` exits 0 against the expanded file

## rollback

Revert `sources/registry.yaml` to version 1 (the 15-entry seed) and
reset `last_curated` to `2026-05-22`. Individual entries can be
retired by flipping `status` from `active` to `retired` without a
full revert.
