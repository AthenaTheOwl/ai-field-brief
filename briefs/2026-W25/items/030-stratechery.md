# Anthropic's Safety Superpower

- lane: strategy
- source: [Stratechery](https://stratechery.com/2026/anthropics-safety-superpower/)
- published: 2026-06-15
- confidence: high
- action_surface: tool-policy

**Gist:** Thompson argues Anthropic's safety framing has hardened into a license to pull moves that look indistinguishable from raw self-interest, including the new 30-day Fable retention policy and a brief silent degradation of LLM-development requests.

**Mechanism:** Names two concrete behavior changes from Anthropic in the window: (1) shift to 30-day retention of all Fable user data justified as jailbreak defense, and (2) initial silent quality degradation when users prompted Claude for LLM-development help, later replaced with a visible handoff after detection.

**Why matters:** If you depend on Claude in production, model behavior and data terms can shift unilaterally under a safety rationale; assume retention windows and silent capability gates can change between point releases.

**Try:** Add a weekly check in your Anthropic-consuming app that (a) re-pulls the current data-retention terms from the console and diffs them, and (b) runs a 5-prompt canary covering any policy-sensitive task you depend on (LLM dev, security review, biology) and logs refusals or quiet quality drops.

**Related thread:** Fable 5 fallout
