---
id: DEC-SRC-019-w22-tier-1-ecosystem-sweep
spec: specs/0002-source-registry/
requirement: R-SRC-018
date: 2026-05-29
status: approved
reversible: true
decision: |
  Expand the active source registry from 52 to 134 entries by appending
  82 vetted tier-1 sources spanning vendor and research-lab blogs,
  practitioner blogs, podcasts, YouTube channels and playlists, course
  pages, textbook pages, forums, aggregators, and newsletters; also
  apply URL recoveries to 8 prior W22 failures so each lands on a
  verified working endpoint.
alternatives:
  - label: keep the 52-source W22 seed and add candidates incrementally
    rejected_because: |
      The 52-entry W22 seed still produced a brief that swept under 25
      sources because too many lanes (forums, courses, textbooks, video)
      were under-represented or absent. One-at-a-time staging would
      delay tier-1 ecosystem coverage by weeks without changing the
      shape of the final registry.
  - label: append every Phase 1 proposal without dedupe
    rejected_because: |
      The 133-entry Phase 1 proposal list contained 33 collisions with
      existing entries (same id) plus 18 phase-internal duplicates
      (different ids, same surface). Naive append would have produced
      duplicate registry rows, broken the seed loader's unique-id
      assumption, and tripped the validator's duplicate-id rule.
  - label: replace the registry instead of appending
    rejected_because: |
      The existing 52 entries carry stable IDs that downstream code,
      run records, and prior DECs already reference. Replacement would
      have orphaned those references and required a wider migration
      pass than the expansion warrants.
rationale: |
  The W22 brief established that registry breadth caps brief breadth:
  the inaugural sweep crossed under 10 sources, the expanded W22 sweep
  crossed 24. User direction is to land tier-1 ecosystem coverage in
  one pass and let the runner pick its own subset. The 82 appended
  entries each carry a verifiable tie to a primary surface (lab blog,
  vendor research outlet, recognized practitioner blog, canonical
  course or textbook) and a per-entry quality triple so downstream
  scoring has the signal it needs to triage. Eight URL recoveries
  flip stale endpoints to working RSS or html-scrape surfaces so the
  runner stops failing on entries the registry already endorses.
  The append-with-dedupe path was chosen over replacement because
  every existing id is already referenced by downstream code, run
  records, and prior DEC traceability.
evidence:
  - kind: doc
    ref: sources/registry.yaml
  - kind: decision
    ref: DEC-SRC-018-source-registry-w22-expansion
  - kind: run
    ref: scripts/validate_registry.py
  - kind: doc
    ref: specs/0002-source-registry/requirements.md
rollback: |
  Revert `sources/registry.yaml` to version 2 (the 52-entry W22 seed)
  and reset `last_curated` to `2026-05-22`. Individual added entries
  are reversible per-id by flipping `status` from `active` to
  `retired`; URL recoveries are reversible by reverting the `url` and
  `last_reviewed` keys on the eight affected entries.
owner: product.source-curator
---

## decision

Expand the active source registry from 52 to 134 entries by appending
82 vetted tier-1 sources spanning vendor blogs, research-lab blogs,
practitioner blogs, podcasts, YouTube channels and playlists, course
pages, textbook pages, forums, aggregators, and newsletters; apply
URL recoveries to 8 prior W22 failures.

## alternatives

- Keep the 52-source W22 seed and promote candidates incrementally:
  rejected because the W22 brief still missed tier-1 lanes (forums,
  courses, textbooks, video) that the user named as in-scope; staging
  one at a time would delay coverage without changing the shape of
  the final registry.
- Append every Phase 1 proposal without dedupe: rejected because the
  proposal list carried 33 id collisions with existing entries plus
  18 phase-internal duplicates; naive append would have broken the
  unique-id rule the validator enforces.
- Replace the registry instead of appending: rejected because the
  existing 52 entries carry stable IDs that downstream code, run
  records, and prior DECs already reference.

## rationale

Registry breadth caps brief breadth. The inaugural W22 brief swept
under 10 sources; the expanded W22 swept 24. The user directed a one-
pass tier-1 ecosystem expansion that covers the long-tail surfaces
(forums, courses, textbooks, video). The 82 appended entries each
carry a verifiable tie to a primary surface (lab blog, vendor research
outlet, recognized practitioner blog, canonical course or textbook)
and a per-entry quality triple so downstream scoring has the signal
it needs. The eight URL recoveries flip stale endpoints to working
RSS or html-scrape surfaces so the runner stops failing on entries
the registry already endorses.

## evidence

- `sources/registry.yaml` (134 entries, `version: 3`,
  `last_curated: 2026-05-29`)
- `DEC-SRC-018-source-registry-w22-expansion` (prior expansion that
  established the 52-entry seed this DEC builds on)
- `scripts/validate_registry.py` exits 0 against the expanded file
- `specs/0002-source-registry/requirements.md#R-SRC-018` (new
  requirement this DEC resolves)

## rollback

Revert `sources/registry.yaml` to version 2 (the 52-entry W22 seed)
and reset `last_curated` to `2026-05-22`. Individual added entries
are reversible per-id by flipping `status` from `active` to
`retired`; URL recoveries are reversible by reverting the `url` and
`last_reviewed` keys on the eight affected entries.
