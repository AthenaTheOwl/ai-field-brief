---
id: PROM-W22-003
brief: 2026-W22
pick_slug: anthropic-widens-the-conversation-outside-readers
target_repo: ai-field-brief
target_artifact_type: agents-md
date: 2026-05-25
status: proposed
landed_commit: null
---

## What

Add two outside-reader sections to `.agents/AGENTS.md` in this repo:
finance constraints (sourced from a finance partner) and legal /
compliance constraints (sourced from legal). Include the
`ethics_check(action)` self-callable tool pattern as a note.

## Why this earns a promotion

The brief argues the two outside readers most missing from a typical
engineer-written AGENTS.md are finance and legal. ai-field-brief is the
first repo whose AGENTS.md should reflect the pattern the brief named
publicly. Filing it here closes the gap between "we recommended it" and
"we did it." The two sections are short and concrete; the work is the
two 30-minute conversations.

## Where it would land

`ai-field-brief/.agents/AGENTS.md` gains two new sections under a
"Outside readers" heading. The brief pick's template lifts directly.

## How we'd know it worked

The next coding-agent run on this repo can name the unattended-run cost
cap and the legal channel-tagging rule without being told.

## Source

Brief pick:
[briefs/2026-W22/brief.md - Anthropic widens the conversation](../../briefs/2026-W22/brief.md#anthropic-widens-the-conversation--pick-the-two-outside-readers-your-agentsmd-is-missing).
