---
id: DEC-PUB-008-brief-portable-repo-uri-migration
spec: specs/0007-publishing/
requirement: R-PUB-018
date: 2026-05-29
status: approved
reversible: true
amends: DEC-PUB-007-brief-replay-command
decision: |
  ai-field-brief's run-evidence emitter migrates to the portable
  `repo://` and `artifact://` URI grammar defined in DEC-CDCP-014
  (athena-site). The emitter writes `sandbox_image_ref` as
  `repo://ai-field-brief@<sha>/`, wraps every `inputs[].ref` as
  `repo://ai-field-brief@<sha>/<rel-path>`, and wraps every
  `outputs[].artifact_id` as either `repo://ai-field-brief@<sha>/<rel-path>`
  for path-shaped outputs or `artifact://ai-field-brief/<id>` for
  logical artifact ids. `workspace_id` stays the bare repo identifier
  (`ai-field-brief`); it is an identity string, not a file reference.
  The validator (`scripts/validate_run_evidence.py`) and the replay
  CLI (`scripts/replay_run.py`) ship `resolve_uri(uri, portfolio_root)`
  helpers that accept the new URI forms AND legacy local paths during
  the interop window, per the DEC-CDCP-014 interop clause.

  The systemic `sandbox_image_ref` off-by-one (the emitter reads
  `git rev-parse HEAD` at emit time, which names the PARENT of the
  commit that will land the sample) is closed via a two-pass protocol
  (Option A from the round-6 spec):

  1. The emitter writes `repo://ai-field-brief@PENDING/` as a
     placeholder into `sandbox_image_ref` and into every inputs/outputs
     URI when called with `sandbox_sha_pending=True`.
     `scripts/backfill_run_records.py` always uses the placeholder;
     `scripts/finalize_run.py` accepts a `--sandbox-pending` flag for
     the same shape on live runs.
  2. `scripts/finalize_sandbox_ref.py --all --sha <sha>` (or
     `--run-id <id>`) rewrites every `@PENDING/` occurrence to
     `@<sha>/` in one or every Run record. The CLI defaults `--sha`
     to `git rev-parse HEAD`, so the regenerate workflow is:
     emit-with-placeholder → commit → run finalize_sandbox_ref →
     commit. The second commit closes the off-by-one because the
     finalize step records the SHA of the records-containing commit
     that just landed.

  The replay CLI accepts both the new URI form and the legacy
  `<abs-path>@<sha>` form on `sandbox_image_ref`; the shared
  `run_evidence.parse_sandbox_sha` helper extracts the SHA from either
  shape. The validator's `resolve_uri` mirrors the emitter helper and
  is exported for the Round 7 file-existence gate.
alternatives:
  - label: emit `sandbox_image_ref` with `git rev-parse HEAD` at emit
      time and accept that replay HEAD-strict targets the parent commit
    rejected_because: |
      Round 5 surfaced the cost across four agents independently:
      `sandbox_image_ref` recorded at emit time names the PARENT of the
      commit that lands the sample. Replay HEAD-strict then verifies
      against a SHA at which the Run record itself does not exist
      (and at which the briefs that the record names may or may not
      exist depending on the regen flow). The patches the Round 5
      agents made all targeted the symptom (rewrite the SHA after
      commit, hand-edit the sample, or pick an earlier SHA). The
      two-pass protocol is the root-cause fix: emit a placeholder
      explicitly, rewrite once the SHA is known, document the
      protocol in this DEC. Idempotent rewrites mean re-running
      `finalize_sandbox_ref.py` is safe; nothing relies on the
      legacy "guess the right SHA at emit time" shape.
  - label: option B — pass `--sandbox-sha` to the emitter from a
      regenerate wrapper that commits the briefs first
    rejected_because: |
      Option B works for live runs where the brief content is the
      delta being committed, but the W20/W21/W22 backfill writes
      ONLY the Run record and the ledger; there is no separate
      "brief content" commit to anchor against. The two-pass
      protocol (Option A) handles both cases with one shape: the
      emitter never has to know the future SHA, and the rewriter
      runs after every records-containing commit lands. Option C
      (post-edit the just-written JSON in the same wrapper) is a
      close cousin of Option A but couples the rewrite to the
      regenerate script, which means hand-running the emitter
      misses the rewrite step silently. Splitting the second pass
      into its own CLI keeps the contract explicit and testable.
  - label: emit URIs in the new grammar but keep `sandbox_image_ref`
      as an absolute path
    rejected_because: |
      Cross-repo refs in Run records become unintelligible the moment
      the portfolio moves between machines: `E:/claude_code/random-apps/`
      on one box, `/Users/x/random-apps/` on another, neither of
      which a consumer in another repo can reason about. DEC-CDCP-014
      names the portable shape; landing the migration in round 6 keeps
      the run-evidence shape coherent before Round 7 wires the gates
      and before the trace-to-eval-harness packets in Phase 3 start
      consuming these refs cross-repo.
