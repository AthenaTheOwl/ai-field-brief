# Cell Faithfulness Check

Given a matrix cell and the source text/transcript, determine whether the cell is faithful.

Read `prompts/editorial_contract.md`. Match the claim to the actual source
span, including its unit, denominator, time window, baseline and limits.
Check whether the wording turns a company account into an independent
result, a proposed test into an executed one, or an association into a
cause. A matching numeral or a valid URL does not settle those questions.

Check:
- unsupported claim
- overstated certainty
- missing caveat
- invented consensus
- wrong source span
- too generic to be useful
- action recommendation not supported by the source

Verdict:
- PASS
- PATCH_CELL
- FAIL_CELL

Return a short patch instruction when needed.

Identify the exact unsupported words and the smallest source-backed
correction. Preserve the author's voice in that correction. Record a
current review as current; do not rewrite an earlier run's verdict.
