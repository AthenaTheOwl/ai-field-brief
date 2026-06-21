# PowerAgentBench-Dyn: agents on power-system dynamic studies

- lane: frontier-scout
- source: [arXiv (cs.AI)](https://arxiv.org/abs/2606.20401)
- published: 2026-06-18
- confidence: high
- action_surface: eval

**Gist:** Benchmark for evaluating agents on two power-engineering tasks (dynamic-model quality review, dynamic security risk screening) with simulator-based observation/action spaces and deterministic seeds for reproducibility.

**Mechanism:** Tasks defined as simulation envs with explicit obs/action specs; metrics combine success rate with cost-of-simulation budgets; agents must rank short-circuit contingencies under bounded budget.

**Why matters:** Example of a vertical agent benchmark with engineering-style cost budgets baked in, not just task completion. Pattern is reusable wherever you need to grade agents under bounded tool spend.

**Try:** Borrow the simulation-budget metric: add a 'max tool calls' constraint to one of your existing agent evals and re-score.
