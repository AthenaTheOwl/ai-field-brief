# Agents' Last Exam: 1000+ economically-valuable tasks across 13 industry clusters

- lane: frontier-scout
- source: [arXiv (cs.AI)](https://arxiv.org/abs/2606.05405)
- published: 2026-06-03
- confidence: high
- action_surface: eval

**Gist:** 300+ authors released ALE, a living benchmark of 1000+ verifiable, long-horizon professional tasks across 13 industry clusters aligned to US federal occupational taxonomy; hardest tier has avg full pass rate under 1%.

**Mechanism:** Tasks sourced from 250+ domain experts, each scored by objective professional standards rather than synthetic rubrics; task pool grows continuously; explicit framing as GDP-relevant rather than capability-isolated.

**Why matters:** First eval at this scale tied to actual occupational categories rather than synthetic puzzles; useful counterweight to the swelling 'agent benchmark of the week' churn the eval lane keeps catching.

**Try:** Pick one ALE sub-field that overlaps your domain, run your current agent on three tasks, and log where it fails at the workflow level vs the capability level.

**Related thread:** eval discipline shift
