# Cell Faithfulness Check

Given a matrix cell and the source text/transcript, determine whether the cell is faithful.

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
