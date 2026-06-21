# Claude Code 2.1.183 blocks destructive git in auto mode

- lane: primary-source
- source: [Anthropic / GitHub (Claude Code changelog)](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- published: 2026-06-19
- confidence: high
- action_surface: tool-policy

**Gist:** Claude Code 2.1.183 in auto mode now blocks destructive git commands unless explicitly requested, and adds model deprecation warnings plus a /config --help shortcut.

**Mechanism:** Auto mode policy gate intercepts git reset --hard, force push, branch -D and similar before execution; user must explicitly authorize. 2.1.181 same week added /config key=value prompt-based settings and a sandbox.allowAppleEvents macOS setting; 2.1.185 (Jun 21) extended stream-stall hint window from 10s to 20s.

**Why matters:** Confirms that auto mode is the default agent surface and that safety is now enforced at the tool-policy layer rather than via prompts. Worth mirroring in your own agent harnesses.

**Try:** In your own agent harness, add a denylist of destructive git verbs that require explicit user confirm; copy the verb list from the 2.1.183 release.

**Related thread:** agent runtime maturation
