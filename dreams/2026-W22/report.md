# dream 2026-W22 - Friday retrospective on the v2 engineering-grade rollout

**week of 2026-05-22 through 2026-05-29 - generated 2026-05-29 - model: claude-opus-4-7 - run by: learning.dream-orchestrator**

The second weekly dream pass against ai-field-brief, written on the Friday that closes the v2 engineering-grade run-evidence rollout. Twenty commits landed on `main` between 2026-05-22 and 2026-05-29, covering eight named rounds plus the two parallel workflows: typed event payloads (Rounds 1-2), the run-evidence emitter library and CLIs (Rounds 3-4), the validate_run_evidence gate with four cross-checks (Round 5), the replay equivalence CLI (Round 6), the portable `repo://` URI migration (Round 7), the sandbox-SHA finalize pass (Round 8), the CI run-evidence gate chain enforcement (Workflow A), and the source-registry W22 expansion (Workflow B). This pass runs four of the eight dream modes against that window and proposes five forward bets.

The mode-by-mode shape:

- **memory_consolidation** - folded into the candidates, not emitted standalone. The recurring lesson across the rollout is that two-pass protocols leak into every downstream consumer; that lesson sits inside candidate `reduce-001`.
- **architecture_drift_detection** - the spec ledger and the file tree match. The 22 R-PUB-* requirements added across the rollout all carry DEC coverage. No drift; instead the dream surfaces what is now load-bearing without an exercise gate (candidate `audit-001`).
- **skill_extraction** - the run-evidence emission pattern has shipped through the same shape three times (W20 backfill, W21 backfill, W22 regenerate) and is about to ship a fourth time in the prompt-matrix plane. Three is the graduation threshold; candidate `extend-002` graduates the pattern into a named skill.
- **adversarial_simulation** - the prior W21 pass deferred this mode because no fragile parser was named. The v2 rollout named several: `canonicalize_payload_for_hash`, `replay_run.py --strict-head`, and the `@PENDING/` two-pass tail. Candidate `audit-001` proposes the first adversarial gate against `replay_run.py`.

## What is now load-bearing that wasn't 30 days ago

Five surfaces moved from documented intent to enforced contract in this window:

1. **Typed event payloads.** `ops/schemas-cache/event.schema.json` (refreshed in `ee55ef0`) is the cross-repo contract; `validate_run_evidence.py` (`9002fec`, `2a8af1e`) enforces the typed shape on every committed event ledger. Before the rollout, `pipeline.complete` payloads were free-form blobs; now every payload conforms to its declared event_type or the gate fails the PR.
2. **`run.evidence.replayed` event type.** Round 6 (`0c16298`) added the per-replay event emission. Every replay run writes a fresh `ops/event-ledger/replay-run-<run-id>-<timestamp>.jsonl` carrying the verdict. The replay history is now a durable audit trail, not a transient CI artifact.
3. **Portable `repo://` URIs.** Round 7 (`457bbd2`, `f2291a4`) migrated every output reference from local-relative paths to `repo://ai-field-brief@<sha>/<path>`. trace-to-eval-harness can now resolve outputs cross-repo with `--portfolio-root`; before the migration, every consumer carried bespoke path-resolution code.
4. **Sandbox SHA finalization.** Round 8 (`e4fa4d5`, `2836c5f`) added the `finalize_sandbox_ref` CLI plus `--force` for re-anchoring real SHAs. The two-pass protocol (record at PENDING, finalize after the records-containing commit lands) is documented in DEC-PUB-008 and DEC-PUB-009 as the unavoidable consequence of putting the records-containing SHA inside the records themselves.
5. **Three-sample CI matrix gate.** Workflow A (`ee752a9`, `b138b31`) shipped `.github/workflows/run-evidence-gates.yml`, which matrix-tests packet generation + validation + replay smoke against `run-36e307499472`, `run-d74d787e6756`, and `run-1f1fc1f3d36d` on every PR. Before the workflow, only `ci.yml` ran, and the canonical samples were committed snapshots without a per-PR replay gate.

## What landed as DECs vs what is documented but unenforced

Seven DECs landed in the window: DEC-PUB-005 (brief emits conformant run evidence), DEC-PUB-006 (four cross-checks), DEC-PUB-007 (replay command), DEC-PUB-008 (portable URI migration), DEC-PUB-009 (CI run-evidence chain enforcement), DEC-SRC-017 (static registry connector readiness), DEC-SRC-018 (W22 source-registry expansion). Every DEC carries the matching `R-PUB-*` or `R-SRC-*` requirement coverage in `specs/0007-publishing/requirements.md` or `specs/0002-source-registry/requirements.md`.

Three surfaces are documented but not yet gate-enforced:

- The `replay_equivalent: false` verdict shape. `replay_run.py` produces a structured verdict, but a CI consumer reading the verdict to surface the delta does not exist yet; the gate only checks the boolean.
- The `@PENDING/` placeholder semantic. DEC-PUB-008 documents the two-pass tail; the records-restore-from-main step in `run-evidence-gates.yml` works around it; no test fails the build if a Run record ships with `@PENDING/` still in it after finalize.
- The `--portfolio-root` resolver shape. trace-to-eval-harness owns the dereferencer for `repo://`; no in-repo test confirms a sample Run packet round-trips through the resolver. CI exercises it as part of the matrix gate, but a unit-test-grade contract does not exist locally.

