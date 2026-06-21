# Artifacts support in Claude Code

- lane: primary-source
- source: [Anthropic / Claude.com](https://claude.com/blog/artifacts-in-claude-code)
- published: 2026-06-18
- confidence: high
- action_surface: workflow

**Gist:** Claude Code sessions can now publish live, versioned web pages (PR walkthroughs, dashboards, incident pages) that auto-refresh for viewers.

**Mechanism:** Artifact is built from full session context (codebase + tools + history). Each publish creates a new version at the same URL with history; private by default with org-level sharing toggles and role-based scoping. Beta on Team and Enterprise plans, CLI and desktop app.

**Why matters:** Replaces ad-hoc status update loops for agent runs. A Claude Code run can ship its own deliverable surface, which changes how TPMs consume agent output.

**Try:** Run one incident or PR review session in Claude Code with an artifact and share the URL instead of a Slack writeup; measure time saved.

**Related thread:** agent runtime maturation
