# Agent fan-out, loop engineering, Cloudflare for long-running agents

- lane: fast-signal
- source: [AI News by Smol AI](https://news.smol.ai/issues/26-06-19-not-much)
- published: 2026-06-19
- confidence: high
- action_surface: runtime-adapter

**Gist:** Documented 'agent fan-out' pattern (5-100 parallel child agents), Hermes Agent v0.17.0 with session compression, Cloudflare Workers temporary accounts removing OAuth deployment friction, Durable Objects fix for long-running agents with active WebSocket connections.

**Mechanism:** Cloudflare Durable Objects now hold long-lived WebSocket sessions across worker restarts; Hermes adds session compression and agent distribution; fan-out becomes named pattern with reliability semantics instead of ad-hoc parallelism.

**Why matters:** If you've been hand-rolling agent runtime plumbing, the components for fan-out + durable session + zero-touch deploy now exist as commodity infra.

**Try:** Port one current sequential agent loop to a 10-way fan-out on Durable Objects and measure end-to-end latency + cost vs the sequential baseline.

**Related thread:** agent runtime maturation
