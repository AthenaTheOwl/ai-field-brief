# Eve: open-source TypeScript agent framework where every agent is a directory

- lane: frontier-scout
- source: [Vercel](https://vercel.com/changelog/introducing-eve-an-open-source-agent-framework)
- published: 2026-06-17
- confidence: high
- action_surface: agent-role

**Gist:** Vercel released Eve at Ship 26 London, an Apache-2.0 TypeScript framework that compiles a directory of files (instructions.md, tools/, skills/, connections/, channels/, schedules/, subagents/) into a durable agent service on Vercel Functions.

**Mechanism:** Filesystem-as-contract: build-time discovery wires tools/skills by file path; instructions.md is prepended to every model call; durable execution via Vercel Workflow; sandboxed compute via Vercel Sandbox; OpenTelemetry traces emitted by default; no decorator-based registration.

**Why matters:** Mirrors the AGENTS.md / skills directory pattern but compiles to a runnable production target on a hosted platform, lowering the gap between 'agent as a repo' and 'agent as a deployed service'. Useful comparison point for CDCP role-contract directory layout.

**Try:** Clone github.com/vercel/eve, scaffold one agent with a single tool and a skills/onboarding.md, then diff its compiled manifest against an equivalent CDCP role contract to see what registration boilerplate disappears.

**Related thread:** agent runtime maturation / directory-as-agent convergence
