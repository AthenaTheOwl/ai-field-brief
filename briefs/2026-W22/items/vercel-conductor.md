# vercel-conductor

- **Source:** Vercel Blog (Conductor case study)
- **URL:** https://vercel.com/blog/how-conductor-moved-parallel-coding-agents-from-the-laptop-to-the-cloud-with-vercel-sandbox
- **Captured:** 2026-05-28
- **Priority:** medium-high
- **Cells:** MTRX-W22-vercel-conductor-source_gist, MTRX-W22-vercel-conductor-mechanism_extraction, MTRX-W22-vercel-conductor-reusable_pattern, MTRX-W22-vercel-conductor-governance_surface, MTRX-W22-conductor-cloud-agents-source_gist, MTRX-W22-vercel-sandbox-persistence-source_gist

## What

Conductor moved its parallel-coding-agent execution layer off
developer laptops onto Vercel Sandboxes. The orchestrator is
model-agnostic across Claude Code, Codex, and other agent SDKs,
and the operator characterizes the UX as feeling "just like the
local version" because Sandbox cold-start is fast enough to
preserve the local feel. In the same window Vercel made Sandbox
filesystem persistence GA and on-by-default, and Mistral shipped
Vibe + Medium 3.5 with cloud-side coding agents on the same
architectural shape.

## Why it matters

The default place to run a coding agent in H2 2026 is no longer
your laptop. The platform decision is now: which sandbox provider
(Vercel, E2B, Daytona, Modal), with which persistence semantics,
behind which gateway allowlist, with which audit log.
Persistence-on-by-default is the trap — PII and secrets now linger
across sessions unless you write a retention policy. Model-
agnosticism is the hedge — interfacing across multiple agent SDKs
keeps the agent vendor a config decision, not a structural lock-in.

## Action surface

architecture, runtime-adapter, tool-policy

## Concrete move

Pick one workflow that currently runs parallel coding agents on
laptops. Prototype it on a hosted sandbox provider; bench
cold-start against the laptop baseline. Write the data-retention
policy *before* turning persistence on: which directories persist,
for how long, encrypted by what key, surfaced to which audit log.
Decide which projects opt out of persistence. Pin recurring-prompt
budgets (Cursor's `/loop`, equivalents) at a per-user / per-team
cap with the same 70% alert as the consumption budget item.

## Caveats

Conductor's "feels just like local" is a UX claim, not a measured
number. The openai-agents-python v0.17.3 release notes flagged
Vercel Sandbox terminal-state issues, suggesting the runtime is
still maturing. Cost scales with parallel agents — 10x agents is
10x billed compute. Data-residency, egress, and audit constraints
on the hosted sandbox are inherited and must be verified before
broad adoption.
