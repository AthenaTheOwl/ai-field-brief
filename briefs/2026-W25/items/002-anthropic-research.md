# Agentic coding and persistent returns to expertise

- lane: primary-source
- source: [Anthropic Research](https://www.anthropic.com/research/claude-code-expertise)
- published: 2026-06-16
- confidence: high
- action_surface: agent-role

**Gist:** Anthropic analyzed ~400k Claude Code sessions from ~235k users (Oct 2025 to Apr 2026) and found domain expertise, not coding background, predicts how much work Claude does per instruction.

**Mechanism:** Decomposed sessions into planning vs execution decisions. Users contribute ~70% of planning decisions; Claude contributes ~80% of execution decisions. Higher user domain expertise correlates with longer effective Claude turns per instruction.

**Why matters:** Reframes hiring and team composition for agent-using orgs: the bottleneck is people who can specify the right thing, not people who can type code. Maps directly to role-contract design.

**Try:** For one repo, log who triggers each Claude Code session and rate planning specificity 1-5; over a week compare specificity score vs PR merge rate.

**Related thread:** eval discipline shift