rationale: |
  Round 6 is the portable-URI migration round. DEC-CDCP-014 lands the
  grammar (`repo://<repo>@<sha>/<rel-path>` for files, `artifact://<repo>/<id>`
  for logical artifacts); this DEC lands the per-repo emission +
  resolution change in ai-field-brief. The amended DEC-PUB-007
  semantic (`sandbox_image_ref` names the SHA at which the recorded
  hashes are reproducible) carries through unchanged; only the wire
  format moves.

  The systemic `sandbox_image_ref` off-by-one observed across four
  Round 5 agent reports is the second piece. The agents independently
  recognized that the emitter reads `git rev-parse HEAD` BEFORE the
  regenerate commit lands, so the recorded SHA is the parent of the
  commit that contains the sample. Each agent patched it via a
  different ad-hoc route (`--head-sha` override, hand-edit after
  commit, anchor at publishing-commit SHA, etc.); none of the
  patches were durable because the next regenerate pass would
  re-introduce the off-by-one. The two-pass protocol is the
  durable fix: the emitter emits a placeholder, a dedicated CLI
  rewrites the placeholder once the SHA is known, and the protocol
  is documented here so the next contributor finds the documented
  pattern instead of rediscovering the symptom.

  Interop is non-negotiable through this round. Existing Run records
  on other portfolio repos still carry the legacy
  `<abs-path>@<sha>` form; the replay CLI's `parse_sandbox_sha`
  helper extracts the SHA from either shape so a consumer that
  reads a Run record produced under the legacy emitter still works.
  Round 7 may deprecate the legacy form behind a CI gate; this
  round migrates without breakage.
evidence:
  - kind: decision
    ref: decisions/DEC-PUB-007-brief-replay-command.md
  - kind: decision
    ref: decisions/DEC-PUB-006-brief-emits-conformant-run-evidence-cross-checks.md
  - kind: code
    ref: scripts/run_evidence.py
  - kind: code
    ref: scripts/finalize_sandbox_ref.py
  - kind: code
    ref: scripts/backfill_run_records.py
  - kind: code
    ref: scripts/finalize_run.py
  - kind: code
    ref: scripts/validate_run_evidence.py
  - kind: code
    ref: scripts/replay_run.py
  - kind: code
    ref: tests/scripts/test_run_evidence.py
  - kind: code
    ref: tests/scripts/test_finalize_sandbox_ref.py
  - kind: spec
    ref: specs/0007-publishing/requirements.md
rollback: |
  Revert the emitter to write the legacy `<abs-path>@<sha>` form by
  flipping `derive_sandbox_image_ref` back to the absolute-path
  shape, drop the `compose_repo_uri` / `compose_artifact_uri` /
  `resolve_uri` / `parse_sandbox_sha` helpers, delete
  `scripts/finalize_sandbox_ref.py`, drop the
  `sandbox_sha_pending` parameter on `build_run_evidence_fields`,
  remove the `--sandbox-pending` flag from `scripts/finalize_run.py`,
  re-run `scripts/backfill_run_records.py --all` to regenerate the
  three sample records in the legacy shape, drop the
  `R-PUB-018..R-PUB-021` rows from `specs/0007-publishing/`, drop
  the new DEC-PUB-008 entries from
  `decisions/.spec-check-allowlist.yaml`, and delete this DEC. The
  replay CLI's interop branch (legacy form acceptance) does not
  need to be removed; it stays as a no-op once everything is back
  to legacy. No data migration is needed because the run records
  and ledgers are append-only audit trails with no fan-out.
owner: science.proof-gate-runner
---

## decision

