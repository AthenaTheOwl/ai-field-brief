# @aifieldbrief/evals

Eval datasets, graders, reports, thresholds. Phase 0 ships the *dataset
shape* so future prompt and model changes have a stable contract to grade
against. Runners + graders land with spec 0005 (extraction) and spec 0009
(retrieval / RAG).

## Suites in v1

| Suite | Schema | What it gates |
|---|---|---|
| `citation-faithfulness` | `schemas/citation-faithfulness.schema.json` | Every brief claim points at a span that exists verbatim in the cited target. Pass rate ≥ 0.95 (R-BOOT-005). |
| `hallucination` | `schemas/hallucination.schema.json` | Insight `what_changed` and `actionable_takeaway` are supported by their citations. Flag false-positive rate kept low. |

Future suites (retrieval-quality, supplier-risk-questions, refusal-cases,
abstention, regression) land alongside the specs that produce them.

## Rule

> No LLM output without evals.

Prompt or model changes must run the matching suite. CI gates regressions
below the baseline scores committed in `reports/` (created when the runner
lands in spec 0005).