## What gates fire on every PR now

`ci.yml` (universal gates): schema-cache freshness, voice lint, no-BOM, spec-check, decisions validation, validate_run_evidence, pnpm lint/typecheck/test/build, pnpm audit (advisory, `|| true`).

`run-evidence-gates.yml` (product-repo-specific): packet-generation-from-canonical-sample (matrix x 3), packet-validation (matrix x 3), replay-smoke (matrix x 3 with `git checkout <sandbox-sha>` + records-restore-from-main).

What used to be manual:

- Voice lint was a run-before-push reminder; now it is a CI step.
- Run evidence was a we-will-wire-it-after-the-first-brief deferred work item; now it is a typed-payload contract with four cross-checks per Run record.
- Replay was a manual diff exercise across two brief revisions; now `python scripts/replay_run.py --run-id <id>` returns a verdict.
- Schema-cache freshness was an honor-system step in the playbook; now `check_schema_cache_freshness.py` enforces it.

## What surfaced as a fragile or under-documented edge

Four edges showed up during the rollout. Each one is the kind of edge that compiles, passes tests today, and breaks silently under a small enough mutation:

1. **The two-pass tail.** Recording the records-containing SHA inside the records themselves creates a recursive-tail problem that DEC-PUB-008 names as unreachable in one pass. The workaround (records-restore-from-main in `run-evidence-gates.yml`) is honest engineering, and it is also a workaround. Candidate `reduce-001` proposes the content-addressable indirection that retires the workaround.
2. **`canonicalize_payload_for_hash` non-determinism risk.** The canonicalizer in `run_evidence.py` sorts keys and normalizes line endings, and the sample set is three Run records; a small enough N that a subtle non-determinism (locale-dependent sort, encoding edge case) might not surface until the fourth sample regenerates differently. Candidate `audit-001` proposes a chaos test that mutates the canonical samples and confirms replay reports the delta cleanly with no crash and no accidental match.
3. **`replay_equivalent: false` is a boolean.** When replay fails the only signal is the verdict file says false. The next agent reading the failed gate has to re-run replay locally to learn what changed. Candidate `extend-001` proposes a structured-diff explainer attached to the verdict so the next failed gate report tells the story without a re-run.
4. **The matrix-plane (spec 0012) does not inherit the run-evidence shape yet.** The four science roles (cell-verifier, lens-designer, matrix-runner, matrix-synthesis-editor) all emit cells, and the cell-emission pattern is not the same as the Run-emission pattern. The matrix-runner WIP in the working tree does not yet wire `run_evidence.emit_pipeline_complete`. Candidate `extend-002` proposes graduating the run-evidence pattern into a skill that the matrix-runner inherits from day one.

## Five forward bets

Each candidate names a concrete forward move. The mix:

- One AUDIT - chaos-test the replay equivalence gate (`audit-001`).
- One REDUCE - retire the two-pass tail via content-addressable sandbox refs (`reduce-001`).
- Two EXTEND - `--explain` flag on replay (`extend-001`); run-evidence skill graduation that matrix-plane inherits (`extend-002`).
- One CROSS-LINK - surface the three canonical samples in athena-site's portfolio replay panel (`crosslink-001`).

Each candidate file under `candidates/` carries the proposal, the why, the cost, the risk, and the suggested timeline. Every candidate is human-gated; the dream does not auto-promote.

## What this dream does not surface

- **No counterfactual replay candidate.** `replay_run.py` already runs a counterfactual on every PR; a dream-level counterfactual would duplicate the gate.
- **No prompt patch candidate.** The repo holds no versioned prompt files yet. The matrix-plane WIP (spec 0012) is putting some prompts under `prompts/`, and they are not in scope for this dream.
- **No failure cluster.** Zero CI failures landed in the rollout window; the gate chain shipped green on the first run after the regenerate pass.

## Handoff

This dream pass hands off to `control.coordinator` per the weekly-dream workflow (`.agents/workflows/weekly-dream.yaml`, step `human-review`). The coordinator routes each picked candidate to the role that owns the target file:

- `audit-001` to `science.proof-gate-runner` (the gate owner role per DEC-PUB-009)
- `reduce-001` to `engineering.implementation` (touches `run_evidence.py`)
- `extend-001` to `engineering.implementation` (touches `replay_run.py`)
- `crosslink-001` to `control.coordinator` (cross-repo work needs portfolio routing)
- `extend-002` to `learning.skill-curator` + `science.matrix-runner` (skill graduation + new-role adoption)

No candidate moves to its target file without the human approval the coordinator gates.

## Costs

This run produced one human-readable narrative, five candidate files, and one meta.yaml. The dream-job event lands as part of the regular `ops/event-log/` cadence when the candidate review pass closes; the dream itself is the artifact.

## Candidate index

- `candidates/audit-001-replay-chaos-adversarial-mutations.md`
- `candidates/reduce-001-content-addressable-sandbox-ref.md`
- `candidates/extend-001-replay-explain-flag-structured-diff.md`
- `candidates/crosslink-001-portfolio-replay-panel-in-athena-site.md`
- `candidates/extend-002-run-evidence-skill-for-matrix-plane.md`
