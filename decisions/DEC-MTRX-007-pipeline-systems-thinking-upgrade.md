---
id: DEC-MTRX-007-pipeline-systems-thinking-upgrade
spec: specs/0012-prompt-matrix-plane/
requirement: R-MTRX-015
date: 2026-05-29
status: approved
reversible: true
amends: DEC-MTRX-006-brief-os-refinement-on-matrix-plane
decision: |
  ai-field-brief gains three new matrix lenses under a Pass 4
  systems-synthesis stage: `systems_thinking` (interpretive),
  `transferable_principle` (synthetic), and `falsification_test`
  (critique). The three lenses run on the Top picks the Pass 3
  scoring gate promotes, not on every source item swept. The
  synthesis editor constructs an `adoption_ladder` per pick at
  synthesis time (four sub-fields: `minimum_viable`,
  `mid_adoption`, `full_adoption`, `monitoring_signals`); the
  ladder is not a per-source lens because adoption is about how
  the reader incorporates the signal, not what the source says.
  Every Top Signal in a published digest MUST carry all four
  fields (`systems_map`, `transferable_principle`,
  `falsification_test`, `adoption_ladder`); a candidate missing any
  of the four demotes to Archive notes. The evidence-spine rules
  in `AGENTS.md` extend to name this requirement; the lens catalog
  at `config/prompt_lenses.yaml`, the synthesis prompt at
  `prompts/matrix_synthesis.md`, and the brief template at
  `templates/weekly-brief.md` all carry the contracted shape.
alternatives:
  - label: keep the three Brief OS passes; let the synthesis editor add systems framing case-by-case
    rejected_because: |
      A case-by-case framing reverts to prose discipline and drops
      the typed-artifact contract. The three Pass 4 lenses turn
      systems framing into a structural field the brief validator
      checks per pick; the adoption ladder turns reader uptake
      into a four-step ladder the digest reader can act on. A
      brief author working ad hoc cannot replay the framing across
      weeks, and downstream artifacts (procurement-lab action
      items, supplier-risk eval reports) lose the join key the
      four fields supply.
  - label: add the four fields to AGENTS.md as a recommendation, not a non-negotiable
    rejected_because: |
      DEC-CDCP-020 contracted the four dimensions at the portfolio
      level for substantive artifacts. A recommendation lands the
      fields on some Top Signals and skips others, which defeats
      the cross-week pattern detection the Reusable patterns
      section reads. The brief is the most-read external artifact
      in the portfolio; the contract earns the framing only if
      every Top Signal carries the four fields without exception.
  - label: make adoption_ladder a per-source lens like the other three
    rejected_because: |
      The ladder describes how the reader steps into the signal,
      not what the source says. A per-source lens would record the
      source's framing of adoption, which over-fits to vendor
      pitch language and loses the editor's read of the reader's
      adoption surface. The synthesis-time construct preserves the
      editor's role as the reader-side translator and stays
      faithful to the source via the cell ids the ladder cites
      under the Evidence line.
  - label: rename Pass 3 to absorb the systems-thinking fields without adding Pass 4
    rejected_because: |
      Pass 3 produces reusable patterns and action candidates; the
      Pass 4 fields produce a system claim, a transferable
      principle, a falsification test, and an adoption ladder.
      Collapsing the two passes into one would conflate action
      extraction with system claim, and the role contract for
      `science.matrix-synthesis-editor` would carry two distinct
      output shapes under one label. A named Pass 4 keeps the role
      contract clean and the cell-id resolution one-to-one.
rationale: |
  Portfolio-wide DEC-CDCP-020 contracted the four dimensions for
  substantive artifacts; the brief is the most-read external
  artifact in the portfolio. Each Top Signal becoming a system
  claim with explicit transferability + falsifiability + adoption
  ladder is the pipeline upgrade that earns the framing. The
  three new lenses sit cleanly inside the existing matrix plane
  (DEC-MTRX-001): they conform to `schemas/prompt_lens.schema.json`,
  they emit cells that pass through `science.cell-verifier` the
  same way Pass 1 cells do, and they cite source refs the same way
  the existing lenses do. The synthesis-time adoption ladder honors
  the editor's read of the reader's adoption surface and avoids
  vendor-pitch framing. The non-negotiable rule mirrors the
  evidence-spine rules in `AGENTS.md` and the per-pick audit in
  DEC-PUB-004; a Top Signal that cannot carry the four fields is a
  candidate the digest reader cannot act on without further
  research, so the demotion to Archive notes is the honest call.
evidence:
  - kind: decision
    ref: decisions/DEC-MTRX-001-prompt-matrix-plane-install.md
  - kind: decision
    ref: decisions/DEC-MTRX-006-brief-os-refinement-on-matrix-plane.md
  - kind: decision
    ref: decisions/DEC-PUB-004-faithfulness-audit-before-publish.md
  - kind: doc
    ref: prompts/lenses/systems_thinking.md
  - kind: doc
    ref: prompts/lenses/transferable_principle.md
  - kind: doc
    ref: prompts/lenses/falsification_test.md
  - kind: doc
    ref: prompts/matrix_synthesis.md
  - kind: doc
    ref: templates/weekly-brief.md
  - kind: doc
    ref: config/prompt_lenses.yaml
  - kind: doc
    ref: AGENTS.md
