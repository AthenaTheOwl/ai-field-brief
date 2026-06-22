# SciAgentArena: 200 stepwise-verified scientific tasks for agent-agnostic eval

- lane: frontier-scout
- source: [arXiv (cs.AI)](https://arxiv.org/abs/2606.12736)
- published: 2026-06-10
- confidence: high
- action_surface: eval

**Gist:** A 30+ author group (Zou, Zitnik, Cohan, Ying, Ding, Jin, etc.) released SciAgentArena, ~200 real scientific tasks with stepwise verification and an agent-agnostic interactive environment.

**Mechanism:** Stepwise verification per task instead of only final-answer grading; agent-agnostic env so any harness can plug in; results show agents do well on specified data-analysis flows but fail at open-ended research requiring novel insight.

**Why matters:** Stepwise-verification + agent-agnostic env is the eval shape the rest of the field will copy. Worth using as a template if your control plane needs to compare role implementations head-to-head.

**Try:** Adopt SciAgentArena's stepwise-verification shape for one of your own internal evals — split a single task into 3-5 checkpoint assertions instead of one final score.

**Related thread:** eval discipline shift
