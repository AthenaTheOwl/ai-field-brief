---
id: PROM-W21-001
brief: 2026-W21
pick_slug: anthropic-acquires-stainless-sdk-pin-contract-test
target_repo: ai-field-brief
target_artifact_type: regression-test
date: 2026-05-25
status: proposed
landed_commit: null
---

## What

Land the SDK contract test pattern from the brief as a regression test
across the three product repos that depend on the Anthropic SDK:
ai-field-brief (apps/web), supplier-risk-rag-agent, and
chip-supply-chain-map. The test exercises the two or three call shapes
the repo relies on and fails CI when an SDK upgrade silently re-shapes
errors.

## Why this earns a promotion

The Stainless acquisition is the exact case the contract-test pattern
was written for. Each repo currently floats on `anthropic@latest` or
similar; the test costs nothing because it never reaches the model and
catches a class of in-flight breakage that lands in error handling
first. Three repos applying the same shape is the multiplier.

## Where it would land

- `ai-field-brief/apps/web/test/sdk-contract.test.ts`
- `supplier-risk-rag-agent/tests/sdk-contract.test.py` (or equivalent)
- `chip-supply-chain-map/tests/sdk-contract.test.ts`

Each repo also pins SDK minors in its lockfile.

## How we'd know it worked

A future SDK changelog with "improved error handling" or "default
timeout adjusted" trips CI in the affected repos before users notice.

## Source

Brief pick:
[briefs/2026-W21/brief.md - Anthropic acquires Stainless](../../briefs/2026-W21/brief.md#anthropic-acquires-stainless--pin-your-sdk-versions-this-week).
