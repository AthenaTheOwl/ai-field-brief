# alignment-msm

- **Source:** Anthropic Alignment Science Blog
- **URL:** https://alignment.anthropic.com/2026/msm/
- **Captured:** 2026-05-21
- **Priority:** high
- **Cells:** MTRX-W22-msm-source_gist, MTRX-W22-msm-mechanism_extraction, MTRX-W22-msm-reusable_pattern

## What

Model Spec Midtraining (MSM) inserts a new stage between pre-
training and alignment fine-tuning where the model trains on
synthetic documents discussing its own model spec. The reported
result: Qwen2.5-32B agentic-misalignment drops from 68% to 5%;
Qwen3-32B from 54% to 7%. Alignment fine-tuning becomes 40x more
token-efficient on Qwen2.5-32B.

## Why it matters

The mechanism is teaching the *why* before the *how*. Two models
trained on the same demonstration data but different specs
generalize to different held-out behaviors, showing the spec
shapes value acquisition independent of demonstrations. At the
application layer the analog is AGENTS.md / CLAUDE.md as the spec
the agent reads before it acts.

## Action surface

prompt, agent-role

## Concrete move

If your AGENTS.md only states *what* the agent should do, add a
*why* paragraph for each rule. If your eval set only scores
outputs, add a scoring slot for stated reasoning quality. The
generalization signal MSM identifies is one you can capture at
prompt-engineering scale without retraining anything.

## Caveats

The training-time results are not directly transferable to prompt-
time. The MSM gains require a midtraining pass; the analog at the
application layer is rhetorical and slower-acting. Treat the paper
as motivation for the rhetorical shift, not a numeric promise.
