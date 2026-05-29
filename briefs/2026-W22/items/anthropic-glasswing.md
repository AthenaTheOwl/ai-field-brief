# anthropic-glasswing

- **Source:** Anthropic Research (Project Glasswing initial update)
- **URL:** https://www.anthropic.com/research/glasswing-initial-update
- **Captured:** 2026-05-28
- **Priority:** high
- **Cells:** MTRX-W22-anthropic-glasswing-source_gist, MTRX-W22-anthropic-glasswing-mechanism_extraction, MTRX-W22-anthropic-glasswing-adoption_action, MTRX-W22-anthropic-glasswing-governance_surface, MTRX-W22-anthropic-glasswing-risk_and_caveats

## What

Anthropic plus roughly 50 vetted partners using Claude Mythos
Preview have surfaced more than 10,000 high or critical
vulnerabilities across critical infrastructure. Cloudflare
reportedly found 2,000 bugs at better accuracy than human testers;
Mozilla found 271 Firefox vulnerabilities, more than 10x the
prior testing throughput. The Glasswing post names the new
bottleneck explicitly: verify, disclose, patch.

## Why it matters

The finding-side capacity just multiplied by an order of
magnitude. The downstream pipeline did not. The same week,
Daniel Stenberg's curl pressure post named the inverse failure
mode for OSS maintainers without the vetted-partner structure:
more than one AI-assisted report per day, 4-5x 2024, double 2025.
The two posts describe the offense and defense of the same shape.

## Action surface

workflow, tool-policy, agent-role

## Concrete move

If you maintain critical OSS or vendor critical software, plan
for an order-of-magnitude increase in inbound vulnerability
reports inside the next two quarters. Size triage and disclosure
capacity to match. Establish an AI-assisted report intake rubric
that requires a PoC and a severity claim; route reports that fail
the rubric to a separate queue with a different SLA.

## Caveats

All Glasswing numbers are vendor-program-internal and partner-
reported; no independent audit. "Better accuracy than human
testers" is asserted, not benchmarked, in the excerpt. The
concentration on a single vendor model (Mythos Preview) is a
governance question for any participating PSIRT. Low-quality AI-
generated reports may flood maintainers downstream as the
technique generalizes beyond the vetted partner set.
