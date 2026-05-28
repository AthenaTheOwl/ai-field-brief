---
id: PROM-W20-001
brief: 2026-W20
pick_slug: claude-for-small-business-buyer-persona-check
target_repo: ai-supply-chain-copilot-prd
target_artifact_type: portfolio-policy
date: 2026-05-25
status: proposed
landed_commit: null
---

## What

Land the `buyer-persona-check.md` template (target buyer shape, the
sentence the buyer would say to a peer, the 90-day behavior change, the
explicit "not for" list, unit-economics fit) as a pre-ship gate for
every AI feature in the copilot PRD.

## Why this earns a promotion

The copilot PRD is the portfolio's product-shape document; the brief's
buyer-persona pattern lifts directly. The "not for" lines are the part
most teams flinch on; the template forces the answer before the product
page goes live. One filled template per AI feature is the lightest
version of the discipline.

## Where it would land

`ai-supply-chain-copilot-prd/templates/buyer-persona-check.md`, with a
PRD reference saying every shipped AI feature carries one in the
review folder.

## How we'd know it worked

Next AI feature added to the copilot PRD ships with a filled-in
template, and the product page reads to one buyer shape, not three.

## Source

Brief pick:
[briefs/2026-W20/brief.md - Claude for Small Business](../../briefs/2026-W20/brief.md#claude-for-small-business--pick-the-buyer-persona-your-ai-feature-sells-to-today).
