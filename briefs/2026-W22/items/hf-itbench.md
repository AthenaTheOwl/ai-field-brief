# hf-itbench

- **Source:** Hugging Face Blog (Artificial Analysis + IBM Research)
- **URL:** https://huggingface.co/blog/ibm-research/itbench-aa
- **Captured:** 2026-05-27
- **Priority:** high
- **Cells:** MTRX-W22-itbench-source_gist, MTRX-W22-itbench-claims_and_bets, MTRX-W22-itbench-adoption_action, MTRX-W22-itbench-governance_surface

## What

ITBench-AA, from Artificial Analysis and IBM, is the first public
benchmark for agentic enterprise IT tasks. Frontier models score
below 50%.

## Why it matters

The gap between consumer-facing demos and IT-specific workflow
tasks is wide. The benchmark gives buyers a number to anchor pilot
success criteria when a vendor pitches AI replacement for an
internal IT workflow. A 50% headline is a realistic floor; a
generic "AI can do this" pitch sets a ceiling that fails on contact
with production.

## Action surface

eval, source-registry

## Concrete move

Add ITBench-AA to the vendor review template under an "agentic-IT
eval coverage" row. Cite the result when scoping pilots so the
buyer agrees to a realistic floor. Any vendor pitching enterprise-
IT agent replacement should publish a result on a public benchmark
or admit they have none.

## Caveats

A single new benchmark functions as a Q2 2026 anchor; it is not a
permanent calibration. Methodology is recent and the result
distribution will shift as model versions update.
