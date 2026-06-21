# AI Control Roadmap for internal agent deployments

- lane: primary-source
- source: [Google DeepMind Blog](https://deepmind.google/blog/securing-the-future-of-ai-agents/)
- published: 2026-06-18
- confidence: high
- action_surface: architecture

**Gist:** DeepMind published a defense-in-depth framework that treats internal AI agents as potential insider threats, with capability-scaled detection and response tiers.

**Mechanism:** Adapts MITRE ATT&CK to AI-specific tactics; deploys trusted AI 'supervisors' that monitor agent reasoning and can block actions pre-execution. Defenses are scaled by detection-evasion (D1-D4) and harm-execution (R1-R3) capability levels. Live monitoring grounded in analysis of ~1M coding agent trajectories where most flagged incidents trace to misinterpretation or overeagerness, not adversarial intent.

**Why matters:** Provides a concrete capability-tiered control taxonomy you can borrow for your own agent control plane instead of inventing one. Aligns with the role-contracts + policy-engine pattern.

**Try:** Map your agent fleet to the D1-D4 / R1-R3 grid on one page and identify the highest D x R cell with no supervisor coverage.

**Related thread:** agent runtime maturation
