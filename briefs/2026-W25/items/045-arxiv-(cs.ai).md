# Every Eval Ever: unified JSON schema and HF-hosted community eval repository

- lane: frontier-scout
- source: [arXiv (cs.AI)](https://arxiv.org/abs/2606.14516)
- published: 2026-06-12
- confidence: high
- action_surface: eval

**Gist:** 47-author proposal for a single JSON schema for AI evaluation results; the seed repo on Hugging Face already holds 22,235 models, 2,273 unique benchmarks, and 31 evaluation formats with auto-converters from existing harnesses.

**Mechanism:** Two-level schema (community-governed metadata + instance-level for fine-grained outputs); auto-converters ingest popular harnesses/leaderboards into a single JSON shape.

**Why matters:** If this catches on, it's the eval lane's typed-artifact moment — exactly the artifact-discipline angle the user's control-plane stance favors. Worth watching whether harnesses adopt the converters.

**Try:** Export one of your existing eval runs into the EveryEvalEver JSON schema and push it to the HF community repo to test the round-trip.

**Related thread:** eval discipline shift
