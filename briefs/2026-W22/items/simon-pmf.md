# simon-pmf

- **Source:** Simon Willison's Weblog
- **URL:** https://simonwillison.net/2026/May/27/product-market-fit/
- **Captured:** 2026-05-27
- **Priority:** high
- **Cells:** MTRX-W22-pmf-source_gist, MTRX-W22-pmf-claims_and_bets, MTRX-W22-pmf-adoption_action, MTRX-W22-pmf-risk_and_caveats

## What

Willison argues Anthropic and OpenAI found product-market fit in
early 2026 by moving enterprise customers from seat-based pricing
to API pricing, where coding agents burn vastly more tokens than
humans. His personal data: $1,199.79 (Claude Code) + $980.37
(OpenAI) over 30 days against a $200/mo subscription each. The
Uber data point: 25% of commits via Claude Code last quarter,
"rapidly consuming annual AI budgets set in 2025."

## Why it matters

April 2026 is the pricing-model inflection. The Anthropic Series H
+ $47B run-rate disclosure (later in the same week) is the
financial confirmation. The build-vs-buy and budget-planning
questions teams answered in 2024 are stale; the line item moved
categories.

## Action surface

config, workflow

## Concrete move

Rebuild the AI-tooling line item as consumption-per-developer with
a monthly cap and a 70% alert. For finance partners: assume any
team running coding agents inside an annual seat budget set before
April 2026 is off by an order of magnitude.

## Caveats

Willison is one practitioner with above-median usage; n=1 spend
numbers are illustrative, not benchmark. The Uber 25% figure is
relayed second-hand without an underlying disclosure to verify.
Both are directionally credible and not commitable to a budget
without your own pilot.
