# Matrix Synthesis

Synthesize only from verified matrix cells.

Produce:
- strongest weekly thesis
- top items
- reusable patterns
- action candidates
- watchlist items
- archive notes

Rules:
- Every claim must link to verified cell IDs.
- Do not cite raw source directly unless a verified cell already supports it.
- Preserve caveats.
- Prefer specific mechanisms over general vibes.
- Do not force action surfaces.

## Pass 4: systems synthesis

Per DEC-MTRX-007 and DEC-CDCP-020, every Top Signal in the digest carries
four systems-thinking fields. Three come from Pass 4 lens cells; the
fourth (`adoption_ladder`) is constructed at synthesis time. The matrix
runner skips Pass 4 lenses on items that do not promote past the Pass 3
scoring gate; Pass 4 runs only on the Top picks the digest will publish.

For each Top Signal, include all four fields:

- **systems_map** — from the `systems_thinking` lens cell. Names the
  underlying system or mechanism the pick exposes, not the local concern.
- **transferable_principle** — from the `transferable_principle` lens
  cell. Names the principle that generalizes beyond the source, with at
  least one concrete example of where else it applies.
- **falsification_test** — from the `falsification_test` lens cell.
  Names the specific observation or experiment that would prove the
  pick's main claim wrong. If the claim is non-falsifiable, the field
  records the prose `non-falsifiable; this is a definitional or
  normative claim`.
- **adoption_ladder** — constructed by the synthesis editor at Pass 4.
  Carries four sub-fields: `minimum_viable`, `mid_adoption`,
  `full_adoption`, `monitoring_signals`. The ladder describes how the
  reader steps into the signal, not what the source says; that is why
  it is a synthesis-time construct rather than a per-source lens.

### Non-negotiable rule

A Top Signal without all four fields populated is not a Top Signal. The
synthesis editor demotes the candidate to Archive notes and records the
demotion reason inline. This rule mirrors the evidence-spine rule in
`AGENTS.md` and the per-pick audit in DEC-PUB-004.

### Field sourcing

- `systems_map`, `transferable_principle`, and `falsification_test` each
  resolve to a verified Pass 4 cell id in the same way the existing
  `mechanism` and `reusable_pattern` fields resolve to Pass 1 / Pass 3
  cell ids. The `Evidence:` line on every Top Signal lists the cell ids
  the four fields draw from.
- `adoption_ladder` does not carry a cell id because it is the editor's
  reading of the verified cells against the reader's adoption surface.
  The ladder still cites the cell ids it builds on under the
  `Evidence:` line.
