# openai-cookbook-claude-migration

- **Source:** openai/openai-cookbook commits
- **URL:** https://github.com/openai/openai-cookbook/commit/f6a7ffa9ddd57849bb280b20102da7ff8620e8fa
- **Captured:** 2026-05-27
- **Priority:** medium
- **Cells:** MTRX-W22-cookbook-source_gist, MTRX-W22-cookbook-claims_and_bets, MTRX-W22-cookbook-governance_surface

## What

OpenAI's cookbook merged a "Claude Agent SDK migration" recipe via
PRs #2671 and #2742 on May 27. The cookbook now publishes a
documented path for teams running on Anthropic's Agent SDK to
migrate to OpenAI agents.

## Why it matters

Publishing the migration recipe is an explicit competitive bet —
OpenAI expects net flow from Anthropic Agent SDK to OpenAI agents
and is reducing the friction. The signal is the cookbook add, not
a marketing post. Anthropic does not currently publish the reverse.

## Action surface

source-registry, architecture

## Concrete move

For procurement teams reviewing AI agent vendor lock-in: ask both
labs for a published migration path to the other. The asymmetric
absence of the reverse recipe is now a concrete lock-in
consideration.

## Caveats

A cookbook recipe is a documentation artifact, not a feature
release; migration cost is still meaningful and the recipe is
expected to be revised. The signal here is the strategic posture,
not the implementation completeness.
