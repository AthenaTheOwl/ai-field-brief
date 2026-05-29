# claude-code-2-1-154

- **Source:** anthropics/claude-code releases
- **URL:** https://github.com/anthropics/claude-code/releases/tag/v2.1.154
- **Captured:** 2026-05-28
- **Priority:** high
- **Cells:** MTRX-W22-claude-code-2-1-154-source_gist, MTRX-W22-claude-code-2-1-154-mechanism_extraction, MTRX-W22-claude-code-2-1-154-adoption_action, MTRX-W22-claude-code-2-1-154-risk_and_caveats, MTRX-W22-claude-code-2-1-154-governance_surface, MTRX-W22-claude-code-2-1-156-source_gist

## What

Claude Code v2.1.154 set Opus 4.8 as the default model, exposed an
`/effort xhigh` knob for the hardest tasks, made the lean system
prompt the default for new models, introduced "dynamic workflows"
that orchestrate tens to hundreds of background agents via
`/workflows`, and made streaming tool execution available
everywhere including Bedrock, Vertex, and Foundry. Fast mode on
Opus 4.8 is 2x cost for 2.5x speed. Two days later v2.1.156
hotfixed an Opus 4.8 thinking-block regression that was causing
API errors.

## Why it matters

Dynamic workflows move the orchestration boundary inside the
model. The model now plans, branches, and dispatches sub-agents at
runtime; the operator's `/workflows` view is the surface that
makes the run tree visible. The trade is operator certainty for
agent-side adaptability — and a meaningfully higher per-run cost
ceiling when xhigh-effort pairs with multi-agent dispatch.
Combined with the same week's Cursor Auto-review (a three-tier
policy ladder on the IDE side) and Vercel's BYOK-enforced provider
allowlist on the gateway side, the message is consistent: the
agent platform is the policy ladder, the cost cap, and the audit
log — not the model.

## Action surface

agent-role, config, tool-policy, software-control-plane

## Concrete move

Before turning on dynamic workflows in a shared install, add four
guardrails. The first two are the budget perimeter; the second two
are the audit surface.

```yaml
per_workflow_budget_cap_usd: 50
per_workflow_max_subagents: 10
allowed_subagent_skills:
  - code-review
  - test-runner
  - doc-extractor
  # deny by default; add per business need
audit_log_retention_days: 90
require_human_review_when:
  - workflow_writes_to_branch: main
  - workflow_calls_tool: prod_database_write
  - workflow_cost_exceeds_usd: 25
```

Pin Claude Code at v2.1.156 or later before standardizing on the
new flag set — the .154 thinking-block regression was real and
.156 fixed it.

## Caveats

Treat v2.1.154 as still settling. The cadence (eight versions in
eight days) is itself the carrier signal — the surface is moving
faster than the documentation. A team scripting against new flags
should wait one cycle. Lean-system-prompt-default and effort-knob-
default change response behavior; A/B comparisons against the
prior baseline are unreliable until evals are re-baselined.
