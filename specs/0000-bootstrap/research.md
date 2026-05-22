# research: bootstrap

Research checked 2026-05-22:

- Inngest functions support event, cron, delayed, and workflow patterns with
  retriable steps. Use it for ingestion, transcription, summarization, evals,
  publishing, and replay.
- pgvector stores vectors in Postgres alongside relational data and supports
  exact/approximate nearest-neighbor search. Use Postgres + pgvector as the
  default retrieval base, with full-text search for hybrid retrieval.
- OpenAI Evals provides a pattern for custom evals over LLM systems. Use
  repo-local evals as release gates for prompt/model/source changes.
- GitHub Actions supports concurrency cancellation and required checks. Use
  fast PR checks and scheduled/manual heavier checks.
- Turborepo/pnpm-style monorepo task graphs are a fit once apps/packages
  multiply; declare outputs and avoid leaking secrets into cached logs.
- Expo/EAS mobile releases need separate runtime/channel thinking. The mobile
  app should inherit the proof ladder from the procurement-lab mobile plan.
- LeCun/JEPA process lesson: build a state model and evaluator before action.
- Karpathy/Software 3.0 process lesson: natural language increases generation
  speed; verification and evals become the bottleneck.
- Thinking Machines interaction-model process lesson: separate live interaction
  from asynchronous background reasoning.