ai-field-brief's run-evidence emitter migrates to the portable
`repo://` and `artifact://` URI grammar defined in DEC-CDCP-014
(athena-site). The emitter writes `sandbox_image_ref` as
`repo://ai-field-brief@<sha>/`, wraps every `inputs[].ref` as
`repo://ai-field-brief@<sha>/<rel-path>`, and wraps every
`outputs[].artifact_id` as either `repo://ai-field-brief@<sha>/<rel-path>`
for path-shaped outputs or `artifact://ai-field-brief/<id>` for
logical artifact ids. `workspace_id` stays the bare repo identifier
(`ai-field-brief`). The validator and replay CLI accept both the new
URI forms AND legacy local paths during the interop window per the
DEC-CDCP-014 interop clause.

The systemic `sandbox_image_ref` off-by-one (the emitter reads
`git rev-parse HEAD` BEFORE the regenerate commit lands, so the
recorded SHA names the PARENT of the commit that contains the sample)
is closed via a two-pass protocol. The emitter writes
`repo://ai-field-brief@PENDING/` as a placeholder; a dedicated CLI
`scripts/finalize_sandbox_ref.py` reads the just-landed SHA via
`git rev-parse HEAD` (or `--sha` override) and rewrites every
PENDING placeholder in one or every Run record. The regenerate flow
becomes: emit-with-placeholder → commit → finalize_sandbox_ref →
commit. The second commit's SHA is the one the record names, so
replay HEAD-strict succeeds at HEAD without `git checkout` gymnastics.

## alternatives

- Emit `sandbox_image_ref` with `git rev-parse HEAD` at emit time
  and accept that replay HEAD-strict targets the parent commit.
  Rejected because four Round 5 agents independently patched this
  symptom; the two-pass protocol is the root-cause fix.
- Option B (pass `--sandbox-sha` from a regenerate wrapper that
  commits the briefs first). Rejected because the backfill writes
  only the Run record + ledger; there is no separate brief commit
  to anchor against.
- Emit URIs but keep `sandbox_image_ref` as an absolute path.
  Rejected because cross-repo refs need to survive a portfolio
  move; the portable URI shape is the durable form.

## rationale

Round 6 is the portable-URI migration round. DEC-CDCP-014 lands the
grammar; this DEC lands the per-repo emission and resolution change.
The systemic off-by-one observed across four Round 5 agent reports is
the second piece. Each agent patched the symptom ad-hoc; none of the
patches were durable because the next regenerate pass would
re-introduce the issue. The two-pass protocol is the durable fix:
the emitter emits a placeholder, a dedicated CLI rewrites it once the
SHA is known, and the protocol is documented here so the next
contributor finds the documented pattern instead of rediscovering the symptom.

Interop is non-negotiable through this round. The replay CLI's
`parse_sandbox_sha` helper extracts the SHA from either the new
portable form or the legacy `<abs-path>@<sha>` form, so a consumer
that reads a Run record produced under the legacy emitter still
works. Round 7 may deprecate the legacy form behind a CI gate.

## rollback

Revert the emitter to write the legacy form, drop the
`compose_repo_uri` / `compose_artifact_uri` / `resolve_uri` /
`parse_sandbox_sha` helpers, delete `scripts/finalize_sandbox_ref.py`,
drop the `sandbox_sha_pending` parameter from
`build_run_evidence_fields`, remove the `--sandbox-pending` flag from
`scripts/finalize_run.py`, re-run
`scripts/backfill_run_records.py --all` to regenerate the three
sample records in the legacy shape, drop the R-PUB-018..R-PUB-021
rows from `specs/0007-publishing/`, drop the new DEC-PUB-008 entries
from `decisions/.spec-check-allowlist.yaml`, and delete this DEC.

## coverage

This DEC resolves the following requirements added to
`specs/0007-publishing/requirements.md`:

- `R-PUB-018` ai-field-brief emitter produces portable `repo://` and
  `artifact://` URIs per DEC-CDCP-014.
- `R-PUB-019` validator + replay accept both portable URI forms and
  legacy local paths during the interop window.
- `R-PUB-020` `sandbox_image_ref` off-by-one is closed via a two-pass
  protocol (placeholder emit + post-commit rewrite).
- `R-PUB-021` `scripts/finalize_sandbox_ref.py` ships as the
  second-pass CLI; idempotent on records with no PENDING markers.
