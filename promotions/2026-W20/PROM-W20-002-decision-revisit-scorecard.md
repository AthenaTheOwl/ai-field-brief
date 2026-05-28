---
id: PROM-W20-002
brief: 2026-W20
pick_slug: simon-not-so-locked-in-decision-revisit
target_repo: athena-site
target_artifact_type: portfolio-policy
date: 2026-05-25
status: proposed
landed_commit: null
---

## What

Land the three-axis decision-revisit scorecard (coding-agent fit,
production blast-radius, team capacity, with the "two-of-three green"
threshold) as a portfolio artifact that lives next to the decisions
schema and gets named in the AGENTS.md of any repo running a spike.

## Why this earns a promotion

The scorecard is the artifact the brief's "decision afraid to revisit"
pick asks for. athena-site already owns the decisions schema, so the
scorecard slots in as a sibling. Two repos in the portfolio already
sit on one such decision each (database swap, framework migration);
having the scorecard ready means the spike triggers a written artifact
the CTO can read.

## Where it would land

`athena-site/ops/decision-revisit-scorecard.md` alongside the existing
decisions schema. The schema doc gains a "see also" link.

## How we'd know it worked

The next portfolio repo that runs a "two-week spike" produces a filled
scorecard before the spike starts and again after the spike review.

## Source

Brief pick:
[briefs/2026-W20/brief.md - Not so locked in](../../briefs/2026-W20/brief.md#simon-willison-not-so-locked-in--write-down-the-one-technology-decision-you-are-still-afraid-to-revisit).
