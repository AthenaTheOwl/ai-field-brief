# anthropic-opus-4-8

- **Source:** Anthropic News
- **URL:** https://www.anthropic.com/news/claude-opus-4-8
- **Captured:** 2026-05-28
- **Priority:** high
- **Cells:** MTRX-W22-opus48-source_gist, MTRX-W22-opus48-claims_and_bets, MTRX-W22-opus48-mechanism_extraction, MTRX-W22-opus48-adoption_action, MTRX-W22-opus48-risk_and_caveats, MTRX-W22-opus48-governance_surface, MTRX-W22-opus48-watchlist_trigger

## What

Anthropic released Claude Opus 4.8 on May 28 with vendor-stated
gains in coding, agentic, and professional-work consistency, and
materially lower hallucination on uncertain questions. Simon
Willison summarized the release as "a modest but tangible
improvement" with ~4x lower hallucination rate vs Opus 4.7 — the
mechanism being abstention on questions the model judges uncertain.

## Why it matters

The release shipped paired with Claude Code v2.1.154, which
defaults Opus 4.8 with `/effort xhigh` and a lean system prompt for
new models. Teams running long agentic sessions need to re-baseline
eval suites against the new defaults; teams scoring agents on
question-answer coverage will see scores drift downward as the
model declines borderline questions.

## Action surface

prompt, eval, config

## Concrete move

Pin Claude Code at v2.1.156 or later (the .154 release had an Opus
4.8 thinking-block bug that .156 fixes), add a refusal-rate panel to
agent dashboards, and verify your eval rubric does not penalize
abstention.

## Caveats

The 4x hallucination figure is vendor-reported through a single
secondary source. Independent evals will arrive over the next two
weeks; treat Opus 4.7 as the safer floor for production-critical
workloads until they land.
