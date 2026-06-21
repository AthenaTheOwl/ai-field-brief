# MosaicLeaks: can your research agent keep a secret?

- lane: primary-source
- source: [Hugging Face Blog (ServiceNow)](https://huggingface.co/blog/ServiceNow/mosaicleaks)
- published: 2026-06-18
- confidence: high
- action_surface: eval

**Gist:** ServiceNow released MosaicLeaks, an evaluation suite probing whether research agents leak sensitive information across multi-step tool use.

**Mechanism:** Adversarial probe set that injects sensitive payloads into agent context and measures leakage rate through downstream tool calls and summaries.

**Why matters:** Concrete adversarial eval you can plug into any agent CI to catch information-flow regressions, complementing DeepMind's control framework on the offensive side.

**Try:** Run MosaicLeaks against your default research agent config and record the baseline leakage rate before adding any mitigations.

**Related thread:** agent runtime maturation
