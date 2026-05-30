# Action packet: GEPA-optimize one existing prompt-heavy chain

- Source: `dspy` (https://github.com/stanfordnlp/dspy)
- Snapshot: `ops/scout-snapshots/run-scout-f23d443ff059/dspy-github.html`
- Cell ids: MTRX-scout-run-scout-f23d443ff059-dspy-action_packet, MTRX-scout-run-scout-f23d443ff059-dspy-repo_project_scan
- Disposition: prototype
- Effort: small (one focused afternoon for the eval set; one compile run overnight)

## Hypothesis

A DSPy Signature compiled with the GEPA optimizer (Jul'25, arxiv 2507.19457 — "Reflective Prompt Evolution Can Outperform Reinforcement Learning") will beat our current hand-tuned prompt on a measurable eval, without changing the underlying model.

## Test

Pick the single highest-traffic prompt in an active repo (likely a brief-generation or extraction chain), express it as a `dspy.Signature` + `ChainOfThought` module, assemble a 30-example eval set with a deterministic metric (exact-match or rubric score), and run `dspy.GEPA` (or MIPRO if GEPA is still rough) for one compile pass.

## Success metric

>=10% relative lift on the eval metric vs. the current hand-prompt baseline, on the same LM, observed within one week.

## Risk

Lock-in to DSPy abstractions if we don't extract the compiled prompt back out as a plain string artifact. Mitigation: always export the optimized prompt as text and treat DSPy as a build-time tool, not a runtime dependency.

## Kill criterion

Kill if the compiled prompt cannot be exported as a portable string artifact, or if the eval metric lift is below 10% after one compile pass. Demote to reading list if the active repo has fewer than 2 LM-call stages, since DSPy's compile loop assumes a pipeline.
