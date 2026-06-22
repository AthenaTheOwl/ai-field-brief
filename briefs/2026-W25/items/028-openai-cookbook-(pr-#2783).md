# Simplify grounded-answer flow and fix source_policy guidance

- lane: builder-practice
- source: [OpenAI Cookbook (PR #2783)](https://github.com/openai/openai-cookbook/pull/2783)
- published: 2026-06-15
- confidence: high
- action_surface: tool-policy

**Gist:** Cookbook author rips out a five-step grounded-answer pipeline after discovering Parallel's MCP server silently drops the source_policy.include_domains parameter.

**Mechanism:** Replaces search->inspect->filter->re-generate->validate with a single search-and-cite step; removes domain-constraint prompting and post-hoc citation filtering; adds explicit note that strict domain filtering needs Parallel's direct Search API, not MCP. Notebook now targets gpt-5.4.

**Why matters:** Cautionary tale for MCP integrators: tool servers can accept and ignore parameters silently. Trust verification on each parameter, not the schema, is the lesson.

**Try:** For each MCP tool you depend on, write one eval that asserts a passed parameter changed the output; treat silent ignore as a bug.

**Related thread:** MCP reliability; eval discipline shift
