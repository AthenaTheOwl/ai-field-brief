# claude-code-2-1-154

- **Source:** anthropics/claude-code releases
- **URL:** https://github.com/anthropics/claude-code/releases/tag/v2.1.154
- **Captured:** 2026-05-28
- **Priority:** high
- **Cells:** MTRX-W22-cc154-source_gist, MTRX-W22-cc154-mechanism_extraction, MTRX-W22-cc154-adoption_action, MTRX-W22-cc154-risk_and_caveats

## What

Claude Code v2.1.154 ships Opus 4.8 as default, `/effort xhigh` as
default for complex tasks, lean system prompt default for new
models, dynamic workflows that orchestrate tens to hundreds of
agents in the background via `/workflows`, and streaming tool
execution everywhere (including Bedrock, Vertex, Foundry).

## Why it matters

Dynamic workflows shift the orchestration boundary inside the
model. The model now plans, branches, and dispatches sub-agents at
runtime; the operator's `/workflows` view is the surface that makes
this visible. The trade is operator certainty for agent-side
adaptability — and a meaningfully higher per-run cost ceiling when
xhigh effort is paired with multi-agent dispatch.

## Action surface

agent-role, config, tool-policy

## Concrete move

Before you turn on dynamic workflows in a shared org install: add a
per-workflow budget cap and an explicit allowlist of which sub-
agents can be dispatched. Pin v2.1.156 or later (the .154 release
had an Opus 4.8 thinking-block bug that .156 fixed two days later).

## Caveats

Treat v2.1.154 as still settling. The pace of releases in the .14x
through .15x range (eight in eight days) is the carrier signal —
the surface is moving faster than the documentation. A team
scripting against new flags should wait one cycle.
