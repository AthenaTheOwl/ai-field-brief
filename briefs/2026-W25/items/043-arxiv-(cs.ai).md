# WeaveBench: 114 computer-use tasks that require GUI and CLI together

- lane: frontier-scout
- source: [arXiv (cs.AI)](https://arxiv.org/abs/2606.09426)
- published: 2026-06-08
- confidence: high
- action_surface: eval

**Gist:** Microsoft Research authors released WeaveBench, a 114-task benchmark where success requires interleaving GUI control with CLI/code in the same task; GUI-only and CLI-only baselines get <3.5%, hybrid agents reach 35.1%.

**Mechanism:** Channel non-substitutability is baked into task specs; trajectory-aware judges audit the full action sequence to catch fabricated screenshots or hard-coded metric shortcuts.

**Why matters:** Most computer-use benchmarks let agents cheese tasks through one interface. WeaveBench is the first to force cross-channel cooperation and grade trajectories — a sharper test for any agent claiming 'computer use'.

**Try:** Run your current computer-use agent against three WeaveBench tasks and record which channel it defaults to; check whether your harness even exposes both.

**Related thread:** eval discipline shift
