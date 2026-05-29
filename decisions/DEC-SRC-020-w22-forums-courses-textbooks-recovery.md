---
id: DEC-SRC-020-w22-forums-courses-textbooks-recovery
spec: specs/0002-source-registry/
requirement: R-SRC-019
date: 2026-05-29
status: approved
reversible: true
decision: |
  Expand the active source registry from 134 to 159 entries by appending
  25 long-tail sources across four subcategories — forums + community
  (6), courses + lectures (7), textbooks + long-form (5), aggregators
  + newsletters (7) — completing the Workflow I Phase 1 leg that failed
  StructuredOutput mid-flight. Each new entry carries a verified
  canonical URL, a per-entry quality triple on the 1-5 scale, an
  intake mode honest to the fetcher's reach (full RSS where verified,
  show-notes-only for Reddit feeds the runner cannot reach), and a
  `last_reviewed: 2026-05-29` stamp. Registry version bumps to 4.
alternatives:
  - label: ship the recovery as a candidate-only entry in candidates.md
    rejected_because: |
      candidates.md is read by humans, not the run workflow. Parking
      25 vetted long-tail sources outside the runner contract means
      the W23 brief sweeps the same 134 entries the W22 vol. 5 brief
      already swept, and the systems-thinking framing the brief
      promises has nothing new to draw from. Promotion to
      `registry.yaml` is the only path that lands on the brief.
  - label: collapse the recovery into a single forums-and-courses bundle
    rejected_because: |
      A single bundle blurs the subcategory split the StructuredOutput
      contract names. Downstream scoring at Pass 3 reads the lane +
      type fields per entry; collapsing the subcategories would force
      a one-off lane and break the four-lane contract DEC-SRC-018
      contracted. Keeping the 4-way split honors the contract and the
      reader's mental model of long-tail vs fast-signal.
  - label: ship 50 sources to overshoot the target
    rejected_because: |
      Registry breadth has diminishing returns past the 150-entry
      mark; the W22 brief swept under 25 sources across 134 entries
      because the matrix scoring gate triages before the runner reads
      the long tail. Doubling the long tail without first measuring
      pass-through rate would inflate the registry without lifting
      brief breadth. The 25-entry recovery matches the Phase 1 deficit
      the failed run logged and stops there.
rationale: |
  Workflow I's Phase 1 expansion shipped 82 new sources in three of
  four parallel categories; the fourth category (forums + community +
  courses + textbooks + aggregators) failed StructuredOutput before
  the registry write landed. The W22 vol. 4 + vol. 5 briefs swept the
  109 sources the three successful categories carried, but the
  long-tail surfaces that anchor the systems-thinking framing —
  textbooks for principle citation, courses for canonical vocabulary,
  forums for early signal, aggregators for breadth coverage — never
  reached the runner. The recovery sweep lands the missing 25 entries
  so the W23 brief sweeps over the full 159-entry registry the W22
  brief was meant to draw from. Each new entry carries the verifiable
  primary-source tie the registry contract demands: Stanford CS229
  (Tengyu Ma + Chris Ré, verified Spring 2026 syllabus), Anthropic
  Cookbook (44.6k stars, Anthropic-authored), Lilian Weng blog
  (ex-OpenAI Head of Safety Systems), Murphy Probabilistic ML
  (canonical reference series), Smol AI News (swyx-adjacent daily
  digest with verified 2026-05-28 issue). Reddit feeds are marked
  `intake: show-notes-only` with a notes line that names the fetcher
  reach quirk; the entry lives in the registry so the W23 sweep sees
  the URL even though the runner cannot fetch it without an alternate
  fetcher.
evidence:
  - kind: doc
    ref: sources/registry.yaml
  - kind: decision
    ref: decisions/DEC-SRC-019-w22-tier-1-ecosystem-sweep.md
  - kind: decision
    ref: decisions/DEC-SRC-018-source-registry-w22-expansion.md
  - kind: run
    ref: scripts/validate_registry.py
  - kind: doc
    ref: specs/0002-source-registry/requirements.md
  - kind: doc
    ref: specs/0002-source-registry/traceability.md
rollback: |
  Revert `sources/registry.yaml` to version 3 (the 134-entry tier-1
  ecosystem registry) and reset `last_curated` to `2026-05-29` if
  earlier. Drop R-SRC-019 from
  `specs/0002-source-registry/requirements.md` and the matching row
  from `traceability.md`. Individual added entries are reversible
  per-id by flipping `status` from `active` to `retired`; the seed
  loader contract is unchanged so no downstream code edits.
owner: product.source-curator
systems_map: |
  Registry as control surface — long-tail sources (forums, courses,
  textbooks) capture practitioner discourse + foundational reference
  material that vendor blogs and podcasts miss; without them the
  brief's systems-thinking framing has no canon to cite.
