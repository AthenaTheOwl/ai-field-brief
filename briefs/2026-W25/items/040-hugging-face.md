# hf CLI redesigned to detect and adapt output for coding agents

- lane: frontier-scout
- source: [Hugging Face](https://huggingface.co/blog/hf-cli-for-agents)
- published: 2026-06-04
- confidence: high
- action_surface: runtime-adapter

**Gist:** Hugging Face shipped a redesign of the hf CLI that detects agent environments (CLAUDECODE, CODEX_SANDBOX, etc.) and switches output to TSV/JSON with full untruncated values and suggested next commands.

**Mechanism:** Single command, two renderings — humans get ANSI tables and prose; agents get clean TSV/JSON, no truncation, no interactive prompts, explicit '--yes to skip' hints; reports 1.3x-6x token efficiency vs hand-rolled REST or SDK calls.

**Why matters:** Concrete pattern for the runtime-adapter lane: instead of building a wrapper agent tool, instrument the underlying CLI to detect non-human callers. Cheap to replicate in any CLI you ship.

**Try:** Pick one CLI in your stack, add CLAUDECODE detection, and emit --json by default when set; measure token cost of the same multi-step task before and after.

**Related thread:** agent runtime maturation