rollback: |
  Remove the three Pass 4 lens prompts from `prompts/lenses/`
  (`systems_thinking.md`, `transferable_principle.md`,
  `falsification_test.md`). Drop the three lens entries from
  `config/prompt_lenses.yaml`. Revert the Pass 4 section from
  `prompts/matrix_synthesis.md`. Drop the four Top Signal fields
  (Systems map, Transferable principle, Falsification test,
  Adoption ladder) from `templates/weekly-brief.md`. Drop the
  systems-thinking rule + the Pass 4 paragraph from `AGENTS.md`.
  Drop R-MTRX-015..018 from `specs/0012-prompt-matrix-plane/`
  (requirements, acceptance, tasks, traceability). The Brief OS
  refinement layer (DEC-MTRX-006) stays intact; the systems
  upgrade unwinds without touching the Pass 1 / Pass 2 / Pass 3
  loop.
owner: science.proof-gate-runner
systems_map: |
  Brief generation as a control plane — the matrix lenses are the
  typed-input layer, the synthesis is the typed-output layer; adding
  4 dimensions per Top Signal turns the brief from prose into queryable
  claims.
transferable_principle: |
  Any synthesis pipeline producing high-signal output should require
  structural fields per output unit (here: per Top Signal); this
  generalizes to procurement-lab's action items, supplier-risk's eval
  reports, etc.
falsification_test: |
  If readers' adoption rate of Top Signals (measured via action_queue
  follow-through over 90 days) does NOT increase compared to vol. 3,
  the upgrade is falsified.
adoption_ladder:
  minimum_viable: |
    3 new lens prompts + template fields; Pass 5 (re-synthesis)
    lands the format on W22 vol. 5.
  mid_adoption: |
    Validator extension flags Top Signals missing the 4 fields; W23
    brief uses upgraded pipeline natively.
  full_adoption: |
    Every brief vol. carries the 4 fields per Top Signal; readers cite
    the principles in action backlogs.
  monitoring_signals:
    - "% of Top Signals with all 4 fields populated"
    - "action_queue follow-through rate"
    - "transferable_principle citation count in downstream artifacts"
---

## decision

ai-field-brief gains three new matrix lenses under a Pass 4
systems-synthesis stage: `systems_thinking` (interpretive),
`transferable_principle` (synthetic), and `falsification_test`
(critique). The three lenses run on the Top picks the Pass 3 scoring
gate promotes, not on every source item swept. The synthesis editor
constructs an `adoption_ladder` per pick at synthesis time
(`minimum_viable`, `mid_adoption`, `full_adoption`,
`monitoring_signals`); the ladder is not a per-source lens because
adoption is about how the reader incorporates the signal, not what
the source says. Every Top Signal in a published digest MUST carry
all four fields; a candidate missing any of the four demotes to
Archive notes.

## alternatives

- Keep the three Brief OS passes and let the synthesis editor add
  systems framing case-by-case. Rejected because case-by-case framing
  reverts to prose discipline and drops the typed-artifact contract,
  and downstream artifacts lose the join key the four fields supply.
- Add the four fields to `AGENTS.md` as a recommendation. Rejected
  because DEC-CDCP-020 contracted the four dimensions at portfolio
  level; a recommendation lands the fields on some Top Signals and
  skips others, which defeats cross-week pattern detection.
- Make `adoption_ladder` a per-source lens. Rejected because the
  ladder describes how the reader steps into the signal, not what
  the source says; the synthesis-time construct preserves the
  editor's role as the reader-side translator.
- Rename Pass 3 to absorb the systems-thinking fields. Rejected
  because Pass 3 produces reusable patterns and action candidates;
  the Pass 4 fields produce a system claim, a transferable principle,
  a falsification test, and an adoption ladder. A named Pass 4 keeps
  the role contract clean.

## rationale

Portfolio-wide DEC-CDCP-020 contracted the four dimensions for
substantive artifacts. The brief is the most-read external artifact
in the portfolio; each Top Signal becoming a system claim with
explicit transferability + falsifiability + adoption ladder is the
pipeline upgrade that earns the framing. The three new lenses sit
inside the existing matrix plane: they conform to
`schemas/prompt_lens.schema.json`, they emit cells that pass through
`science.cell-verifier`, and they cite source refs the same way the
existing lenses do.

## evidence

- `decisions/DEC-MTRX-001-prompt-matrix-plane-install.md` carries the
  matrix-plane install contract this DEC extends.
- `decisions/DEC-MTRX-006-brief-os-refinement-on-matrix-plane.md` is
  the Brief OS refinement DEC this DEC amends.
- `decisions/DEC-PUB-004-faithfulness-audit-before-publish.md` carries
  the per-pick audit pattern the four-field rule joins.
- `prompts/lenses/systems_thinking.md`,
  `prompts/lenses/transferable_principle.md`, and
  `prompts/lenses/falsification_test.md` carry the three Pass 4 lens
  prompts.
- `prompts/matrix_synthesis.md` carries the Pass 4 synthesis section.
- `templates/weekly-brief.md` carries the four Top Signal fields.
- `config/prompt_lenses.yaml` carries the three lens catalog entries.
- `AGENTS.md` carries the non-negotiable four-field rule.

## rollback

Remove the three Pass 4 lens prompts, drop the three catalog
entries, revert the Pass 4 section from the synthesis prompt, drop
the four Top Signal fields from the template, drop the
systems-thinking rule from `AGENTS.md`, and drop R-MTRX-015..018
from the spec. The Brief OS refinement layer (DEC-MTRX-006) stays
intact; the systems upgrade unwinds without touching the Pass 1 /
Pass 2 / Pass 3 loop.
