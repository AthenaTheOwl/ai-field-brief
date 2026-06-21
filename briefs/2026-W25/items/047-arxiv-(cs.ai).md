# AutoResearch: LLM offline research agent for spacecraft control with credibility gates

- lane: frontier-scout
- source: [arXiv (cs.AI)](https://arxiv.org/abs/2606.20394)
- published: 2026-06-18
- confidence: high
- action_surface: agent-role

**Gist:** Jain and Linares (MIT) present AutoResearch, where an LLM iteratively edits and tests control-policy scripts offline; no result is credited unless it passes three audit checks.

**Mechanism:** Audit layer requires (1) seed-noise threshold measurement, (2) reseeded verification of top configs, (3) leave-one-out pruning of agent edits; otherwise the reported improvement is discarded.

**Why matters:** Direct template for a 'verification-gated research agent' role contract: the LLM proposes, but the harness only accepts results that survive structured ablations. Maps cleanly to typed-artifact discipline.

**Try:** Add a 'no result credited until reseeded' gate to any auto-tuning agent you run; log how many of its self-reported wins disappear.

**Related thread:** eval discipline shift
