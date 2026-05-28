---
id: PROM-W21-002
brief: 2026-W21
pick_slug: kpmg-pwc-gates-ai-incident-playbook
target_repo: athena-site
target_artifact_type: portfolio-policy
date: 2026-05-25
status: proposed
landed_commit: null
---

## What

File the three-section AI incident playbook (model-output, data
exposure, vendor outage) the brief drafted, each section carrying
detect / contain / communicate sub-steps. Land it as a portfolio
runbook that every product repo links from its AGENTS.md.

## Why this earns a promotion

KPMG (276,000 seats), PwC, and Gates landed in five days. Every product
repo that ships AI features inherits the same incident classes; one
copy of the runbook in athena-site beats three drift-prone copies.
Customer-success teams break here first; the playbook is one page and
gets written this week or it gets written under fire.

## Where it would land

`athena-site/ops/ai-incident-playbook.md` carries the three sections.
Each product repo's AGENTS.md gains a one-line link.

## How we'd know it worked

The next AI incident across the portfolio (any of the three classes) is
routed by the runbook, and the post-mortem links back to which section
governed.

## Source

Brief pick:
[briefs/2026-W21/brief.md - KPMG, PwC, Gates in five days](../../briefs/2026-W21/brief.md#kpmg-pwc-gates-in-five-days--build-the-ai-incident-playbook-before-someone-asks-for-it).
