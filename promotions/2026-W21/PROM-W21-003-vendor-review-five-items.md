---
id: PROM-W21-003
brief: 2026-W21
pick_slug: project-glasswing-vendor-review-five-items
target_repo: supplier-risk-rag-agent
target_artifact_type: portfolio-policy
date: 2026-05-25
status: proposed
landed_commit: null
---

## What

Land the five-item AI vendor review (SOC2 Type II report date + audit
firm, DPA terms, model-isolation guarantee, audit-log retention +
export, API-key compromise SLA under 1 minute) as a procurement intake
artifact in supplier-risk-rag-agent.

## Why this earns a promotion

supplier-risk-rag-agent is the portfolio repo whose buyers ask exactly
these questions. The brief gives the YAML shape; landing it as a
procurement intake file means the next vendor review covers all five
without anyone re-deriving them. The "industry-standard" answer-refusal
discipline is part of the artifact, not just commentary.

## Where it would land

`supplier-risk-rag-agent/policies/vendor-review-ai.yaml`, with a
sibling
`supplier-risk-rag-agent/decisions/DEC-OPS-NNN-ai-vendor-review-five-items.md`
that captures why these five and not others.

## How we'd know it worked

The next AI vendor review in supplier-risk-rag-agent fills the YAML
end-to-end, and any sub-1-minute SLA gap is a tracked procurement red
flag.

## Source

Brief pick:
[briefs/2026-W21/brief.md - Project Glasswing](../../briefs/2026-W21/brief.md#project-glasswing--add-five-items-to-your-ai-vendor-review).
