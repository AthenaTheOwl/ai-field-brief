---
id: extend-002-run-evidence-skill-for-matrix-plane
target_kind: skill_patch
skill_id: emit-run-evidence
human_review_required: true
status: candidate
evidence:
  - kind: code
    ref: scripts/run_evidence.py - the emitter library that has shipped through the same shape three times (W20 backfill, W21 backfill, W22 regenerate)
  - kind: code
    ref: scripts/finalize_run.py - the finalize pass CLI
  - kind: code
    ref: scripts/backfill_run_records.py - the backfill CLI used for W20 and W21
  - kind: decision
    ref: decisions/DEC-PUB-005-brief-emits-conformant-run-evidence.md - the contract the brief generator implements
  - kind: decision
    ref: decisions/DEC-PUB-006-brief-emits-conformant-run-evidence-cross-checks.md - the four cross-checks every emission must clear
  - kind: doc
    ref: specs/0012-prompt-matrix-plane/ (untracked WIP) - the next plane that will emit Run-shaped records; the four science roles do not yet inherit the emission pattern
  - kind: doc
    ref: ".agents/roles/science.matrix-runner/instructions.md (untracked WIP) - the role that runs prompt-matrix cells and is the natural first consumer of the skill"
---

## proposal

Graduate the run-evidence emission pattern into a named skill at `.agents/skills/emit-run-evidence/SKILL.md`. The skill packages the contract (DEC-PUB-005, DEC-PUB-006, DEC-PUB-008), the helper library (`scripts/run_evidence.py`), the four cross-checks the validator enforces, and the two-pass tail handling (or content-addressable equivalent if `reduce-001` lands first) into one named operation that any new emitter inherits from day one.

Proposed `SKILL.md` outline:

```markdown
# emit-run-evidence

## When to use
A new code path produces an output that should be replayable and
audit-anchored: a brief, a matrix cell, a connector run, a sweep audit.

## What it produces
- one ops/run-records/run-<id>.json with typed event payloads
- one ops/event-ledger/run-<id>.jsonl with the per-event audit trail
- recorded snapshot hashes for each output (canonicalized per the v1 helper)
- a portable repo:// URI per output (DEC-PUB-008 contract)
- a sandbox_image_ref (per current shape) or sandbox_image_cid (if reduce-001 lands)

## Inputs
- run_id (generator-provided, hex 12 chars)
- inputs object (typed, schema-cached)
- outputs list (path + canonicalized hash)
- the four cross-check inputs (DEC-PUB-006)

## Steps
1. Construct the typed events via run_evidence.emit_pipeline_complete().
2. Write the Run record + event ledger atomically.
3. Run scripts/validate_run_evidence.py against the new files; fail loud on any cross-check miss.
4. Commit the records-containing commit; run scripts/finalize_sandbox_ref.py against it.
5. (If reduce-001 lands: skip step 4; the cid-> sha ledger row gets appended.)

## Evals
- The validator exits 0 against the new Run record.
- Replaying the Run via replay_run.py returns replay_equivalent: true.
- Every repo:// URI in the Run record resolves through trace-to-eval-harness with --portfolio-root.
- The chaos suite from audit-001 (if landed) is green against the new record.

## Version: 0.1.0 (skill graduates to 1.0.0 after the matrix-plane runner inherits cleanly)
```

The skill graduates the pattern from "three commits' worth of copy-paste" into "one named operation." The matrix-plane runner (spec 0012) becomes the first consumer that inherits the skill from day one instead of re-discovering the steps.

## why it earns its keep

Three is the dream's graduation threshold. The run-evidence emission pattern has shipped three times: W20 backfill (`d98a533`), W21 backfill (`d98a533`), W22 regenerate (`959bcff`). The fourth shipping path is spec 0012's matrix-runner, which the working tree shows is in active WIP. Without the skill, the matrix-runner re-discovers the shape from the prior commits, and any subtle drift (a missing cross-check, a different event payload key) ships unnoticed.

