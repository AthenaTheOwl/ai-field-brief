# model-not-agent

- **Source:** AlphaSignal (Shangding Gu / UC Berkeley summary)
- **URL:** https://alphasignalai.substack.com/p/the-model-isnt-the-agent-anymore
- **Captured:** 2026-05-28
- **Priority:** medium
- **Cells:** MTRX-W22-model-not-agent-source_gist, MTRX-W22-model-not-agent-claims_and_bets, MTRX-W22-model-not-agent-reusable_pattern, MTRX-W22-model-not-agent-governance_surface, MTRX-W22-magenticlite-fara-source_gist, MTRX-W22-co-scientist-source_gist

## What

UC Berkeley's Shangding Gu, via AlphaSignal, argues long-horizon
agent performance over horizon H decomposes into six factors:
reasoning capability and five system-level factors (memory,
retrieval, planning, tooling, feedback). Once reasoning clears a
threshold, marginal gains from larger models taper and the five
other factors carry the lift. The same week, Microsoft Research
shipped MagenticLite (a stack pairing 14B MagenticBrain with the
Fara1.5 browser-acting model) on exactly this thesis, and
DeepMind's Co-Scientist landed as a role-specialized multi-agent
system with a human strategy lead. Hugging Face published an agent
glossary (harness, scaffold) on the vocabulary side.

## Why it matters

"Pick a better model" is now an incomplete answer to "my agent
underperforms on horizon-H work." The right diagnostic is to
score the six factors and invest in the bottleneck. For buyers,
this means a benchmark on the model alone is no longer sufficient
evidence of production fitness; the benchmark must score the
system. For builders, a 14B planner plus a 1B browser executor
may beat a frontier-model-only stack on cost per completed task.

## Action surface

architecture, agent-role, eval

## Concrete move

Pick one multi-step agent workflow you run today. Run a six-factor
diagnostic: reasoning quality, memory hits and misses, retrieval
precision and recall, planner step-count and revision rate,
tool-policy false-permits and false-denies, feedback-loop
latency. The factor that bottlenecks horizon H is the one to
invest in next. Commit a no-model-swap rule for one sprint and
verify whether the system-side fix delivers the lift.

## Caveats

The six-factor framing is conceptual not empirical in the
AlphaSignal excerpt; without the full factor list and empirical
attribution from Gu's paper, treat as a research direction more
than a deployable recipe. Multi-agent systems compound error
propagation — Co-Scientist's role-specialization gains are not
free, and may cost more than the single-agent baseline if roles
are not strictly enforced.
