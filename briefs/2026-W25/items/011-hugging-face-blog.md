# Benchmarking open models on your own tooling

- lane: primary-source
- source: [Hugging Face Blog](https://huggingface.co/blog/is-it-agentic-enough)
- published: 2026-06-18
- confidence: high
- action_surface: eval

**Gist:** HF post on building agentic benchmarks scoped to your own tools rather than relying on public agent leaderboards.

**Mechanism:** Walkthrough for assembling per-org evals: instrument your toolset, sample real tasks, score with rubric or LLM-judge, run open models against the harness.

**Why matters:** Directly relevant to the eval-discipline thread: public agent benchmarks under-predict in-house performance because tools differ.

**Try:** Stand up a 20-task internal eval harness against your live toolset and run two open models through it this week.

**Related thread:** eval discipline shift