The skill also gives the role-engineering layer (the `science.matrix-runner` role's instructions.md) a named operation to call: "emit run evidence per `.agents/skills/emit-run-evidence/SKILL.md`" beats "see the brief generator for the pattern; copy it; verify the four cross-checks." Role instructions become shorter and more durable.

Cross-link with `audit-001` and `extend-001`: the skill's eval list explicitly includes the chaos suite and the `--explain` shape, so future improvements to the contract propagate to every consumer through the skill's version bump.

## cost

Small to medium. The skill packaging is mostly documentation; the helper code already exists in `scripts/run_evidence.py`.

- `.agents/skills/emit-run-evidence/SKILL.md` - the skill content. ~150-200 lines.
- `.agents/skills/emit-run-evidence/install.md` - optional playbook with the copyable bash blocks the brief generator currently uses inline.
- `.agents/CATALOG.md` - entry naming the skill and its owner role.
- `decisions/DEC-CDCP-011-emit-run-evidence-skill-graduation.md` - the DEC recording the graduation per DEC-CDCP-007's skill-graduation pattern.
- Update to `science.matrix-runner` role instructions (when the role's working-tree file gets committed) to call the skill instead of inlining the pattern.

About one day of focused work, mostly extraction and consolidation.

## risk

- The skill bakes in today's shape. If `reduce-001` lands and changes the sandbox-ref protocol, the skill needs a v0.2.0 bump in the same window. Mitigation: name `reduce-001` in the skill's "version bump triggers" section and require the bump as part of the `reduce-001` PR.
- The matrix-plane is WIP. Graduating a skill that the matrix-runner has not yet exercised is graduation-by-prediction. Mitigation: ship the skill as v0.1.0; bump to v1.0.0 only after the matrix-runner's first end-to-end run lands clean.
- Skill graduation creates a new contract surface. A future emitter that needs a slightly different shape (a connector run with a different cross-check set) has to either fit the skill or fork it. Mitigation: the skill's "When to use" section is narrow (Run-shaped emissions only); a connector-evidence skill would be a sibling, not a fork.
- The role-instruction update sits in the working tree (uncommitted) at dream time. The skill graduation lands as a standalone change; the role wiring happens when the role's instructions file ships.

## timeline

Next sprint. The skill is mostly extraction; the harder work is the role-wiring step that happens when spec 0012's role files commit. Ordering: skill text + DEC + CATALOG entry (week 1); role wiring lands with spec 0012's first commit (when the working-tree files ship).

## promotion path

If approved, the promotion touches:

- `.agents/skills/emit-run-evidence/SKILL.md` - new skill content.
- `.agents/skills/emit-run-evidence/install.md` - optional playbook (recommended).
- `.agents/CATALOG.md` - new skill entry under the skill section.
- `decisions/DEC-CDCP-011-emit-run-evidence-skill-graduation.md` - new DEC.
- `specs/0010-cognitive-delivery-control-plane/requirements.md` - new R-CDCP requirement covering the skill (or extend an existing requirement).

The role-wiring step (when spec 0012 lands the role instructions on main) calls the skill from `science.matrix-runner/instructions.md` line ~N.

Reviewer checks:

1. The skill's steps reproduce the W22 regenerate flow (`959bcff` + `e4fa4d5`) against a fresh sample.
2. The skill's eval list is concrete (each eval is a runnable command, not a vague aspiration).
3. The skill carries the `human_review_required` flag on its output (emission is an apply_patch-class change against the records directory).
4. The skill does not duplicate `templates/spec-six-pack.md` if that file exists; if it does, point at it instead.

Owner role: `learning.skill-curator` (the skill graduates per the curator's process per DEC-CDCP-007) with `science.matrix-runner` as the first consumer.

## risks if promoted blindly

- Without the matrix-runner's first end-to-end consumer run, graduating to v1.0.0 is premature. Promote as v0.1.0; bump after the consumer ships.
- The skill bakes the four cross-checks from DEC-PUB-006. A future cross-check (say a fifth, for cross-repo URI resolution) needs a skill version bump. Confirm the "version bump triggers" section is explicit.
- The skill could become a stand-in for re-reading the DECs. The skill is a packaging, not a replacement. Each promotion should link the skill back to DEC-PUB-005, DEC-PUB-006, and DEC-PUB-008 explicitly.
