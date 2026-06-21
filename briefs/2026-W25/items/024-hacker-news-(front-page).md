# Running local models is good now (Vicki Boykis)

- lane: fast-signal
- source: [Hacker News (front page)](https://vickiboykis.com/2026/06/15/running-local-models-is-good-now/)
- published: 2026-06-15
- confidence: high
- action_surface: runtime-adapter

**Gist:** Practitioner writeup: 2022 M2 Mac + 64GB RAM running Gemma-4-12b-qat + Pi agent harness + LM Studio reaches ~75% of frontier accuracy/speed on real Python work.

**Mechanism:** Specific stack: Gemma-4-12b-qat as model, Pi as agent harness, LM Studio as inference server, Docker containers with restricted permissions for agentic loops, JSON-configured local endpoints.

**Why matters:** First mainstream practitioner post that treats local agentic coding as default-on for a non-trivial workload, not a demo; sets the bar HN now expects from any 'local AI' post.

**Try:** Install LM Studio + Gemma-4-12b-qat on a dev laptop and route one real refactor task through it via Pi; record the actual quality delta vs your cloud default.

**Related thread:** local agent maturation
