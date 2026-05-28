---
id: PROM-W21-004
brief: 2026-W21
pick_slug: gemini-flash-35-rerun-unit-economics
target_repo: athena-site
target_artifact_type: portfolio-policy
date: 2026-05-25
status: proposed
landed_commit: null
---

## What

Land the LLM unit-economics rerun template (input cost, output cost,
quarter cost at current volume, quarter cost at +30% volume across
candidate models) as a portfolio cost-tracking artifact in athena-site.
Cadence: rerun on every cheap-tier model price change.

## Why this earns a promotion

Flash 3.5 GA priced up the cheap tier and embedded as the default in
Workspace. Three portfolio repos route LLM traffic; without a shared
template, each one re-derives the rerun. athena-site is the right home
for the template; each product repo fills its own copy when its cost
line changes.

## Where it would land

`athena-site/ops/llm-unit-economics-template.md` carries the table
shape and the three downstream decisions it surfaces. Each product
repo's finance or cost-tracking doc links to it.

## How we'd know it worked

The next cheap-tier model price change in any cloud triggers a same-day
rerun in the affected portfolio repos with the template applied
verbatim.

## Source

Brief pick:
[briefs/2026-W21/brief.md - Gemini 3.5 Flash GA](../../briefs/2026-W21/brief.md#gemini-35-flash-ga-across-workspace--rerun-your-unit-economics-this-week).