transferable_principle: |
  Any intelligence registry should include both fast-signal
  (news / podcasts) and slow-signal (textbooks / courses) sources;
  the slow-signal anchors the framework the fast-signal items
  populate, and a registry that ships only fast-signal entries
  cannot support framing claims under audit.
falsification_test: |
  If the 25 new long-tail sources contribute fewer than 2 promoted
  items to the W23 matrix over the four-week rolling window after
  landing, the recovery is noise; retire them and revisit the
  registry-breadth thesis.
adoption_ladder:
  minimum_viable: |
    25 new sources active, queued for the W23 sweep at the same
    quality bar as the 134-entry tier-1 registry.
  mid_adoption: |
    5+ items from long-tail sources land in W23 / W24 matrices;
    Top Signals cite at least one textbook or course entry under
    the Evidence line.
  full_adoption: |
    Long-tail sources contribute to one or more Top Signals per
    brief on average; the transferable-principle field cites a
    textbook or course entry on at least half of Top Signals.
  monitoring_signals:
    - "promoted-items-per-source over four-week rolling window"
    - "Top Signals citing long-tail sources under Evidence"
    - "transferable_principle citations of textbook / course entries"
---

## decision

Expand the active source registry from 134 to 159 entries by appending
25 long-tail sources across four subcategories — forums + community
(6), courses + lectures (7), textbooks + long-form (5), aggregators +
newsletters (7) — completing the Workflow I Phase 1 leg that failed
StructuredOutput mid-flight. Each new entry carries a verified
canonical URL, a per-entry quality triple on the 1-5 scale, an honest
intake mode (full RSS where verified, show-notes-only for Reddit
feeds the runner cannot reach), and a `last_reviewed: 2026-05-29`
stamp. Registry version bumps to 4.

## alternatives

- Ship the recovery as candidate-only entries in `candidates.md`:
  rejected because `candidates.md` is read by humans, not the run
  workflow; parking 25 vetted sources outside the runner contract
  means the W23 brief sweeps the same 134 entries vol. 5 already
  swept, and the systems-thinking framing has nothing new to draw
  from.
- Collapse the recovery into a single forums-and-courses bundle:
  rejected because a single bundle blurs the subcategory split the
  StructuredOutput contract names; downstream scoring at Pass 3
  reads the lane + type fields per entry, so collapsing the
  subcategories would force a one-off lane and break the four-lane
  contract.
- Ship 50 sources to overshoot the target: rejected because
  registry breadth has diminishing returns past 150 entries; the W22
  brief swept under 25 sources across 134 entries because the matrix
  scoring gate triages before the runner reads the long tail.
  Doubling the long tail without first measuring pass-through would
  inflate the registry without lifting brief breadth.

## rationale

Workflow I's Phase 1 expansion shipped 82 new sources in three of
four parallel categories; the fourth category (forums + community +
courses + textbooks + aggregators) failed StructuredOutput before the
registry write landed. The W22 vol. 4 + vol. 5 briefs swept the 109
sources the three successful categories carried, but the long-tail
surfaces that anchor the systems-thinking framing — textbooks for
principle citation, courses for canonical vocabulary, forums for
early signal, aggregators for breadth coverage — never reached the
runner. The recovery sweep lands the missing 25 entries so the W23
brief sweeps over the full 159-entry registry the W22 brief was meant
to draw from. Each new entry carries a verifiable primary-source tie
(Stanford CS229 verified Spring 2026, Anthropic Cookbook 44.6k stars,
Lilian Weng ex-OpenAI Safety, Murphy Probabilistic ML, Smol AI News
verified 2026-05-28). Reddit feeds carry `intake: show-notes-only`
with notes that name the fetcher quirk; the entries live in the
registry so the W23 sweep sees the URL even though the runner cannot
fetch it without an alternate fetcher.

## evidence

- `sources/registry.yaml` (159 entries, `version: 4`,
  `last_curated: 2026-05-29`)
- `DEC-SRC-019-w22-tier-1-ecosystem-sweep` (prior expansion 52 -> 134
  this DEC builds on)
- `DEC-SRC-018-source-registry-w22-expansion` (initial W22 seed)
- `scripts/validate_registry.py` exits 0 against the expanded file
- `specs/0002-source-registry/requirements.md#R-SRC-019` (new
  requirement this DEC resolves)
- `specs/0002-source-registry/traceability.md` (R-SRC-019 row)

## rollback

Revert `sources/registry.yaml` to version 3 (the 134-entry tier-1
ecosystem registry). Drop R-SRC-019 from
`specs/0002-source-registry/requirements.md` and the matching row
from `traceability.md`. Individual added entries are reversible per-id
by flipping `status` from `active` to `retired`; the seed loader
contract is unchanged so no downstream code edits.
