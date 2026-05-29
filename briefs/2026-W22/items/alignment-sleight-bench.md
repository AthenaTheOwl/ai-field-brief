# alignment-sleight-bench

- **Source:** Anthropic Alignment Science Blog
- **URL:** https://alignment.anthropic.com/2026/sleight-bench/
- **Captured:** 2026-05-26
- **Priority:** high
- **Cells:** MTRX-W22-sleight-source_gist, MTRX-W22-sleight-mechanism_extraction, MTRX-W22-sleight-adoption_action, MTRX-W22-sleight-risk_and_caveats, MTRX-W22-sleight-governance_surface

## What

SLEIGHT-Bench is a hand-crafted benchmark of 40 attacks across 11
categories that stress LLM-based monitors. At a 1% false-positive
rate, Claude Opus 4.6 reliably catches 8 of 40; 50% of attacks are
never caught. Per-blind-spot catch rates range from 0% (N-hops,
omission, jailbreaks embedded in transcripts) to 90% (plausible
naming).

## Why it matters

The "monitored agent" claim is now the most common safety frame in
agent product marketing. SLEIGHT-Bench gives buyers a number to
hold against the claim. Most current LLM-only monitors will fail at
multi-session stitching, omission, and authorization confusion. The
Claude-Code-as-monitor variant (letting the monitor execute code to
verify claims) measurably improves detection.

## Action surface

eval, tool-policy, agent-role

## Concrete move

Name the three or four blind spots most relevant to your agent
workload (multi-session stitching, omission, and authorization
confusion are common defaults) and add targeted probes to your
monitor eval set. Prototype the agentic-monitor pattern as a one-
week experiment before committing to it as production.

## Caveats

The benchmark is 40 hand-crafted attacks; it is illustrative, not a
quantitative ceiling. Ensemble monitoring (multiple specialized
prompts) costs roughly 10x invocations and 14x tokens, putting it
out of reach for high-volume workflows. LLM monitors should be
paired with execution-environment isolation, not used as sole gate.
