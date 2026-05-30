# Killed experiment: DSPy as a runtime framework adoption

- Source: `dspy` (https://github.com/stanfordnlp/dspy)
- Snapshot: `ops/scout-snapshots/run-scout-f23d443ff059/dspy-github.html`
- Cell ids: MTRX-scout-run-scout-f23d443ff059-dspy-source_arbitrage
- Disposition: reject (framework-as-runtime)
- Kept as: prototype on the GEPA optimizer only (see `action-packets/dspy.md`)

## What was killed

Adopting DSPy as a runtime framework across ai-field-brief lenses or roles. The source_arbitrage cell flags DSPy as already-mainstream (34.7k stars, 109 releases, ICLR'24 paper) and notes that adoption typically stalls at toy examples; production wins concentrate in retrieval and classifier pipelines, not open-ended agent stacks.

## Reason

The user's portfolio memory carries an explicit "reject framework soup" preference. DSPy's compile loop assumes a multi-stage LM pipeline; the current ai-field-brief loop is a sequence of single-prompt lens calls plus a synthesis pass, which is the shape DSPy adopters routinely fail to migrate cleanly. Importing `dspy` as a runtime dep would pull a LiteLLM-shaped provider matrix, an optimizer-state directory, and a telemetry surface the repo does not need.

## What survives

The GEPA optimizer (arxiv 2507.19457) as a build-time prompt-search tool — exported back as a plain string and pinned into the prompt directory. The cell `MTRX-scout-run-scout-f23d443ff059-dspy-action_packet` carries the bounded prototype; this kill is the boundary that prevents the prototype from leaking into a framework adoption.

## Revisit trigger

Revisit if ai-field-brief grows to >=3 LM-call stages in a single role, or if a DSPy-compiled pipeline lands a >=20% lift on one of our own evals in another portfolio repo.
