# Three Ways Codex Can Use a Computer

- lane: builder-practice
- source: [Jason Liu (jxnl.co)](https://jxnl.co/writing/2026/06/16/three-ways-codex-can-use-a-computer/)
- published: 2026-06-16
- confidence: high
- action_surface: agent-role

**Gist:** Liu routes Codex computer-control tasks across three mechanisms (Computer Use, Chrome Extension, In-App Browser) chosen by 'narrowest tool that finishes the job'.

**Mechanism:** Per-task routing rule: native/cross-app workflow -> Computer Use; authenticated multi-tab websites -> Chrome Extension (carries cookies/profile); public pages with visual annotation -> In-App Browser. Routing rules live in AGENTS.md; approval boundary is 'research/draft freely; ask before send/publish/buy/submit'.

**Why matters:** Concrete decision tree for builders wiring agents to desktop work; cuts the 'one agent does everything' anti-pattern and gives an AGENTS.md slot you can copy.

**Try:** Add a 'Routing' section to your repo's AGENTS.md with three lines mapping task type -> mechanism, and one approval rule for irreversible actions.

**Related thread:** agent runtime maturation; AGENTS.md pattern
