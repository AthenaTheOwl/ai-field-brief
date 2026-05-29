# playbook: run a weekly brief

The operating contract for a Claude or Codex agent running the manual
weekly pass. Read this top-to-bottom before starting.

## Inputs

- `sources/registry.yaml` — the active source list.
- `templates/weekly-brief.md` — the format.
- `briefs/INDEX.md` — index of past briefs.
- Last 2 brief markdown files under `briefs/YYYY-WNN/` for continuity.
- `scripts/voice_lint.py` — voice rules the brief must pass.

## Steps

1. **Determine ISO week.** Today's date, ISO 8601 calendar. Folder is
   `briefs/YYYY-WNN/`. If the folder exists, halt and ask the human
   whether to overwrite or append.

2. **Sweep sources.** For each `status: active` source in
   `sources/registry.yaml`, fetch the homepage / archive / RSS surface
   and capture posts published since the previous brief's
   `meta.yaml.through_date` (or the last 7 days if this is the first
   run). Some sources will 403 or rate-limit; record the failure in
   `meta.yaml` and continue — do not block on a single source.

3. **Triage.** For each captured item, decide:
   - Include in *This week* — material change, substantive piece,
     primary-source signal.
   - Mention in *Worth your time* — useful but not the week's pattern.
   - Note for the *Watchlist* — open question worth tracking.
   - Drop — not worth the reader's attention.

   The rubric is informal in v1; spec 0005 (R-EXT) lands the scored
   version.

4. **Matrix cell production.** For each captured source item that
   survived triage, apply every `required: true` lens from
   `config/prompt_lenses.yaml` (and any optional lens the profile
   selects) to produce one matrix cell per source-item-lens pair.
   Each cell records: source-item id, lens id, extraction mode,
   answer text, source refs (every claim cites a span), confidence
   (`high`/`medium`/`low`), and `faithfulness_status: not_checked`.
   Cells land in the run-evidence path so the brief generation can
   reference them later. The cell shape matches
   `schemas/matrix_cell.schema.json`; the lens prompts live at
   `prompts/lenses/`. This step pins to the `science.matrix-runner`
   role; see `.agents/roles/science.matrix-runner/instructions.md`
   for the run-time contract.

5. **Cell faithfulness verification.** Read every cell from step 4
   against the source body. Apply the seven-question check in
   `prompts/cell_faithfulness.md`: unsupported claim, overstated
   certainty, missing caveat, invented consensus, wrong source span,
   too generic, action recommendation not supported by the source.
   Each cell receives one verdict: `PASS`, `PATCH_CELL`, or
   `FAIL_CELL`. Patched cells move to `verified`; failed cells drop.
   This step pins to the `science.cell-verifier` role.

6. **Theme and row synthesis.** Cluster verified cells by theme and
   draft row summaries from cell evidence. Every sentence in a row
   summary, theme cluster, or action candidate carries an inline
   cell-id reference. Action candidates that cannot point at a
   verified cell drop. This step pins to the
   `science.matrix-synthesis-editor` role and produces the input the
   brief author pulls from in step 7.

7. **Synthesize.** Draft `briefs/YYYY-WNN/brief.md` against
   `templates/weekly-brief.md`, drawing on the row summaries from
   step 6. Every pick names the cell ids it leans on as inline
   comments (the rendered markdown stays clean; the cell-id stays in
   a comment alongside the link). The opening reflection names the
   pattern; the picks earn their place with comment, not link-dumps.

8. **Faithfulness audit (per cell).** Before voice-lint, re-read
   each pick with these questions:

   - Did we overstate? Is there a claim that goes beyond what the
     source supports?
   - Did we drop a caveat? Did the source include conditions that we
     lost?
   - Does every claim have a source link? "Per Anthropic's blog"
     without a link is not citation.
   - Did we invent consensus? Are we describing one analyst's take as
     if it were a field thesis?
   - Did we mistake hype for mechanism? Is the "what changed" a
     specific behavior change, or a narrative claim wearing the same
     clothes?

   For each pick that fails any of these, fix before voice-lint. If a
   claim can't be backed by a source link, drop it.

   This pass takes 10-15 minutes per brief. Not optional. Captured as
   DEC-PUB-004.

9. **Voice pass.** Run `python scripts/voice_lint.py`. Fix every FAIL.
   Re-read the draft top-to-bottom — does the rhythm sound like a
   considered weekly letter, or like an aggregator?

10. **Meta log.** Write `briefs/YYYY-WNN/meta.yaml`: sources reviewed,
    items captured per source, items included, failures during sweep,
    notes for next run.

11. **Update the index.** Add the new row to `briefs/INDEX.md`. Newest
    first.

12. **Verify.** Run all four gates:
    ```
    python scripts/spec_check.py
    python scripts/voice_lint.py
    python scripts/validate_schemas.py
    python scripts/validate_registry.py
    ```
    All must be green.

13. **Pause for human review.** Output a short summary: sources swept,
    items included, surprises, any sources to add. The human reads
    `brief.md` + `meta.yaml`, edits voice, then approves.

14. **Emit run evidence.** Before commit, write the Run record and
    event ledger for this run:
    ```
    python scripts/finalize_run.py \
        --brief briefs/YYYY-WNN/ \
        --gates "voice_lint:passed,spec_check:passed,check_no_bom:passed,validate_schemas:passed,validate_registry:passed,validate_decisions:passed"
    ```
    The CLI writes `ops/run-records/<run-id>.json` and
    `ops/event-ledger/<run-id>.jsonl`. The validator gate
    `scripts/validate_run_evidence.py` will catch any malformed
    record before the push lands.

15. **Commit.** Match the existing commit-message style. One commit
    per brief; subject `brief 2026-WNN: <one-line frame>`. The Run
    record and event ledger go in the same commit as the brief.

## What this playbook is not

- Not a fixed template. The shape under `templates/weekly-brief.md` is
  a suggestion. The author varies cadence to match the week.
- Not automated. Cron + Inngest land with spec 0003. Until then, the
  agent runs on a human's "go".
- Not silent. Every brief logs its sweep + decisions in `meta.yaml`.

## Style reference

The shape is taken loosely from Farnam Street's *Brain Food*, Ben
Thompson's day-after notes, and Simon Willison's roundups — slow news
letters that earn the reader's attention by saying less and saying it
better. The structural rules in `scripts/voice_lint.py` exist so an
agent's first-draft tone never lands on AI-cadence.
