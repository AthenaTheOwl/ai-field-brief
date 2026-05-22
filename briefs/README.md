# briefs/

Weekly digests, archived by ISO week. Each week's folder ends up looking
like this:

```
briefs/
  INDEX.md                     rolling table of every published brief
  README.md                    this file
  2026-W21/
    brief.md                   the published digest
    meta.yaml                  sources reviewed, scoring decisions, run
                               timestamp; consumed by the audit log
```

## Format

The brief is the primary artifact. It reads top-to-bottom in 5–10
minutes and follows a loose shape:

1. **Opening reflection** — one or two short paragraphs that name the
   pattern of the week. Not a TL;DR; a viewpoint.
2. **This week** — three to six picks with substantive comment. Each
   pick names what changed, why it matters, and the slow read.
3. **Worth your time** — links the reader might miss without the
   sweep. Smaller picks; one paragraph each.
4. **Watchlist** — a few open questions to track, not answer.
5. **Closing thought** — one sentence or paragraph that grounds the
   week.

The shape is a suggestion, taken loosely from Farnam Street's *Brain
Food* and similar slow-news letters. Variation is fine; voice
discipline is not.

## Discipline

- `scripts/voice_lint.py` scans every brief markdown file. FAIL hits
  block commit. `voice_lint:allow <label>` on the offending line is
  the escape, but the rule is fix-don't-allowlist except for the
  rare case where the construction earns its keep.
- Every claim in a brief should be backed by a link to a primary
  source. The verifier (citation-faithfulness, R-EXT-004) lands with
  spec 0005; until then, the discipline is manual.
- The brief is published; the per-item structured notes that produced
  it are an audit trail. Both end up under `briefs/YYYY-WNN/` once the
  full playbook lands.

## Cadence

Manually triggered. Runs whenever a Claude or Codex agent executes
`playbook/run-weekly-brief.md`. No cron until spec 0003.
