---
id: PROM-W22-001
brief: 2026-W22
pick_slug: glasswing-10000-bug-queue-overflow
target_repo: athena-site
target_artifact_type: portfolio-policy
date: 2026-05-25
status: proposed
landed_commit: null
---

## What

Land a "queue overflow" policy that every portfolio repo with an
agent-fed work queue applies: name the agent output rate, name the
human absorption rate, set a 1.5x ratio trigger for one of three
mitigations (severity gate, triage-bot first pass, slow-mode flag).

## Why this earns a promotion

The brief pick names a pattern, the brief lists three mitigations, and
two product repos (supplier-risk-rag-agent, chip-supply-chain-map) ship
agent-written work to human queues today. The Glasswing maintainers
asked Anthropic to slow disclosure for this reason. A portfolio policy
that the procurement-side repos apply by hand the next time a queue
backs up is the cheapest version of the lesson.

## Where it would land

`athena-site/ops/control-plane.md` (the operating-model file) gains a
new section, or a sibling `athena-site/ops/queue-overflow-policy.md`
keeps it modular. Each product repo's AGENTS.md links to it.

## How we'd know it worked

Next time a procurement-side repo ships an agent-written PR pipeline,
the queue-overflow policy ships with it before the queue backs up.

## Source

Brief pick:
[briefs/2026-W22/brief.md - Project Glasswing 10,000-bug update](../../briefs/2026-W22/brief.md#project-glasswing-10000-bug-update--write-a-queue-overflow-policy-this-week).
